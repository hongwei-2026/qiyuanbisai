# 于鸿伟_九齿skill创新挑战_中期报告

**赛事**：2026 春季启元人工智能大赛 · 九齿 .skill 创新挑战  
**报告类型**：初赛中期报告  
**小组名称 / 选手**：于鸿伟（个人参赛）  
**GitHub ID**：hongwei-2026  
**赛题编号**：T3-1-1（elementwise 算子开发，暂定）  
**仓库**：https://github.com/hongwei-2026/qiyuanbisai  
**报告日期**：2026 年 6 月 8 日  

---

## 摘要

本报告汇报 ntops-forge（v1.0）与 ntops-copilot（v0.5）双 Skill 套件的初赛进展。项目在 RTX 4080 GPU 环境完成 silu / add / gelu 三算子 `forge gate` 一键验收，pytest 8/8 通过；A/B 首轮显示 Treatment 相对 Baseline 步骤减少 5 步、人工介入减少 4 次。

---

## 一、.skill 名称、赛题与小组信息

| 项目 | 内容 |
|------|------|
| 主 Skill | **ntops-forge**（九齿算子工厂） |
| 辅助 Skill | ntops-copilot（轻量副驾驶） |
| 赛题编号 | T3-1-1（暂定，以赛题组通知为准） |
| 小组名称 | 于鸿伟 |
| 建议 PR 分支 | `2026-spring-hongwei-2026-T3-1-1` |
| 建议 PR 标题 | `[2026春季][T3-1-1] hongwei-2026` |

> 提交载体以后续赛题组通知为准；初赛以独立 skill 仓库 + commit + zip 提交，不要求 PR 合入。

---

## 二、.skill 目标、设计原则与包结构

### 2.1 目标

解决 Agent 开发 ntops 九齿算子时三类失败：写错范式（Triton）、流程断裂（漏注册/漏测）、无法自检（错误推到 CI）。

### 2.2 设计原则

1. **可执行优先**：规范落到脚本，不只写文档  
2. **五段闭环**：PLAN → CODEGEN → GUARD → PROVE → SHIP  
3. **精准测试**：只跑 `tests/test_<op>.py`，禁止全量 pytest  
4. **可审计**：jsonl 记录每阶段结果  

### 2.3 包结构

```
skills/ntops-forge/     # 主作品：SKILL.md, specs/, taxonomy.md, fix_cards.md
skills/ntops-copilot/   # 轻量路径：SKILL.md, tasks/, formulas.md
scripts/                # forge.py, preflight.py, compare_ref.py, doctor.py 等
docs/screenshots/       # GPU 实测截图（本报告附图）
```

![图1 五段流水线架构](screenshots/forge-pipeline-arch.png)

**图1** ntops-forge 五段流水线架构

---

## 三、核心工作流说明

| 阶段 | 动作 | 脚本 |
|------|------|------|
| PLAN | 读 spec，taxonomy 路由 | forge.py |
| CODEGEN | 注入 formula，生成 kernel/torch | scaffold_kernel.py |
| GUARD | preflight + compare_ref | preflight.py, compare_ref.py |
| PROVE | 精准 pytest | pytest tests/test_<op>.py |
| SHIP | PR 提示 + jsonl 审计 | forge_runs.jsonl |

![图2 环境自检 doctor](screenshots/01-doctor-gpu-ok.png)

**图2** GPU 环境自检：ninetoothed / torch / pytest / ntops / CUDA 全部 OK

![图3 单算子五段流水线 silu](screenshots/03-forge-run-silu-full.png)

**图3** `forge run silu` 完整输出：PLAN → SHIP，约 6.8s

---

## 四、适用任务范围与不适用范围

### 4.1 适用范围

- ntops **elementwise 一元/二元**算子（silu、add、gelu、relu、mul 等）  
- 大赛 2026-spring 分支/PR 规范  
- GPU 环境 + conda + `pip install -e ntops`  

### 4.2 不适用范围

- Triton `@triton.jit` 风格（会被 preflight 拒绝）  
- norm / attention 等复杂算子（forge 在 PLAN 阶段停止，提示先读 reference）  
- 无 CUDA 环境（pytest cuda 用例会 skip）  
- 全量 `pytest tests/`（可能误触发 conv2d 上游问题）  

---

## 五、安装与使用方式

### 5.1 安装

```bash
# 克隆仓库
git clone https://github.com/hongwei-2026/qiyuanbisai.git /root/work/skill
git clone https://github.com/InfiniTensor/ntops.git /root/work/ntops

# 环境
source /root/miniconda3/bin/activate base
pip install pytest
pip install -e /root/work/ntops
cd /root/work/skill
```

### 5.2 Cursor / Agent 安装 Skill

```text
.cursor/skills/ntops-forge/
.cursor/skills/ntops-copilot/
```

### 5.3 推荐使用方式

```bash
python scripts/doctor.py
python scripts/forge.py gate --ntops-root /root/work/ntops   # 主入口
python scripts/run_task.py --task silu --ntops-root /root/work/ntops --finish  # 轻量路径
```

