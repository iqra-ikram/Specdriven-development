# Quickstart: Authentication Service

## Prerequisites

- Node.js v20+
- pnpm
- Access to the shared Neon Database

## Setup Auth Service

1. Navigate to the `auth-service` directory (to be created):
   ```bash
   cd auth-service
   ```

2. Install dependencies:
   ```bash
   pnpm install
   ```

3. Configure Environment:
   Create `.env` in `auth-service/`:
   ```bash
   DATABASE_URL="postgres://user:pass@host/db?sslmode=require"
   BETTER_AUTH_SECRET="your-generated-secret"
   BETTER_AUTH_URL="http://localhost:4000"
   ```

4. Run Migrations (via Better Auth / Drizzle):
   ```bash
   pnpm db:migrate
   ```

5. Start the Server:
   ```bash
   pnpm dev
   ```
   Server runs at `http://localhost:4000`.

## Frontend Integration (Docusaurus)

1. Install client:
   ```bash
   cd docusaurus-root
   npm install better-auth
   ```

2. Create Client:
   `src/lib/auth-client.ts`:
   ```typescript
   import { createAuthClient } from "better-auth/react"
   export const authClient = createAuthClient({
       baseURL: "http://localhost:4000" // Adjust for production
   })
   ```

3. Use in Components:
   ```typescript
   import { authClient } from "../../lib/auth-client";
   
   const { data: session } = authClient.useSession();
   ```

## Backend Verification (Python)

Ensure `sqlalchemy` is configured with the same `DATABASE_URL`.
Use the provided `auth_middleware.py` (to be implemented) to verify the `better-auth.session_token` cookie against the `session` table.
