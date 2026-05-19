# NineToothed / ntops 速查

## 最小内核骨架（elementwise unary）

```python
import ninetoothed
import ninetoothed.language as ntl  # 需要 sigmoid/exp 等时
from ninetoothed import Symbol, Tensor

BLOCK_SIZE = Symbol("BLOCK_SIZE", constexpr=True)

def arrangement(input, output, BLOCK_SIZE=BLOCK_SIZE):
    return input.tile((BLOCK_SIZE,)), output.tile((BLOCK_SIZE,))

def application(input, output):
    x = input
    output = x  # 替换为真实公式

tensors = (Tensor(1), Tensor(1))
kernel = ninetoothed.make(arrangement, application, tensors)
```

## 最小内核骨架（binary）

```python
def arrangement(input, other, output, BLOCK_SIZE=BLOCK_SIZE):
    return (
        input.tile((BLOCK_SIZE,)),
        other.tile((BLOCK_SIZE,)),
        output.tile((BLOCK_SIZE,)),
    )

def application(input, other, output):
    output = input + other  # noqa: F841

tensors = tuple(Tensor(1) for _ in range(3))
kernel = ninetoothed.make(arrangement, application, tensors)
```

## 与 Triton 的分工

| | NineToothed (ntops) | Triton |
|---|---------------------|--------|
| 抽象 | `Tensor.tile`、TOM | 指针、block、mask |
| 入口 | `ninetoothed.make` | `@triton.jit` |
| 本赛道 | **要交这个** | 仅作对比/示例仓库 |

## 仓库路径

| 资源 | URL |
|------|-----|
| ntops | https://github.com/InfiniTensor/ntops |
| 示例 | https://github.com/InfiniTensor/ninetoothed-examples |
| 文档 | https://ninetoothed.org/ |
| InfiniCore | https://github.com/InfiniTensor/InfiniCore |

## ntops 目录

```
ntops/
  src/ntops/kernels/<op>.py   # 内核
  src/ntops/kernels/__init__.py
  src/ntops/torch/            # torch 封装
  tests/                      # pytest
```

## 大赛相关

- 算子 PR 提交到 **ntops** 仓库（非本 skill 仓库）
- 本 skill 仓库只存放 **Agent 知识与工具**
- 评测在组委会环境；选手无需自建云服务
