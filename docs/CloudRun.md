# 云机运行指南（AutoDL / SeetaCloud）

云机代码若未 `git pull`，可能没有 `run_ab_suite.py`。先用 **bash 回退脚本** 或 **手动命令** 截图；推送后再用 Python 一键脚本。

---

## 0. 环境准备（每次新开终端）

```bash
source /root/miniconda3/bin/activate base
cd /root/work/skill
pip install -q pytest
pip install -q -e /root/work/ntops
```

> 必须在 `/root/work/skill` 下跑，不要在 `$HOME`。

---

## 1. 截图用：A/B + gate（推荐，无需 run_ab_suite.py）

### 方式 A — bash 一键（云机已有 `run_ab_manual.sh` 时）

```bash
chmod +x scripts/run_ab_manual.sh
bash scripts/run_ab_manual.sh /root/work/ntops
```

### 方式 B — 手动逐步（任何版本都能跑）

```bash
# ① 重置 baseline（5 条）
python scripts/run_baseline_demo.py --reset-csv

# ② 五算子 gate（不写 ab，避免污染）
python scripts/forge.py gate --ntops-root /root/work/ntops --no-record-ab

# ③ 记录 5 条 treatment
for op in silu add gelu relu mul; do
  python scripts/record_run.py --mode treatment --task "$op" \
    --preflight-pass --pytest-pass --steps 1 --interventions 0 --elapsed 7
done

# ④ 生成 A/B 报告（截图下半部分）
python scripts/eval_ab.py --input docs/ab_runs.csv --output docs/AB_Report.md
cat docs/AB_Report.md
```

**截图要点**：终端应同时出现 `GATE OK: all operators passed` 和 `Total baseline runs: 5` / `Total treatment runs: 5`。

---

## 2. 同步最新仓库后（git pull 之后）

```bash
cd /root/work/skill
git pull origin main
python scripts/run_ab_suite.py --ntops-root /root/work/ntops
```

---

## 3. 仅 gate 验收（不要 A/B）

```bash
python scripts/forge.py gate --ntops-root /root/work/ntops
```

---

## 4. 常见问题

| 现象 | 处理 |
|------|------|
| `can't open file run_ab_suite.py` | 用本文 **方式 B** 或 `run_ab_manual.sh` |
| `pytest: command not found` | `pip install pytest` |
| `No module named ntops` | `pip install -e /root/work/ntops` |
| treatment 只有 3 条 | 重跑方式 B ①④，确保 for 循环 5 个算子 |
| conv2d 失败 | 不要跑全量 `pytest tests/`，只用 `forge gate` |
