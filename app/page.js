import Nav from './components/Nav';
import Hero from './components/Hero';
import Timeline from './components/Timeline';
import Cases from './components/Cases';
import Skills from './components/Skills';
import './globals.css';

export default function HomePage() {
  return (
    <div className="container">
      <Nav />
      <Hero />
      <Cases />
      <Skills />
      <Timeline />
      <footer style={{ textAlign: 'center', padding: '28px 0 16px', color: 'var(--text-tertiary)', fontSize: 11.5 }}>
        © 2026 Boone Liang (梁清波) · 个人履历与专业作品集
      </footer>
    </div>
  );
}
