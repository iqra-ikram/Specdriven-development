---
id: 003
title: add urdu translation mandate
stage: constitution
date: 2025-12-05
surface: agent
model: gemini-2.0-flash-exp
feature: none
branch: main
user: user
command: /sp.constitution
labels: ["constitution", "i18n", "urdu"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - null
---

## Prompt

i want to integrate a feature in my website so that user can translate my book in urdu also

## Response snapshot

Updated constitution to v1.2.0 adding Principle VIII for Global Accessibility & Multi-language Support (Urdu).

## Outcome

- ✅ Impact: Constitution amended to mandate i18n and Urdu support.
- 🧪 Tests: n/a
- 📁 Files: Modified constitution.md
- 🔁 Next prompts: Feature implementation
- 🧠 Reflection: User request was a feature request but routed to constitution; interpreted as a mandate update.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): n/a
- Prompt variant (if applicable): default
- Next experiment (smallest change to try): none
