# 功能演示与截图说明

**选手**：于鸿伟 · **GitHub**：hongwei-2026  
**测试环境**：AutoDL · NVIDIA RTX 4080 · conda `base`  
**日期**：2026-06-08

本文档对照 `docs/screenshots/` 中的实测截图，说明 ntops-forge / ntops-copilot 的**功能、优势与创新点**。所有截图均在 GPU 云机 `/root/work/skill` 真实执行产生。

---

## 截图索引

| 图 | 文件 | 展示内容 | 结论 |
|----|------|----------|------|
| 1 | `01-doctor-gpu-ok.png` | 环境自检 | ninetoothed / torch / pytest / ntops / CUDA 全部 OK |
| 2 | `02-forge-gate-summary.png` | 一键 gate | silu/add/gelu **GATE OK: all operators passed** |
| 3 | `03-forge-run-silu-full.png` | 五段流水线 | PLAN→CODEGEN→GUARD→PROVE→SHIP 全通过，~6.8s |
| 4 | `04-spec-formula-injection.png` | 规格驱动 | spec `formula` → 生成内核 `application()` 一致 |
| 5 | `05-preflight-triton-vs-forge.png` | 结构护栏 | Triton 稿 **5 项 FAIL**；forge 稿 **OK** |
| 6 | `06-fix-cards-diagnose.png` | 失败诊断 | FC-001 / FC-004 自动匹配修复建议 |
| 7 | `07-forge-audit-jsonl.png` | 审计日志 | 三算子 jsonl 五阶段 `ok: true`，~7s/算子 |
| 8 | `08-ab-report-metrics.png` | A/B 量化 | preflight 0%→100%，步骤 6→1，介入 4→0 |
| 9 | `09-copilot-run-task-finish.png` | 轻量路径 | `run_task --finish` 一键完工 |
| 10 | `10-forge-spec-nl-and-copilot.png` | NL→spec | 「relu unary max zero」→ YAML spec |
| 11 | `11-forge-spec-and-repo-structure.png` | 仓库结构 | forge list + skills/scripts 目录 |
| 12 | `12-demo-logs-batch.png` | 批量演示 | demo-logs 全套日志可复现 |
| 13 | `13-forge-gate-gelu-pipeline.png` | gelu 特例 | `default_application` 语义对照 + 8 passed |
| 14 | `14-forge-run-silu-pipeline.png` | silu 流水线 | 与图 3 互补，含 SHIP 记录 |
| 15 | `15-compare-ref-silu-gelu.png` | 语义对照 | silu/gelu 均 `matches reference` |
| — | `forge-pipeline-arch.png` | 架构图 | 五段流水线示意图 |
| — | `forge-gate-gpu-test.png` | 早期 gate | 4090 环境首次验收 |

---

## 三类问题 → 三类能力

| Agent 常见失败 | Skill 能力 | 截图证据 |
|----------------|-----------|----------|
| 写错范式（Triton） | `preflight --strict` 结构护栏 | 图 5 |
| 流程断裂（漏测/漏注册） | PLAN→SHIP 五段闭环 | 图 2、3 |
| 无法自检（CI 才暴露） | compare_ref + 精准 pytest | 图 4、15 |

---

## 创新点（有截图支撑）

1. **工厂流水线**（PLAN→SHIP）：图 2、3、13 — 非文档型 Skill，每段可执行、可审计  
2. **规格驱动公式注入**：图 4 — YAML `formula` 自动写入 `application()`  
3. **语义对照护栏**：图 15 — 生成稿与官方 reference 逐函数比对  
4. **失败诊断卡**：图 6 — 错误文本 → FC-xxx 修复动作  
5. **jsonl 全链路审计**：图 7 — 每算子五阶段耗时与路径可追溯  
6. **自然语言生成 spec**：图 10、11 — `forge_spec.py` 一句话出 YAML  
7. **A/B 可量化**：图 8 — Treatment 相对 Baseline 步骤 −5、介入 −4  

---

## 答辩推荐演示顺序（约 3 分钟）

```bash
source /root/miniconda3/bin/activate base
cd /root/work/skill

python scripts/doctor.py                              # 图 1
python scripts/forge.py gate --ntops-root /root/work/ntops   # 图 2
cat docs/AB_Report.md                                 # 图 8
```

备用对比：`05-preflight-triton-vs-forge.png`（无 skill vs 有 skill）

---

## 复现命令

```bash
source /root/miniconda3/bin/activate base
cd /root/work/skill
mkdir -p docs/demo-logs

python scripts/doctor.py | tee docs/demo-logs/00-doctor.log
python scripts/forge.py gate --ntops-root /root/work/ntops 2>&1 | tee docs/demo-logs/01-forge-gate.log
python scripts/forge.py run silu --ntops-root /root/work/ntops 2>&1 | tee docs/demo-logs/02-forge-run-silu.log
python scripts/eval_ab.py --input docs/ab_runs.csv --output docs/AB_Report.md
```

完整截图拍摄清单见初赛阶段提供的演示命令列表。
