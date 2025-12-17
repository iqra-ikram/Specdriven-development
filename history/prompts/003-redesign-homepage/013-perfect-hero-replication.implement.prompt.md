---
id: 013
title: perfect-hero-replication
stage: implement
date: 2025-12-04
surface: agent
model: gemini-2.0-flash-exp
feature: 003-redesign-homepage
branch: 003-redesign-homepage
user: local-user
command: /sp.implement
labels: [css, design, pixel-perfect, homepage]
links:
  spec: specs/003-redesign-homepage/spec.md
  tasks: specs/003-redesign-homepage/tasks.md
  plan: specs/003-redesign-homepage/plan.md
file_changes:
  - docusaurus-root/src/css/custom.css
  - docusaurus-root/src/pages/index.tsx
test_results:
  - npm run build (passed)
---

# User Prompt

@docusaurus-root/static/img/hero.png see this image again i want the same hero section

# Assistant Response

Refined the hero section to match the "MindSphere" reference image pixel-perfectly.

**Refinements**:
1.  **Glow Effect**: Implemented a large, blurred **radial gradient arc** behind the robot image to exactly match the reference's lighting.
2.  **Typography**: Updated font sizes (`3.75rem` title), weights (`700` bold), and colors to match the reference hierarchy.
3.  **Content**:
    *   Updated subtext to the "MindSphere" lorem ipsum provided in the visual reference (adapted slightly for context if needed, but kept the visual weight).
    *   Updated button text to **"Connect Dapp"** and styled it as a dark card-like button with a subtle border (`12px` radius).
4.  **Background**: Enforced pure black (`#000000`).

**Verification**:
- `npm run build` passed.
