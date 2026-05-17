# Changelog

All notable changes to the 笨笨的韭菜 Skill project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.7.0] - 2026-05-17

### Added
- 新建3个按需模块：
  - `take-profit` — 止盈策略（H41高位止盈三维信号独立成模块，宏观/板块/个股三层撤退信号）
  - `macro-analysis` — 宏观分析（Model14中美竞争极限逻辑、Model23关税战情景推演、H23CPI/H29跨市场对冲/H39关税应对）
  - `quant-enhanced` — 量化增强（Tushare数据验证定性判断，5个量化维度：纯度/壁垒/估值/撤退/宏观）
- 新增3个OMC子Skill：benbenjiucai-take-profit、benbenjiucai-macro、benbenjiucai-quant
- 新建4个开发模板：`agent-research-task`、`on-demand-module`、`validation-test-case`、`omc-subskill`
- 构建自动化脚本：
  - `scripts/sync_omc.py` — OMC子Skill自动同步（10个映射）
  - `scripts/validate_skill.py` — 质量验证（禁用词/人称/引用格式/OMC同步状态）
- Tushare中转站数据源接入（http://tsy.xiaodefa.cn，15000积分权限）
- 量化增强模式用户引导（首次激活时询问是否开启，可随时切换）

### Fixed
- `thinking-models.md` 删除Model 20重复内容
- `benben-stock-guide/SKILL.md` 重构去重（删除3处重复内容，342→269行）
- `industry-chain.md` 内容充实（39→111行，新增壁垒维度/轮动规律/行业案例）
- `.omc/skills/` 全部重新同步（修复最高33%的内容缩水问题）
- `SKILL.md` / `modules/README.md` 补充 benben-stock-guide / 止盈策略 / 宏观分析 / 量化增强 索引

### Changed
- 宏观验证数据源从 `cn_m` 改为 `mcp__MiniMax__web_search`（Tushare宏观数据延迟/为空）
- 子Skill总数从7个扩展至10个
- 模块总数从6个扩展至9个（+止盈策略+宏观分析+量化增强）

## [2.6.1] - 2026-05-15

### Added
- OMC 子 Skill 架构（方案二实现）
- 6个按需子 Skill 拆分为独立 Skill：
  - `benbenjiucai-stock` — 个股分析（触发词：个股名/代码/"怎么看"/"能买吗"）
  - `benbenjiucai-portfolio` — 仓位管理（触发词："仓位"/"减仓"/"加仓"/"单调"）
  - `benbenjiucai-psychology` — 心态情绪（触发词："被套"/"慌了"/"怕输"）
  - `benbenjiucai-market` — 市场环境（触发词："大盘"/"情绪"/"成交量"）
  - `benbenjiucai-industry` — 产业链分析（触发词："产业链"/"谁最受益"）
  - `benbenjiucai-quarterly` — 季报解读（触发词："季报"/"毛利率"/"扣非"）
  - `benben-stock-guide` — 选股导航（已移至 `.omc/skills/`）
- 主 SKILL.md 新增"可用子模块"索引表
- `.omc/skills/` 目录结构建立
- `.gitignore` 更新：保留 `.omc/skills/` 跟踪
- modules/README.md 重写：说明源文件与加载文件的区别
- 文档统一：版本号、数据规模、目录结构全部更新

### Changed
- `modules/on-demand/` 定位改为"源文件"而非"加载文件"
- `benben-stock-guide` 从 `modules/` 同步至 `.omc/skills/`

## [2.6.0] - 2026-05-14

### Added
- 合集字幕深度挖掘（Phase 10完成）
- 新增4个心智模型（Model 21-24）：
  - Model 21: AI终极方向（生命科学+星际文明）
  - Model 22: 判断力-品位-责任三要素
  - Model 23: 关税战情景推演
  - Model 24: 硅基消费
- 新增10条决策启发式（H41-H50）：
  - H41: 高位止盈三维信号
  - H42: 一带一路选股6条标准
  - H43: 自主可控反向验证法
  - H44: 压力越大越冷静
  - H45: 现象级事件四要素
  - H46: 政策新闻四要素
  - H47: 换手率警戒线
  - H48: 储能投资海外优先
  - H49: 恒生科技ETF筛选标准
  - H50: 消费板块系统性回避
