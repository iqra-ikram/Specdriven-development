# Research: Better Auth Integration

## 1. Node.js Auth Service Setup

**Decision**: Use **Hono** with **better-auth**.
**Rationale**: Hono is lightweight, fast, and has a dedicated adapter for `better-auth`. It's perfect for a microservice that just handles auth endpoints.
**Alternatives**: Express (heavier), Fastify.

**Implementation Details**:
-   **Runtime**: Node.js (v20+)
-   **Framework**: Hono
-   **ORM**: Drizzle ORM (for `better-auth` to manage the DB).
-   **Database**: Connect to the *same* Neon Postgres connection string as the Python backend.

## 2. Database Schema & Sharing

**Decision**: `better-auth` will manage its own tables (`user`, `session`, `account`, `verification`). The Python backend will *read* from these tables but not modify them (except maybe linking users to application data).
**Rationale**: `better-auth` expects to own its schema.
**Schema**:
-   `user`: id, email, name, emailVerified, image, createdAt, updatedAt
-   `session`: id, userId, token, expiresAt, ipAddress, userAgent
-   `account`: id, userId, accountId, providerId, ...

**Python Integration**:
-   The Python backend needs to verify the `session_token` passed in the Cookie.
-   It will query the `session` table: `SELECT * FROM session WHERE token = :token AND expiresAt > NOW()`.
-   If valid, it fetches the `user` details.

## 3. Frontend Integration (Docusaurus)

**Decision**: Use `@better-auth/react` client in Docusaurus.
**Details**:
-   Install `better-auth` in `docusaurus-root`.
-   Create a client instance pointing to the Auth Service URL (e.g., `http://localhost:4000`).
-   Use `useSession()` hook in React components to get user state.
-   **CORS**: The Auth Service must allow requests from the Docusaurus origin (e.g., `http://localhost:3000`).

## 4. Environment Variables

We need to sync `.env` across services or have separate ones.
-   `DATABASE_URL`: Shared.
-   `BETTER_AUTH_SECRET`: Shared (if Python needs to verify signatures, though DB check is safer/simpler for opaque tokens).
-   `BETTER_AUTH_URL`: The URL of the auth service.

## 5. Deployment Considerations

-   **Auth Service**: Deployed as a Node.js web service (Render/Railway/Vercel).
-   **Python Backend**: Existing deployment.
-   **Frontend**: Static/SPA deployment.

**Open Questions Resolved**:
-   *How to verify in Python?* Direct SQL query to the `session` table is the most reliable method for a hybrid stack sharing a DB.
