import profile from '../../data/profile.json';

const { cases } = profile;

export default function Cases() {
  return (
    <section id="cases" style={{ marginBottom: 44 }}>
      {/* 1. 主舞台：Marimo 反应式全息商业研报 */}
      <div className="section-header">
        <div>
          <div className="section-badge">{cases.badge}</div>
          <h2 className="section-title">{cases.title}</h2>
          <div className="section-subtext">{cases.subtext}</div>
        </div>
      </div>

      <div className="cases-grid" style={{ marginBottom: 36 }}>
        {cases.items.map((c) => (
          <div className="case-card marimo-card" key={c.title}>
            <div>
              <div className="case-header">
                <span className="case-badge marimo-badge">{c.badge}</span>
                <span className="case-period">{c.period}</span>
              </div>
              <h3 className="case-title">{c.title}</h3>
              <div className="case-scope">{c.scope}</div>
              <p className="case-abstract">{c.abstract}</p>
              {c.tags && (
                <div className="tag-row" style={{ marginTop: 10, marginBottom: 12 }}>
                  {c.tags.map((t) => (
                    <span className="tag marimo-tag" key={t}>
                      {t}
                    </span>
                  ))}
                </div>
              )}
            </div>
            <div className="case-footer">
              <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                {c.port && (
                  <span className="live-pill" title={`本地运行端口: ${c.port}`}>
                    LIVE :{c.port}
                  </span>
                )}
                <span style={{ fontSize: 11.5, color: 'var(--text-tertiary)' }}>
                  纯 Python 反应式全息研报
                </span>
              </div>
              <a
                className="btn-view-detail"
                style={{ textDecoration: 'none' }}
                href={`/monographs/${encodeURIComponent(c.file)}`}
              >
                <span>{c.cta}</span>
                <span>➔</span>
              </a>
            </div>
          </div>
        ))}
      </div>

      {/* 2. 历史商业专案底稿与合同审计归类存档 */}
      {cases.archived && (
        <div className="archived-section">
          <div className="archived-header">
            <div className="section-badge" style={{ background: 'rgba(120, 100, 80, 0.08)', color: '#6d5330' }}>
              {cases.archived.badge}
            </div>
            <h3 className="archived-title">{cases.archived.title}</h3>
            <div className="section-subtext">{cases.archived.subtext}</div>
          </div>

          <div className="archived-grid">
            {cases.archived.items.map((a) => (
              <a
                className="archived-card"
                key={a.code}
                href={`/monographs/${encodeURIComponent(a.file)}`}
                style={{ textDecoration: 'none', color: 'inherit' }}
              >
                <div className="archived-card-top">
                  <span className="archived-code">{a.code}</span>
                  {a.scope && <span className="archived-scope">{a.scope}</span>}
                </div>
                <div className="archived-card-title">{a.title}</div>
                <div className="archived-card-desc">{a.desc}</div>
                <div className="archived-card-cta">
                  <span>查看原版底稿档案</span>
                  <span>→</span>
                </div>
              </a>
            ))}
          </div>
        </div>
      )}
    </section>
  );
}
