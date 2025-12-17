# Specification: Redesign Homepage Hero Section

**Feature**: Redesign Homepage
**Ref**: User provided `hero.png`
**Goal**: Update the Docusaurus homepage to match the visual style of the provided reference image.

## 1. Visual Design Requirements

### 1.1. Layout
- **Alignment**: Centered content.
- **Order**:
  1.  **Hero Image**: 3D Humanoid Robot with green backlighting/glow.
  2.  **Headline**: Large, bold typography.
  3.  **Subhead**: Smaller, descriptive text (grey/muted).
  4.  **CTA Button**: Pill-shaped, dark background with border.

### 1.2. Color Palette
- **Background**: Black (`#000000`) or very dark grey (`#0a0a0a`).
- **Text Primary**: White (`#ffffff`).
- **Text Secondary**: Grey (`#888888`).
- **Accent**: Green (`#4ade80` or similar from image).

### 1.3. Typography
- **Headline**: "Where Digital Brains / Meet Physical Bodies – Physical AI."
  - "Physical AI" should be in the Green accent color.
- **Subhead**: "Bridging the gap between the digital brain and the physical body. Students apply their AI knowledge to control Humanoid Robots."

### 1.4. Assets
- Need a new "3D Humanoid Robot" image to replace the Docusaurus logo/default hero.

## 2. Technical Changes
- **File**: `src/pages/index.tsx`
  - Refactor the `HomepageHeader` component.
- **File**: `src/css/custom.css`
  - Add classes for `.hero-robot-img`, `.hero-title`, `.hero-subtitle`, `.hero-cta`.
  - Override default Docusaurus hero styles.

## 3. Acceptance Criteria
- Homepage matches the visual hierarchy of `hero.png`.
- "Physical AI" text is green.
- Background is dark.
- Robot image is centered at the top.
