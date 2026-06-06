# 于鸿伟_九齿skill创新挑战_中期报告

> 导出 PDF 时另存为：`于鸿伟_九齿skill创新挑战_中期报告.pdf`

| 项目 | 内容 |
|------|------|
| 赛道 | 九齿 .skill 创新挑战 |
| 组名 | 于鸿伟（个人） |
| 成员 | 于鸿伟 |
| GitHub | hongwei-2026 |
| 仓库 | https://github.com/hongwei-2026/qiyuanbisai |
| 日期 | 2026-06-06 |

---

## 一、选题与目标

### 1.1 选题

**NineToothed / ntops 算子开发 Agent Skill**——帮助 AI 智能体完成大赛 T1-1 类 elementwise 算子（silu、add、gelu 等）的开发、自检与验收。

### 1.2 目标

1. 减少 Agent 写错范式（Triton、`make` 误用）
2. 提供可执行闭环（非纯文档）
3. 支持 GPU 实测与可复现审计

### 1.3 交付物

| Skill | 定位 | 版本 |
|-------|------|------|
| **ntops-forge** | 主作品：五段工厂流水线 | v1.0 |
| **ntops-copilot** | 轻量备选：单命令 `--finish` | v0.5 |

---

## 二、当前进度（按赛题）

| 赛题/任务 | 进度 | 证据 |
|-----------|------|------|
| skill 包可安装 | ✅ 完成 | `skills/ntops-forge/` + `skills/ntops-copilot/` |
| 任务卡/spec | ✅ 完成 | 5 张 task + 3 张 forge spec |
| 可执行脚本 | ✅ 完成 | scaffold/preflight/forge/gate 等 14 个脚本 |
| GPU 实测 silu | ✅ 8/8 passed | forge gate |
| GPU 实测 add | ✅ 8/8 passed | forge gate |
| GPU 实测 gelu | ✅ 8/8 passed | forge gate + compare_ref 修复 |
| A/B baseline 对照 | 🔄 进行中 | treatment 已记录，baseline 待补 1 轮 |
| 决赛隐藏题适配 | ⏳ 未开始 | 决赛阶段 |

---

## 三、主要工作

### 3.1 ntops-forge（创新主叙事）

五段流水线：**PLAN → CODEGEN → GUARD → PROVE → SHIP**

```bash
python scripts/forge.py gate --ntops-root /root/work/ntops
```

创新点：

- 规格驱动（forge spec YAML）
- taxonomy 算子分类路由
- fix_cards 失败诊断
- jsonl 全链路审计

### 3.2 ntops-copilot（轻量路径）

```bash
python scripts/run_task.py --task silu --finish
```

### 3.3 GPU 实测摘要

环境：NVIDIA RTX 4090，conda `base`

| 命令 | 结果 |
|------|------|
| `forge gate` | **GATE OK: all operators passed** |
| silu GUARD | `matches reference` + 8 passed |
| add GUARD | `matches reference` + 8 passed |
| gelu GUARD | `matches reference` + 8 passed |

---

## 四、自测与评测

详见 `docs/SelfTestPlan.md`。

量化结果（treatment）：

- preflight 通过率：100%
- pytest 通过率：100%（silu/add/gelu）
- 单算子流水线：约 5.7 秒

---

## 五、问题与解决

| 问题 | 解决 |
|------|------|
| GPU 无 `python3` | `source miniconda activate base` |
| compare_ref 路径 bug | 修复 `resolve_reference_path` |
| gelu 无 `application()` | compare_ref 支持 `default_application` |
| pytest 误跑 conv2d | 精准 `tests/test_<op>.py` |

---

## 六、后续计划

1. 补 1 轮 Baseline vs Treatment 对照实验
2. 决赛前扩展 norm/attention 任务卡（只读参考模式）
3. 按组委会通知适配最终提交载体

---

## 七、提交信息（初赛）

| 字段 | 填写 |
|------|------|
| Github 仓库 | https://github.com/hongwei-2026/qiyuanbisai |
| Commit 链接 | 见 README 或最新 release commit |
| 附件 zip | `submission-initial-*.zip` |

**说明**：初赛不要求 PR 合入 ntops 主仓库；以独立 skill 仓库 + commit 链接 + 附件包提交。

---

**选手签名**：于鸿伟  
**日期**：2026-06-06
