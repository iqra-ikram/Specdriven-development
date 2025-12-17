# Quickstart Guide

This guide provides the essential steps to get the "Physical AI & Humanoid Robotics" documentation site up and running on a local machine for development and content creation.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

1.  **Node.js**: Version `18.0` or higher. You can check your version by running `node -v`.
2.  **npm**: Comes bundled with Node.js. You can check your version with `npm -v`.

## Setup

This step involves scaffolding the Docusaurus project. This only needs to be done once.

1.  **Navigate to your development directory**:
    ```bash
    cd path/to/your/projects
    ```

2.  **Run the Docusaurus initialization command**:
    This command will create a new directory named `physicl-ai-book` (or similar) containing the project.
    ```bash
    npx create-docusaurus@latest physicl-ai-book classic
    ```

3.  **Navigate into the new project directory**:
    ```bash
    cd physicl-ai-book
    ```

## Running the Local Development Server

To preview the site as you make changes, use the local development server. It provides live reloading, so changes to markdown files or React components will be reflected in your browser automatically.

1.  **Start the server**:
    ```bash
    npm run start
    ```

2.  **Open your browser**:
    Once the build is complete, open your web browser and navigate to `http://localhost:3000`. You should see the default homepage.

## Adding Content

-   To add or edit documentation pages, go to the `docs/` directory.
-   To modify the sidebar navigation, edit the `sidebars.js` file.
-   To change the homepage, edit `src/pages/index.js`.

## Building for Production

When you are ready to deploy the site, you need to create a static build.

1.  **Run the build command**:
    ```bash
    npm run build
    ```

2.  **Find the output**:
    The complete, production-ready website will be generated in the `build/` directory. These are the files you would upload to a web host.