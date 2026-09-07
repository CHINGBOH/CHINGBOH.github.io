import { skills } from '../../data/profile';

export default function Skills() {
  return (
    <section id="skills" style={{ marginBottom: 40 }}>
      <div className="section-header">
        <div>
          <div className="section-badge">{skills.badge}</div>
          <h2 className="section-title">{skills.title}</h2>
          <div className="section-subtext">{skills.subtext}</div>
        </div>
      </div>

      <div className="skills-grid">
        {skills.tiles.map((tile) => (
          <div className={`skill-tile${tile.highlight ? ' skill-tile--highlight' : ''}`} key={tile.title} data-highlight={tile.highlight || undefined}>
            <h4>{tile.title}</h4>
            <ul>
              {tile.items.map((item, i) => (
                <li key={i}>
                  {tile.highlight && i < 3 ? <strong>{item}</strong> : item}
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </section>
  );
}
