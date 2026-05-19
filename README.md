# ntops-copilot — 九齿 .skill 创新挑战（Proposal 提交）

让 AI 智能体按 **「读规格 → 选模板 → 写内核 → 自检 → 测通 → 交 PR」** 闭环完成 [ntops](https://github.com/InfiniTensor/ntops) 算子开发。

## 安装 Skill（Cursor / Agent）

将 `skills/ntops-copilot` 复制到：

- 项目：`.cursor/skills/ntops-copilot/`
- 或全局：`~/.cursor/skills/ntops-copilot/`

## 快速验证（无需 GPU）

```bash
pip install ninetoothed   # 仅做结构检查时可不装 GPU 运行时
python scripts/preflight.py skills/ntops-copilot
python scripts/scaffold_kernel.py --name gelu --pattern unary --out /tmp/gelu.py
python scripts/preflight.py /tmp/gelu.py --kernel
```

## 身份信息

| 用途 | 填写 |
|------|------|
| 启元 / InfiniTensor 报名姓名 | 于鸿伟 |
| GitHub 仓库、PR 分支、commit | **hongwei-2026** |

## 提交大赛表单时填写

| 字段 | 填什么 |
|------|--------|
| Github 仓库 | `https://github.com/hongwei-2026/qiyuan-skill-ntops-copilot`（push 后使用你的实际 URL） |
| PR 链接 **或** Commit 链接 | 任选其一（建议用含 `skills/ntops-copilot` 的 commit） |
| 附件 | 运行 `python scripts/pack_submission.py` 生成的 zip |

## 目录

```
skills/ntops-copilot/     # 核心 .skill
scripts/                  # 脚手架 + 自检（可执行，非空泛文档）
docs/Proposal.md          # Proposal 正文（导出 PDF 放进 zip）
HONOR_CODE.md
REFERENCE.md
```

## 许可

Apache-2.0（与 NineToothed / ntops 生态一致）
