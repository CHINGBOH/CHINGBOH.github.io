import Link from 'next/link';
import profile from '../../data/profile.json';

const { hero, monographs } = profile;
const monographHref = (k) => `/monographs/${encodeURIComponent(monographs[k].file)}`;

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

      <div className="hero-thesis" dangerouslySetInnerHTML={{ __html: hero.thesis }} />

      {hero.specMatrix && (
        <div className="hero-spec-matrix">
          {hero.specMatrix.map((item, idx) => (
            <a
              key={idx}
              href={monographHref(item.monograph)}
              className="hero-spec-cell"
              style={{ textDecoration: 'none', color: 'inherit' }}
            >
              <div className="hero-spec-label">{item.label}</div>
              <div className="hero-spec-val">
                {item.val} <span className="hero-spec-unit">{item.unit}</span>
              </div>
              <div className="hero-spec-desc">{item.desc}</div>
            </a>
          ))}
        </div>
      )}

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
            <a
              className="btn-view-detail"
              style={{ marginTop: 'auto', paddingTop: 10, alignSelf: 'flex-start', textDecoration: 'none' }}
              href={monographHref(p.monograph)}
              aria-label={`查看${p.title}专案`}
            >
              查看专案 →
            </a>
          </div>
        ))}
      </div>
    </header>
  );
}
