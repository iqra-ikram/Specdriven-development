# Data Model: Internationalization Structure

**Feature**: Add Urdu Translation

## File Structure

Docusaurus uses a filesystem-based data model for translations.

```text
docusaurus-root/
├── i18n/
│   └── ur/                                      # Locale code for Urdu
│       ├── code.json                            # Global UI strings (navbar, footer, etc.)
│       ├── docusaurus-plugin-content-docs/      # Documentation content
│       │   └── current/                         # Version (default)
│       │       ├── intro.md                     # Translated Intro
│       │       └── ...                          # Other docs
│       ├── docusaurus-plugin-content-pages/     # Standalone pages
│       │   ├── index.md                         # Translated Homepage (if markdown)
│       │   └── ...
│       └── docusaurus-theme-classic/            # Theme-specific overrides
│           └── navbar.json                      # (Optional) Navbar items
```

## Configuration Model (`docusaurus.config.ts`)

The configuration object is the single source of truth for available languages.

```typescript
interface I18nConfig {
  defaultLocale: string; // 'en'
  locales: string[];     // ['en', 'ur']
  localeConfigs: {
    [key: string]: {
      label: string;     // 'Urdu'
      direction: string; // 'rtl'
      htmlLang: string;  // 'ur'
    }
  }
}
```

## Translation Data

- **JSON format**: Key-value pairs.
  ```json
  {
    "theme.navbar.title": {
      "message": "Physical AI & Humanoid Robotics (Urdu)",
      "description": "The title in the navbar"
    }
  }
  ```
- **Markdown format**: Standard Frontmatter + Content.
  ```markdown
  ---
  title: تعارف (Introduction)
  ---
  
  یہاں آپ کا متن ہے...
  ```
