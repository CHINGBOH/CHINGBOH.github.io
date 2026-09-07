// 内容单一数据源：构建时由 DuckDB 视图校验的数字锚点 + 手工撰写叙事
// 数字口径（合同 135 份 / 6.83 亿、8 大自研系统 / 2,804 万行、120.8 小时）与 data/career_analytics_lake.duckdb 视图一致，可 SQL 复验。

export const MONOGRAPHS = {
  'monograph-hust': {
    file: '华中科技大学统计学学术奠基与数理底座商业研报.html',
    short: '华科统计学术奠基',
  },
  'monograph-gov': {
    file: '上市公司董办合规资本运作与总经办企业运营商业研报.html',
    short: '上市公司合规与资本',
  },
  'monograph-cloud': {
    file: '深圳市广田云软装科技全生命周期商业操盘与供应链大盘商业研报.html',
    short: '广田云软装大盘',
  },
  'monograph-zy': {
    file: '遵义大酒店五星级软装工程全周期商业操盘研报.html',
    short: '遵义大酒店操盘',
  },
  'monograph-hhg': {
    file: '红花岗项目全生命周期深度商业研报.html',
    short: '红花岗项目洞察',
  },
  'monograph-ht': {
    file: '上海华泰中心售楼处全生命周期商业操盘研报.html',
    short: '华泰中心操盘',
  },
  'monograph-mt': {
    file: '湄潭项目全生命周期数据洞察研报.html',
    short: '湄潭项目洞察',
  },
  'monograph-ai': {
    file: 'AI全栈工程与VibeCoding敏捷研发商业研报.html',
    short: 'AI全栈与VibeCoding',
  },
};

export const monographHref = (key) => `/monographs/${encodeURIComponent(MONOGRAPHS[key].file)}`;

export const navLinks = [
  { href: '#timeline', label: '生涯时间线' },
  { href: '#cases', label: '代表专案' },
  { href: '#skills', label: '专业能力' },
  { href: '#provenance', label: '数据依据' },
];

export const hero = {
  eyebrow: ['Boone Liang', '/', 'PROFESSIONAL PORTFOLIO', '/', 'SELECTED WORK'],
  name: '梁清波',
  enName: 'Boone Liang',
  contacts: [
    { label: '性别', value: '男' },
    { label: '城市', value: '中国 · 深圳' },
    { label: '手机', value: '130-7787-2618' },
    { label: '邮箱', value: 'kinpual@foxmail.com', href: 'mailto:kinpual@foxmail.com' },
  ],
  headline: '华中科技大学统计学 · 数字化解决方案顾问 · 全业务流程操盘者与工程化落地者',
  thesis: (
    <>
      我的价值交付横跨两条主线：一是<strong>大规模商业工程操盘</strong>——统领 135 份盖章合同、合计 6.83 亿的工程大盘，穿透成本底盘与多级定价博弈，锁定 30%~35% 稳健经营毛利与四维资金回款；二是<strong>数字化与工程化落地</strong>——以 <strong>［VIBE+ 敏捷研发］LLM×Harness 为支点，通过 Context 压缩、索引与复用撬动研发杠杆</strong>，一人覆盖 8 大自研系统、2,804 万行源码与 120.8 小时纯有效工时。二者由同一底层能力链接：华中科技大学统计学带来的严格数理推断与机制设计思维。
    </>
  ),
  pillars: [
    {
      code: '全资子公司奠基',
      period: '2014 - 2024',
      title: '企业创办与制度治理',
      fact: '从0到1组建45人编制，主笔8大模块730条管理制度总纲与1,491㎡展厅，奠定10年合规与零仲裁底盘。',
      mono: '3,000万超募创办 · 45人编制 · 730条制度总纲 · 10年零仲裁',
      monograph: 'monograph-cloud',
    },
    {
      code: '大宗工程总操盘',
      period: '2014 - 2024',
      title: '重大工程大盘与商务博弈',
      fact: '统领135份全盘盖章合同大盘（签约6.83亿/确权5.92亿），主导遵义大酒店等破亿地标交付与四维回款。',
      mono: '135份盖章合同 · 6.83亿大盘 · 遵义等破亿地标 · 30%~35%毛利锁定',
      monograph: 'monograph-zy',
    },
    {
      code: '数字化全栈方案',
      period: '2024 - 至今',
      title: '业务分析与AI全栈研发',
      fact: '以 VIBE+ 敏捷研发（LLM×Harness 支点 + Context 杠杆）自主推进 AI Agent 状态机、企业混合 RAG 与 DuckDB 列式中枢研发。',
      mono: '8大自研系统 · 2,804万行代码 · DuckDB列式中枢 · Agent状态机',
      monograph: 'monograph-ai',
    },
    {
      code: '数理统计学术底座',
      period: '2002 - 2006',
      title: '统计学与科学计算思维',
      fact: '华中科技大学统计学理学学士，修读24门数理骨干课与160+学分，毕业论文攻关LBM介观流体数值模拟。',
      mono: '985理学学士 · 160+必修学分 · 24门数理骨干 · LBM介观流体模拟',
      monograph: 'monograph-hust',
    },
  ],
};

