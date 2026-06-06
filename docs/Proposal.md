# Proposal：ntops-copilot

**赛道**：九齿 .skill 创新挑战  
**Skill 名称**：`ntops-copilot`  
**提交阶段**：Proposal（2026/05/21 前）

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

本方案不堆文档，而是交付 **可安装的 skill + 可执行脚本**，把失败前移到本地秒级检查。

---

## 二、解决方案（可实现）

### 2.1 核心设计：闭环而非手册

```
赛题规格(YAML) → 选 unary/binary 模板 → scaffold 生成骨架
    → 只改 application() → preflight(AST) → pytest → PR 模板
```

| 组件 | 路径 | 作用 |
|------|------|------|
| Agent 指令 | `skills/ntops-copilot/SKILL.md` | 6 步工作流 + 大赛 PR 规范 |
| 速查 | `reference.md` | arrangement/application/make 最小样例 |
| Walkthrough | `examples.md` | silu 一元算子端到端 |
| **脚手架** | `scripts/scaffold_kernel.py` | 从模板生成内核文件，减少结构错误 |
| **自检** | `scripts/preflight.py` | 检查 skill 包 / 内核 AST 是否含 make |
| 任务卡 | `tasks/TEMPLATE.yaml` | 赛题规格机器可读，便于评测复现 |

### 2.2 创新点（可验证、不空洞）

1. **可执行 skill**：同类方案多只有 Markdown；本方案把「规范」落到 `preflight` / `scaffold`，Agent 出错可在提交前拦截。  
2. **模式化算子分类**：elementwise unary/binary 覆盖大赛 T1-1 大量基础算子；复杂算子强制先读 `ninetoothed-examples` 同名实现。  
3. **可复现评测协议**：`examples.md` 定义 Baseline vs Treatment 两轮对比（通过率、人工介入次数），与赛道「看 Agent 实际完成效果」一致。

### 2.3 不做什么（保证能落地）

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
| 初赛（06/08） | 至少 3 个任务卡 + Agent A/B 评测记录；preflight 覆盖更多模式 |
| 决赛（07/13） | 对接组委会标准任务集；优化 SKILL 触发词与错误表 |

---

## 五、成功指标

- `preflight` 对合法 `silu.py` 类内核 **100% 通过**；对缺 `make` 的 Triton 稿 **100% 拒绝**。  
- 加载 skill 后，模拟赛题（ unary 算子）**pytest 通过率** 高于无 skill 基线（初赛实测写入 REFERENCE/报告）。

---

## 六、诚信

已阅读大赛诚信守则。本 Proposal 与 skill 为原创；参考 NineToothed 官方示例已在 `REFERENCE.md` 列出，后续 ntops PR 将附 HONOR_CODE。

**选手姓名（启元报名）**：于鸿伟  
**GitHub ID**：hongwei-2026  
**日期**：2026-05-19
