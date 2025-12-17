id: 007
title: Fix Text Selection Popup for Urdu Locale
stage: fix
date: 2025-12-05
surface: agent
model: gemini-1.5-pro-a006-20240730
feature: add-urdu-translation
branch: 006-add-urdu-translation
user: user
command: it is doing but somwetimes and only on local host 3001 why ?? please fix this make the process correct i am talking about translate in urdu dunctionality
labels: ["fix", "i18n", "urdu", "chatbot", "docusaurus"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - docusaurus-root/src/components/TextSelectionPopup/index.tsx
tests_yaml: |
  - N/A (Manual verification on localhost:3001)
prompt_text: |
  it is doing but somwetimes and only on local host 3001 why ?? please fix this make the process correct i am talking about translate in urdu dunctionality
response_text: |
  The `TextSelectionPopup` component was modified to dynamically adjust the prompt sent to the AI chatbot based on the current Docusaurus locale. When the user is viewing the site in Urdu (`i18n.currentLocale === 'ur'`), the prompt for the selected text will now explicitly request an explanation in Urdu (e.g., "Explain this in Urdu: ..."). This resolves the intermittent issue where the AI chatbot would sometimes provide explanations in English even when on the Urdu site, ensuring consistent language behavior for the "translate in urdu functionality" as described by the user.
