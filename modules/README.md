# 笨笨的韭菜 · 渐进加载模块系统

## 架构概览

```
SKILL.md (主 Skill — 始终加载)
    ├── 风险提示与免责声明
    ├── 角色扮演规则
    ├── 身份卡 + 时间线
    ├── 24 个心智模型
    ├── 50 条决策启发式
    ├── 表达DNA
    └── 子模块索引表

.omc/skills/ (子 Skill — 条件自动加载)
    ├── benbenjiucai-stock/       # 用户问个股时触发
    ├── benbenjiucai-portfolio/   # 用户问仓位时触发
    ├── benbenjiucai-psychology/  # 用户说被套/慌了时触发
    ├── benbenjiucai-market/      # 用户问大盘时触发
    ├── benbenjiucai-industry/    # 用户问产业链时触发
    └── benbenjiucai-quarterly/   # 用户问季报时触发

modules/
    ├── core/                     # 核心层源文件（供参考）
    └── on-demand/                # 按需层源文件（供参考）
```

## 渐进加载机制

### 核心层（始终加载）

`SKILL.md` 在主 Skill 激活时始终加载，包含：
- 角色扮演规则与身份卡
- 24 个核心心智模型
- 50 条决策启发式
- 完整表达DNA
- 子模块索引表

### 按需层（OMC 条件加载）

6 个子 Skill 位于 `.omc/skills/` 目录，通过 OMC 的自动技能发现机制实现条件加载。
每个子 Skill 的 `description` 字段定义了触发关键词：

| 子 Skill | 触发关键词 | 内容 |
|----------|-----------|------|
| `benbenjiucai-stock` | 个股名/代码/"怎么看"/"能买吗"/"分析" | 个股分析流程、行业专题判断 |
| `benbenjiucai-portfolio` | "仓位"/"减仓"/"加仓"/"单调"/"重仓" | 仓位纪律、超配策略、收益固化 |
| `benbenjiucai-psychology` | "被套"/"拿不住"/"慌了"/"怕输" | 心态框架、折扣思维、成功四要素 |
| `benbenjiucai-market` | "大盘"/"市场"/"情绪"/"成交量" | 情绪指标、系统性风险、量价背离 |
| `benbenjiucai-industry` | "产业链"/"上下游"/"谁最受益" | 产业链分析框架、定价权判断 |
| `benbenjiucai-quarterly` | "季报"/"财报"/"业绩"/"毛利率" | 季报三指标、快速分类法 |
| `benben-stock-guide` | "选股"/"打分"/"分析股票" | 七维度量化打分、交互式引导 |
| `benbenjiucai-take-profit` | "止盈"/"减仓"/"高位"/"撤退" | 三维撤退信号、分层退出策略 |
| `benbenjiucai-macro` | "宏观"/"关税"/"CPI"/"中美" | 中美竞争、关税战、跨市场对冲 |
| `benbenjiucai-quant` | "量化"/"数据验证"/"查数据" | 实时数据验证定性判断 |

### 加载规则

1. **自动触发**：用户输入匹配子 Skill 的 `description` 时，OMC 自动加载
2. **多模块叠加**：一个问题可能触发多个子 Skill（如"中芯现在能买吗"→ stock + market）
3. **上下文继承**：子 Skill 假设主 Skill 已激活，使用"我"的身份回答问题
4. **主 Skill 索引**：主 SKILL.md 的"可用子模块"表格帮助 Claude 感知可用模块

### 源文件说明

`modules/core/` 和 `modules/on-demand/` 中的 `.md` 文件是子 Skill 的**源内容**，用于版本追踪和内容审阅。
`.omc/skills/` 下的 SKILL.md 是从这些源文件编译而来，用于实际加载。

## 使用示例

```
用户: "帮我看看中芯国际怎么样"

系统动作:
1. 主 Skill benbenjiucai-perspective 已加载（核心系统）
2. benbenjiucai-stock 子 Skill 自动触发（匹配"中芯国际"+"看"）
3. 可选: websearch "中芯国际 2026 财报 毛利率"
4. 按笨总框架输出分析

---

用户: "被套了，慌得一匹"

系统动作:
1. 主 Skill 已加载
2. benbenjiucai-psychology 子 Skill 自动触发（匹配"被套"+"慌"）
3. 心态安抚 + 诊断病因
```

## 模块编写规范

1. **子 Skill 文件头部**：
   ```yaml
   ---
   name: benbenjiucai-xxx
   description: |
     笨笨的韭菜XXX模块。
     当用户问XXX/提到XXX时使用。
     在笨笨的韭菜主 Skill 已激活的前提下补充XXX深度内容。
   ---
   ```

2. **内容来源**：从 `modules/on-demand/` 源文件同步

3. **独立性保证**：每个子 Skill 应能独立理解，但假设主 Skill 的身份上下文已加载

4. **保持同步**：修改 `modules/on-demand/*.md` 后，同步更新 `.omc/skills/*/SKILL.md`

## 扩展方式

新增模块时：
1. 在 `modules/on-demand/` 下创建 `.md` 源文件
2. 在 `.omc/skills/` 下创建子 Skill 目录和 SKILL.md
3. 更新主 SKILL.md 的"可用子模块"表格
4. 更新本 README 的表格和目录图
5. 更新 CHANGELOG.md
