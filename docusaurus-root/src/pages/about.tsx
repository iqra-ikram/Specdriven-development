import React from 'react';
import Layout from '@theme/Layout';
import clsx from 'clsx';
import styles from './about.module.css';

const SKILLS = [
  { name: "Next.js", icon: "⚡" },
  { name: "Python", icon: "🐍" },
  { name: "TypeScript", icon: "📘" },
  { name: "GenAI", icon: "🧠" },
  { name: "Web3", icon: "🌐" },
  { name: "Figma", icon: "🎨" },
];

const PROJECTS = [
  {
    title: "Banking Architecture",
    desc: "Secure banking backend engineered with Python & FastAPI.",
    tags: ["Backend", "Security"],
    link: "https://github.com/iqra-ikram/Banking-app"
  },
  {
    title: "Word Engine CLI",
    desc: "High-performance text analysis tool designed for efficiency.",
    tags: ["Tooling", "TypeScript"],
    link: "https://github.com/iqra-ikram/word-counter-project"
  },
  {
    title: "ATM Simulator",
    desc: "Complex state-machine simulation of financial transaction logic.",
    tags: ["System Design", "Logic"],
    link: "https://github.com/iqra-ikram/Atm-Machine-Project"
  }
];

function HeroSection() {
  return (
    <section className={styles.heroSection}>
      {/* Abstract Aurora Backgrounds */}
      <div className={styles.auroraBg}>
        <div className={styles.aurora1}></div>
        <div className={styles.aurora2}></div>
        <div className={styles.aurora3}></div>
      </div>

      <div className={clsx("container", styles.heroContainer)}>
        <div className={styles.heroContent}>
          <div className={styles.introLabel}>
            <span className={styles.line}></span>
            <span>Meet The Developer</span>
          </div>
          
          <h1 className={styles.heroTitle}>
            Iqra Ikram<span className={styles.dot}>.</span>
          </h1>
          
          <p className={styles.heroSubtitle}>
            Blending <strong>Artistic Vision</strong> with <strong>Algorithmic Precision</strong>.
            <br />
            Specializing in <span className={styles.highlight}>Generative AI</span> and the <span className={styles.highlight}>Metaverse</span>.
          </p>

          <div className={styles.statRow}>
            <div className={styles.statItem}>
              <span className={styles.statNum}>10+</span>
              <span className={styles.statLabel}>Projects</span>
            </div>
            <div className={styles.statSeparator}></div>
            <div className={styles.statItem}>
              <span className={styles.statNum}>GenAI</span>
              <span className={styles.statLabel}>Specialist</span>
            </div>
            <div className={styles.statSeparator}></div>
            <div className={styles.statItem}>
              <span className={styles.statNum}>Web3</span>
              <span className={styles.statLabel}>Native</span>
            </div>
          </div>

          <div className={styles.actionRow}>
            <a href="https://github.com/iqra-ikram" className={styles.primaryBtn}>
              GitHub Profile
            </a>
            <a href="#expertise" className={styles.secondaryBtn}>
              View Expertise
            </a>
          </div>
        </div>

        <div className={styles.heroImageWrapper}>
          <div className={styles.imageGlassCard}>
            <img 
              src="https://avatars.githubusercontent.com/u/163900896?v=4" 
              alt="Iqra Ikram" 
              className={styles.profileImage} 
            />
            <div className={styles.glassReflection}></div>
          </div>
          {/* Decorative Elements */}
          <div className={styles.decoCircle}></div>
          <div className={styles.decoDots}>
            {[...Array(25)].map((_, i) => <div key={i} className={styles.dotGridItem}></div>)}
          </div>
        </div>
      </div>
    </section>
  );
}

function ExpertiseSection() {
  return (
    <section id="expertise" className={styles.expertiseSection}>
      <div className="container">
        <div className={styles.expertiseHeader}>
          <h2>The Toolkit</h2>
        </div>
        <div className={styles.skillsMarquee}>
          <div className={styles.marqueeTrack}>
            {[...SKILLS, ...SKILLS, ...SKILLS].map((skill, idx) => (
              <div key={idx} className={styles.skillBadge}>
                <span className={styles.skillIcon}>{skill.icon}</span>
                <span className={styles.skillName}>{skill.name}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}

function WorkSection() {
  return (
    <section className={styles.workSection}>
      <div className="container">
        <div className={styles.workHeader}>
          <h2>Featured Creations</h2>
        </div>
        <div className={styles.projectList}>
          {PROJECTS.map((project, idx) => (
            <a key={idx} href={project.link} target="_blank" rel="noreferrer" className={styles.projectRow}>
              <div className={styles.projectInfo}>
                <h3 className={styles.projectTitle}>{project.title}</h3>
                <p className={styles.projectDesc}>{project.desc}</p>
              </div>
              <div className={styles.projectMeta}>
                <div className={styles.projectTags}>
                  {project.tags.map((tag, tIdx) => (
                    <span key={tIdx} className={styles.tag}>{tag}</span>
                  ))}
                </div>
                <span className={styles.arrowIcon}>→</span>
              </div>
            </a>
          ))}
        </div>
      </div>
    </section>
  );
}

export default function About(): JSX.Element {
  return (
    <Layout
      title="Iqra Ikram | Creative Developer"
      description="Creative Portfolio of Iqra Ikram">
      <main className={styles.mainWrapper}>
        <HeroSection />
        <ExpertiseSection />
        <WorkSection />
      </main>
    </Layout>
  );
}