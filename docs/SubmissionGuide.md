# 初赛提交指南（对照组委会要求）

## 组委会要求的 4 类材料

| # | 材料 | 本仓库对应文件 |
|---|------|----------------|
| 1 | **Proposal** | `docs/Proposal.md` |
| 2 | **.skill 初版** | `skills/ntops-forge/` + `skills/ntops-copilot/` + `scripts/` |
| 3 | **自测计划** | `docs/SelfTestPlan.md` |
| 4 | **中期报告** | `docs/MidTermReport.md` → 导出 PDF |

## 中期报告 PDF 命名

```
于鸿伟_九齿skill创新挑战_中期报告.pdf
```

可用 Word / Typora / VS Code 打开 `docs/MidTermReport.md` 导出 PDF。

## 官网表单填写（初赛）

| 字段 | 填什么 |
|------|--------|
| **Github 仓库** | `https://github.com/hongwei-2026/qiyuanbisai` |
| **Commit 链接** | `https://github.com/hongwei-2026/qiyuanbisai/commit/e7b32bb` |
| **附件 zip** | `submission-initial-20260608.zip`（运行 `pack_submission.py` 可重新生成） |

> **2026-06 更新**：组委会通知需向 **NineToothed 主仓库** 提 PR，见 **[UpstreamPRGuide.md](UpstreamPRGuide.md)**。  
> 初赛官网仍以 **独立 skill 仓库 + commit + zip** 为准；**两个渠道都要完成**。

| 渠道 | 链接 |
|------|------|
| 官网 skill 仓库 | https://github.com/hongwei-2026/qiyuanbisai |
| NineToothed PR | https://github.com/InfiniTensor/ninetoothed（fork 后提 PR） |

## 附件 zip 内含

- 双 skill 包（forge + copilot）
- 全部 scripts
- Proposal / 自测计划 / 中期报告（md）
- GPU 测试报告、A/B 报告、forge 设计说明、决赛路线图、Benchmark 计划
- 截图集 `docs/screenshots/`（19 张实测 + 架构图）
- 四类自测案例 `docs/selftests/`、评分对照 `docs/ScoringAlignment.md`
- 截图说明 `docs/DemoShowcase.md`

## 本地打包命令

```bash
cd qiyuan-skill-ntops-copilot
python scripts/pack_submission.py --stage initial
```

## 答辩一句话

> **ntops-forge** 在 RTX 4080 上 `forge gate` 一键验收五算子（silu/add/gelu/relu/mul）：公式注入、语义对照、pytest 全通过，A/B 步骤 6→1、人工介入 4→0，全程 jsonl 可审计。
