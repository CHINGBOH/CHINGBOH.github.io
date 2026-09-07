import Link from 'next/link';
import { hero, monographHref } from '../../data/profile';

export default function Hero() {
  return (
    <header className="hero">
      <div className="archival-eyebrow">
        {hero.eyebrow.map((e, i) => (
          <span key={i}>{e}</span>
        ))}
      </div>

      <div className="hero-title-row">
        <h1 className="hero-title">
          {hero.name}
          <span className="hero-en">{hero.enName}</span>
        </h1>
        <div className="hero-contacts">
          {hero.contacts.map((c) =>
            c.href ? (
              <a key={c.label} href={c.href} style={{ color: 'inherit', textDecoration: 'none' }}>
                {c.label === '邮箱' ? '✉️ ' : ''}
                {c.value}
              </a>
            ) : (
              <span key={c.label}>
                {c.label === '性别' && '♂ '}
                {c.label === '城市' && '📍 '}
                {c.label === '手机' && '📱 '}
                {c.label === '邮箱' && '✉️ '}
                {c.value}
              </span>
            )
          )}
        </div>
      </div>

      <div className="hero-headline" style={{ marginBottom: 16 }}>
        <span className="hero-headline-chip">{hero.headline}</span>
      </div>

      <div className="hero-corevalue">
        <div className="corevalue-label">核心价值 · CORE VALUE</div>
        <div className="corevalue-grid">
          <div className="corevalue-card corevalue-card--vibe">
            <div className="corevalue-kicker">① 最强差异化</div>
            <div className="corevalue-title">数字化 &amp; AI 全栈 · VIBE+ 敏捷研发</div>
            <div className="corevalue-desc">
              以 LLM×Harness 为支点、Context 为杠杆，把“怎么做”教给 AI 高速执行，
              一人覆盖 需求 → 数据 → 系统 → 落地 全链路。
            </div>
            <div className="corevalue-mono">8 大自研系统 · 2,804 万行源码 · 120.8 小时纯有效工时 · 61 个工程仓库</div>
          </div>
          <div className="corevalue-card corevalue-card--biz">
            <div className="corevalue-kicker">② 最硬商业价值</div>
            <div className="corevalue-title">大宗商业工程操盘</div>
            <div className="corevalue-desc">
              统领全资子公司从 0 到 1，穿透成本底盘与多级定价博弈，
              锁定稳健经营毛利与四维资金回款。
            </div>
            <div className="corevalue-mono">135 份盖章合同 · 6.83 亿工程大盘 · 30%~35% 经营毛利 · 45 人编制</div>
          </div>
        </div>
      </div>

      <div className="hero-thesis">{hero.thesis}</div>

      <div className="hero-pillars-grid">
        {hero.pillars.map((p) => (
          <div className="hero-pillar-card" key={p.code}>
            <div className="pillar-eyebrow">
              <span className="pillar-code">{p.code}</span>
              <span className="pillar-period">{p.period}</span>
            </div>
            <div className="pillar-title">{p.title}</div>
            <div className="pillar-fact">{p.fact}</div>
            <div className="pillar-mono">{p.mono}</div>
            <Link
              className="btn-view-detail"
              style={{ marginTop: 'auto', paddingTop: 10, alignSelf: 'flex-start' }}
              href={monographHref(p.monograph)}
              aria-label={`查看${p.title}专案`}
            >
              查看专案 →
            </Link>
          </div>
        ))}
      </div>
    </header>
  );
}