export const timeline = {
  badge: 'CAREER CHRONOLOGY',
  title: '职业生涯时间线与业务演进',
  subtext: '从华科数理基础出发，经历管理咨询、上市公司合规治理、实体大盘运营至数字化全栈探索',
  rows: [
    {
      period: '2024.03 - 至今',
      duration: '2年',
      org: '数字化解决方案与全栈技术研发 (独立顾问 / 软件原型研发)',
      role: '数字化解决方案顾问 / 全栈架构与技术研发',
      bullets: [
        '结合二十年数理分析与实体商业操盘经验，以 VIBE+ 敏捷研发方法论（LLM×Harness 支点 + Context 杠杆）自主推进企业级数字化原型研发，主导混合检索 RAG 知识库、工作流编排 Agent 状态机与外贸业务自动化工具的系统设计与开发。',
        '基于 DuckDB 现代列式分析中枢，深度整合 vss 向量检索、httpfs 远程直查与跨源 Scanner 插件生态，并通过 Model Context Protocol (FastMCP) 建立 AI Agent 对本地湖仓与异构数据的即席分析与工具调用闭环。',
      ],
      tags: ['VIBE+ 敏捷研发', 'RAG 混合检索', 'Agent 状态机', 'DuckDB 插件生态', 'FastMCP 协议'],
    },
    {
      period: '2014.03 - 2024.06',
      duration: '10年',
      org: '深圳市广田云软装艺术科技有限公司 (广田全资子公司)',
      role: '全资子公司筹办初创负责人 · 大宗商业工程总操盘 · 重大工程专班牵头人',
      bullets: [
        '【企业创办与制度奠基】承接集团上市公司 3,000 万元超募投资创办全资子公司，从 0 到 1 组建 45 人初创团队编制，主笔发布八大业务模块 730 条管理制度总纲与 1,491 ㎡ 现代美学旗舰展厅，奠定 10 年 100% 用工合规与零劳动仲裁治理底盘。',
        '【重大工程专班总操盘】统领全盘 135 份真实盖章合同大盘（签约 6.83 亿元，确权产值 5.92 亿元），打破传统科层以重大工程为战元牵头跨部门敏捷专班，主揽并总操盘遵义大酒店（1.25 亿国宾工程）、开元名都（1.03 亿）、汇川康养城（1.09 亿）等 24 项标杆工程全流程高品质交付。',
        '【多轨定价博弈与毛利锁定】首创穿透珠三角源头工坊出厂成本底盘，建立"出厂成本 ➔ 内部控制 ➔ 商务底限 ➔ 正式报审报价"多级商务防波堤与动态加乘模型，在大货批量采购中运用价值工程 (VE) 刚性降本 30%+，始终坚守 30%~35% 综合经营毛利率红线。',
        '【四维回款防线与审计确权】构建"比例联动 / 节点进度 / 极速出厂 / 战采流水"四维资金回款机制，破解背靠背免责霸王条款，实现全盘 97.4% 高回款率；挂帅竣工结算答辩，凭激光实测底账与闭环现场签证抗辩财评审计，阻断审减风险，守住数千万元合法经营成果。',
      ],
      tags: ['全资子公司创办', '730条制度总纲', '6.83亿合同大盘', '破亿级标杆专班', '30%~35%毛利锁定', '四维回款防线'],
    },
    {
      period: '2011.03 - 2014.02',
      duration: '3年',
      org: '深圳广田装饰集团股份有限公司 (SZ.002482)',
      role: '总经办经营数据分析 ➔ 证券事务部专职 (合规与法定信披)',
      bullets: [
        '前段在总经办搭建经营数据分析模型，督办 19 期月度经营例会决议按期落实（办结率 97.9%）。',
        '后调任证券事务部专职，主导 12 亿元中小企业私募债发债全流程尽职调查，整理归档 55 类专业底稿；撰写同业竞品财务对标报告；负责深交所 206 篇法定信披公告，保持零监管函件与 A 级考评。',
      ],
      tags: ['上市公司合规', '12亿发债尽调', '深交所A级信披', '经营例会决议督办'],
    },
    {
      period: '2009.07 - 2011.02',
      duration: '1.5年',
      org: '鹏金元金融公司',
      role: '营运部金融产品运营分析',
      bullets: ['负责金融产品底层资产数据梳理，协助搭建基础投资风险监测模型与量化测算台账，支撑投资组合动态跟踪与风险测算。'],
      tags: ['金融资产运营', '量化测算台账', '风险监测'],
    },
    {
      period: '2006.07 - 2009.06',
      duration: '3年',
      org: '高柏顾问公司',
      role: '企管部业务流程重构与运营数据分析',
      bullets: ['从事企业管理咨询，参与企业业务流程重构 (BPR) 与绩效考核指标体系设计；负责企业运营数据的清洗、建模与统计分析，提供经营报表与测算支持。'],
      tags: ['管理咨询BPR', '绩效指标设计', '运营数据分析'],
    },
    {
      period: '2002.09 - 2006.06',
      duration: '4年',
      org: '华中科技大学 数学与统计学院',
      role: '统计学专业 · 理学学士 (Bachelor of Science)',
      bullets: [
        '系统修读数学分析 (I-III)、高等代数与几何 (I-II)、常微分方程、概率论、数理统计、多元统计分析等 24 门数理核心骨干课，修满 160+ 学分。',
        '本科毕业论文攻关《格子玻尔兹曼 (LBM) 算法与数值模拟》，在 D2Q9 速度空间实现流体介观演化编程，奠定终身受用的数理逻辑与科学计算底座。',
      ],
      tags: ['985 理学学士', '24门数理骨干', 'LBM 介观模拟', '科学计算'],
    },
  ],
};

