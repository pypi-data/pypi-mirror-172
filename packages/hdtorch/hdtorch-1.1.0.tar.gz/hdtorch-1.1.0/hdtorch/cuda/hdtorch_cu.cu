#include <torch/extension.h>

#include <cuda.h>
#include <cuda_runtime.h>
#include <algorithm>
#include <vector>
#include <stdio.h>
#include <type_traits>
#include <cuda/barrier>

using namespace torch::indexing;

template<typename N, int64_t d>
using PAcc64 = torch::PackedTensorAccessor64<N,d,torch::RestrictPtrTraits>;

__inline__ int iceil(int in, int div){ return (in + div - 1)/div;}						  
		  
#define POPC1B(arr) (__popc(arr[0]) << 0 )| \
					(__popc(arr[1]) << 8 )| \
					(__popc(arr[2]) << 16)| \
					(__popc(arr[3]) << 24);	
					
long lowestPowerof2(unsigned x)
{
	x--;
    x |= x >> 1;
    x |= x >> 2;
    x |= x >> 4;
    x |= x >> 8;
    x |= x >> 16;
	x += 1;
    return (x == 0) ? 1 : x;
}

template <unsigned int blockSize>
__device__ __inline__ void h_warpReduce(volatile int *sdata, unsigned int tid) {
	if (blockSize >= 64) sdata[tid] += sdata[tid + 32];
	if (blockSize >= 32) sdata[tid] += sdata[tid + 16]; 
	if (blockSize >= 16) sdata[tid] += sdata[tid +  8];
	if (blockSize >=  8) sdata[tid] += sdata[tid +  4];
	if (blockSize >=  4) sdata[tid] += sdata[tid +  2];
	if (blockSize >=  2) sdata[tid] += sdata[tid +  1];
}

template<bool packed,typename inp_t>
struct load {};

template <typename inp_t>
struct load<true,inp_t> {
	__inline__ __device__ int operator()(const PAcc64<inp_t,2> inp, const int gridSize, const int row, int col) {
		int sum_count = 0;
		int d = 0, out = 0;
		//8-bit summation
		while(col < inp.size(1) - 3) {
			if(sum_count == 7) {
				out += (0x000000FF & d) + (0x000000FF & (d>>8)) + (0x000000FF & (d>>16)) + (0x000000FF & (d>>24));
				d = 0;
				sum_count = 0;
			}
			d += POPC1B((&inp[row][col])); 
			sum_count++;
			col += gridSize;
		} 
		out += (0x000000FF & d) + (0x000000FF & (d>>8)) + (0x000000FF & (d>>16)) + (0x000000FF & (d>>24));
		//Leftover summation
		while(col < inp.size(1)) {
			out += __popc(inp[row][col]);
			col += 1;
		}
		return out;
	}
};

template <typename inp_t>
struct load<false,inp_t> {
	__inline__ __device__ int operator()(const PAcc64<inp_t,2> inp, const int gridSize, const int row, int col) {
		int sum_count = 0;
		int d = 0, out = 0;
		//8-bit summation
		int s = inp.size(1);
		while(col < s) {
			if(sum_count == 7) {
				out += (0x000000FF & d) + (0x000000FF & (d>>8)) + (0x000000FF & (d>>16)) + (0x000000FF & (d>>24));
				d = 0;
				sum_count = 0;
			}
			d += inp[row][col]; 
			sum_count++;
			col += gridSize;
		} 
		out += (0x000000FF & d) + (0x000000FF & (d>>8)) + (0x000000FF & (d>>16)) + (0x000000FF & (d>>24));
		return out;
	}
};
					
