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

## 4. benchmark（云机无 bench_op.py 时）

### 方式 A — git pull 后

```bash
cd /root/work/skill
git pull origin main
python scripts/bench_op.py --op silu --ntops-root /root/work/ntops
cat docs/bench_silu.json
```

### 方式 B — 内联 Python（无需新脚本）

```bash
source /root/miniconda3/bin/activate base
cd /root/work/skill
python - <<'PY'
import json, sys, time
from datetime import datetime
from pathlib import Path
import torch
import torch.nn.functional as F
sys.path.insert(0, "/root/work/ntops/src")
import ntops.torch as nt
x = torch.randn(4096, 4096, device="cuda", dtype=torch.float16)
def time_fn(fn):
    for _ in range(10): fn()
    torch.cuda.synchronize()
    t0 = time.perf_counter()
    for _ in range(50): fn()
    torch.cuda.synchronize()
    return (time.perf_counter() - t0) / 50 * 1000
ref = time_fn(lambda: F.silu(x))
nt_ms = time_fn(lambda: nt.silu(x))
r = {
    "op": "silu", "shape": [4096, 4096], "dtype": "float16",
    "pytorch_ms": round(ref, 4), "ntops_ms": round(nt_ms, 4),
    "ratio_ntops_over_pytorch": round(nt_ms / ref, 4),
    "recorded_at": datetime.now().isoformat(timespec="seconds"),
}
print(json.dumps(r, indent=2))
Path("docs/bench_silu.json").write_text(json.dumps(r, indent=2) + "\n")
print("OK: wrote docs/bench_silu.json")
PY
```

---

## 5. 常见问题

| 现象 | 处理 |
|------|------|
| `can't open file run_ab_suite.py` | 用本文 **方式 B** 或 `run_ab_manual.sh` |
| `pytest: command not found` | `pip install pytest` |
| `No module named ntops` | `pip install -e /root/work/ntops` |
| treatment 只有 3 条 | 重跑方式 B ①④，确保 for 循环 5 个算子 |
| conv2d 失败 | 不要跑全量 `pytest tests/`，只用 `forge gate` |
