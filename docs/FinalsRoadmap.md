# 决赛补全路线图（对照赛题 4.2）

初赛已完成 **逐元素/广播类** 五算子 gate + A/B 5v5。决赛前按赛题 4.2 四类自测任务补全如下。

## 四类自测任务对照

| 赛题 4.2 要求 | 初赛状态 | 决赛计划 | spec / 文档 |
|---------------|----------|----------|-------------|
| 逐元素/广播 | ✅ 已完成 | 维持 gate 回归 | silu/add/gelu/relu/mul |
| 归约/分块 | 📋 已规划 | softmax PLAN→读 reference→pytest | `specs/softmax.yaml` |
| 布局敏感 stride | 📋 已规划 | max_pool2d stride 参数覆盖 | `specs/max_pool2d.yaml` |
| 性能/benchmark | 📋 已规划 | silu 计时 + 流水线耗时对比 | `docs/BenchmarkPlan.md` |

## 决赛执行顺序（建议）

```bash
# 1. 维持五算子回归
python scripts/forge.py gate --ntops-root /root/work/ntops

# 2. 归约类（先 PLAN，读 reference）
python scripts/forge.py spec softmax
python scripts/forge.py plan softmax --ntops-root /root/work/ntops

# 3. 布局敏感
python scripts/forge.py spec max_pool2d
python scripts/forge.py plan max_pool2d --ntops-root /root/work/ntops

# 4. 性能材料
python scripts/bench_op.py --op silu --ntops-root /root/work/ntops
```

## 不支持场景（明确边界）

- 动态 shape 极端 case、非 CUDA 平台 correctness 结论
- 修改 NineToothed 编译器核心
- 依赖未披露的外部 API / 密钥

## 与隐藏任务的关系

隐藏任务 8 题覆盖：elementwise×2、reduce×2、layout×2、perf/diag×2。  
本路线图确保 **泛化能力** 不局限于公开五算子样例。