template <typename scalar_t, int blockSize, int batchSize, bool packed, typename inp_t>
__global__ void h_reduce(const PAcc64<inp_t,2> inp, PAcc64<scalar_t,2> accum) {
	__shared__ int sdata[1024];
	
	const int tid = threadIdx.x;
	
	int col = (tid%blockSize)*((packed) ? 4 : 1);
	const int row = blockIdx.z*(65535*batchSize) + blockIdx.y*batchSize + tid/blockSize;
	
	const unsigned int gridSize = blockSize*gridDim.x * ((packed) ? 4 : 1);

	sdata[tid] = (row < inp.size(0) && col < inp.size(1)) ? load<packed,inp_t>()(inp, gridSize, row, col) : 0;
	
	__syncthreads();
	
	
	const int last_warp_threads = (blockSize > 64) ? 32 : blockSize/2;
	const int block_tid = tid % blockSize;
	if (blockSize >= 512) { if (block_tid < 256) { sdata[tid] += sdata[tid + 256]; } __syncthreads(); }
	if (blockSize >= 256) { if (block_tid < 128) { sdata[tid] += sdata[tid + 128]; } __syncthreads(); }
	if (blockSize >= 128) { if (block_tid < 64) { sdata[tid] += sdata[tid + 64]; } __syncthreads(); }
	if (block_tid < last_warp_threads) h_warpReduce<blockSize>(sdata, tid);
	if (block_tid == 0 && row < accum.size(0)) accum[row][blockIdx.x] = sdata[tid];
}

template<int blockSize, typename inp_t, bool packed>
void hcount_dispatch(const torch::Tensor inp, torch::Tensor accum)
{
	const int samples_per_block = 1024/blockSize;
	auto flattened_inp   = inp.view({-1,inp.size(inp.dim()-1)});
	auto flattened_accum = accum.view({-1,accum.size(accum.dim()-1)});
	const int y_blocks = std::min(65535, iceil(flattened_inp.size(0), samples_per_block));
	const int z_blocks = iceil(iceil(flattened_inp.size(0), samples_per_block),65535);
	if(z_blocks > 65535) {printf("hcount: input too large\n"); return;}
	dim3 blocks(1,y_blocks,z_blocks);
	AT_DISPATCH_INTEGRAL_TYPES(accum.type(), "vcount_cuda", ([&] {
	h_reduce<scalar_t,blockSize,1024/blockSize, packed, inp_t><<<blocks,1024>>>(
		flattened_inp.packed_accessor64<inp_t,2,torch::RestrictPtrTraits>(),
		flattened_accum.packed_accessor64<scalar_t,2,torch::RestrictPtrTraits>());
	}));
}

template<typename inp_t, bool packed>
void call_hcount(const torch::Tensor inp, torch::Tensor accum, int blockSize) { 
	switch(blockSize) {
		case 1024: hcount_dispatch<1024, inp_t, packed> (inp, accum); break;
		case 512:  hcount_dispatch<512,  inp_t, packed> (inp, accum); break;
		case 256:  hcount_dispatch<256,  inp_t, packed> (inp, accum); break;
		case 128:  hcount_dispatch<128,  inp_t, packed> (inp, accum); break;
		case 64:   hcount_dispatch<64,   inp_t, packed> (inp, accum); break;
		case 32:   hcount_dispatch<32,   inp_t, packed> (inp, accum); break;
		case 16:   hcount_dispatch<16,   inp_t, packed> (inp, accum); break;
		case 8:    hcount_dispatch<8,    inp_t, packed> (inp, accum); break;
		case 4:    hcount_dispatch<4,    inp_t, packed> (inp, accum); break;
		case 2:    hcount_dispatch<2,    inp_t, packed> (inp, accum); break;
		case 1:    hcount_dispatch<1,    inp_t, packed> (inp, accum); break;
		default:   printf("Non power of 2 reduce requested\n");       break;
	}

}

torch::Tensor hcount_cuda(torch::Tensor inp, torch::Tensor accum) {
	
	const int max_block_size = std::min((long)1024,lowestPowerof2(inp.size(inp.dim()-1)>>3));
	call_hcount<int32_t, true>(inp, accum, max_block_size);
    return accum.index({Ellipsis,0});
}

