# CLI Contracts

The primary interfaces for this feature are Command-Line Interface (CLI) commands, managed via `npm`. These commands are the "contracts" for setting up, developing, and building the Docusaurus project.

## 1. Project Initialization

This is the command that will be used to scaffold the entire Docusaurus project.

-   **Command**:
    ```bash
    npx create-docusaurus@latest <project-name> classic
    ```
-   **Description**: Initializes a new Docusaurus site using the `classic` template. The `<project-name>` will be the root directory for the new site.
-   **Inputs**:
    -   `project-name`: The name of the directory to create for the project.
    -   `template`: The template to use (`classic`).
-   **Outputs**:
    -   A new directory with the specified project name, containing a complete Docusaurus project structure.
    -   `node_modules` populated with the necessary dependencies.

## 2. Development Server

This command allows developers to preview the site locally with live reloading.

-   **Command**:
    ```bash
    npm run start
    ```
-   **Description**: Starts a local development server, typically on `http://localhost:3000`. The server watches for changes to content and configuration files and automatically rebuilds the site and reloads the browser.
-   **Inputs**: None.
-   **Outputs**:
    -   A running web server process.
    -   Console output indicating the server URL and build status.

## 3. Static Site Build

This command generates the final, production-ready static assets for the website.

-   **Command**:
    ```bash
    npm run build
    ```
-   **Description**: Compiles the Docusaurus project into a `build` directory containing static HTML, CSS, JavaScript, and other assets. This directory is ready to be deployed to a web hosting service.
-   **Inputs**: None.
-   **Outputs**:
    -   A `build` directory containing the optimized, static website.

## 4. Local Build Preview

This command allows for a local preview of the production build.

-   **Command**:
    ```bash
    npm run serve
    ```
-   **Description**: Serves the contents of the `build` directory locally. This is used to test the production build before deploying it.
-   **Inputs**: None.
-   **Outputs**:
    -   A running web server process serving the static files from the `build` directory.
