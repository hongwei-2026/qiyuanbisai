import triton
import triton.language as tl

@triton.jit
def bad_kernel(x_ptr, y_ptr, n, BLOCK: tl.constexpr):
    pass