export const cases = {
  badge: 'REPRESENTATIVE MONOGRAPHS & CAREER DOSSIERS',
  title: '代表性商业专案与核心履职档案',
  subtext: '系统涵盖数理学术奠基、上市公司合规治理与资本运作、实体供应链大盘操盘与数字化技术研发四大独立专案研报',
  items: [
    {
      badge: '学术奠基',
      period: '2002 - 2006',
      title: '华中科技大学统计学专业 · 本科数理培养与思维底座',
      scope: '160+ 必修学分 · 24 门数理核心必修课 · LBM 介观模拟',
      abstract: '系统梳理本科四年的纯数推导、概率统计、科学计算课程体系，以及格子玻尔兹曼 (LBM) 介观动力学流体数值模拟毕业设计研究。',
      cta: '查看专案详情',
      monograph: 'monograph-hust',
    },
    {
      badge: '合规与资本',
      period: '2011 - 2014',
      title: '上市公司治理合规、重大发债尽调与总经办运营',
      scope: '深交所信披最高 A 级 · 12 亿私募债尽调 · 19 期经营例会督办',
      abstract: '展现上市公司董事会办公室及证券事务部的法定信息披露实操、12 亿元发债融资尽调底稿归档，以及总经办经营例会决议的闭环督办体系。',
      cta: '查看合规专案',
      monograph: 'monograph-gov',
    },
    {
      badge: '商业与操盘',
      period: '2014 - 2024',
      title: '广田全资子公司创办奠基与大宗商业工程大盘',
      scope: '45 人编制 · 730 条制度总纲 · 135 份合同 (6.83 亿) · 遵义等破亿标杆',
      abstract: '完整复盘全资子公司创办历程、制度建设与商业工程大盘操盘实践，沉淀多轨博弈定价模型、价值工程降本与四维资金回款防线。',
      cta: '查看大盘全景',
      monograph: 'monograph-cloud',
    },
    {
      badge: '技术与数字化',
      period: '2024 - 至今',
      title: '数字化解决方案与全栈技术原型研发',
      scope: '8 大自研系统 · 2,804 万行源码 · DuckDB 插件生态 · FastMCP 智能体协议',
      abstract: '以 VIBE+ 敏捷研发（LLM×Harness 支点 + Context 杠杆）展现围绕 DuckDB 现代列式湖仓与丰富插件生态（vss 向量检索、httpfs 远程直查、跨源 scanner、spatial 空间计算）、Model Context Protocol (FastMCP) 统一智能体数据协议、混合检索 RAG 与流程编排状态机，实现从本地分析到智能体即席推理的全栈研发闭环。',
      cta: '查看研发全貌',
      monograph: 'monograph-ai',
    },
  ],
};

