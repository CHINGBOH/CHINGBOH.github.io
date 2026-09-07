import { provenance } from '../../data/profile';

export default function Provenance() {
  return (
    <footer id="provenance" className="provenance-footnote">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: 6 }}>
        <strong style={{ color: 'var(--text-secondary)' }}>📊 {provenance.title}</strong>
        <span>数据库底座: {provenance.db}</span>
      </div>
      <p style={{ lineHeight: 1.6, color: 'var(--text-tertiary)', marginBottom: 8 }}>{provenance.desc}</p>
      <div className="provenance-views-list">
        {provenance.views.map(([name, desc]) => (
          <div className="provenance-item" key={name}>
            <div className="provenance-name">{name}</div>
            <div style={{ color: 'var(--text-secondary)', marginTop: 2 }}>{desc}</div>
          </div>
        ))}
      </div>
      <div className="runtime-audit" style={{ marginTop: 18, padding: '12px 14px', background: '#f7f6f1', border: '1px solid var(--border-hairline)' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 7, flexWrap: 'wrap', gap: 6 }}>
          <div style={{ fontFamily: 'var(--font-mono)', fontSize: 11, color: 'var(--accent-bronze)', fontWeight: 700 }}>
            DUCKDB FASTMCP DIRECT-LAKE ENGINE · VERIFIED
          </div>
          <div style={{ fontFamily: 'var(--font-mono)', fontSize: 10, color: 'var(--accent-navy)', background: '#fff', padding: '1px 6px', borderRadius: 2, border: '1px solid var(--border-hairline)' }}>
            {provenance.runtime.extensions}
          </div>
        </div>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px 18px', color: 'var(--text-secondary)', fontSize: 12 }}>
          {provenance.runtime.facts.map((f) => (
            <span key={f}>{f}</span>
          ))}
        </div>
      </div>
      <div style={{ textAlign: 'center', marginTop: 24, color: 'var(--text-tertiary)', fontSize: 11.5 }}>
        © 2026 Boone Liang (梁清波) · 个人履历与专业作品集 · Next.js 静态站点 (GitHub Pages)
      </div>
    </footer>
  );
}
