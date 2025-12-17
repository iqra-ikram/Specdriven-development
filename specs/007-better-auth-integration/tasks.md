# Implementation Tasks: Better Auth Integration

**Feature Branch**: `007-better-auth-integration`
**Status**: Pending

## Phase 1: Setup (Project Initialization)

Establish the new Node.js service and database infrastructure.

- [x] T001 Initialize `auth-service` directory with `package.json` and TypeScript config
- [x] T002 Install `better-auth`, `hono`, `dotenv`, `pg`, `drizzle-orm` in `auth-service`
- [x] T003 Configure Drizzle and Better Auth schema in `auth-service/src/db/schema.ts`
- [x] T004 Implement Hono server with Better Auth handler in `auth-service/src/index.ts`
- [ ] T005 [P] Run database migrations to create `user`, `session`, `account` tables in Neon

## Phase 2: Foundational (Blocking Prerequisites)

Enable communication between services and session verification.

- [x] T006 Configure `docusaurus-root` with `better-auth` client in `src/lib/auth-client.ts`
- [x] T007 [P] Create Python SQLAlchemy models for `user` and `session` tables in `backend/src/models/auth_models.py` (Read-only)
- [x] T008 Implement Python auth middleware to verify session tokens in `backend/src/core/auth_middleware.py`

## Phase 3: User Story 1 - User Registration

**Goal**: Users can create an account using email and password.
**Independent Test**: Register a new user via the UI and verify the record exists in the `user` table.

- [x] T009 [US1] Create Sign Up page component in `docusaurus-root/src/pages/signup.tsx`
- [x] T010 [US1] Implement form submission handler calling `authClient.signUp.email` in `docusaurus-root/src/components/Auth/SignUpForm.tsx`
- [x] T011 [US1] Add error handling for duplicate emails in `docusaurus-root/src/components/Auth/SignUpForm.tsx`
- [x] T012 [US1] [P] Verify new user creation logic works via manual test

## Phase 4: User Story 2 - User Login

**Goal**: Users can log in to access their account.
**Independent Test**: Login with valid credentials and verify a session token is set in cookies.

- [x] T013 [US2] Create Login page component in `docusaurus-root/src/pages/login.tsx`
- [x] T014 [US2] Implement form submission handler calling `authClient.signIn.email` in `docusaurus-root/src/components/Auth/LoginForm.tsx`
- [x] T015 [US2] Implement redirect logic to home/dashboard after successful login in `docusaurus-root/src/pages/login.tsx`

## Phase 5: User Story 3 - Protected Route Access

**Goal**: Certain pages or features should only be accessible to authenticated users.
**Independent Test**: Accessing a protected route without a session redirects to login.

- [x] T016 [US3] Create `RequireAuth` Higher-Order Component (HOC) in `docusaurus-root/src/components/Auth/RequireAuth.tsx`
- [x] T017 [US3] Apply `RequireAuth` to a demo dashboard page in `docusaurus-root/src/pages/dashboard.tsx`
- [x] T018 [US3] [P] Update Python backend to require `auth_middleware` dependency on protected API routes in `backend/src/api/protected.py`

## Phase 6: User Story 4 - Sign Out

**Goal**: Authenticated users should be able to securely log out.
**Independent Test**: Clicking logout removes the session cookie and updates UI state.

- [x] T019 [US4] Create Sign Out button component in `docusaurus-root/src/components/Auth/SignOutButton.tsx`
- [x] T020 [US4] Implement logout handler calling `authClient.signOut` in `docusaurus-root/src/components/Auth/SignOutButton.tsx`
- [x] T021 [US4] Update Navbar to show Login/Sign Up vs Sign Out/Profile based on session state in `docusaurus-root/src/theme/NavbarItem/AuthNavbarItem.tsx` (Custom Item)

## Final Phase: Polish

- [x] T022 Add loading skeletons/spinners during auth state resolution in `docusaurus-root/src/components/Auth/AuthLoading.tsx`
- [x] T023 Ensure all auth pages support internationalization (i18n) via `Translate` component

## Dependencies

1. **Setup** (T001-T005) MUST complete before all others.
2. **Foundational** (T006-T008) MUST complete before US3 (Protected Routes) and Backend verification.
3. **US1** (Registration) and **US2** (Login) can be developed in parallel, but US2 depends on US1 data for testing.
4. **US3** (Protected Routes) depends on US2 (Login) to be verifiable.

## Implementation Strategy

1. **MVP**: Setup Service + Registration + Login (Phases 1, 2, 3, 4).
2. **Security**: Add Backend Middleware (Phase 2/5).
3. **UX**: Add Protected Routes and Navbar updates (Phases 5, 6).
