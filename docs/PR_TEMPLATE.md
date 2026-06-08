# PR 描述模板（对照组委会提交要求）

> 适用分支：`2026-spring-hongwei-2026-T3-1-1`  
> 适用标题：`[2026春季][T3-1-1] hongwei-2026`  
> 初赛阶段以独立仓库提交；本模板供后续向指定仓库提 PR 时使用。

---

## 1. .skill 名称、赛题编号和小组名称

- **Skill 名称**：ntops-forge（主）+ ntops-copilot（辅）
- **赛题编号**：T3-1-1
- **小组名称**：于鸿伟

## 2. 适用任务范围与不适用范围

**适用**：
- ntops elementwise 一元/二元算子（silu、add、gelu、relu、mul）
- 2026-spring 大赛 PR 规范

**不适用**：
- Triton `@triton.jit` 风格
- norm / attention 等复杂算子（需先读 reference）
- 无 CUDA 环境

## 3. 安装与使用方式

```bash
source /root/miniconda3/bin/activate base
pip install pytest && pip install -e /path/to/ntops
cd /root/work/skill
python scripts/forge.py gate --ntops-root /path/to/ntops
```

Cursor：安装 `skills/ntops-forge/` 到 `.cursor/skills/`

## 4. 自测任务或自测案例的运行记录

见 `docs/GPU_Test_Report.md`、`docs/forge_runs.jsonl`、`docs/demo-logs/`（云机可复现）

## 5. 自测结果（AI 使用 .skill 前后对比）

见 `docs/AB_Report.md`：

| 指标 | Baseline | Treatment |
|------|----------|-----------|
| preflight | 0% | 100% |
| pytest | 未跑通 | 100% |
| 步骤 | 6 | 1 |
| 人工介入 | 4 | 0 |

截图：`docs/screenshots/08-ab-report-metrics.png`

## 6. HONOR_CODE.md 与 REFERENCE.md

- 仓库根目录 `HONOR_CODE.md`
- 仓库根目录 `REFERENCE.md`

## 7. Proposal 与赛题报告

- Proposal：`docs/Proposal.md`
- 中期报告：`docs/于鸿伟_九齿skill创新挑战_中期报告.pdf`
- 最终报告（待决赛）：`于鸿伟_九齿skill创新挑战_T3-1-1_赛题报告.pdf`
