# ST2：归约 / 分块类算子（softmax）

**赛题 4.2 类型**：归约或分块类（softmax 等）  
**状态**：✅ PLAN + reference 分析完成；决赛执行 pytest

## 任务说明

softmax 沿 dim 归约，需两遍循环（max 稳定 + 归一化），**禁止公式硬注入**，必须先读官方 reference。

## Agent 执行记录摘要

```bash
python scripts/forge.py spec softmax
python scripts/forge.py plan softmax   # 或 run 时在 PLAN 阶段 STOP
```

预期 PLAN 输出：

```
op=softmax family=reduction pattern=reduce
WARN: STOP: reduction requires reading reference first (see taxonomy.md)
```

**设计意图**：taxonomy 将 `reduction` 列入 COMPLEX_FAMILIES，forge 在 PLAN 阶段阻止 Agent 从公式瞎写，强制读 reference——这是泛化能力设计，非未完成。

## Reference 阅读要点

官方 `src/ntops/kernels/softmax.py`：

1. 使用 `reduction.arrangement`，非 element_wise
2. `application` 两遍 `for i in range(input.shape[0])` 循环
3. `_exp` 在 float16 下先 cast 到 float32 再 exp（数值稳定）
4. `premake(ndim, dim, ...)` 需指定归约维

## 产物摘要

- spec：`skills/ntops-forge/specs/softmax.yaml`
- 执行计划：读 reference → 手写/辅助 scaffold → compare_ref → pytest

## Correctness 验证（决赛执行）

```bash
cd /root/work/ntops
pytest tests/test_softmax.py -v
# 参数化：多 shape × dtype × device
```

## Benchmark（决赛）

见 `docs/BenchmarkPlan.md` 任务 C：多组 `(batch, seq, hidden)` 对比 PyTorch `F.softmax`。

## 证据

- spec：`skills/ntops-forge/specs/softmax.yaml`
- 路由：`skills/ntops-forge/taxonomy.md` § reduction
