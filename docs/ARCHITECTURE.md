# MailPilot AI — Architecture Specification (Phase 1)

## 1. System Overview

MailPilot AI is a multi-user SaaS platform for intelligent email management. Phase 1 provides the foundational layer:
- Modern Monorepo (`apps/web`, `services/api`, `infra`, `docs`)
- Multi-tenant relational data models (PostgreSQL / Neon DB) with SQLAlchemy 2.x and Alembic
- Application authentication via managed OIDC provider (with RS256 JWKS validation)
- Secure mailbox OAuth architecture (Google Gmail and Microsoft Outlook) using PKCE and authenticated symmetric token encryption

```
┌────────────────────────────────────────────────────────────────────────┐
│                          Next.js App Router                            │
│           (Dashboard, Connection Management, Tailwind CSS)             │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │ HTTPS / JSON API
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│                          FastAPI Core Backend                          │
│                                                                        │
│  ┌───────────────────────┐  ┌───────────────────────────────────────┐  │
│  │   Managed OIDC Auth   │  │           OAuth Adapters              │  │
│  │  (JWKS Caching, RS256 │  │    (PKCE S256, HMAC Signed State,     │  │
│  │   Token Validation)   │  │   Least-Privilege Scopes, Revoke)     │  │
│  └───────────┬───────────┘  └───────────────────┬───────────────────┘  │
│              │                                  │                      │
│              ▼                                  ▼                      │
│  ┌───────────────────────┐  ┌───────────────────────────────────────┐  │
│  │   User Resolution     │  │      Authenticated Token Storage      │  │
│  │ (Derived from claims) │  │         (AES-256-GCM / Fernet)        │  │
│  └───────────┬───────────┘  └───────────────────┬───────────────────┘  │
│              │                                  │                      │
│              └─────────────────┬────────────────┘                      │
│                                │ SQLAlchemy 2.x (Async)                │
└────────────────────────────────┼───────────────────────────────────────┘
                                 │
                                 ▼
┌────────────────────────────────────────────────────────────────────────┐
│             PostgreSQL 16 / Neon Serverless PostgreSQL                 │
│         (users, email_accounts, oauth_connections, audit_events)       │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Database Schema & Data Models

### 2.1 Entity Relationships
- **`users`**: Represents the platform identity derived from the OIDC `sub` claim.
- **`email_accounts`**: Stores connected user mailboxes (Gmail or Outlook). Foreign key `user_id` cascades on deletion.
- **`oauth_connections`**: Holds encrypted OAuth access and refresh tokens. 1-to-1 relationship with `email_accounts` with cascade deletion.
- **`audit_events`**: Immutable security audit log tracking logins, token exchanges, state failures, and disconnects. `user_id` is set to `NULL` upon user deletion to retain compliance history.

### 2.2 Database Support (PostgreSQL & Neon Serverless Postgres)
- Uses `asyncpg` for high-throughput asynchronous execution with SQLAlchemy 2.x.
- Fully compatible with Neon DB (`?ssl=require` and SSL context support built into `services/api/src/database.py`).
- Automatic GUID type adapter supports native PostgreSQL `UUID` as well as string UUIDs.

---

## 3. Application Authentication

- **Provider**: Any compliant OpenID Connect (OIDC) identity provider (Auth0, Clerk, AWS Cognito, etc.).
- **Validation**:
  1. Token extracted from `Authorization: Bearer <token>`.
  2. Public keys fetched and cached from `{OIDC_JWKS_URI}`.
  3. Signature verified with `RS256`.
  4. Mandatory claims verified: `exp` (expiry), `iss` (issuer), `aud` (audience), `sub` (subject).
  5. User automatically resolved or provisioned in local `users` table.

---

## 4. OAuth Mailbox Integration Architecture

### 4.1 Least-Privilege Scopes (Read-Only)
- **Google Gmail**:
  - `openid`
  - `https://www.googleapis.com/auth/userinfo.email`
  - `https://www.googleapis.com/auth/userinfo.profile`
  - `https://www.googleapis.com/auth/gmail.readonly`
- **Microsoft Outlook**:
  - `openid`
  - `profile`
  - `email`
  - `offline_access`
  - `Mail.Read`

### 4.2 PKCE & State Security Handshake
1. **PKCE**: Backend generates a high-entropy 64-character unreserved code verifier and computes its SHA-256 base64url challenge (`S256`).
2. **Confidential State**: State token is generated as an encrypted, authenticated JSON payload storing `state_id`, `user_id`, `provider`, `code_verifier`, and `exp` (10-minute TTL).
3. **Replay & Tamper Detection**: Verified on callback. Consumed states are cached to reject replay attacks.
4. **Token Encryption**: Access tokens and refresh tokens are encrypted at rest using authenticated symmetric encryption (`Fernet` / `AES-256-GCM`). Raw tokens are never logged or exposed to the client.

