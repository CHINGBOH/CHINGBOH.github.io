import { timeline } from '../../data/profile';

export default function Timeline() {
  return (
    <section id="timeline" style={{ marginBottom: 40 }}>
      <div className="section-header">
        <div>
          <div className="section-badge">{timeline.badge}</div>
          <h2 className="section-title">{timeline.title}</h2>
          <div className="section-subtext">{timeline.subtext}</div>
        </div>
      </div>

      <div className="booktabs-container">
        <table className="booktabs-table">
          <thead>
            <tr>
              <th style={{ width: 140 }}>起止周期</th>
              <th style={{ width: 220 }}>机构与主体</th>
              <th style={{ width: 220 }}>职务 / 业务角色</th>
              <th>核心工作职责与操盘要点</th>
            </tr>
          </thead>
          <tbody>
            {timeline.rows.map((row) => (
              <tr key={row.period}>
                <td className="cell-period">
                  {row.period}
                  <div className="cell-duration">({row.duration})</div>
                </td>
                <td>
                  <div className="cell-org">{row.org}</div>
                </td>
                <td>
                  <div className="cell-role">{row.role}</div>
                </td>
                <td>
                  <ul className="bullet-list">
                    {row.bullets.map((b, i) => (
                      <li key={i}>{b}</li>
                    ))}
                  </ul>
                  <div className="tag-row">
                    {row.tags.map((t) => (
                      <span className="tag" key={t}>
                        {t}
                      </span>
                    ))}
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
