# Implementation Plan: Add Urdu Translation

**Branch**: `006-add-urdu-translation` | **Date**: 2025-12-05 | **Spec**: [specs/006-add-urdu-translation/spec.md](../spec.md)
**Input**: Feature specification from `specs/006-add-urdu-translation/spec.md`

## Summary

Enable Urdu language support in the Docusaurus-based documentation site to fulfill the new accessibility mandate. This involves configuring Docusaurus internationalization (i18n) settings, adding the Urdu locale (`ur`) with Right-to-Left (RTL) directionality, and establishing the file structure for localized content and translation strings.

## Technical Context

**Language/Version**: TypeScript 5.x, React 18+ (Docusaurus v3)
**Primary Dependencies**: Docusaurus core i18n system
**Storage**: File-based (Markdown for content, JSON for UI translations)
**Testing**: Playwright (E2E) for locale switching and RTL layout verification
**Target Platform**: Static Web (Docusaurus build)
**Project Type**: Web application (Frontend only for this feature)
**Performance Goals**: Minimal impact on build time; instant client-side locale switching
**Constraints**: Must support RTL layout; Fallback to English for missing translations
**Scale/Scope**: Initial setup for 1 new language (Urdu), scalable to more

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Principle III (Docusaurus for Frontend UI)**: ✅ Compliant. Using native Docusaurus i18n features.
- **Principle VIII (Global Accessibility & Multi-language Support)**: ✅ Compliant. Directly addresses the mandate for Urdu support.
- **Principle IV (Prescribed Core Technology Stack)**: ✅ Compliant. Uses standard Docusaurus/React stack.

## Project Structure

### Documentation (this feature)

```text
specs/006-add-urdu-translation/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # N/A (Static Site)
└── tasks.md             # Phase 2 output (future)
```

### Source Code (repository root)

```text
docusaurus-root/
├── docusaurus.config.ts      # Config update
├── i18n/                     # New directory
│   └── ur/
│       ├── docusaurus-plugin-content-docs/  # Localized docs
│       ├── docusaurus-theme-classic/        # Localized navbar/footer
│       └── code.json                        # UI strings
└── tests/
    └── e2e/                  # New locale tests
```

**Structure Decision**: Standard Docusaurus i18n file structure.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None      | -          | -                                   |
