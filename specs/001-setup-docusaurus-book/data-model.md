# Data Model: Docusaurus Project Structure

The feature "Initial Docusaurus Project Setup" does not involve a database or traditional data models. The "data" in this context is the file system structure of the generated Docusaurus project.

## Project Root (`/`)

The following directory structure will be generated at the root of the repository.

```
/
├── .docusaurus/      # Docusaurus build-time cache and data. Automatically generated.
├── docs/             # Contains the markdown files for the documentation.
│   └── intro.md      # A placeholder introduction page.
├── src/              # Non-documentation files like pages or custom React components.
│   ├── components/   # Directory for custom React components.
│   ├── css/          # Directory for custom CSS.
│   └── pages/        # Directory for standalone pages (e.g., homepage).
│       └── index.js  # The homepage React component.
├── static/           # Static assets (images, etc.) that will be copied to the build root.
├── docusaurus.config.js # Main configuration file for the site.
├── package.json         # Lists project dependencies and scripts.
├── package-lock.json    # Records the exact versions of dependencies.
└── sidebars.js          # Configures the navigation sidebar for the `docs` section.
```

## Key Entities

### 1. Docusaurus Project
-   **Description**: The entire collection of files and folders that define the static website. It is managed via `npm` scripts and configured primarily through `docusaurus.config.js`.

### 2. Configuration File (`docusaurus.config.js`)
-   **Description**: The central control file for the project.
-   **Key Attributes**:
    -   `title`: The main title of the site ("Physical AI & Humanoid Robotics").
    -   `url`: The production URL of the site.
    -   `baseUrl`: The base path for the site (defaults to `/`).
    -   `presets`: Defines the core plugins and themes (e.g., `@docusaurus/preset-classic`).
    -   `themeConfig`: Configures UI elements like the navbar, footer, and color scheme.

### 3. Documentation Page (`*.md`)
-   **Description**: A single page of content within the `docs/` directory, written in Markdown.
-   **Key Attributes**:
    -   **Front Matter**: YAML metadata at the top of the file to set the page `title`, `description`, `sidebar_label`, etc.
    -   **Content**: Standard Markdown content.

### 4. Sidebar Configuration (`sidebars.js`)
-   **Description**: A JavaScript file that defines the structure of the navigation sidebar for the documentation pages. It can be configured to automatically generate a sidebar from the `docs/` directory structure or to create a custom, manually ordered sidebar.