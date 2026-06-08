# 双 Skill 调用关系与边界

## 何时用 ntops-forge（主）

- 新算子开发、多算子回归验收
- 需要五段流水线 + jsonl 审计 + gate
- 需要 A/B 量化证据

```bash
python scripts/forge.py run silu --ntops-root /root/work/ntops
python scripts/forge.py gate --ntops-root /root/work/ntops
```

## 何时用 ntops-copilot（辅）

- 单算子快速完工、任务卡驱动
- Agent 已熟悉流程，只需轻量引导

```bash
python scripts/run_task.py --task silu --ntops-root /root/work/ntops --finish
```

## 边界

| 能力 | forge | copilot |
|------|-------|---------|
| taxonomy 路由 | ✅ | — |
| 复杂算子 STOP | ✅ reduction/pooling | 任务卡提示 |
| fix_cards 诊断 | ✅ | 引用 forge |
| jsonl 审计 | ✅ | CSV 可选 |
| NL→spec | ✅ forge_spec.py | — |

**原则**：forge 工厂负责标准路径与护栏；copilot 负责轻量备选。二者共享 `preflight.py`、`compare_ref.py`、`scripts/`。
