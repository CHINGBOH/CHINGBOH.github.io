import profile from '../../data/profile.json';
const timeline = profile.timeline;

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

      <div className="career-timeline">
        {timeline.rows.map((row) => (
          <div className="timeline-entry" key={row.period}>
            <div className="timeline-marker" aria-hidden="true">
              <span className="timeline-dot" />
              <span className="timeline-line" />
            </div>

            <div className="timeline-period">
              <div className="period-text">{row.period}</div>
              <div className="duration-text">{row.duration}</div>
            </div>

            <div className="timeline-card">
              <div className="timeline-org">{row.org}</div>
              <div className="timeline-role">{row.role}</div>
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
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
