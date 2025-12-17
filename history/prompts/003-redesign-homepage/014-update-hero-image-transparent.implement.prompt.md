---
id: 014
title: update-hero-image-transparent
stage: implement
date: 2025-12-04
surface: agent
model: gemini-2.0-flash-exp
feature: 003-redesign-homepage
branch: 003-redesign-homepage
user: local-user
command: /sp.implement
labels: [design, image, update, homepage]
links:
  spec: specs/003-redesign-homepage/spec.md
  tasks: specs/003-redesign-homepage/tasks.md
  plan: specs/003-redesign-homepage/plan.md
file_changes:
  - docusaurus-root/static/img/hero-robot.png
  - docusaurus-root/src/css/custom.css
test_results:
  - npm run build (passed)
---

# User Prompt

image is not good on the hero section change the image use the robot image with no bg that will be good

# Assistant Response

Updated the hero section with a high-quality, transparent background robot image.

**Changes**:
1.  **Image Update**: Replaced `hero-robot.png` with a transparent PNG of a robot (`robot_PNG86.png` from pngimg.com) to eliminate the boxy background artifact.
2.  **CSS Refinement**: Removed the `mask-image` property from `.heroImage` in `custom.css` as it's no longer needed for a clean PNG, and replaced it with a subtle `drop-shadow` for better depth.

**Verification**:
- `npm run build` passed.
