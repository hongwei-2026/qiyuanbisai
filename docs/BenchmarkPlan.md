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

## 任务 B：silu GPU kernel 计时（决赛执行）

```bash
source /root/miniconda3/bin/activate base
cd /root/work/skill
python scripts/bench_op.py --op silu --ntops-root /root/work/ntops \
  --shape 4096,4096 --warmup 10 --repeat 50
```

记录项：

| 字段 | 说明 |
|------|------|
| 输入规模 | 如 `(4096, 4096)` float16 |
| 基线 | `torch.nn.functional.silu` 或 ntops.torch 官方路径 |
| Treatment | forge 生成内核经 ntops 调用 |
| 结论 | 无明显回退 / 回退比例 |

输出：`docs/bench_silu.json`（脚本自动生成）

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
