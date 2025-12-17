# Tasks: Author Book Content

**Feature**: 002-author-book-content
**Prerequisites**: Feature 001 complete (Docusaurus setup).

## Phase 1: Cleanup & Structure
- [ ] **T001**: Remove default Docusaurus tutorial files.
    - **Action**: Delete `docs/tutorial-basics`, `docs/tutorial-extras`, `docs/intro.md` (will replace).
    - **Verification**: `docs/` folder should be clean.

- [ ] **T002**: Create new directory structure.
    - **Action**: Create `docs/modules`.
    - **Verification**: Directory exists.

## Phase 2: Content Authoring
- [ ] **T003**: Create `docs/intro.md`.
    - **Content**: Course Overview, Goal, Why Physical AI Matters, Learning Outcomes.
    - **Action**: Write MDX file.

- [ ] **T004**: Create `docs/schedule.md`.
    - **Content**: Weekly breakdown (Weeks 1-13).
    - **Action**: Write MDX file using a table or list format.

- [ ] **T005**: Create `docs/modules/01-nervous-system.md`.
    - **Content**: Module 1 (ROS 2).
    - **Action**: Write MDX file.

- [ ] **T006**: Create `docs/modules/02-digital-twin.md`.
    - **Content**: Module 2 (Gazebo & Unity).
    - **Action**: Write MDX file.

- [ ] **T007**: Create `docs/modules/03-ai-robot-brain.md`.
    - **Content**: Module 3 (NVIDIA Isaac).
    - **Action**: Write MDX file.

- [ ] **T008**: Create `docs/modules/04-vla.md`.
    - **Content**: Module 4 (VLA) and Capstone Project.
    - **Action**: Write MDX file.

- [ ] **T009**: Create `docs/hardware.md`.
    - **Content**: Workstations, Edge Kits, Robot Lab options. Use Tabs for organization.
    - **Action**: Write MDX file.

- [ ] **T010**: Create `docs/assessments.md`.
    - **Content**: List of assessments and details.
    - **Action**: Write MDX file.

## Phase 3: Assets & Configuration
- [ ] **T011**: Update `docusaurus-root/sidebars.ts` (if needed).
    - **Action**: Verify sidebar generation logic covers the new structure.
    - **Verification**: Sidebar displays correctly.

- [ ] **T012**: Add placeholder assets.
    - **Action**: Create `static/img/architecture-placeholder.png` (or similar).
    - **Verification**: Image exists.

## Phase 4: Verification
- [ ] **T013**: Build the site.
    - **Action**: Run `npm run build`.
    - **Verification**: Build succeeds.
