# 九齿 .skill 创新挑战 — ntops 算子开发双 Skill 套件

| Skill | 定位 | 入口 |
|-------|------|------|
| **ntops-forge** 🆕 | **算子工厂**（五段流水线 + 诊断 + 审计） | `python scripts/forge.py run silu` |
| ntops-copilot | 轻量副驾驶（单命令 `--finish`） | `python scripts/run_task.py --task silu --finish` |

让 AI 智能体完成 [ntops](https://github.com/InfiniTensor/ntops) 算子开发闭环。

## 安装 Skill（Cursor / Agent）

推荐同时安装两个 skill：

- `.cursor/skills/ntops-forge/` — **大赛主叙事（创新）**
- `.cursor/skills/ntops-copilot/` — 轻量快速路径

## ntops-forge 快速验证（全新 v1.0）

```bash
python scripts/forge.py list
python scripts/forge.py run silu --ntops-root /root/work/ntops
python scripts/forge.py run add --ntops-root /root/work/ntops
python scripts/forge.py gate --ntops-root /root/work/ntops   # silu+add+gelu 演示闸门
python scripts/forge_spec.py "gelu unary" --out skills/ntops-forge/specs/custom.yaml
cat docs/forge_runs.jsonl
```

**forge 突破点**：PLAN→CODEGEN→GUARD→PROVE→SHIP 工厂流水线 + taxonomy 路由 + fix_cards 诊断 + jsonl 审计。

## ntops-copilot 快速验证（v0.5）

```bash
# 环境自检
python scripts/doctor.py

# 一键任务流：任务卡公式自动注入骨架
python scripts/run_task.py --task silu --ntops-root d:\启元\ntops-master\ntops-master

# 新算子全链路（注册 + pytest 验收）
python scripts/run_task.py --task gelu --ntops-root <ntops> --force --register --verify

# 交 PR 前严格自检 + 与官方实现对齐
python scripts/preflight.py /tmp/gelu.py --kernel --strict
python scripts/compare_ref.py /tmp/gelu.py --ref <ntops>/src/ntops/kernels/gelu.py
```

**v0.4 突破点**：任务卡 `formula_hint` 驱动代码生成 + `verify_task` 闭环验收 + `compare_ref` 语义对照 + `record_run` 可复现 A/B。

## 身份信息

| 用途 | 填写 |
|------|------|
| 启元 / InfiniTensor 报名姓名 | 于鸿伟 |
| GitHub 仓库、PR 分支、commit | **hongwei-2026** |

## 初赛执行（建议流程）

1. 在 `ntops` 仓库实现 2-3 个算子任务（可参考 `skills/ntops-copilot/tasks/`）。
2. 每个任务跑 `preflight` + `pytest`，保存结果截图。
3. 跑一轮 A/B 评测并生成统计：

```bash
python scripts/eval_ab.py --input docs/ab_runs.csv --output docs/AB_Report.md
```

4. 将过程和结果更新到 `docs/InitialRound.md`。
5. 重新打包初赛附件（默认打初赛包）：

```bash
python scripts/pack_submission.py --stage initial
```

## 初赛提交（详见 `docs/SubmissionGuide.md`）

| 字段 | 填什么 |
|------|--------|
| Github 仓库 | `https://github.com/hongwei-2026/qiyuanbisai` |
| Commit 链接 | `https://github.com/hongwei-2026/qiyuanbisai/commit/d3c7590` |
| 附件 zip | `python scripts/pack_submission.py --stage initial` → `submission-initial-*.zip` |
| 中期报告 PDF | 由 `docs/MidTermReport.md` 导出为 `于鸿伟_九齿skill创新挑战_中期报告.pdf` |

> 初赛**不需要 PR**；提交载体以后续赛题组通知为准。

## 目录

```
skills/ntops-forge/       # 🆕 工厂流水线 skill（创新主叙事）
skills/ntops-copilot/     # 轻量副驾驶 skill
scripts/                  # forge + copilot 可执行工具链
docs/Forge_Design.md      # forge 设计说明
docs/Proposal.md          # Proposal 正文（导出 PDF 放进 zip）
docs/InitialRound.md      # 初赛结果与A/B评测
HONOR_CODE.md
REFERENCE.md
```

## 许可

Apache-2.0（与 NineToothed / ntops 生态一致）
