# 启元大赛 · 九齿 .skill 创新挑战 — ntops 算子开发

> **选手**：于鸿伟 · **GitHub**：hongwei-2026  
> **赛道**：九齿 .skill 创新挑战 · **阶段**：初赛提交

让 AI 智能体按可执行流水线完成 [InfiniTensor/ntops](https://github.com/InfiniTensor/ntops) 九齿算子开发，并在 GPU 上实测通过。

---

## 项目简介

本仓库交付 **双 Skill 套件**，解决 Agent 写 ntops 算子时的三类典型失败：

1. 写错范式（Triton / examples 风格 `make`）
2. 流程断裂（漏注册、漏 torch 封装、漏 pytest）
3. 无法自检（错误推到 CI 才暴露）

| Skill | 版本 | 定位 | 一条命令 |
|-------|------|------|----------|
| **ntops-forge** | v1.0 | **主作品**：五段工厂流水线 | `python scripts/forge.py gate` |
| ntops-copilot | v0.5 | 轻量副驾驶 | `python scripts/run_task.py --task silu --finish` |

---

## GPU 实测结果（RTX 4090）

```bash
source /root/miniconda3/bin/activate base
cd /root/work/skill
python scripts/forge.py gate --ntops-root /root/work/ntops
```

| 算子 | GUARD | pytest | 结果 |
|------|-------|--------|------|
| silu | `matches reference` | 8 passed | ✅ |
| add | `matches reference` | 8 passed | ✅ |
| gelu | `matches reference` | 8 passed | ✅ |

```
GATE OK: all operators passed
```

截图见 `docs/screenshots/forge-gate-gpu-test.png`

---

## 快速开始

### 安装 Skill（Cursor / Agent）

```text
.cursor/skills/ntops-forge/      # 主 skill（推荐）
.cursor/skills/ntops-copilot/    # 轻量备选
```

### ntops-forge（推荐演示）

```bash
python scripts/forge.py list
python scripts/forge.py run silu --ntops-root /path/to/ntops
python scripts/forge.py gate --ntops-root /path/to/ntops
python scripts/forge.py diagnose --log docs/forge_runs.jsonl
```

五段流水线：**PLAN → CODEGEN → GUARD → PROVE → SHIP**

### ntops-copilot（快速路径）

```bash
python scripts/doctor.py
python scripts/run_task.py --task silu --ntops-root /path/to/ntops --finish
```

---

## 初赛提交材料（对照组委会要求）

| 组委会要求 | 本仓库文件 |
|------------|------------|
| Proposal | [`docs/Proposal.md`](docs/Proposal.md) |
| .skill 初版 | [`skills/ntops-forge/`](skills/ntops-forge/) + [`skills/ntops-copilot/`](skills/ntops-copilot/) |
| 自测计划 | [`docs/SelfTestPlan.md`](docs/SelfTestPlan.md) |
| 中期报告 | [`docs/MidTermReport.md`](docs/MidTermReport.md) → 导出 PDF |

### 官网表单填写

| 字段 | 内容 |
|------|------|
| **Github 仓库** | `https://github.com/hongwei-2026/qiyuanbisai` |
| **Commit 链接** | `https://github.com/hongwei-2026/qiyuanbisai/commit/42e568a` |
| **附件 zip** | 见下方打包命令 |

> **初赛不需要 PR。** 提交载体以后续赛题组通知为准；当前以独立 skill 仓库 + commit + zip 提交。

### 打包附件

```bash
python scripts/pack_submission.py --stage initial
# 生成 submission-initial-YYYYMMDD.zip
```

### 中期报告 PDF 命名

```text
于鸿伟_九齿skill创新挑战_中期报告.pdf
```

由 `docs/MidTermReport.md` 导出。

完整说明：[`docs/SubmissionGuide.md`](docs/SubmissionGuide.md)

---

## 目录结构

```text
skills/
  ntops-forge/          # 工厂流水线 skill（创新主叙事）
    SKILL.md
    specs/              # 算子规格 silu/add/gelu
    taxonomy.md
    fix_cards.md
  ntops-copilot/        # 轻量副驾驶 skill
    SKILL.md
    tasks/              # 任务卡
    formulas.md
scripts/
  forge.py              # 主流水线 + gate
  run_task.py           # copilot 一键流
  compare_ref.py        # 语义对照
  preflight.py          # 结构护栏
  doctor.py             # 环境自检
  ...
docs/
  Proposal.md           # 提案
  MidTermReport.md      # 中期报告
  SelfTestPlan.md       # 自测计划
  SubmissionGuide.md    # 提交指南
  GPU_Test_Report.md    # GPU 实测
  Forge_Design.md       # forge 设计说明
  forge_runs.jsonl      # 流水线审计日志
```

---

## 创新点摘要

1. **可执行 skill**：规范落到 `preflight` / `scaffold` / `forge`，非空泛文档
2. **工厂流水线**：PLAN→SHIP 五段闭环 + jsonl 审计
3. **任务卡驱动**：`formula_hint` 自动注入 `application()`
4. **语义对照**：`compare_ref` 对齐官方内核（含 gelu `default_application`）
5. **精准 pytest**：只跑 `tests/test_<op>.py`，避免 conv2d 误失败
6. **失败诊断**：fix_cards 自动匹配修复建议

---

## 身份信息

| 用途 | 填写 |
|------|------|
| 启元 / InfiniTensor 报名姓名 | 于鸿伟 |
| GitHub ID | hongwei-2026 |
| PR 分支命名 | `2026-spring-hongwei-2026-<赛题号>` |

---

## 许可

Apache-2.0（与 NineToothed / ntops 生态一致）