__global__ void transpose_packed(const PAcc64<int32_t,3> inp, PAcc64<int32_t,3> trans) {
	
	__shared__ int sdata[128][4];
	
	const int tid = threadIdx.x;
	const int tile_x = blockIdx.x;
	const int tile_y = blockIdx.y;
	
	const int val_y = tid;
	const int batch = blockIdx.z;
	
	int in_x = tile_x*4;
	const int in_y = tile_y*128 + val_y;
	if(in_y < inp.size(1)) {
		for(int i = 0; i < 4; i++, in_x++) {
			sdata[val_y][i] = (in_x < inp.size(2)) ? inp[batch][in_y][in_x] : 0;
		}
	} else {
		sdata[val_y][0] = 0;
		sdata[val_y][1] = 0;
		sdata[val_y][2] = 0;
		sdata[val_y][3] = 0;
	}
	__syncthreads();
	
	const int warp_y = tid%128;
	const int transposed_x = warp_y/32;
	const int d[4] = {sdata[warp_y][0],sdata[warp_y][1],sdata[warp_y][2],sdata[warp_y][3]};
	__syncthreads();
	for(int i = 0; i < 4; i++) {
		sdata[i*32 + 0 ][transposed_x] = __ballot_sync(0xffffffff,d[i] & 0b00000000000000000000000000000001);
		sdata[i*32 + 1 ][transposed_x] = __ballot_sync(0xffffffff,d[i] & 0b00000000000000000000000000000010);
		sdata[i*32 + 2 ][transposed_x] = __ballot_sync(0xffffffff,d[i] & 0b00000000000000000000000000000100);
		sdata[i*32 + 3 ][transposed_x] = __ballot_sync(0xffffffff,d[i] & 0b00000000000000000000000000001000);
		sdata[i*32 + 4 ][transposed_x] = __ballot_sync(0xffffffff,d[i] & 0b00000000000000000000000000010000);
		sdata[i*32 + 5 ][transposed_x] = __ballot_sync(0xffffffff,d[i] & 0b00000000000000000000000000100000);
		sdata[i*32 + 6 ][transposed_x] = __ballot_sync(0xffffffff,d[i] & 0b00000000000000000000000001000000);
		sdata[i*32 + 7 ][transposed_x] = __ballot_sync(0xffffffff,d[i] & 0b00000000000000000000000010000000);
		sdata[i*32 + 8 ][transposed_x] = __ballot_sync(0xffffffff,d[i] & 0b00000000000000000000000100000000);
		sdata[i*32 + 9 ][transposed_x] = __ballot_sync(0xffffffff,d[i] & 0b00000000000000000000001000000000);
		sdata[i*32 + 10][transposed_x] = __ballot_sync(0xffffffff,d[i] & 0b00000000000000000000010000000000);
		sdata[i*32 + 11][transposed_x] = __ballot_sync(0xffffffff,d[i] & 0b00000000000000000000100000000000);
		sdata[i*32 + 12][transposed_x] = __ballot_sync(0xffffffff,d[i] & 0b00000000000000000001000000000000);
		sdata[i*32 + 13][transposed_x] = __ballot_sync(0xffffffff,d[i] & 0b00000000000000000010000000000000);
		sdata[i*32 + 14][transposed_x] = __ballot_sync(0xffffffff,d[i] & 0b00000000000000000100000000000000);
		sdata[i*32 + 15][transposed_x] = __ballot_sync(0xffffffff,d[i] & 0b00000000000000001000000000000000);
		sdata[i*32 + 16][transposed_x] = __ballot_sync(0xffffffff,d[i] & 0b00000000000000010000000000000000);
		sdata[i*32 + 17][transposed_x] = __ballot_sync(0xffffffff,d[i] & 0b00000000000000100000000000000000);
		sdata[i*32 + 18][transposed_x] = __ballot_sync(0xffffffff,d[i] & 0b00000000000001000000000000000000);
		sdata[i*32 + 19][transposed_x] = __ballot_sync(0xffffffff,d[i] & 0b00000000000010000000000000000000);
		sdata[i*32 + 20][transposed_x] = __ballot_sync(0xffffffff,d[i] & 0b00000000000100000000000000000000);
		sdata[i*32 + 21][transposed_x] = __ballot_sync(0xffffffff,d[i] & 0b00000000001000000000000000000000);
		sdata[i*32 + 22][transposed_x] = __ballot_sync(0xffffffff,d[i] & 0b00000000010000000000000000000000);
		sdata[i*32 + 23][transposed_x] = __ballot_sync(0xffffffff,d[i] & 0b00000000100000000000000000000000);
		sdata[i*32 + 24][transposed_x] = __ballot_sync(0xffffffff,d[i] & 0b00000001000000000000000000000000);
		sdata[i*32 + 25][transposed_x] = __ballot_sync(0xffffffff,d[i] & 0b00000010000000000000000000000000);
		sdata[i*32 + 26][transposed_x] = __ballot_sync(0xffffffff,d[i] & 0b00000100000000000000000000000000);
		sdata[i*32 + 27][transposed_x] = __ballot_sync(0xffffffff,d[i] & 0b00001000000000000000000000000000);
		sdata[i*32 + 28][transposed_x] = __ballot_sync(0xffffffff,d[i] & 0b00010000000000000000000000000000);
		sdata[i*32 + 29][transposed_x] = __ballot_sync(0xffffffff,d[i] & 0b00100000000000000000000000000000);
		sdata[i*32 + 30][transposed_x] = __ballot_sync(0xffffffff,d[i] & 0b01000000000000000000000000000000);
		sdata[i*32 + 31][transposed_x] = __ballot_sync(0xffffffff,d[i] & 0b10000000000000000000000000000000);
	}
	__syncthreads();
	
	int out_x = tile_y;
	int out_y = tile_x*128 + val_y;
	if(out_y < trans.size(1) && out_x < trans.size(2))
		trans[batch][out_y][out_x] = POPC1B(sdata[val_y]);
}



