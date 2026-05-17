# OMC 子 Skill 转换模板

> 用于将 `modules/on-demand/*.md` 源文件转换为 `.omc/skills/{name}/SKILL.md` 子 Skill。

## 转换流程

```
modules/on-demand/{module-name}.md
        ↓
    [提取 front matter + 清理正文]
        ↓
.omc/skills/{skill-name}/SKILL.md
```

## Step 1: 确定 skill-name

skill-name 使用 kebab-case，与模块名对应：

| 模块文件 | OMC 子 Skill 名称 |
|---------|-----------------|
| `stock-analysis.md` | `benbenjiucai-stock` |
| `portfolio.md` | `benbenjiucai-portfolio` |
| `psychology.md` | `benbenjiucai-psychology` |

命名规则：`benbenjiucai-{主题缩写}` 或 `benben-{功能名}`

## Step 2: 编写 Front Matter

```yaml
---
name: {skill-name}
description: |
  笨笨的韭菜[模块功能描述]。
  当用户[触发条件1]"[关键词1]""[关键词2]"时使用。
  在笨笨的韭菜主 Skill 已激活的前提下补充[模块主题]深度内容。
---
```

Front matter 规范：
- `name`: 必须与目录名一致
- `description`: 3-4行，第一行是功能概述，第二行是触发条件，第三行是加载前提
- 触发关键词必须与源文件的"触发条件"注释一致

## Step 3: 正文转换规则

### 规则1: 去掉触发条件注释

源文件中的这两行**不保留**：
```markdown
> 触发条件：用户问"..."
> 加载方式：渐进加载（...）
```

### 规则2: 调整模块标题

源文件：
```markdown
# 模块：个股分析流程
```

OMC 子 Skill：
```markdown
# 个股分析流程
```

去掉"模块："前缀，保留纯主题名。

### 规则3: 去掉渐进加载声明

源文件末尾的这两行**不保留**：
```markdown
---
*本模块由核心系统渐进加载*
```

### 规则4: 保留所有正文内容

正文内容**原样保留**，包括：
- 所有 H2/H3/H4 标题
- 所有引用和证据标注
- 所有表格和代码块
- 所有"⭐来源深化"标签

## Step 4: 验证同步

转换完成后，运行以下检查：

```bash
# 1. 检查文件大小差异（OMC 应略大于源文件，因 front matter 开销）
diff_size=$(($(stat -c%s .omc/skills/{skill-name}/SKILL.md) - $(stat -c%s modules/on-demand/{module-name}.md)))
echo "Size diff: ${diff_size}B"
# 预期: diff_size > 0 且 < 500

# 2. 检查正文行数差异（应接近）
wc -l .omc/skills/{skill-name}/SKILL.md modules/on-demand/{module-name}.md

# 3. 检查是否遗漏关键内容
grep -c "⭐" .omc/skills/{skill-name}/SKILL.md
grep -c "⭐" modules/on-demand/{module-name}.md
# 两者数量应一致
```

## 目录结构

```
.omc/skills/
└── {skill-name}/
    └── SKILL.md          # 唯一文件，自包含全部内容
```

OMC 子 Skill **不引用**外部文件（包括主 SKILL.md 或 modules/ 下的文件），必须是自包含的。

## 与主 Skill 的关系

- **主 Skill** (`SKILL.md`)：包含角色规则、核心心智模型、决策启发式、表达DNA
- **子 Skill** (`.omc/skills/*/SKILL.md`)：包含特定主题的深度内容
- **加载方式**：OMC 根据用户输入的关键词，自动匹配并加载对应的子 Skill
- **内容冲突**：如子 Skill 与主 Skill 有重叠，以子 Skill 的深化内容为准
