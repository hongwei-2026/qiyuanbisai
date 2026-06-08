# 优化项与截图结果说明

本截图（`16-gate-ab-5v5-final.png`）对应 **2026-06-08 GPU 实测**，已确认 **5 baseline / 5 treatment** + 五算子 GATE OK。

---

## 截图里是什么结果？

### 上半部分：五算子 GATE OK

```
OK  silu / add / gelu / relu / mul
GATE OK: all operators passed
```

表示 **ntops-forge 五段流水线**在 GPU 上对 5 个 elementwise 算子全部跑通：

| 阶段 | 作用 | 截图可见证据 |
|------|------|-------------|
| PLAN | 读 spec，taxonomy 路由 | `[PLAN] OK: plan ready` |
| CODEGEN | formula 注入生成内核 | `Wrote /tmp/*_forge_kernel.py` |
| GUARD | preflight + compare_ref | `matches reference` |
| PROVE | 精准 pytest | `8 passed`（relu 为 16 passed） |
| SHIP | PR 提示 + jsonl | `FORGE OK (mul) in Xs` |

### 下半部分：A/B 报告

正确版本应为 **5 baseline vs 5 treatment**：

| 指标 | Baseline（无 skill） | Treatment（有 skill） |
|------|---------------------|----------------------|
| preflight | 0% | 100% |
| pytest | 未跑通 | 100% |
| 步骤 | 6 | 1 |
| 人工介入 | 4 | 0 |
| 耗时 | ~1200s | ~7s/算子 |

> 旧截图若仅 `3 treatment`，为 gate 未补录 treatment 所致；最终截图已用 `run_ab_manual.sh` / 手动 for 循环补齐 5 条。

---

## 这些结果由哪些优化带来？

| 优化 | 解决的问题 | 对应结果 |
|------|------------|----------|
| **五段工厂流水线** | Agent 命令零散、漏步骤 | 一条 `forge gate` 跑完 5 算子 |
| **spec 公式注入** | 手写 application 易错 | CODEGEN 自动写入公式 |
| **preflight 结构护栏** | Triton 稿混入 | Baseline preflight 0% |
| **compare_ref 语义护栏** | 公式对但语义不对 | 每算子 `matches reference` |
| **精准 pytest** | 全量 tests 误失败 | 只跑 `tests/test_<op>.py` |
| **relu/mul 扩展 spec** | 覆盖算子少 | gate 从 3 算子扩到 5 算子 |
| **run_baseline_demo.py** | A/B 无基线证据 | 5 算子 baseline 可复现 |
| **run_ab_suite.py** | ab_runs 被重复污染 | 一键 5v5 干净报告 |
| **gelu default_application** | GUARD 误失败 | gelu compare_ref 通过 |

---

## 一键复现（云机）

云机若无 `run_ab_suite.py`，用 bash 回退：

```bash
source /root/miniconda3/bin/activate base
cd /root/work/skill
bash scripts/run_ab_manual.sh /root/work/ntops
```

`git pull` 后可用：

```bash
python scripts/run_ab_suite.py --ntops-root /root/work/ntops
```

预期：`5 baseline / 5 treatment` + `GATE OK: all operators passed`。详见 [CloudRun.md](CloudRun.md)。