- 新增选股导航交互系统：`modules/benben-stock-guide/SKILL.md`
- SKILL.md v2.6 更新完成

### Changed
- 心智模型从 20 个扩展至 24 个
- 决策启发式从 40 条扩展至 50 条

### Data
- 3个合集字幕并行分析（选股逻辑教学+高景气机会事件+优秀直播录像）

## [2.5.0] - 2026-05-14

### Added
- B站动态批量挖掘（Phase 9完成）
- 新增5个心智模型（Model 16-20）：
  - Model 16: 剑宗-气宗双战法
  - Model 17: 水位/成交量理论
  - Model 18: 投票定律
  - Model 19: A股不可能三角
  - Model 20: 慢牛优于快牛
- 新增10条决策启发式（H31-H40）：
  - H31: 做T五条件法则
  - H32: 港股解禁杀伤力规则
  - H33: 评论医情绪反向指标
  - H34: 台积电资本开资=海外AI见顶信号
  - H35: 70%个股破五日线=撤退信号
  - H36: 情绪高点右侧止盈
  - H37: 核心主线特殊对待
  - H38: 资金规模与持股数量
  - H39: 关税应对策略
  - H40: 存储涨价行情规律
- 持仓数据补充：账户规模900-1015万、满仓99.97%
- SKILL.md v2.5 更新完成

### Changed
- 心智模型从 15 个扩展至 20 个
- 决策启发式从 30 条扩展至 40 条

### Data
- 4个并行Agent分析1188条B站动态

## [2.4.0] - 2026-05-13

### Added
- 批量挖掘视频转录补充（Phase 8完成）
- 新增4个心智模型（Model 12-15）：
  - Model 12: 情绪蔓延判断/板块退潮动力学
  - Model 13: 港股间歇性下跌规律
  - Model 14: 中美竞争极限逻辑
  - Model 15: 黑天鹅分级应对
- 新增8条决策启发式（H23-H30）：
  - H23: CPI回暖是消费前置条件
  - H24: 超配策略
  - H25: 精简回本战略
  - H26: 阶段性收益固化
  - H27: 小资金翻倍市值门槛
  - H28: ETF恐慌定投
  - H29: 跨市场对冲
  - H30: 黑天鹅分级
- 模块文件更新：portfolio.md、psychology.md、market-context.md、stock-analysis.md

### Changed
- 心智模型从 11 个扩展至 15 个
- 决策启发式从 22 条扩展至 30 条
- SKILL.md 从 v2.3 升级至 v2.4

### Data
- 8个并行Agent批量读取视频转录

## [2.3.0] - 2026-05-13

### Added
- Skill 模块化拆分 + 渐进加载系统
- 核心层（始终加载）：`modules/core/identity.md`、`thinking-models.md`、`heuristics.md`
- 按需层（渐进加载）：6个模块
  - `market-context.md` — 市场环境判断（成交量/情绪/反向指标/2周验证窗）
  - `stock-analysis.md` — 个股分析流程（三层漏斗/事件分级/双触发买回）
  - `portfolio.md` — 仓位管理（纪律/加减规则/心态/分餐奥义）
  - `quarterly-report.md` — 季报解读（三指标/快速分类法）
  - `industry-chain.md` — 产业链分析（定价权/环节筛选）
  - `psychology.md` — 心态与情绪（怕输/成功四要素/劝退）
- `modules/README.md` — 模块加载机制说明和扩展规范
- 视频转录数据质量问题记录：`references/video-transcript-data-quality.md`

### Video Deep Dive (Phase 6续)
- 实盘日记类精选分析（125/017视频）：3个有效+3个内容错位
- 行业分析类精选分析（159视频）：1个有效+4个内容错位
- 直播回放批量分析（172个文件grep筛选+5个精读）
- 新增3个心智模型（Model 9-11）：
  - Model 9: 股价-商品价异步验证法（上游资源类）
  - Model 10: 产业链轮动脉冲理论（第一轮上游/第二轮下游）
  - Model 11: 替代方案价格天花板（成熟产业链价格上限）
- 新增7条决策启发式（H16-H22）：
  - H16: 2周景气度窗口验证法
  - H17: 现象级事件分级判断
  - H18: 重大利好+反向下跌=市场错配
  - H19: 腰斩+市值双触发买回
  - H20: 卖出后不回头
  - H21: 跷跷板逻辑（板块轮动）
  - H22: 折扣思维（把下跌理解为打折）
