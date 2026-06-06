# 初赛报告：ntops-copilot

## 1. 选手信息

- 姓名（启元报名）：于鸿伟
- GitHub ID：hongwei-2026
- Skill：`ntops-copilot`

## 2. 初赛目标

- 将通用 Agent 在 ntops 任务中的常见失败（写错范式、漏流程、无自检）前移到本地拦截。
- 用 A/B 对比验证：加载 skill 后，任务通过率和效率是否提升。

## 3. 实施内容

- Skill 工作流：`read spec -> scaffold -> implement -> preflight -> pytest -> PR material`
- 可执行脚本：
  - `scripts/scaffold_kernel.py`
  - `scripts/preflight.py`
  - `scripts/eval_ab.py`
- 任务卡：
  - `skills/ntops-copilot/tasks/TEMPLATE.yaml`
  - `skills/ntops-copilot/tasks/task_silu.yaml`
  - `skills/ntops-copilot/tasks/task_add.yaml`

## 4. A/B 实验方法

- Baseline：不加载 `ntops-copilot`
- Treatment：加载 `ntops-copilot`
- 统一记录字段见 `docs/ab_runs.csv`
- 自动汇总命令：

```bash
python scripts/eval_ab.py --input docs/ab_runs.csv --output docs/AB_Report.md
```

## 5. 实验结果

### 5.1 Skill 工具链（远端 GPU 机验证）

环境：SeetaCloud `connect.westb.seetacloud.com:48605`，**NVIDIA GeForce RTX 4090**，`torch.cuda.is_available()=True`。

| 测试项 | 结果 |
|--------|------|
| `preflight.py skills/ntops-copilot` | ✅ OK |
| `scaffold_kernel.py` + kernel `preflight` | ✅ OK |
| `pytest -k silu`（ntops） | ✅ **8 passed** |
| `pytest tests/test_add.py`（ntops） | ✅ **8 passed** |

> 注意：远端需先 `source /root/miniconda3/bin/activate base`，系统默认无 `python3` 命令。

### 5.2 华为 CPU 机（对照）

- `pytest` 收集用例正常，但全部 `SKIPPED: CUDA not available`（无 `nvidia-smi`）。
- 说明 ntops 测试依赖 CUDA，CPU 机仅能验证安装与用例发现，不能作为算子正确性结论。

### 5.3 v0.4 / v0.5 优化（实用性 + 创新性）

| 版本 | 能力 |
|------|------|
| v0.3 | `premake` 范式对齐、`run_task`、`doctor`、`formulas.md` |
| v0.4 | 任务卡 `formula_hint` 注入、`compare_ref`、`verify_task`、`register_op`、`record_run` |
| v0.5 | 任务卡 `pytest_file` 精准测试、`--finish` 一键完工、`list_tasks` |

**GPU 闭环（v0.4 实测）**：

| 算子 | compare_ref | pytest |
|------|-------------|--------|
| silu | ✅ matches reference | ✅ 8 passed |
| add | ✅ matches reference | ✅ 8 passed |

### 5.4 A/B 报告

远端已用 `record_run.py` 记录 treatment 跑数；汇总：

```bash
python scripts/eval_ab.py --input docs/ab_runs.csv --output docs/AB_Report.md
```

## 6. 结论

- 实用性：该 skill 可直接复用于后续算子任务，降低人工返工。
- 可实现性：依赖轻量，无需自建云服务；可在本地与组委会环境复现。
- 后续计划：补充复杂算子任务卡（如 norm/attention）与错误样例库。
