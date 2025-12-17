---
id: 012
title: redesign-homepage-hero
stage: implement
date: 2025-12-04
surface: agent
model: gemini-2.0-flash-exp
feature: 003-redesign-homepage
branch: 003-redesign-homepage
user: local-user
command: /sp.implement
labels: [design, css, docusaurus, homepage]
links:
  spec: specs/003-redesign-homepage/spec.md
  tasks: specs/003-redesign-homepage/tasks.md
  plan: specs/003-redesign-homepage/plan.md
file_changes:
  - docusaurus-root/src/css/custom.css
  - docusaurus-root/src/pages/index.tsx
  - docusaurus-root/static/img/hero-robot.png
test_results:
  - npm run build (passed)
---

# User Prompt

@docusaurus-root/static/img/hero.png the hero section of the homepage of the docussaurus website will same to same like this ensure the pixel perfectness i want the same sections make it for me

# Assistant Response

Redesigned the Docusaurus homepage to match the provided reference style ("MindSphere").

**Visual Updates**:
1.  **Dark Theme**: Enforced a deep black/grey background (`#050505`).
2.  **Hero Image**: Sourced a 3D humanoid robot image (`hero-robot.png`) and added a radial green glow effect behind it.
3.  **Typography**:
    *   Title: "Where Digital Brains Meet Physical Bodies" with a green accent on "Physical AI".
    *   Subtitle: Grey text matching the layout.
4.  **CTA Button**: Styled as a pill-shaped dark button with hover effects.
5.  **Layout**: Centered all elements to mimic the reference.

**Verification**:
- `npm run build` passed successfully.
