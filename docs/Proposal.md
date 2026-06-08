# Proposal：ntops-forge + ntops-copilot

**赛道**：九齿 .skill 创新挑战  
**Skill 名称**：`ntops-forge`（主）+ `ntops-copilot`（轻量备选）  
**提交阶段**：初赛（Proposal 2026/05/21 · 初版 2026/06/08）

| 项目 | 内容 |
|------|------|
| 选手姓名（InfiniTensor / 启元报名） | 于鸿伟 |
| GitHub ID（仓库、PR 分支命名） | hongwei-2026 |

---

## 一、要解决什么问题（实用）

大赛九齿开发赛道与 ntops 仓库的真实工作是：**在 `src/ntops/kernels/` 用 NineToothed 写算子 → 测通 → 按规范提 PR**。  
通用 AI Agent 在无领域知识时反复出现三类失败：

1. **写错范式**：生成 Triton `@triton.jit`，无法通过 ntops 评审；  
2. **流程断裂**：不会注册 `__init__.py`、torch 封装、pytest，PR 材料缺 HONOR/REFERENCE；  
3. **无法自检**：语法/结构错误推到 CI 才暴露，浪费 GPU 机时。

本方案不堆文档，而是交付 **双 Skill 套件 + 可执行脚本链**，把失败前移到秒级本地/GPU 检查。

---

## 二、解决方案（可实现）

### 2.1 双 Skill 定位

| Skill | 版本 | 角色 | 典型入口 |
|-------|------|------|----------|
| **ntops-forge** | v1.0 | **主作品**：五段工厂流水线 | `python scripts/forge.py gate` |
| ntops-copilot | v0.5 | 轻量备选：单命令流程 | `python scripts/run_task.py --finish` |

### 2.2 核心设计：ntops-forge 五段流水线

```
PLAN → CODEGEN → GUARD → PROVE → SHIP
规格解读   生成内核   preflight+compare_ref   精准pytest   PR提示+审计
```

| 阶段 | 脚本/资源 | 作用 |
|------|-----------|------|
| PLAN | `forge spec` + `taxonomy.md` | 算子分类路由、执行计划 |
| CODEGEN | `scaffold_kernel.py` + `scaffold_torch.py` | 注入 formula，生成 ntops 范式骨架 |
| GUARD | `preflight.py` + `compare_ref.py` | 结构护栏 + 语义对照官方 reference |
| PROVE | 精准 `tests/test_<op>.py` | GPU pytest 验收（禁止全量） |
| SHIP | `forge_runs.jsonl` + PR 模板 | 可审计交付 |

演示闸门：`forge gate` 一键串联 silu / add / gelu / relu / mul 五算子回归验收。

### 2.3 ntops-copilot（轻量路径）

```
任务卡(YAML) → scaffold → preflight → pytest → PR 模板
```

| 组件 | 路径 | 作用 |
|------|------|------|
| Agent 指令 | `skills/ntops-copilot/SKILL.md` | 6 步工作流 + 大赛 PR 规范 |
| 任务卡 | `tasks/task_*.yaml` | 赛题规格机器可读 |
| 一键完工 | `run_task.py --finish` | 验证 + A/B 记录 |

### 2.4 创新点（可验证、不空洞）

1. **工厂流水线**：同类方案多只有 Markdown；本方案 PLAN→SHIP 每段有输入/输出与失败路由（`fix_cards`）。  
2. **语义对照护栏**：`compare_ref` 对齐官方内核（含 gelu `default_application` 特例）。  
3. **可复现评测协议**：`run_baseline_demo.py` + `forge gate` 生成 A/B 证据——pytest 100%、步骤 1 vs 6、介入 0 vs 4。  
4. **五算子 gate**：silu / add / gelu / relu / mul 一键回归（覆盖 unary + binary）。

### 2.5 与同类方案对比

详见 `docs/CompetitiveAnalysis.md`。核心差异：**文档型 Skill → 可执行工厂 + 双护栏 + jsonl 审计 + 五算子 gate**。

### 2.6 不做什么（保证能落地）

- 不依赖自建云服务；初赛起使用大赛算力即可。  
- 不在 Proposal 阶段承诺完成 50 个算子；聚焦 **流程与工具**，初赛迭代任务卡与脚本。  
- 不替代官方文档，所有 API 以 https://ninetoothed.org 为准。

---

## 三、与提交表单的关系

| 表单字段 | 本方案对应 |
|----------|------------|
| Github 仓库 | `https://github.com/hongwei-2026/qiyuanbisai` |
| PR / Commit | 指向含 `skills/ntops-copilot` 的 commit（或 README 说明的 PR） |
| 附件 zip | `python scripts/pack_submission.py` → `submission-proposal-*.zip` |

**Proposal 阶段交付物**：本仓库 + zip（含本文档 + skill 包）。完整算子实现于初赛在 **ntops 上游仓库** 提 PR。

---

## 四、里程碑

| 时间 | 目标 |
|------|------|
| Proposal（05/21） | 本仓库、skill v0.1、zip 提交 |
| 初赛（06/08） | forge v1.0 + gate 五算子 GPU 实测 + A/B 可复现脚本 |
| 决赛（07/13） | softmax/max_pool2d + benchmark；对接隐藏任务集 |

赛题 4.2 四类自测映射见 `docs/FinalsRoadmap.md`；完整示例见 `skills/ntops-forge/examples/silu_walkthrough.md`。

---

## 五、赛题 4.2 四类自测对照

| 类型 | 案例 | 初赛状态 | 证据 |
|------|------|----------|------|
| 逐元素/广播 | ST1 五算子 | ✅ GPU 完成 | `docs/selftests/ST1_elementwise.md` |
| 归约/分块 | ST2 softmax | ✅ GPU 8 passed | `docs/selftests/ST2_softmax_reduce.md` |
| 布局 stride | ST3 max_pool2d | ✅ GPU 62 passed | `docs/selftests/ST3_max_pool2d_layout.md` |
| 性能/诊断 | ST4 | ✅ A/B+benchmark | `docs/selftests/ST4_perf_diagnosis.md` |

评分逐条对照：`docs/ScoringAlignment.md`

## 六、成功指标（初赛已测）

| 指标 | 目标 | 实测（RTX 4080 / AutoDL） |
|------|------|---------------------------|
| preflight 合法内核 | 100% 通过 | ✅ 五算子 |
| preflight 拒绝 Triton | 100% 拒绝 | ✅ run_baseline_demo |
| compare_ref 一致率 | 100% | ✅ matches reference |
| pytest 通过率 | Treatment > Baseline | ✅ 100% vs 未跑通 |
| 单算子流水线耗时 | < 30 s | ✅ ~7 s |
| gate 五算子 | 全通过 | ✅ GATE OK |
| silu benchmark | 同量级 | ✅ ratio 1.37× |
| A/B 样本 | 5v5 | ✅ 干净对照 |

---

## 七、诚信

已阅读大赛诚信守则。本 Proposal 与 skill 为原创；参考 NineToothed 官方示例已在 `REFERENCE.md` 列出，后续 ntops PR 将附 HONOR_CODE。

**选手姓名（启元报名）**：于鸿伟  
**GitHub ID**：hongwei-2026  
**日期**：2026-06-08（初赛更新）