![图4 一键 gate 三算子验收](screenshots/02-forge-gate-summary.png)

**图4** `forge gate`：silu / add / gelu 全部 GATE OK

---

## 六、自测任务与运行记录

### 6.1 自测任务集

| 类型 | 任务 | pytest 文件 |
|------|------|-------------|
| 公开任务 | silu / add / gelu | tests/test_*.py |
| 模拟任务 | forge spec + 任务卡 | skills/ntops-forge/specs/*.yaml |
| 仓库规范 | PR 分支/标题 | SHIP 阶段自动打印 |

### 6.2 运行记录（GPU · RTX 4080 · 2026-06-08）

| 算子 | GUARD | pytest | 耗时 |
|------|-------|--------|------|
| silu | matches reference | 8 passed | ~6.8s |
| add | matches reference | 8 passed | ~7.0s |
| gelu | matches reference | 8 passed | ~6.9s |

![图5 规格驱动公式注入](screenshots/04-spec-formula-injection.png)

**图5** spec `formula` 自动写入生成内核 `application()`

![图6 语义对照 compare_ref](screenshots/15-compare-ref-silu-gelu.png)

**图6** silu / gelu 生成稿与官方 reference 一致

![图7 jsonl 全链路审计](screenshots/07-forge-audit-jsonl.png)

**图7** 三算子 jsonl 五阶段 ok:true，可追溯

---

## 七、自测结果与 A/B 对比（有 skill vs 无 skill）

### 7.1 结构护栏对比

![图8 Triton 被拒 vs forge 通过](screenshots/05-preflight-triton-vs-forge.png)

**图8** 无 skill：Triton 稿 5 项 FAIL；有 skill：forge 稿 preflight OK

### 7.2 A/B 量化结果

| 指标 | Baseline（无 skill） | Treatment（有 skill） | 差值 |
|------|---------------------|----------------------|------|
| preflight 通过率 | 0% | 100% | +100% |
| pytest 通过率 | 未跑通 | 100% | — |
| 平均步骤 | 6 | 1 | -5 |
| 人工介入 | 4 次 | 0 次 | -4 |
| 平均耗时 | ~1200s | ~6s/算子 | -99.5% |

![图9 A/B 评估报告](screenshots/08-ab-report-metrics.png)

**图9** ab_runs.csv 与 AB_Report.md 汇总

### 7.3 轻量路径对比

![图10 copilot 一键完工](screenshots/09-copilot-run-task-finish.png)

**图10** `run_task.py --finish` 亦可完成 silu 全链路

---

## 八、失败诊断案例与修复过程

| 案例 | 现象 | 修复 |
|------|------|------|
| FC-001 | Triton @triton.jit | 改用 premake/application |
| FC-004 | 脚本路径错误 | cd /root/work/skill |
| FC-012 | No module named pytest | pip install pytest |
| gelu 特例 | default_application | compare_ref 多函数名支持 |

![图11 失败自动诊断 fix_cards](screenshots/06-fix-cards-diagnose.png)

**图11** forge_diagnose 自动匹配 FC-001 / FC-004

![图12 自然语言生成 spec](screenshots/10-forge-spec-nl-and-copilot.png)

**图12** `forge_spec.py "relu unary max zero"` 生成 YAML spec

---

## 九、安全、依赖、授权与引用披露

### 9.1 安全与依赖

- **无密钥**：仓库不含 token / 密码  
- **无联网强依赖**：本地脚本 + ntops + pytest  
- **依赖**：Python 3.10+、torch、ninetoothed、ntops（editable）  

### 9.2 HONOR_CODE.md 与 REFERENCE.md

- **HONOR_CODE.md**：本人独立编写声明，见仓库根目录  
- **REFERENCE.md**：引用 ninetoothed-examples（Apache-2.0）与官方文档  

### 9.3 诚信

已阅读大赛诚信守则；内核模式参考公开发布示例，非抄袭其他选手作品。

---

## 十、Proposal 与附件说明

| 材料 | 路径 |
|------|------|
| Proposal | docs/Proposal.md |
| 自测计划 | docs/SelfTestPlan.md |
| GPU 测试报告 | docs/GPU_Test_Report.md |
| 截图说明 | docs/DemoShowcase.md |
| A/B 数据 | docs/ab_runs.csv, docs/AB_Report.md |
| 附件 zip | submission-initial-20260608.zip |
| 本报告 PDF | 于鸿伟_九齿skill创新挑战_中期报告.pdf |

| 提交项 | 链接 |
|--------|------|
| Github | https://github.com/hongwei-2026/qiyuanbisai |
| Commit | https://github.com/hongwei-2026/qiyuanbisai/commit/31bcf3c |

---

## 十一、后续可维护计划

1. **决赛前**：扩展 norm/attention spec（只读 reference 模式）  
2. **对接隐藏任务集**：优化 SKILL 触发词与 fix_cards  
3. **最终赛题报告**：按命名 `于鸿伟_九齿skill创新挑战_T3-1-1_赛题报告.pdf` 补充 benchmark 与性能回退分析  

---

**选手签名**：于鸿伟  
**日期**：2026 年 6 月 8 日
