# Plan: Redesign Homepage

**Feature**: 003-redesign-homepage

## 1. Asset Acquisition
We need a "3D Robot" image.
- **Action**: Search and download a suitable open-license image or use a high-quality placeholder.
- **Path**: `static/img/hero-robot.png`

## 2. CSS Styling (`src/css/custom.css`)
We need to implement the "MindSphere" aesthetic.

```css
:root {
  --ifm-color-primary: #4ade80; /* Green accent */
  --ifm-background-color: #050505; /* Almost black */
}

.heroBanner {
  padding: 4rem 0;
  text-align: center;
  background: #050505;
}

.heroImage {
  max-width: 400px;
  margin-bottom: 2rem;
  filter: drop-shadow(0 0 40px rgba(74, 222, 128, 0.3)); /* Green glow */
}

.heroTitle {
  font-size: 4rem;
  font-weight: 700;
  line-height: 1.1;
  color: white;
  margin-bottom: 1.5rem;
}

.heroTitleAccent {
  color: #4ade80;
}

.heroSubtitle {
  font-size: 1.25rem;
  color: #9ca3af;
  max-width: 600px;
  margin: 0 auto 2rem;
}

.heroButton {
  background-color: #1f2937;
  border: 1px solid #374151;
  color: white;
  padding: 12px 32px;
  border-radius: 9999px;
  font-weight: 600;
  transition: all 0.2s;
}

.heroButton:hover {
  background-color: #374151;
  color: #4ade80;
  text-decoration: none;
}
```

## 3. React Component (`src/pages/index.tsx`)
Refactor the structure:

```tsx
<header className={clsx('hero', styles.heroBanner)}>
  <div className="container">
    <img src="/img/hero-robot.png" className={styles.heroImage} alt="Robot" />
    <h1 className={styles.heroTitle}>
      Where Digital Brains Meet<br />
      Physical Bodies – <span className={styles.heroTitleAccent}>Physical AI.</span>
    </h1>
    <p className={styles.heroSubtitle}>
      {siteConfig.tagline}
    </p>
    <div className={styles.buttons}>
      <Link className={styles.heroButton} to="/docs/intro">
        Start Learning
      </Link>
    </div>
  </div>
</header>
```

## 4. Execution Steps
1. Download robot image.
2. Update CSS.
3. Update Page Component.
4. Verify build.
