# ST3：布局敏感算子（max_pool2d · stride）

**赛题 4.2 类型**：非连续输入、步长或偏移量场景  
**状态**：✅ spec + pytest 设计完成；决赛 GPU 执行

## 任务说明

max_pool2d 涉及 kernel_size、stride、padding、dilation、ceil_mode，pytest 覆盖多种 stride 组合。

## pytest 覆盖（ntops 官方）

`tests/test_max_pool2d.py` 参数化：

- `stride`: `None`, `1`, `(2, 3)`
- `kernel_size`, `padding`, `dilation`, `ceil_mode`
- 多 dtype / device

## Agent 执行记录摘要

```bash
python scripts/forge.py spec max_pool2d
python scripts/forge.py plan max_pool2d
```

预期 PLAN 输出（`pooling` 属 COMPLEX_FAMILIES）：

```
WARN: STOP: pooling requires reading reference first (see taxonomy.md)
```

## Reference 阅读要点

- `src/ntops/kernels/max_pool2d.py`：分块 load/store、stride 计算
- 布局敏感：输入 H×W 与 stride 共同决定输出 shape
- 与 elementwise 不同：不能仅用 formula 注入

## 产物摘要

- spec：`skills/ntops-forge/specs/max_pool2d.yaml`
- 决赛路径：读 reference → scaffold → compare_ref → `pytest tests/test_max_pool2d.py`

## Correctness 验证（决赛）

```bash
cd /root/work/ntops
pytest tests/test_max_pool2d.py -v
```

## 布局场景说明

| 场景 | 验证点 |
|------|--------|
| stride=None | 默认等于 kernel_size |
| stride=1 | 密集滑动 |
| stride=(2,3) | 非对称步长，输出尺寸与 padding 联动 |

## 证据

- spec：`skills/ntops-forge/specs/max_pool2d.yaml`
- 路由：`skills/ntops-forge/taxonomy.md`
