# Baseline Demo（无 Skill）

**时间**：2026-06-08 18:16

## 1. 模拟 Agent 无领域知识：写出 Triton 稿

```bash
python scripts/preflight.py docs\demo-logs\baseline_triton.py --kernel --strict
```

**exit=1**（预期非 0）

```
FAIL: found Triton @triton.jit — use NineToothed premake/application instead
FAIL: missing function: application
FAIL: kernel must use premake (ntops) or arrangement+make (examples)
FAIL: missing ninetoothed import/usage
FAIL: missing # noqa: F841 on output assignment (ntops convention)
```

## 2. 模拟流程断裂：缺 premake / ninetoothed

**exit=1**（预期非 0）

```
FAIL: kernel must use premake (ntops) or arrangement+make (examples)
FAIL: missing ninetoothed import/usage
FAIL: missing # noqa: F841 on output assignment (ntops convention)
```

## 3. Baseline 记录（无 skill 典型路径）

| 算子 | 典型步骤 | 人工介入 | 耗时(估) | preflight | pytest |
|------|----------|----------|----------|-----------|--------|
| silu | 6 | 4 | 1200s | FAIL | 未跑通 |
| add | 6 | 4 | 1200s | FAIL | 未跑通 |
| gelu | 6 | 4 | 1200s | FAIL | 未跑通 |
| relu | 6 | 4 | 1200s | FAIL | 未跑通 |
| mul | 6 | 4 | 1200s | FAIL | 未跑通 |

## 4. Treatment 对照命令（有 skill）

```bash
source /root/miniconda3/bin/activate base
cd /root/work/skill
python scripts/forge.py gate --ntops-root /root/work/ntops
python scripts/eval_ab.py --input docs/ab_runs.csv --output docs/AB_Report.md
```

> Treatment 由 `forge gate` 自动 record_run；本脚本只负责 Baseline 侧证据。
