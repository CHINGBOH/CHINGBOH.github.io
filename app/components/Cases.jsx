import Link from 'next/link';
import profile from '../../data/profile.json';

const { cases, monographs } = profile;
const monographHref = (k) => `/monographs/${encodeURIComponent(monographs[k].file)}`;

export default function Cases() {
  return (
    <section id="cases" style={{ marginBottom: 40 }}>
      <div className="section-header">
        <div>
          <div className="section-badge">{cases.badge}</div>
          <h2 className="section-title">{cases.title}</h2>
          <div className="section-subtext">{cases.subtext}</div>
        </div>
      </div>

      <div className="cases-grid">
        {cases.items.map((c) => (
          <div className="case-card" key={c.title}>
            <div>
              <div className="case-header">
                <span className="case-badge">{c.badge}</span>
                <span className="case-period">{c.period}</span>
              </div>
              <h3 className="case-title">{c.title}</h3>
              <div className="case-scope">{c.scope}</div>
              <p className="case-abstract">{c.abstract}</p>
            </div>
            <div className="case-footer">
              <span style={{ fontSize: 12, color: 'var(--text-tertiary)' }}>独立专案档案</span>
              <Link className="btn-view-detail" href={monographHref(c.monograph)} prefetch={false}>
                <span>{c.cta}</span>
                <span>➔</span>
              </Link>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
