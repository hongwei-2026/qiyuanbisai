# GPU 环境测试报告

**日期**：2026-06-06  
**选手**：于鸿伟（hongwei-2026）  
**Skill 版本**：v0.4 / v0.5  
**环境**：SeetaCloud / AutoDL，`connect.westb.seetacloud.com:48605`

## 硬件与 CUDA

```
GPU: NVIDIA GeForce RTX 4090
Driver: 580.105.08
CUDA: 13.0 (nvidia-smi)
torch: 2.8.0+cu128
torch.cuda.is_available(): True
```

## 工作目录

```bash
source /root/miniconda3/bin/activate base
cd /root/work/skill    # 脚本在此，不要在 ~ (/root) 直接跑
```

## v0.4 闭环验证

| 算子 | 类型 | run_task | compare_ref | pytest |
|------|------|----------|-------------|--------|
| silu | unary | `+formula` ✅ | matches reference ✅ | 8 passed |
| add | binary | `+formula` ✅ | matches reference ✅ | 8 passed |

```bash
python scripts/run_task.py --task silu --ntops-root /root/work/ntops --contest-id T1-1-1
python scripts/compare_ref.py /tmp/silu_kernel.py --ref /root/work/ntops/src/ntops/kernels/silu.py
python scripts/verify_task.py --name silu --ntops-root /root/work/ntops \
  --kernel /tmp/silu_kernel.py --compare-ref /root/work/ntops/src/ntops/kernels/silu.py --pytest

cd /root/work/ntops && pytest -q tests/test_add.py   # add: 8 passed
```

## 注意事项

- **不要**运行 `pytest tests/` 全量：上游 `conv2d` 在当前 Triton 环境可能失败，与 skill 无关。
- 使用任务卡 `pytest_file`（v0.5）或 `tests/test_<op>.py` 做精准测试。

## 结论

- `ntops-copilot` 在 GPU 环境完成 v0.4 任务卡驱动公式注入、语义对照、pytest 闭环验收。
- silu/add 官方测试各 8/8 通过，可作为初赛「可实现」证据。
