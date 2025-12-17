import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';
import styles from '@site/src/pages/index.module.css'; // Updated import path for styles
import { JSX } from 'react';
import ChatbotWidget from '@site/src/components/ChatbotWidget'; // Updated import path for ChatbotWidget

function HomepageHeader() {
  const { siteConfig } = useDocusaurusContext();
  return (
    <header className="heroBanner">
      <div className="heroContainer container">
        {/* Image First, per reference */}
        <img
          src="img/hero-1.png"
          alt="Physical AI Robot"
          className="heroImage"
        />

        {/* Headline */}
        <h1 className="heroTitle">
          Where Digital Brains Meet<br />
          Physical Bodies – <span className="heroTitleAccent">Physical AI.</span>
        </h1>

        {/* Subtext */}
        <p className="heroSubtitle">
          MindSphere brings AI agents together to collaborate, solve challenges, and deliver transformative results—seamless, scalable, and adaptive.
        </p>

        {/* Button */}
        <div>
          <Link
            className="heroButton"
            to="/docs/intro">
            Connect Dapp
          </Link>
        </div>
        <ChatbotWidget />
      </div>
    </header>
  );
}

function CreativeFeaturesSection() {
  return (
    <section className="featuresSection">
      <div className="featuresGrid">

        {/* Chatbot Card */}
        <div className="creativeCard">
          <div className="cardContent">
            <h3 className="cardTitle">Interactive AI Tutor</h3>
            <p className="cardDesc">
              Stuck on a node? Get instant, context-aware help with our integrated AI assistant.
            </p>
          </div>
          <div className="visualContainer">
            <div className="chatVisual">
              <div className="chatBubble bubbleLeft">How do I launch Gazebo?</div>
              <div className="chatBubble bubbleRight">Run `ros2 launch gazebo_ros...`</div>
            </div>
          </div>
        </div>

        {/* Translation Card */}
        <div className="creativeCard">
          <div className="cardContent">
            <h3 className="cardTitle">Learn in Urdu</h3>
            <p className="cardDesc">
              Master robotics in your native language. Breaking barriers for global learners.
            </p>
          </div>
          <div className="visualContainer">
            <div className="translateVisual">
              <div className="langNode">EN</div>
              <div className="langArrow">⇄</div>
              <div className="langNode active">UR</div>
            </div>
          </div>
        </div>

      </div>
    </section>
  );
}

function TechStackSection() {
  return (
    <section className="techStackSection">
      <div className="container">
        <div className="sectionHeader">
          <h2 className="sectionTitle">The Intelligence Stack</h2>
          <p className="sectionSubtitle">Powered by industry-standard tools for embodied intelligence.</p>
        </div>
        <div className="techGrid">
          {/* Card 1 */}
          <div className="techCard">
            <div className="techIcon">⚛️</div>
            <h3 className="techName">ROS 2</h3>
            <p className="techDesc">Robotic Nervous System</p>
          </div>
          {/* Card 2 */}
          <div className="techCard">
            <div className="techIcon">🦾</div>
            <h3 className="techName">Isaac Sim</h3>
            <p className="techDesc">Photorealistic Physics</p>
          </div>
          {/* Card 3 */}
          <div className="techCard">
            <div className="techIcon">🧠</div>
            <h3 className="techName">PyTorch</h3>
            <p className="techDesc">Deep Learning Brain</p>
          </div>
          {/* Card 4 */}
          <div className="techCard">
            <div className="techIcon">⚡</div>
            <h3 className="techName">Jetson Orin</h3>
            <p className="techDesc">Edge Compute</p>
          </div>
        </div>
      </div>
    </section>
  );
}

export default function Home(): JSX.Element {
  const { siteConfig } = useDocusaurusContext();
  return (
    <Layout
      title={`${siteConfig.title}`}
      description="Physical AI & Humanoid Robotics Course">
      <HomepageHeader />
      <main>
        <CreativeFeaturesSection />
        <TechStackSection />
      </main>
    </Layout>
  );
}