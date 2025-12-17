# Tasks: Initial Docusaurus Project Setup

**Input**: Design documents from `/specs/001-setup-docusaurus-book/`
**Prerequisites**: plan.md, spec.md

**Organization**: The tasks are structured sequentially as this is a foundational setup feature.

## Format: `[ID] Description`

---

## Phase 1: Project Scaffolding & Configuration

**Purpose**: Create the initial Docusaurus project and apply basic configuration.

- [x] **T001**: Scaffold a new Docusaurus project named `docusaurus-root`.
    - **Action**: Run `npx create-docusaurus@latest docusaurus-root classic`.
    - **Verification**: The `docusaurus-root` directory is created, containing `package.json` and `docusaurus.config.js`. The command and subsequent dependency installation complete without errors.

- [x] **T002**: Configure the project title.
    - **Action**: Modify the `title` property in `docusaurus-root/docusaurus.config.js` to be "Physical AI & Humanoid Robotics".
    - **Verification**: A file inspection (e.g., using `grep` or `findstr`) confirms the `title` field is set correctly.

---

## Phase 2: Verification

**Purpose**: Ensure the newly created project is functional.

- [x] **T003**: Verify the local development server.
    - **Action**: From the `docusaurus-root` directory, run `npm start`.
    - **Verification**: The server starts successfully on `http://localhost:3000`. A web browser can access this URL, and the rendered page displays the title "Physical AI & Humanoid Robotics".

- [x] **T004**: Verify the static site build process.
    - **Action**: From the `docusaurus-root` directory, run `npm run build`.
    - **Verification**: The command completes successfully. A `build` directory is created inside `docusaurus-root`, and it contains an `index.html` file.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Scaffolding & Configuration)**: Can start immediately.
- **Phase 2 (Verification)**: Depends on the successful completion of all tasks in Phase 1.

### Task Dependencies

- **T001** must be completed before **T002**, **T003**, and **T004**.
- **T002** must be completed before **T003**.
- **T003** and **T004** can technically be run in any order after T001/T002, but verifying the dev server first is a common workflow.

---
