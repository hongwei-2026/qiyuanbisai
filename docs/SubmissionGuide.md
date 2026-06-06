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
| **Commit 链接** | `https://github.com/hongwei-2026/qiyuanbisai/commit/c22fbcc` |
| **附件 zip** | 运行 `python scripts/pack_submission.py --stage initial` 生成 |

> 初赛**不需要 PR**。代码提交载体以后续赛题组通知为准；当前以**独立 skill 仓库 + commit + zip** 提交。

## 附件 zip 内含

- 双 skill 包（forge + copilot）
- 全部 scripts
- Proposal / 自测计划 / 中期报告（md）
- GPU 测试报告、A/B 报告、forge 设计说明
- 截图 `docs/screenshots/forge-gate-gpu-test.png`

## 本地打包命令

```bash
cd qiyuan-skill-ntops-copilot
python scripts/pack_submission.py --stage initial
```

## 答辩一句话

> **ntops-forge** 在 RTX 4090 上 `forge gate` 一键验收 silu/add/gelu：公式注入、语义对照、pytest 8/8 通过，全程 jsonl 可审计。
