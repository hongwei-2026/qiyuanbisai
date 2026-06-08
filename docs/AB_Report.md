# A/B Evaluation Report

## Data Summary

- Total baseline runs: 1
- Total treatment runs: 3

## Metrics

| Metric | Baseline | Treatment | Delta (Treatment - Baseline) |
|---|---:|---:|---:|
| preflight pass rate | 0.0% | 100.0% | 100.0% |
| pytest pass rate | N/A | 100.0% | N/A |
| avg steps | 6.00 | 1.00 | -5.00 |
| avg interventions | 4.00 | 0.00 | -4.00 |
| avg elapsed seconds | 1200.00 | 6.00 | -1194.00 |

## Conclusion

- Quality: Treatment 在 GPU 环境 pytest 通过率 100.0%；Baseline 无 skill 时 preflight 0.0%、pytest 未跑通。
- Efficiency: Treatment 平均步骤 1.0 vs Baseline 6.0（-5.00）。
- Human effort: Treatment 人工介入 0.0 次 vs Baseline 4.0 次（-4.00）。
