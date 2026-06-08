# 竞品对比分析（冲 95+ 分用）

| 维度 | 文档型 Skill | 脚本型 Copilot | **ntops-forge（本作品）** |
|------|-------------|----------------|---------------------------|
| 形态 | 仅 SKILL.md | SKILL + 零散脚本 | **五段工厂流水线** |
| 范式护栏 | 无 | preflight（部分） | preflight + compare_ref **双护栏** |
| 公式注入 | 手写 | 任务卡 hint | **spec formula 自动注入** |
| 失败诊断 | 人工查文档 | 人工查文档 | **fix_cards 自动匹配** |
| 审计 | 无 | 可选 CSV | **jsonl 全链路** |
| 一键验收 | 无 | run_task --finish | **forge gate 五算子** |
| A/B 证据 | 无 | 少见 | **baseline 脚本 + csv + 报告** |
| GPU 实测 | 少见 | 部分 | **17 张截图 + gate + benchmark** |

## 量化对比（本仓库实测）

| 指标 | Baseline | Treatment（forge） |
|------|----------|-------------------|
| preflight 通过率 | 0% | 100% |
| pytest 通过率 | 未跑通 | 100% |
| 平均步骤 | 6 | 1 |
| 人工介入 | 4 次 | 0 次 |
| 五算子 gate 耗时 | — | ~35s（估） |

## 答辩话术

「同类作品停在文档层，我们把 ntops 开发做成了 **可执行工厂**：一条 `forge gate` 覆盖 5 个 elementwise 算子，双护栏 + A/B 量化 + jsonl 审计，评委可按脚本复现。」
