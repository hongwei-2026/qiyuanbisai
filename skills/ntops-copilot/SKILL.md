---
name: ntops-copilot
description: >-
  Complete NineToothed ntops operator tasks: read spec, pick elementwise/binary
  template from ninetoothed-examples, implement src/ntops/kernels/*.py with
  arrangement/application/ninetoothed.make, run preflight and pytest, prepare
  InfiniTensor contest PR with HONOR_CODE and REFERENCE. Use for ntops, NineToothed,
  九齿, TOM, arrange-and-apply, 算子开发, 2026-spring PR.
---

# ntops-copilot

面向 **InfiniTensor/ntops** 仓库的算子开发 Agent Skill。目标：在通用大模型上也能稳定产出 **可合并的 PR**，而不是只写说明文档。

## 何时启用

用户提到：`ntops`、`NineToothed`、`九齿`、`算子`、`kernels/`、`ninetoothed.make`、`2026-spring` PR、InfiniCore 接入、T1-1 赛题等。

## 硬性原则（按优先级）

1. **正确性 > 性能**：先 `pytest` 通过，再谈 benchmark。
2. **禁止把 Triton 内核当 NineToothed 交**：ntops 内核必须是 `arrangement` + `application` + `ninetoothed.make`。
3. **禁止抄袭**：凡参考 `ninetoothed-examples` / 他人 PR，必须更新 `REFERENCE.md`。
4. **大赛 PR 规范**（算子开发赛道同样适用）：
   - 分支：`2026-spring-hongwei-2026-<赛题号>`（例：`2026-spring-hongwei-2026-T1-1-1`）
   - 标题：`[2026春季][赛题号] hongwei-2026`
   - 描述含：各平台测试结果截图、`HONOR_CODE.md`、`REFERENCE.md`

## 标准工作流（必须按序）

### Step 0 — 确认仓库与依赖

```bash
git clone https://github.com/InfiniTensor/ntops.git
cd ntops
pip install -e .
# 对照官方示例（实现前至少读 1 个同类型算子）
git clone https://github.com/InfiniTensor/ninetoothed-examples.git  # 放同级目录备查
```

### Step 1 — 读规格并分类

| 类型 | 输入张量数 | 参考示例 |
|------|------------|----------|
| `unary` | 1 in + 1 out | `ninetoothed-examples/ops/ninetoothed/kernels/silu.py` |
| `binary` | 2 in + 1 out | `.../kernels/add.py` |
| `norm` | 见 rms_norm | `.../kernels/rms_norm.py` |

把赛题给的数学定义写成 3 行：**输入 shape/dtype、计算公式、边界**。

### Step 2 — 脚手架（可选但推荐）

在 **ntops 仓库根目录**执行（本 skill 自带脚本路径按实际调整）：

```bash
python /path/to/ntops-copilot/scripts/scaffold_kernel.py \
  --name <op_name> --pattern unary|binary --out src/ntops/kernels/<op_name>.py
```

然后 **只改 `application()` 里的计算逻辑**，不要乱改 `ninetoothed.make` 结尾。

### Step 3 — 实现 checklist

内核文件必须包含：

- [ ] `from ninetoothed import Symbol, Tensor`（按需 `import ninetoothed.language as ntl`）
- [ ] `def arrangement(...):` 内对输入/输出 `.tile((BLOCK_SIZE,))`
- [ ] `def application(...):` 内完成计算；输出张量赋值用 `# noqa: F841` 若 linter 报未使用
- [ ] `tensors = (...)` 与 `kernel = ninetoothed.make(arrangement, application, tensors)`
- [ ] `BLOCK_SIZE = Symbol("BLOCK_SIZE", constexpr=True)` 或赛题指定的 meta 符号

**在 `src/ntops/kernels/__init__.py` 注册导出**（若仓库已有同类算子，照抄其 export 方式）。

**在 `src/ntops/torch/` 增加 Python 封装**（对照已有 `silu`/`add` 文件）。

### Step 4 — 自检（提交 PR 前必跑）

```bash
python /path/to/ntops-copilot/scripts/preflight.py src/ntops/kernels/<op_name>.py --kernel
pytest tests/ -k <op_name> -q
```

`preflight` 失败则 **禁止** 打开 PR。

### Step 5 — InfiniCore 接入（赛题要求时）

对照官方流程（大赛指南）：

1. 参考 `InfiniCore/python/infinicore/nn/functional/silu.py`
2. 在 InfiniCore 取消注释对应算子调用
3. 跑 InfiniCore Python 级测试

### Step 6 — PR 材料

使用 `skills/ntops-copilot/templates/PR_DESCRIPTION.md` 填空。附上：

- 正确性测试通过截图
- 性能对比说明（若赛题要求；评测时会关自动调优）

## 常见错误 → 处理

| 现象 | 原因 | 处理 |
|------|------|------|
| Agent 写了 `@triton.jit` | 混淆 Triton | 删 Triton 内核，改用 arrangement/application |
| `make` 报 tensor 数量不对 | `tensors` 元组长度与 arrangement 参数不一致 | 对齐参数个数 |
| pytest 超时 | `Symbol(..., meta=True)` 自动调优 | 大赛调试时改 `constexpr=True` 或固定整数 BLOCK_SIZE |
| PR 被拒 | 缺 HONOR/REFERENCE | 补全并重新 push |

## 附加资源

- 详细 API 对照：`reference.md`
- 完整 walkthrough：`examples.md`
- 赛题任务卡样例：`tasks/TEMPLATE.yaml`

## 脚本（本 skill 配套）

| 脚本 | 作用 |
|------|------|
| `scripts/scaffold_kernel.py` | 按 unary/binary 生成内核骨架 |
| `scripts/preflight.py` | AST/结构检查，拦截低级错误 |

执行脚本不能代替读官方文档；实现复杂算子（mm、attention）时 **必须先读** `ninetoothed-examples` 中同名或最接近的算子。
