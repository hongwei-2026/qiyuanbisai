# 自测计划（九齿 .skill 创新挑战 · 初赛）

| 项目 | 内容 |
|------|------|
| 组名/选手 | 于鸿伟 |
| GitHub | hongwei-2026 |
| 仓库 | https://github.com/hongwei-2026/qiyuanbisai |
| 日期 | 2026-06-06 |

---

## 1. 自测目标

验证 skill 能否让 Agent **更少犯错、更快完成** ntops 九齿 elementwise 算子开发，并形成可复现证据。

---

## 2. 自测环境

| 环境 | 用途 | 配置 |
|------|------|------|
| **GPU 主环境** | 正确性结论 | SeetaCloud / AutoDL，RTX 4090，conda `base` |
| **CPU 对照** | 安装/结构检查 | 华为 CPU 机（pytest 因无 CUDA 跳过） |
| **本地 Windows** | 脚本/preflight | 无 triton，不跑 ntops pytest |

工作目录（GPU）：`/root/work/skill`，`/root/work/ntops`

---

## 3. 自测任务集

### 3.1 公开任务（ntops 官方测试）

| 算子 | 类型 | pytest 文件 | 预期 |
|------|------|-------------|------|
| silu | unary | `tests/test_silu.py` | 8 passed |
| add | binary | `tests/test_add.py` | 8 passed |
| gelu | unary | `tests/test_gelu.py` | 8 passed（部分 skipped 正常） |
| relu | unary | `tests/test_relu.py` | 8 passed |
| mul | binary | `tests/test_mul.py` | 8 passed |

### 3.2 模拟任务（skill 任务卡 / forge spec）

- `skills/ntops-copilot/tasks/task_*.yaml`（5 张）
- `skills/ntops-forge/specs/*.yaml`（silu/add/gelu）
- 命令：`forge.py run <op>` 或 `run_task.py --finish`

### 3.3 仓库任务（大赛 PR 规范）

- 分支命名：`2026-spring-hongwei-2026-<赛题号>`
- PR 标题：`[2026春季][赛题号] hongwei-2026`
- 初赛阶段：**不要求 PR 合入**，以独立 skill 仓库 + commit 链接提交

---

## 4. 自测流程（forge 主路径）

```bash
source /root/miniconda3/bin/activate base
cd /root/work/skill
python scripts/doctor.py
python scripts/run_baseline_demo.py --reset-csv
python scripts/forge.py gate --ntops-root /root/work/ntops
python scripts/eval_ab.py --input docs/ab_runs.csv --output docs/AB_Report.md
```

五段流水线：**PLAN → CODEGEN → GUARD → PROVE → SHIP**

GUARD 检查项：`preflight --strict` + `compare_ref matches reference`

---

## 5. 量化指标

| 指标 | Baseline（无 skill） | Treatment（有 skill） | 记录方式 |
|------|---------------------|----------------------|----------|
| preflight 通过率 | 待补 1 轮对照 | **100%**（silu/add/gelu） | `ab_runs.csv` |
| pytest 通过率 | 未跑通 | **100%**（8/8 per op） | GPU 日志 |
| 人工介入次数 | **4 次**（估） | **0 次**（gate 一键） | `ab_runs.csv` |
| 端到端耗时 | — | **~5.7s/算子**，gate ~17s | `forge_runs.jsonl` |
| 结构错误拦截 | Triton/缺 premake | preflight **100% 拒绝** | 脚本实测 |

汇总命令：

```bash
python scripts/eval_ab.py --input docs/ab_runs.csv --output docs/AB_Report.md
```

---

## 6. 通过标准（初赛）

- [x] `doctor` 全 OK（GPU）
- [x] `forge gate`：silu + add + gelu 全 `GATE OK`
- [x] 每个算子 GUARD 输出 `matches reference`
- [x] 每个算子 PROVE：`8 passed`
- [x] 审计日志 `docs/forge_runs.jsonl` 可复现
- [x] Baseline 对照 1 轮（silu，见 `docs/AB_Report.md`）

---

## 7. 风险与规避

| 风险 | 规避 |
|------|------|
| 跑全量 `pytest tests/` 误失败 conv2d | 只用 `tests/test_<op>.py` |
| 在 `$HOME` 跑脚本找不到文件 | 固定 `cd /root/work/skill` |
| gelu 参考无 `application()` | `compare_ref` 支持 `default_application` |

---

## 8. 附件

- `docs/GPU_Test_Report.md`
- `docs/screenshots/forge-gate-gpu-test.png`
- `docs/forge_runs.jsonl`
