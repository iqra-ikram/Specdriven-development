---
id: 006
title: fix build and launch serve
stage: misc
date: 2025-12-05
surface: agent
model: gemini-2.0-flash-exp
feature: add-urdu-translation
branch: 006-add-urdu-translation
user: user
command: /sp.implement
labels: ["fix", "build", "docusaurus", "i18n"]
links:
  spec: specs/006-add-urdu-translation/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - docusaurus-root/i18n/ur/docusaurus-plugin-content-pages/index.tsx
tests:
 - null
---

## Prompt

please do this for me (fix build and run serve)

## Response snapshot

Fixed relative import paths in Urdu homepage to use @site alias. Successfully built the project and launched `npm run serve` in a separate process for the user.

## Outcome

- ✅ Impact: Build fixed and server verified.
- 🧪 Tests: Build success.
- 📁 Files: index.tsx
- 🔁 Next prompts: /sp.git.commit_pr
- 🧠 Reflection: Relative paths are fragile in generated code; always prefer framework aliases (@site) when available.

## Evaluation notes (flywheel)

- Failure modes observed: Build failure due to module resolution.
- Graders run and results (PASS/FAIL): n/a
- Prompt variant (if applicable): default
- Next experiment (smallest change to try): none
