# 向 NineToothed 主仓库提 PR（组委会最新要求）

## 官方链接

| 项目 | 链接 |
|------|------|
| **NineToothed 主仓库** | https://github.com/InfiniTensor/ninetoothed |
| **CONTRIBUTING** | https://github.com/InfiniTensor/ninetoothed/blob/master/CONTRIBUTING.md |
| **PR 模板** | https://github.com/InfiniTensor/ninetoothed/blob/master/.github/pull_request_template.md |
| **ntops 算子库**（skill 验收用） | https://github.com/InfiniTensor/ntops |
| **你的 skill 仓库** | https://github.com/hongwei-2026/qiyuanbisai |
| **参考 PR（同赛道 T3-1-1）** | https://github.com/InfiniTensor/ninetoothed/pull/159 |

## 你要做什么

把 **.skill 作品** 以 PR 形式提到 **InfiniTensor/ninetoothed** 的 `master` 分支，目录为：

```
skills/competition/ntops-forge/
skills/competition/ntops-copilot/
```

根目录附带：`HONOR_CODE.md`、`REFERENCE.md`、`PR_DESCRIPTION.md`。

---

## 一键导出 PR 内容

```bash
cd qiyuan-skill-ntops-copilot
python scripts/prepare_ninetoothed_pr.py
# 生成 ninetoothed-pr-export/ 目录
```

---

## 提交步骤（GitHub 网页或命令行）

### 1. Fork 主仓库

打开 https://github.com/InfiniTensor/ninetoothed → **Fork** → 得到 `hongwei-2026/ninetoothed`

### 2. 克隆你的 fork

```bash
git clone https://github.com/hongwei-2026/ninetoothed.git
cd ninetoothed
git remote add upstream https://github.com/InfiniTensor/ninetoothed.git
git fetch upstream
git checkout master
git pull upstream master
```

### 3. 创建大赛分支

```bash
git checkout -b 2026-spring-hongwei-2026-T3-1-1
```

> 分支名对照赛题规则：`2026-spring-<GitHub ID>-T3-1-1`

### 4. 复制导出内容

把本地 `ninetoothed-pr-export/` 里的文件**合并进** fork 仓库根目录（不要覆盖整个仓库，只添加 `skills/competition/` 等新增文件）。

### 5. 设置 Git hooks（CONTRIBUTING 要求）

```bash
git config core.hooksPath .githooks
```

### 6. 本地检查

```bash
ruff format && ruff check   # 若改了 ninetoothed 源码
pytest                      # ninetoothed 自带测试应仍通过
```

本 PR **只添加 skill 文件**，不改 `src/ninetoothed/`，pytest 一般仍全绿。

### 7. 提交并推送

```bash
git add skills/competition HONOR_CODE.md REFERENCE.md PR_DESCRIPTION.md
git commit -m "Add ntops-forge skill for 2026 spring T3-1-1"
git push -u origin 2026-spring-hongwei-2026-T3-1-1
```

> Commit 标题：首字母大写、祈使语气、无句号（见 CONTRIBUTING）

### 8. 创建 PR

打开：https://github.com/InfiniTensor/ninetoothed/compare/master...hongwei-2026:2026-spring-hongwei-2026-T3-1-1

| 字段 | 填写 |
|------|------|
| **Title** | `[2026春季][T3-1-1] hongwei-2026 — ntops-forge 九齿算子工厂` |
| **Body** | 粘贴 `PR_DESCRIPTION.md` 内容，并补上 `pytest` 输出 |

或用命令行（需 `gh auth login`）：

```bash
gh pr create \
  --repo InfiniTensor/ninetoothed \
  --base master \
  --head hongwei-2026:2026-spring-hongwei-2026-T3-1-1 \
  --title "[2026春季][T3-1-1] hongwei-2026 — ntops-forge 九齿算子工厂" \
  --body-file PR_DESCRIPTION.md
```

---

## 与初赛官网提交的关系

| 渠道 | 内容 |
|------|------|
| **官网表单**（已交） | skill 仓库 + commit + zip |
| **NineToothed PR**（本条通知） | 把 skill 同步到主仓 `skills/competition/` |

**两个都要做**：官网是初赛材料，PR 是组委会新要求的统一入口。

---

## PR 标题规范对照

| 选手示例 | 标题格式 |
|----------|----------|
| [PR #163](https://github.com/InfiniTensor/ninetoothed/pull/163) | `[2026春季][T1-2-1] 何ev — …` |
| 你 | `[2026春季][T3-1-1] hongwei-2026 — ntops-forge 九齿算子工厂` |

---

## 常见问题

| 问题 | 处理 |
|------|------|
| pre-push hook 拒绝分支名 | 确认全小写+连字符：`2026-spring-hongwei-2026-T3-1-1` |
| pytest 要贴什么 | 先贴 `pytest`（ninetoothed）；再贴 ntops gate 结果（PR_DESCRIPTION 已留位） |
| skill 脚本路径变了 | 使用 `skills/competition/ntops-forge/scripts/forge.py` |
