id: 012
title: Fix Module Not Found Error in Urdu Homepage
stage: fix
date: 2025-12-05
surface: agent
model: gemini-1.5-pro-a006-20240730
feature: add-urdu-translation
branch: 006-add-urdu-translation
user: user
command: ERROR in ./i18n/ur/docusaurus-plugin-content-pages/index.tsx 2:0-68
Module not found: Error: Can't resolve '../../../../src/components/ChatbotWidget' in 'C:\Users\hp\OneDrive\Desktop\hackathon-ai\hackathon-ai\docusaurus-root\i18n\ur\docusaurus-plugin-content-pages' giving this error
labels: ["fix", "i18n", "docusaurus", "import-path"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - docusaurus-root/i18n/ur/docusaurus-plugin-content-pages/index.tsx
tests_yaml: |
  - N/A (Manual verification on localhost:3000 with --locale ur)
prompt_text: |
  ERROR in ./i18n/ur/docusaurus-plugin-content-pages/index.tsx 2:0-68
  Module not found: Error: Can't resolve '../../../../src/components/ChatbotWidget' in 'C:\Users\hp\OneDrive\Desktop\hackathon-ai\hackathon-ai\docusaurus-root\i18n\ur\docusaurus-plugin-content-pages' giving this error
response_text: |
  Fixed the "Module not found" error in the Urdu homepage (`docusaurus-root/i18n/ur/docusaurus-plugin-content-pages/index.tsx`) by updating the relative import paths for `styles` and `ChatbotWidget` to use the Docusaurus `@site` alias. This ensures correct module resolution when serving the Urdu locale.
