#include <pybind11/pybind11.h>
namespace py = pybind11;

int add(int i, int j)
{
    return i + j;
}

PYBIND11_MODULE(example, m)
{
    // 可选，说明这个模块是做什么的
    m.doc() = "pybind11 example plugin";
    //def( "给python调用方法名"， &实际操作的函数， "函数功能说明" ). 其中函数功能说明为可选
    m.def("add", &add, "A function which adds two numbers", py::arg("i")=1, py::arg("j")=2);
}