void call_bit_transpose(torch::Tensor inp, torch::Tensor trans)
{
	int threads = 128;
	const dim3 blocks((inp.size(2) + 4 - 1) / 4, (inp.size(1)+128 - 1)/128, inp.size(0));
	AT_DISPATCH_INTEGRAL_TYPES(trans.type(), "vcount_cuda", ([&] {
	transpose_packed<<<blocks,threads>>>(
		inp.packed_accessor64<int32_t,3,torch::RestrictPtrTraits>(),
		trans.packed_accessor64<int32_t,3,torch::RestrictPtrTraits>());
	}));
}


torch::Tensor vcount_cuda(torch::Tensor inp, int width) {
    auto flattened_inp   = inp.view({-1,inp.size(inp.dim()-2), inp.size(inp.dim()-1)});
    std::vector<int64_t> transpose_size(inp.sizes().data(), inp.sizes().data()+inp.dim());
    transpose_size[inp.dim()-1] = iceil(iceil(flattened_inp.size(1),32),4);
    transpose_size[inp.dim()-2] = width;
    
	torch::Tensor transposed_array = torch::zeros(transpose_size, torch::dtype(torch::kInt32).device(torch::kCUDA,0));
	auto flattened_trans = transposed_array.view({-1,transposed_array.size(transposed_array.dim()-2), transposed_array.size(transposed_array.dim()-1)});
	call_bit_transpose(flattened_inp, flattened_trans);
	int max_block_size = std::min((long)1024,lowestPowerof2(flattened_trans.size(2)>>3));
	call_hcount<int32_t, false>(flattened_trans, flattened_trans, max_block_size);
    return transposed_array.index({Ellipsis,0});
}

template <int offset>
__device__ __inline__ uint32_t extract_bits(uint32_t inp) {
	switch(inp) {
		case 0:	       return (uint32_t)0b0000<<offset;
		case 1:	       return (uint32_t)0b0001<<offset;
		case 256:	   return (uint32_t)0b0010<<offset;
		case 257:	   return (uint32_t)0b0011<<offset;
		case 65536:	   return (uint32_t)0b0100<<offset;
		case 65537:	   return (uint32_t)0b0101<<offset;
		case 65792:	   return (uint32_t)0b0110<<offset;
		case 65793:	   return (uint32_t)0b0111<<offset;
		case 16777216: return (uint32_t)0b1000<<offset;
		case 16777217: return (uint32_t)0b1001<<offset;
		case 16777472: return (uint32_t)0b1010<<offset;
		case 16777473: return (uint32_t)0b1011<<offset;
		case 16842752: return (uint32_t)0b1100<<offset;
		case 16842753: return (uint32_t)0b1101<<offset;
		case 16843008: return (uint32_t)0b1110<<offset;
		case 16843009: return (uint32_t)0b1111<<offset;
		default: __builtin_unreachable();
	}
	__builtin_unreachable();
}