export const skills = {
  badge: 'CORE COMPETENCIES',
  title: '专业能力与技术栈底座',
  subtext: '二十年复合复利所沉淀的跨界知识结构',
  tiles: [
    {
      title: '数理统计与数据分析',
      items: [
        '多元统计分析、假设检验与多元回归',
        '运筹最优化、线性规划与单纯形法',
        'DuckDB 进程内列式湖仓架构、向量化执行引擎与扩展插件群 (vss 向量检索 / httpfs 远程数据湖 / spatial 空间几何 / 跨源 scanner 联邦直查)',
        '企业经营指标池与 KPI 考核基线搭建',
        '底层资产现金流折现测算与量化风控',
      ],
    },
    {
      title: '企业商业操盘与组织治理',
      items: [
        '全资子公司从0到1组织架构搭建、初创编制与制度总纲制定',
        '重大商业工程跨部门敏捷专班组建、资源调度与端到端实操操盘',
        '采销多轨博弈定价模型、价值工程 (VE) 降本与 30%~35% 毛利锁定',
        '四维刚性资金回款防线、苛刻支付条款抗辩与现金流风险阻断',
        '大宗工程全生命周期集中交验、竣工结算审计答辩与合法收益确权',
      ],
    },
    {
      title: '上市公司治理与资本合规',
      items: [
        '深交所上市公司法定信息披露规范 (考评最高A级)',
        '中小企业私募债及重大融资尽调底稿管理',
        '上市公司三会议事规则与内幕信息登记',
        '同业竞品深度财务对标与竞争战略分析',
        '总经办经营例会决议闭环督办与跨部门推进',
      ],
    },
    {
      title: '软件工程与数字化解决方案',
      highlight: true,
      items: [
        '［VIBE+ 敏捷研发］以 LLM×Harness 为支点，把"怎么做"教给 AI 高速执行，一人覆盖需求→数据→系统→落地全链路',
        '［Context 杠杆］将多领域工程经验压缩、索引、复用进数据湖仓，用 Context 撬动研发，不写重复代码',
        '产出佐证：61 个工程仓库 · 8 大自研系统 · 2,804 万行源码 · 120.8 小时纯有效工时',
        'Python / FastAPI / TypeScript / 前端现代工程',
        'Model Context Protocol (FastMCP) 架构设计与工具封装 (DuckDB MCP 即席分析中枢 / 安全只读沙箱)',
        '混合检索 RAG 知识库 (Dense + Sparse 混合召回 / 重排序 / 知识图谱)',
        'Agent 状态机、工作流编排与自动化工具链交付',
        '数据湖仓 (DuckDB) SSOT 单一真源 · 视图引擎 SQL 复验 · Git / Linux 敏捷交付',
      ],
    },
  ],
};

export const provenance = {
  title: '数据来源与构建说明',
  db: 'data/career_analytics_lake.duckdb',
  desc: '关键量化指标在构建时由本地 DuckDB 数据视图查询并核验后注入；下方保留本次构建的数据快照：',
  views: [
    ['v_profile_flyleaf_summary & v_profile_career_pillars', '履历扉页概括性指标集市 (SSOT 单一真实源)'],
    ['v_hust_curriculum_stages & v_hust_core_course_matrix', '华中科技大学培养阶段 160 学分、24 门核心课与 98 学分核心矩阵'],
    ['v_guangtian_announcements_tenure & v_sec_bond_due_diligence', '董办任职期 345 条公告记录与 54 项发债尽调条目'],
    ['v_gt_contracts_master & v_gt_portfolio_all_135', '24 项标杆工程与 135 份合同汇总（6.8348 亿签约、5.92155 亿审定）'],
    ['v_ai_git_repositories & v_ai_work_summary', '8 个核心代码仓库、WakaTime 工时与 AI 工程资产实录'],
  ],
  runtime: {
    extensions: 'EXTENSIONS: PARQUET · JSON · VSS · SPATIAL · HTTPFS · EXCEL',
    facts: [
      'AI 旗舰仓库 8 个 / 28,038,054 LOC',
      'WakaTime 120.8 小时',
      '云软装 135 份合同 / 68,348.00 万元',
      '断言通过 10 项',
      '湖仓视图群 128 个',
    ],
  },
};
