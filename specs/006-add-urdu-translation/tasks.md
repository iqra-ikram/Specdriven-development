# Tasks: Add Urdu Translation

**Feature Branch**: `006-add-urdu-translation`
**Spec**: [specs/006-add-urdu-translation/spec.md](specs/006-add-urdu-translation/spec.md)
**Status**: Draft

## Implementation Strategy

This feature relies on the native Docusaurus i18n system. The strategy is to first enable the Urdu locale in the configuration (Phase 2), which will break nothing but enable the infrastructure. Then, we will populate the locale with translated content and UI strings (Phase 3). Testing will be done via manual verification of the locale switch and RTL layout, as automated E2E tests for layout visual regression are out of scope for this iteration.

## Phase 1: Setup

*Goal: Initialize the workspace for i18n work.*

- [x] T001 Create i18n directory structure for Urdu in docusaurus-root/i18n/ur

## Phase 2: Foundational

*Goal: Enable Urdu locale in configuration and layout support (RTL).*

- [x] T002 Configure i18n settings in docusaurus-root/docusaurus.config.ts to add 'ur' locale with RTL direction
- [x] T003 Add localeDropdown item to navbar in docusaurus-root/docusaurus.config.ts if not present

## Phase 3: User Story 1 - Switch Language to Urdu

*Goal: Users can switch site language to Urdu and see translated UI.*

**Independent Test**: Click language dropdown -> Select Urdu -> Site reloads with /ur/ prefix and translated UI labels.

- [x] T004 [US1] Generate initial translation JSONs using write-translations command
- [x] T005 [US1] Translate key UI labels (Navbar, Footer) in docusaurus-root/i18n/ur/code.json to Urdu
- [x] T006 [US1] Copy Homepage content to docusaurus-root/i18n/ur/docusaurus-plugin-content-pages/index.tsx (or md)
- [x] T007 [US1] Translate Homepage content to Urdu in docusaurus-root/i18n/ur/docusaurus-plugin-content-pages/index.tsx
- [x] T008 [US1] Copy Intro doc to docusaurus-root/i18n/ur/docusaurus-plugin-content-docs/current/intro.md
- [x] T009 [US1] Translate Intro doc to Urdu in docusaurus-root/i18n/ur/docusaurus-plugin-content-docs/current/intro.md

## Phase 4: User Story 2 - Right-to-Left (RTL) Layout Support

*Goal: Urdu content is displayed correctly in RTL format.*

**Independent Test**: View Urdu site -> Verify text alignment is Right and layout mirrors LTR (e.g., sidebar on opposite side if theme supports, or text direction).

- [x] T010 [US2] Verify and adjust custom CSS in docusaurus-root/src/css/custom.css to support RTL if default theme needs overrides (Optional/Check)

## Dependencies

1. **Setup (T001)** must complete before any translation work.
2. **Configuration (T002, T003)** enables the build system to recognize `ur`.
3. **Translation (T004-T009)** depends on Configuration.
4. **RTL Tweaks (T010)** depends on seeing the rendered Urdu content.

## Parallel Execution Examples

- **Content Translation**: T007 (Homepage) and T009 (Intro Doc) can be done in parallel by different translators/agents once the directory structure (T001) is ready.
