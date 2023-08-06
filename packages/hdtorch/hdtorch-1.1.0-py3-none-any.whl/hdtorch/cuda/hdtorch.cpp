#include <torch/extension.h>

#include <c10/cuda/CUDAGuard.h>
#include <iostream>


torch::Tensor vcount_cuda(torch::Tensor inp, int width);
torch::Tensor hcount_cuda(torch::Tensor inp, torch::Tensor accum);
void pack_cuda(torch::Tensor inp, torch::Tensor out);
void unpack_cuda(torch::Tensor inp, torch::Tensor out);

#define CHECK_CUDA(x) TORCH_CHECK(x.is_cuda(), #x " must be a CUDA tensor")
#define CHECK_CONTIGUOUS(x) TORCH_CHECK(x.is_contiguous(), #x " must be contiguous")
#define CHECK_INPUT(x) CHECK_CUDA(x); CHECK_CONTIGUOUS(x)

torch::Tensor vcount(torch::Tensor inp, int width) {
	CHECK_INPUT(inp)
	return vcount_cuda(inp, width);
	
}

torch::Tensor hcount(torch::Tensor inp) {
	CHECK_INPUT(inp)
    std::vector<int64_t> accum_size(inp.sizes().data(), inp.sizes().data()+inp.dim());
    accum_size[accum_size.size()-1] = 1;
    auto accum = torch::empty(accum_size, torch::dtype(torch::kInt32).device(torch::kCUDA));
	return hcount_cuda(inp, accum);
	
}

torch::Tensor hcount(torch::Tensor inp, torch::Tensor accum) {
	CHECK_INPUT(inp)
    CHECK_INPUT(accum)
	return hcount_cuda(inp, accum);
	
}


torch::Tensor _hcount(torch::Tensor inp) {
	CHECK_INPUT(inp)
	return hcount_cuda(inp, inp);
	
}

torch::Tensor pack(torch::Tensor inp, torch::Tensor out) {
	CHECK_INPUT(inp)
	CHECK_INPUT(out)
	pack_cuda(inp, out);
    return out;
}

torch::Tensor pack(torch::Tensor inp) {
	CHECK_INPUT(inp)
    std::vector<int64_t> out_size(inp.sizes().data(), inp.sizes().data()+inp.dim());
    out_size[out_size.size()-1] = (out_size[out_size.size()-1] + 32 - 1) / 32;
    auto out = torch::empty(out_size, torch::dtype(torch::kInt32).device(torch::kCUDA));
	pack_cuda(inp, out);
    return out;
}


torch::Tensor unpack(torch::Tensor inp, torch::Tensor out) {
	CHECK_CUDA(inp)
	CHECK_CUDA(out)
	unpack_cuda(inp,out);
    return out;
}

torch::Tensor unpack(torch::Tensor inp, int outDim) {
	CHECK_CUDA(inp)
    std::vector<int64_t> out_size(inp.sizes().data(), inp.sizes().data()+inp.dim());
    out_size[out_size.size()-1] = outDim;
    auto out = torch::empty(out_size, torch::dtype(torch::kInt8).device(torch::kCUDA));
	unpack_cuda(inp,out);
    return out;
}



PYBIND11_MODULE(TORCH_EXTENSION_NAME, m) {
	m.def("vcount", &vcount, "Count HD bits vertically");
    m.def("_hcount", &_hcount, "Count HD bits horizontally");
	m.def("hcount", py::overload_cast<torch::Tensor, torch::Tensor>(&hcount), "Count HD bits horizontally");
    m.def("hcount", py::overload_cast<torch::Tensor>(&hcount), "Count HD bits horizontally");
	m.def("pack",   py::overload_cast<torch::Tensor, torch::Tensor>(&pack),   "Pack HD bits into 32-bit integers");
    m.def("pack",   py::overload_cast<torch::Tensor>(&pack),   "Pack HD bits into 32-bit integers");
	m.def("unpack", py::overload_cast<torch::Tensor, torch::Tensor>(&unpack), "Unpack 32-bit integers into HD bits");
    m.def("unpack", py::overload_cast<torch::Tensor, int>(&unpack), "Unpack 32-bit integers into HD bits");
}
