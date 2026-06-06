# ntops-forge 设计说明（全新 Skill）

## 为什么做第二个 Skill？

`ntops-copilot` v0.5 解决了「脚本能用」，但 Agent 仍需**自行编排**多条命令。  
大赛评委更关心：**能否用统一协议驱动 Agent 完成闭环**。

`ntops-forge` 把「辅助脚本集」升级为 **算子工厂流水线**。

## 核心创新

| # | 创新点 | 可验证方式 |
|---|--------|------------|
| 1 | **五段流水线** PLAN→CODEGEN→GUARD→PROVE→SHIP | `forge.py run silu` 一次跑通 |
| 2 | **Taxonomy 路由** | `taxonomy.md` + spec `family` 字段 |
| 3 | **失败诊断卡** | `forge diagnose` 匹配 FC-001~009 |
| 4 | **审计日志** | `docs/forge_runs.jsonl` 每阶段 ok/error |
| 5 | **NL→Spec** | `forge_spec.py "add binary"` 生成 YAML |

## 与 copilot 共存

- **copilot**：轻量、单命令、`run_task --finish`
- **forge**：大赛演示、审计、诊断、规格驱动

推荐 Agent 规则：

```
若用户说「工厂」「流水线」「forge」「大幅度」→ 加载 ntops-forge
若用户说「快速」「单算子」→ 可用 ntops-copilot
```

## 实测命令（GPU）

```bash
cd /root/work/skill
python scripts/forge.py list
python scripts/forge.py run silu --ntops-root /root/work/ntops
python scripts/forge.py run add --ntops-root /root/work/ntops
cat docs/forge_runs.jsonl
```

## 提交建议

初赛附件可同时包含：

- `skills/ntops-copilot/` — 轻量版（已 GPU 实测）
- `skills/ntops-forge/` — 工厂版（创新主叙事）
- `docs/Forge_Design.md` — 本文件
