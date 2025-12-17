# Research: Docusaurus i18n & RTL Support

**Feature**: Add Urdu Translation
**Status**: Complete

## 1. Docusaurus Internationalization (i18n)

### Decision
Use the built-in Docusaurus i18n system.

### Rationale
Docusaurus v2+ (and v3) has first-class support for i18n, including routing, build-time localization, and theme translation. It avoids the need for external libraries or complex custom routing.

### Implementation Details
- **Config**: `docusaurus.config.ts` must export an `i18n` object.
- **Locales**: `ur` (Urdu) will be added. `en` remains default.
- **Path**: URLs will be `/` (English) and `/ur/` (Urdu).

## 2. Right-to-Left (RTL) Support

### Decision
Configure `direction: 'rtl'` in `localeConfigs` for 'ur'.

### Rationale
Docusaurus automatically applies `dir="rtl"` to the `<html>` tag and adjusts CSS (margins, paddings, flex direction) when the locale direction is set to RTL. This is native behavior and requires minimal custom CSS.

## 3. Translation Management

### Decision
- **Content**: Markdown files copied to `i18n/ur/docusaurus-plugin-content-docs/current/`.
- **UI Labels**: JSON files in `i18n/ur/code.json` generated via `npm run write-translations`.

### Rationale
Standard Docusaurus workflow. Allows separating content translation from UI label translation.

## 4. Unknowns Resolved

- **RTL Handling**: Verified Docusaurus supports this via config.
- **Navbar**: Verified language dropdown is a standard theme feature (`type: 'localeDropdown'`).

## 5. Alternatives Considered

- **Google Translate Widget**: Rejected. Low quality, doesn't fulfill the "accessibility" mandate properly, looks unprofessional.
- **Separate Deployment**: Rejected. Harder to maintain, duplicates infrastructure. Single-site i18n is preferred.
