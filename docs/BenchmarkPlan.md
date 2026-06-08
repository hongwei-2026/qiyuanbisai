# Benchmark 与性能验证计划

对照赛题 4.2：至少 2 个自测任务需含 benchmark。初赛以 **流水线耗时 A/B** 为主证据；决赛补充算子级计时。

---

## 任务 A：forge 流水线耗时（初赛已完成）

| 指标 | Baseline | Treatment |
|------|----------|-----------|
| 平均步骤 | 6 | 1 |
| 人工介入 | 4 | 0 |
| 平均耗时 | ~1200s | ~7s/算子 |

证据：`docs/ab_runs.csv`、`docs/AB_Report.md`、截图 `16-gate-ab-5v5-final.png`

**结论**：Skill 将端到端开发验证从约 20 分钟降至约 7 秒/算子，人工介入归零。

---

## 任务 B：silu GPU kernel 计时 ✅ 已实测（2026-06-08）

| 字段 | 结果 |
|------|------|
| 环境 | AutoDL · RTX 4080 |
| 输入规模 | `(4096, 4096)` float16 |
| PyTorch `F.silu` | **0.0523 ms** |
| ntops.torch.silu | **0.0715 ms** |
| 比值 ntops/PyTorch | **1.37×**（同量级，无数量级回退） |

数据：`docs/bench_silu.json` · 截图：`docs/screenshots/17-bench-silu-gpu.png`

**结论**：官方 ntops silu 与 PyTorch 基线同量级；本 skill 重点在 **正确性闭环与开发效率**，非内核极限调优。ratio ~1.37 在 fp16 大矩阵下可接受，决赛可针对 generated source / tile 配置进一步优化。

复现命令见 `docs/CloudRun.md` §4。

---

## 任务 C：softmax 归约 benchmark（决赛计划）

- 输入：`(batch, seq, hidden)` 多组 shape
- 对比：PyTorch `F.softmax` vs ntops.torch.softmax
- 关注：dim 归约路径、dtype cast 开销

---

## 性能回退诊断流程

1. `forge.py diagnose` 读 jsonl 定位失败阶段  
2. `compare_ref` 排除语义偏差  
3. `bench_op.py` 对比官方实现耗时  
4. `fix_cards` FC-xxx 给出最小修复建议  

详见 `skills/ntops-forge/fix_cards.md`。
