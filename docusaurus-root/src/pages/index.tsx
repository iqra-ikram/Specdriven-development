import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';
import styles from './index.module.css';
import { JSX } from 'react';
import ChatbotWidget from '../components/ChatbotWidget';
import Translate, {translate} from '@docusaurus/Translate';

function HomepageHeader() {
  const { siteConfig } = useDocusaurusContext();
  return (
    <header className="heroBanner">
      <div className="heroContainer container">
        {/* Image First, per reference */}
        <img
          src="img/hero-1.png"
          alt={translate({message: 'Physical AI Robot', id: 'homepage.hero.imgAlt'})}
          className="heroImage"
        />

        {/* Headline */}
        <h1 className="heroTitle">
          <Translate id="homepage.hero.title.part1">Where Digital Brains Meet</Translate><br />
          <Translate id="homepage.hero.title.part2">Physical Bodies – </Translate><span className="heroTitleAccent"><Translate id="homepage.hero.title.part3">Physical AI.</Translate></span>
        </h1>

        {/* Subtext */}
        <p className="heroSubtitle">
          <Translate id="homepage.hero.subtitle">
            MindSphere brings AI agents together to collaborate, solve challenges, and deliver transformative results—seamless, scalable, and adaptive.
          </Translate>
        </p>

        {/* Button */}
        <div>
          <Link
            className="heroButton"
            to="/docs/intro">
            <Translate id="homepage.hero.button">Connect Dapp</Translate>
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
            <h3 className="cardTitle"><Translate id="homepage.features.chatbot.title">Interactive AI Tutor</Translate></h3>
            <p className="cardDesc">
              <Translate id="homepage.features.chatbot.desc">
                Stuck on a node? Get instant, context-aware help with our integrated AI assistant.
              </Translate>
            </p>
          </div>
          <div className="visualContainer">
            <div className="chatVisual">
              <div className="chatBubble bubbleLeft"><Translate id="homepage.features.chatbot.bubbleLeft">How do I launch Gazebo?</Translate></div>
              <div className="chatBubble bubbleRight"><Translate id="homepage.features.chatbot.bubbleRight">Run `ros2 launch gazebo_ros...`</Translate></div>
            </div>
          </div>
        </div>

        {/* Translation Card */}
        <div className="creativeCard">
          <div className="cardContent">
            <h3 className="cardTitle"><Translate id="homepage.features.translation.title">Learn in Urdu</Translate></h3>
            <p className="cardDesc">
              <Translate id="homepage.features.translation.desc">
                Master robotics in your native language. Breaking barriers for global learners.
              </Translate>
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
          <h2 className="sectionTitle"><Translate id="homepage.techStack.title">The Intelligence Stack</Translate></h2>
          <p className="sectionSubtitle"><Translate id="homepage.techStack.subtitle">Powered by industry-standard tools for embodied intelligence.</Translate></p>
        </div>
        <div className="techGrid">
          {/* Card 1 */}
          <div className="techCard">
            <div className="techIcon">⚛️</div>
            <h3 className="techName">ROS 2</h3>
            <p className="techDesc"><Translate id="homepage.techStack.ros2">Robotic Nervous System</Translate></p>
          </div>
          {/* Card 2 */}
          <div className="techCard">
            <div className="techIcon">🦾</div>
            <h3 className="techName">Isaac Sim</h3>
            <p className="techDesc"><Translate id="homepage.techStack.isaac">Photorealistic Physics</Translate></p>
          </div>
          {/* Card 3 */}
          <div className="techCard">
            <div className="techIcon">🧠</div>
            <h3 className="techName">PyTorch</h3>
            <p className="techDesc"><Translate id="homepage.techStack.pytorch">Deep Learning Brain</Translate></p>
          </div>
          {/* Card 4 */}
          <div className="techCard">
            <div className="techIcon">⚡</div>
            <h3 className="techName">Jetson Orin</h3>
            <p className="techDesc"><Translate id="homepage.techStack.jetson">Edge Compute</Translate></p>
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