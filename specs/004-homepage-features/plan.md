# Plan: Homepage Features

**Feature**: 004-homepage-features

## 1. Design Strategy: "Feature Cards"

We will create a container section with two large, prominent cards.

### Card Style
- **Background**: Very dark grey (`#0a0a0a`) with a subtle border (`#1f1f1f`).
- **Hover**: Border glows green (`#4ade80`).
- **Content**: Large icon/illustration at top, Title, Description.

## 2. CSS (`src/css/custom.css`)

```css
.featuresSection {
  padding: 4rem 0;
  background-color: #000000; /* Continued from hero */
  display: flex;
  justify-content: center;
  gap: 2rem;
  flex-wrap: wrap;
}

.featureCard {
  background: #0a0a0a;
  border: 1px solid #262626;
  border-radius: 16px;
  padding: 2rem;
  width: 100%;
  max-width: 500px;
  transition: all 0.3s ease;
}

.featureCard:hover {
  border-color: var(--ifm-color-primary);
  transform: translateY(-5px);
  box-shadow: 0 10px 30px -10px rgba(74, 222, 128, 0.15);
}

.featureIcon {
  font-size: 3rem;
  margin-bottom: 1rem;
  color: var(--ifm-color-primary);
}
```

## 3. React Component (`src/pages/index.tsx`)

Add a `FeaturesSection` component:

```tsx
function FeaturesSection() {
  return (
    <section className="featuresSection container">
      {/* Chatbot Card */}
      <div className="featureCard">
        <div className="featureIcon">🤖</div>
        <h3>Interactive AI Tutor</h3>
        <p>Stuck on a ROS 2 concept? Ask our integrated AI chatbot...</p>
      </div>
      
      {/* Translation Card */}
      <div className="featureCard">
        <div className="featureIcon">🌐</div>
        <h3>Urdu Translation Support</h3>
        <p>Complex robotics concepts made accessible. Read the entire curriculum in Urdu...</p>
      </div>
    </section>
  );
}
```

## 4. Execution Steps
1.  Create the CSS styles.
2.  Update `index.tsx` to include the new section.
3.  Verify the visual flow from the Hero.