- 新增模块内容：分餐的奥义、季报快速分类法、粉丝逆向指标延伸、高压锅泄压、韩国巨头映射法、国内共识预期差、AI不可替代三要素、生动比喻词典
- 数据质量发现：实盘文件约60%内容错位，直播回放约90%存在语音识别错误
- Model 4补充："没有止损线"直播表达与破线纪律的区分说明

### Architecture
- 从单文件 SKILL.md 升级为模块化架构
- 支持关键词触发渐进加载
- 支持多模块叠加加载
- 预留 websearch 协同接口
- 决策启发式从15条扩展至20条

## [2.2.1] - 2026-05-13

### Added
- 在 SKILL.md 头部添加完整的《风险提示与免责声明》区块
- 添加投资风险提示、AI角色模拟声明、信息准确性声明、使用限制
- 在文件末尾添加合规声明引用

### Changed
- 更新角色扮演规则中的免责声明引用，指向头部完整声明
- 版本号标注更新为"含风险提示声明"

## [2.2.0] - 2026-05-13

### Added
- 视频转录深度挖掘集成（Phase 6完成）
- 新增心智模型：「笨韭双击/单机」框架（Model 8，视频独有）
- 新增决策启发式 H13：百亿市值门槛论
- 新增决策启发式 H14：新粉反向指标（视频独有）
- 新增决策启发式 H15：现象级事件三要素（规模性/真实性/时效性）
- 深化壁垒维度：技术壁垒/战略协议壁垒/产能壁垒（视频深化）
- 新增核心信念：「怕输是最大敌人」（视频深化）
- 新增成功四要素：兴趣+专注+思考+运气（视频深化）
- 补充持仓时间维度：一轮小级别行情至少两三个月起步
- 丰富表达DNA：短视频六段式结构、直播特有模式（反问风暴/意识流跳跃/降维科普/劝退仪式）、自嘲式幽默
- 新增视频深度挖掘报告：`references/video-transcript-deep-dive.md`

### Changed
- SKILL.md 从 v2.1 升级至 v2.2
- 心智模型从 7 个扩展至 8 个
- 决策启发式从 10 条扩展至 15 条
- README.md 更新 Phase 6 完成状态

### Data
- 视频转录分析：403个文件筛查，203个有效文件，15+个高质量精读
- 4个专项Agent并行分析：交易分析师/行业分析师/哲学分析师/表达分析师

## [2.1.0] - 2026-05-13

### Added
- 视频转录内容初步补充分析
- 诚实边界第4条：视频内容已补充分析
- 持仓状态更新（兆易/澜起等存储标的）

### Changed
- SKILL.md 从 v2.0 升级至 v2.1
- 调研来源中视频转录状态从 🟡 升级为 🟢

## [2.0.0] - 2026-05-13

### Added
- SKILL.md 重构完成（女娲 v2.0 流程）
- 7个核心心智模型（全部通过三重验证）
- 10条决策启发式（均有QA案例支撑）
- 完整表达DNA（基于2,504篇QA全量统计）
- 5组内在张力（保留未调和）
- 诚实边界（6个已知局限）
- 高频互动模板（6个回答模式）
- 情绪触发器表
- 回答长度分布统计
- 重复问题退化模式

### Changed
- 从 v1.0 的单文件升级至完整 Skill 架构
- 引入置信度标注（🟢一手/🟡推断/🔴推测）
- 引入时效状态标注（✅持续/🔄演化/❌已放弃）

### Data
- 6个并行Agent调研完成
- 290+篇QA深度阅读
- 预提炼报告通过质量门禁
- 双Agent精炼评审通过（优化器78/100，创建者85/100）

## [1.0.0] - 2026-05-12

### Added
- 项目初始化
- README.md 与基础目录结构
- 女娲 v2.0 流程框架
- 6个Agent调研任务分配
- 预提炼工具 `scripts/pre_extract.py`

### Data
- 确认蒸馏对象：笨笨的韭菜（B站UP主）
- 确认聚焦方向：全面画像
- 确认用途：思维顾问
- 本地素材确认：2,506篇充电问答