template <typename scalar_t>
__global__ void pack_kernel(const PAcc64<scalar_t,2> inp, PAcc64<int32_t,2> out) {
	extern __shared__ int sdata[];
	
	const int tid = threadIdx.x;
	
	const int col_out = blockIdx.x * blockDim.x + tid; 
	const int col_in = col_out*32;
	const int i = 65535*blockIdx.z + blockIdx.y;
	
	if(col_out < out.size(1) && i < out.size(0)) {
		if(col_in + 4  <= inp.size(1)) sdata[tid]  = extract_bits<0 >(*(uint32_t*)&inp[i][col_in+0 ]);
		if(col_in + 8  <= inp.size(1)) sdata[tid] += extract_bits<4 >(*(uint32_t*)&inp[i][col_in+4 ]);
		if(col_in + 12 <= inp.size(1)) sdata[tid] += extract_bits<8 >(*(uint32_t*)&inp[i][col_in+8 ]);
		if(col_in + 16 <= inp.size(1)) sdata[tid] += extract_bits<12>(*(uint32_t*)&inp[i][col_in+12]);
		if(col_in + 20 <= inp.size(1)) sdata[tid] += extract_bits<16>(*(uint32_t*)&inp[i][col_in+16]);
		if(col_in + 24 <= inp.size(1)) sdata[tid] += extract_bits<20>(*(uint32_t*)&inp[i][col_in+20]);
		if(col_in + 28 <= inp.size(1)) sdata[tid] += extract_bits<24>(*(uint32_t*)&inp[i][col_in+24]);
		if(col_in + 32 <= inp.size(1)) sdata[tid] += extract_bits<28>(*(uint32_t*)&inp[i][col_in+28]);
		out[i][col_out] = sdata[tid];
	}
}


void pack_cuda(torch::Tensor inp, torch::Tensor out) {
	
	const int threads = 256; 
    auto flattened_inp   = inp.view({-1,inp.size(inp.dim()-1)});
	auto flattened_out = out.view({-1,out.size(out.dim()-1)});
	const int z_blocks = (flattened_out.size(0) + 65535 - 1)/65535;
	const int y_blocks = std::min((int64_t)65535,flattened_out.size(0));
	const dim3 blocks(iceil(flattened_out.size(1), threads), y_blocks, z_blocks);
	//printf("x: %d, y: %d, z: %d\n",blocks.x, blocks.y, blocks.z);
	AT_DISPATCH_INTEGRAL_TYPES_AND(torch::kBool,inp.type(), "pack_cuda", ([&] {
		pack_kernel<scalar_t><<<blocks,threads,threads*sizeof(int)>>>(
			flattened_inp.packed_accessor64<scalar_t,2,torch::RestrictPtrTraits>(),
			flattened_out.packed_accessor64<int32_t,2,torch::RestrictPtrTraits>());
	}));
	
}

template <typename scalar_t>
__global__ void unpack_kernel(const PAcc64<int32_t,2> inp, PAcc64<scalar_t,2> out) {
									  
	const int col_out = blockIdx.x * blockDim.x + threadIdx.x;
	const int i = 65535*blockIdx.z + blockIdx.y;

	const int bit_loc = col_out % 32;
	if(col_out < out.size(1)) {
		out[i][col_out] =  (((uint32_t)inp[i][col_out/warpSize]) & (1<<bit_loc))>>bit_loc;
	}
}

void unpack_cuda(torch::Tensor inp, torch::Tensor out) {
	
	const int threads = 1024; 
    auto flattened_inp   = inp.view({-1,inp.size(inp.dim()-1)});
	auto flattened_out = out.view({-1,out.size(out.dim()-1)});
	const int z_blocks = (flattened_out.size(0) + 65535 - 1)/65535;
	const int y_blocks = std::min((int64_t)65535,flattened_out.size(0));
	const dim3 blocks(iceil(flattened_out.size(1), threads),y_blocks,z_blocks);
	AT_DISPATCH_INTEGRAL_TYPES_AND(torch::kBool,out.scalar_type(), "unpack_cuda", ([&] {
		unpack_kernel<scalar_t><<<blocks,threads>>>(
			flattened_inp.packed_accessor64<int32_t,2,torch::RestrictPtrTraits>(),
			flattened_out.packed_accessor64<scalar_t,2,torch::RestrictPtrTraits>());
	}));
	
}