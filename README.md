# MailPilot AI — Multi-User SaaS Platform

MailPilot AI is a multi-user SaaS platform for intelligent email management with Google (Gmail) and Microsoft (Outlook) mailboxes.

This repository implements **Phase 1: Foundation and Authentication**.

---

## Architecture & Features (Phase 1)

- **Frontend**: Next.js 14+ App Router, TypeScript (strict mode), Tailwind CSS, Lucide icons.
- **Backend**: FastAPI, SQLAlchemy 2.x (async), Pydantic v2, Alembic, pytest.
- **Database**: PostgreSQL 16 & Neon Serverless PostgreSQL with SSL support.
- **Security & Cryptography**:
  - Validated OIDC provider authentication (RS256 signature, issuer, audience, expiry via JWKS).
  - Server-side authenticated token encryption (`AES-256-GCM` / `Fernet`).
  - Strict tenant isolation (`user_id` enforced on all queries).
  - OAuth 2.0 with PKCE (`S256`) and confidential, HMAC-signed single-use state tokens.
  - Least-privilege read-only scopes: `gmail.readonly` and `Mail.Read`.
  - Disconnect and token revocation.

---

## Monorepo Structure

```
mailplot/
├── apps/
│   └── web/               # Next.js App Router Frontend
├── services/
│   └── api/               # FastAPI Backend & Alembic Migrations
├── infra/
│   └── docker-compose.yml # PostgreSQL 16 container service
├── docs/                  # Architecture, Security, and API specifications
├── .env.example           # Environment template
└── README.md
```

---

## Prerequisites

- **Python**: 3.11+
- **Node.js**: 18+ (Node 20+ recommended)
- **Database**: Neon Serverless PostgreSQL OR Local PostgreSQL via Docker Compose

---

## Database Setup

### Option A: Using Neon Serverless PostgreSQL (Recommended)
1. Sign up / log in to [Neon Console](https://console.neon.tech).
2. Create a project and copy your pooled connection string.
3. Configure your `.env` file:
   ```env
   # Async engine for FastAPI
   DATABASE_URL=postgresql+asyncpg://<username>:<password>@<endpoint-id>.neon.tech/<dbname>?ssl=require

   # Sync engine for Alembic migrations
   SYNC_DATABASE_URL=postgresql://<username>:<password>@<endpoint-id>.neon.tech/<dbname>?sslmode=require
   ```

### Option B: Using Local Docker PostgreSQL
Start the PostgreSQL container:
```bash
docker compose -f infra/docker-compose.yml up -d
```

---

## Backend Setup (services/api)

1. Navigate to the backend directory:
   ```bash
   cd services/api
   ```
2. Activate your virtual environment and install dependencies:
   ```bash
   # Using uv:
   uv pip install -e ".[dev]"
   # Or using standard pip:
   pip install -r requirements.txt
   ```
3. Run database migrations:
   ```bash
   alembic upgrade head
   ```
4. Start the FastAPI development server:
   ```bash
   uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
   ```
   Interactive Swagger API documentation will be available at [http://localhost:8000/docs](http://localhost:8000/docs).

---

## Frontend Setup (apps/web)

1. Navigate to the web app directory:
   ```bash
   cd apps/web
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the Next.js development server:
   ```bash
   npm run dev
   ```
   Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## Running Automated Tests

Run the full pytest suite with 100% tenant isolation, cryptographic encryption, and OAuth flow coverage:

```bash
cd services/api
pytest -v
```

### Coverage Highlights:
- **`test_health.py`**: Health probe and database connectivity checks.
- **`test_auth_jwt.py`**: Valid, expired, tampered, wrong issuer, and wrong audience JWTs.
- **`test_tenant_isolation.py`**: Cross-user access denial and mailbox isolation.
- **`test_encryption.py`**: Authenticated encryption/decryption and tamper detection.
- **`test_pkce_state.py`**: PKCE generation, S256 verification, state replay protection, and expiration.
- **`test_oauth_flow.py`**: Google & Microsoft authorization URLs, code exchange, token refresh failure, and revocation.

---

## Linting & Code Quality

Run Ruff on the backend:
```bash
cd services/api
ruff check .
```

Run TypeScript and Next.js linting on the frontend:
```bash
cd apps/web
npm run lint
```

