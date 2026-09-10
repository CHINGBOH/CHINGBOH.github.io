import Link from 'next/link';
import navLinksData from '../../data/profile.json';

const navLinks = navLinksData.nav;

export default function Nav() {
  return (
    <nav className="nav-dock">
      <div className="nav-brand">
        <span className="nav-brand-code">PORTFOLIO</span>
        <span className="nav-brand-title">梁清波 · 个人履历与专业作品集</span>
      </div>
      <ul className="nav-links">
        {navLinks.map((l) => (
          <li key={l.href}>
            <a href={l.href}>{l.label}</a>
          </li>
        ))}
      </ul>
      <a href="#cases" className="nav-cta-btn">
        <span>📚 精选代表作</span>
        <span>↓</span>
      </a>
    </nav>
  );
}
