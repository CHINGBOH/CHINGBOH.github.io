import Nav from './components/Nav';
import Hero from './components/Hero';
import Timeline from './components/Timeline';
import Cases from './components/Cases';
import Skills from './components/Skills';
import Provenance from './components/Provenance';
import './globals.css';

export default function HomePage() {
  return (
    <div className="container">
      <Nav />
      <Hero />
      <Skills />
      <Cases />
      <Timeline />
      <Provenance />
    </div>
  );
}
