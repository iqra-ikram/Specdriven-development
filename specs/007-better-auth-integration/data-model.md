# Data Model: Better Auth

**Feature**: Better Auth Integration (`007-better-auth-integration`)
**Database**: Neon Postgres (Shared)

## Overview

The `better-auth` library manages its own tables. This model defines the schema that `better-auth` will generate and that the Python backend must read to verify sessions.

## Entities

### User (`user`)

The core identity of a user.

| Field | Type | Description |
|-------|------|-------------|
| `id` | TEXT (PK) | Unique ID (UUID/CUID) |
| `name` | TEXT | User's full name |
| `email` | TEXT | User's email address (Unique) |
| `emailVerified` | BOOLEAN | Whether email is verified |
| `image` | TEXT | URL to avatar image (optional) |
| `createdAt` | TIMESTAMP | Creation time |
| `updatedAt` | TIMESTAMP | Last update time |

### Session (`session`)

Represents an active login session.

| Field | Type | Description |
|-------|------|-------------|
| `id` | TEXT (PK) | Unique Session ID |
| `userId` | TEXT (FK) | Reference to `user.id` |
| `token` | TEXT | The session token (used in cookies) |
| `expiresAt` | TIMESTAMP | When the session expires |
| `ipAddress` | TEXT | IP address of the client (optional) |
| `userAgent` | TEXT | User Agent string (optional) |

### Account (`account`)

Linked external accounts (OAuth). *Note: Not strictly used in MVP (Email/Pass) but part of standard schema.*

| Field | Type | Description |
|-------|------|-------------|
| `id` | TEXT (PK) | Unique Account ID |
| `userId` | TEXT (FK) | Reference to `user.id` |
| `accountId` | TEXT | ID from provider |
| `providerId` | TEXT | e.g., "google", "github" |
| `accessToken` | TEXT | OAuth access token |
| `refreshToken` | TEXT | OAuth refresh token |
| `expiresAt` | TIMESTAMP | Token expiration |
| `password` | TEXT | Hashed password (if using email/pass here, or sometimes in `user`) |

*Note: For email/password, `better-auth` typically stores the password hash in the `account` table or `user` table depending on configuration. We assume standard configuration.*

### Verification (`verification`)

Used for email verification tokens, etc.

| Field | Type | Description |
|-------|------|-------------|
| `id` | TEXT (PK) | Unique ID |
| `identifier` | TEXT | Email or other identifier |
| `value` | TEXT | The token value |
| `expiresAt` | TIMESTAMP | Expiration time |

## Relationships

- `User` 1:N `Session`
- `User` 1:N `Account`

## SQL DDL (Reference)

```sql
CREATE TABLE "user" (
    "id" TEXT PRIMARY KEY,
    "name" TEXT NOT NULL,
    "email" TEXT NOT NULL UNIQUE,
    "emailVerified" BOOLEAN NOT NULL,
    "image" TEXT,
    "createdAt" TIMESTAMP NOT NULL,
    "updatedAt" TIMESTAMP NOT NULL
);

CREATE TABLE "session" (
    "id" TEXT PRIMARY KEY,
    "expiresAt" TIMESTAMP NOT NULL,
    "token" TEXT NOT NULL UNIQUE,
    "createdAt" TIMESTAMP NOT NULL,
    "updatedAt" TIMESTAMP NOT NULL,
    "ipAddress" TEXT,
    "userAgent" TEXT,
    "userId" TEXT NOT NULL REFERENCES "user"("id")
);

CREATE TABLE "account" (
    "id" TEXT PRIMARY KEY,
    "accountId" TEXT NOT NULL,
    "providerId" TEXT NOT NULL,
    "userId" TEXT NOT NULL REFERENCES "user"("id"),
    "accessToken" TEXT,
    "refreshToken" TEXT,
    "idToken" TEXT,
    "accessTokenExpiresAt" TIMESTAMP,
    "refreshTokenExpiresAt" TIMESTAMP,
    "scope" TEXT,
    "password" TEXT,
    "createdAt" TIMESTAMP NOT NULL,
    "updatedAt" TIMESTAMP NOT NULL
);

CREATE TABLE "verification" (
    "id" TEXT PRIMARY KEY,
    "identifier" TEXT NOT NULL,
    "value" TEXT NOT NULL,
    "expiresAt" TIMESTAMP NOT NULL,
    "createdAt" TIMESTAMP,
    "updatedAt" TIMESTAMP
);
```
