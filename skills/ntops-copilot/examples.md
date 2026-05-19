# 示例：从规格到 PR（silu 类一元算子）

## 1. 规格（赛题常给）

- 算子：`silu(x) = x * sigmoid(x)`
- 输入：1D/多维张量，与 PyTorch `silu` 语义一致
- 输出：同 shape

## 2. 选模板

类型：`unary` → 参考  
https://github.com/InfiniTensor/ninetoothed-examples/blob/master/ops/ninetoothed/kernels/silu.py

## 3. 在 ntops 落盘

```bash
python scripts/scaffold_kernel.py --name silu --pattern unary \
  --out src/ntops/kernels/silu.py
```

将 `application` 改为（与官方示例一致）：

```python
def application(input, output):
    input_loaded = input
    output = input_loaded * ntl.sigmoid(ntl.cast(input_loaded, ntl.float32))  # noqa: F841
```

## 4. 注册与测试

- 更新 `src/ntops/kernels/__init__.py`
- 增加 `src/ntops/torch/` 封装
- `python scripts/preflight.py src/ntops/kernels/silu.py --kernel`
- `pytest tests/ -k silu`

## 5. PR

```bash
git checkout -b 2026-spring-hongwei-2026-T1-1-X
git add src/ntops/kernels/silu.py src/ntops/kernels/__init__.py ...
git commit -m "[2026春季][T1-1-X] hongwei-2026: add silu kernel"
```

PR 描述粘贴 `templates/PR_DESCRIPTION.md` 并附测试截图。

## Agent 评测建议

对同一任务跑两轮：

1. **Baseline**：不加载本 skill
2. **Treatment**：加载 `ntops-copilot`

记录：是否通过 preflight、pytest 是否绿、人工介入次数。
