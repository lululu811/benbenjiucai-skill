# 笨笨的韭菜 · Skill 项目

## 项目定位

这是「女娲 v2.0 思维蒸馏」流程的产物——一个基于 B 站 UP 主「笨笨的韭菜」公开语料构建的 AI 角色 Skill。

**用途**：当用户在任意对话中提到「笨笨的韭菜」「笨总」「笨韭」或要求「用笨笨的韭菜的视角分析」时，Claude 自动加载此 Skill，以该 UP 主的思维框架、表达风格和决策逻辑回答问题。

## 当前状态

- **版本**: v2.6
- **架构**: 模块化渐进加载
- **核心系统**: 24 个心智模型 + 50 条决策启发式 + 完整表达 DNA
- **按需模块**: 6 个（个股分析、仓位管理、心态情绪、市场环境、产业链分析、季报解读）
- **数据来源**: 2,506 篇充电问答 + 203 个视频转录文件 + 1,188 条B站动态 + 3 个合集字幕

## 目录结构

```
benbenjiucai-skill/
├── SKILL.md                    # 主 Skill 文件（核心系统 + 角色规则）
├── CLAUDE.md                   # 本文件（项目说明）
├── README.md                   # 工作目录说明 + 蒸馏流程记录
├── CHANGELOG.md                # 版本更新日志
├── .gitignore                  # 忽略 references/sources/（体积大+版权敏感）
├── modules/
│   ├── core/                   # 核心系统（始终加载）
│   │   ├── thinking-models.md  # 24 个心智模型
│   │   ├── heuristics.md       # 50 条决策启发式
│   │   └── identity.md         # 身份卡 + 时间线 + 智识谱系
│   └── on-demand/              # 按需模块（源文件）
│       ├── stock-analysis.md   # 个股分析流程
│       ├── portfolio.md        # 仓位管理
│       ├── psychology.md       # 心态与情绪
│       ├── market-context.md   # 市场环境判断
│       ├── industry-chain.md   # 产业链分析
│       ├── quarterly-report.md # 季报解读
│       └── benben-stock-guide/ # 选股导航（选股导航交互系统）
├── .omc/
│   └── skills/                 # OMC 子 Skill（条件自动加载）
│       ├── benbenjiucai-stock/     # 个股分析
│       ├── benbenjiucai-portfolio/ # 仓位管理
│       ├── benbenjiucai-psychology/ # 心态情绪
│       ├── benbenjiucai-market/    # 市场环境
│       ├── benbenjiucai-industry/  # 产业链分析
│       ├── benbenjiucai-quarterly/ # 季报解读
│       └── benben-stock-guide/     # 选股导航
├── references/
│   ├── research/               # 6 维度调研结果（Agent 产出）
│   │   ├── 01-writings.md
│   │   ├── 02-conversations.md
│   │   ├── 03-expression-dna.md
│   │   ├── 04-external-views.md
│   │   ├── 05-decisions.md
│   │   └── 06-timeline.md
│   ├── sources/                # 一手原始素材（gitignore，不提交）
│   │   ├── transcripts/        # 203 个视频转录文件
│   │   └── articles/           # 充电问答等
│   ├── extraction-framework.md # 思维框架提炼方法论
│   ├── skill-template.md       # SKILL.md 构建模板
│   ├── framework-extraction.md # 框架提炼阶段记录
│   ├── phase4-verification.md  # Phase 4 质量验证记录
│   ├── phase5-optimizer-review.md  # Phase 5 优化器评审
│   ├── phase5-creator-review.md    # Phase 5 创建者评审
│   ├── qa-response-patterns.md # QA 回答模式分析
│   ├── video-transcript-deep-dive.md      # 视频转录深度挖掘报告
│   └── video-transcript-data-quality.md   # 转录数据质量问题记录
└── scripts/
    ├── pre_extract.py          # Phase 1.5 预提炼工具
    └── screenshot.mjs          # Playwright 高清截图脚本（卡片导出）
```

## 工作规范

### 修改 Skill 内容时

1. **优先编辑 modules/**：新增模型/启发式放入对应模块文件，不要直接膨胀 SKILL.md
2. **保持引用一致性**：视频来源标注 `视频编号_标题`，QA 来源标注 `qa_编号`
3. **置信度标注**：一手（🟢）、推断（🟡）、推测（🔴）
4. **时效状态标注**：持续（✅）、演化（🔄）、已放弃（❌）

### 批量挖掘视频转录时

1. 先用 grep/glob 筛选有效文件（过滤空文件/音乐/错误内容）
2. 用并行 Agent 批量读取，每个 Agent 负责 1-2 个文件
3. 提取内容后，先在 modules/ 对应文件中添加，再更新 SKILL.md 的统计数字
4. 遇到转录错误的文件，记录到 `references/video-transcript-data-quality.md`

### 转录数据质量

- 约 50% 的转录文件存在内容不匹配（视频 ID 混淆、只转录到音乐/其他视频）
- 有效文件约 203 个，高质量精读 20+ 个
- 错误类型：LPL 电竞解说、手办开箱、儿童读物、iPhone 测评等

## 版本历史

| 版本 | 时间 | 核心变化 |
|------|------|----------|
| v2.6 | 2026-05-14 | 合集字幕深度挖掘：Model 21-24、H41-H50、AI终极方向、硅基消费 |
| v2.5 | 2026-05-14 | B站动态批量挖掘：Model 16-20、H31-H40、剑宗-气宗双战法、A股不可能三角 |
| v2.4 | 2026-05-13 | 批量挖掘补充：Model 12-15、H23-H30、中美竞争极限逻辑、黑天鹅分级 |
| v2.3 | 2026-05-13 | 模块化架构拆分、风险提示声明、6 个按需模块 |
| v2.2 | 2026-05-12 | 视频转录深度挖掘、笨韭双击/单机框架、11 个模型、22 条启发式 |
| v2.0 | 2026-05-11 | 女娲 v2.0 流程重构、7 个核心模型、10 条启发式 |

## 关键链接

- **女娲 Skill 造人术**: https://github.com/alchaincyf/nuwa-skill
- **蒸馏对象**: 笨笨的韭菜（B站 UP 主）
- **调研规模**: 2,506 篇充电问答 + 203 个视频转录
