# Quickstart: Running with Urdu Translation

## Prerequisites

- Node.js 18+
- Dependencies installed (`npm install`)

## Starting the Development Server

To start the site in the default language (English):

```bash
npm run start
```

To start the site specifically in **Urdu** (to test RTL and translations):

```bash
npm run start -- --locale ur
```

## Building for Production

To build the static site for all configured locales:

```bash
npm run build
```

This will generate:
- `build/` (English)
- `build/ur/` (Urdu)

## Extracting Translation Strings

If you add new UI elements, update the translation JSONs:

```bash
npm run write-translations -- --locale ur
```

This will populate/update `i18n/ur/code.json`.
