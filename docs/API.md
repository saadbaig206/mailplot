# MailPilot AI — Core API Reference (Phase 1)

Base URL: `http://localhost:8000`

---

## 1. System Endpoints

### `GET /health`
Probes application health and database connectivity.

**Response (200 OK):**
```json
{
  "status": "ok",
  "environment": "development",
  "database": "healthy",
  "timestamp": "2026-11-07T01:00:00Z"
}
```

---

## 2. User & Authentication Endpoints

### `GET /api/v1/me`
Returns the profile and connected accounts of the authenticated user.

**Headers:**
- `Authorization: Bearer <oidc_access_token>`

**Response (200 OK):**
```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "email": "user@company.com",
  "full_name": "Jane Doe",
  "avatar_url": "https://example.com/avatar.png",
  "is_active": true,
  "created_at": "2026-11-07T01:00:00Z",
  "email_accounts": []
}
```

**Errors:**
- `401 Unauthorized`: Token missing, expired, or invalid.

---

## 3. Email Accounts Management

### `GET /api/v1/email-accounts`
Lists all mailboxes connected by the authenticated user (strictly tenant-isolated).

**Headers:**
- `Authorization: Bearer <oidc_access_token>`

**Response (200 OK):**
```json
[
  {
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "provider": "google",
    "email_address": "jane@gmail.com",
    "display_name": "Jane Doe",
    "status": "active",
    "scopes": [
      "openid",
      "https://www.googleapis.com/auth/gmail.readonly"
    ],
    "connected_at": "2026-11-07T01:10:00Z",
    "last_synced_at": null
  }
]
```

### `DELETE /api/v1/email-accounts/{id}`
Disconnects an email account and revokes provider tokens.

**Headers:**
- `Authorization: Bearer <oidc_access_token>`

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Email account successfully disconnected and revoked",
  "email_account_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
```

**Errors:**
- `404 Not Found`: Account does not exist or belongs to another user.

---

## 4. Mailbox OAuth Endpoints

### `GET /api/v1/oauth/{provider}/start`
Initiates OAuth connection with PKCE. Supported providers: `google`, `microsoft`.

**Headers:**
- `Authorization: Bearer <oidc_access_token>`

**Response (200 OK):**
```json
{
  "provider": "google",
  "authorization_url": "https://accounts.google.com/o/oauth2/v2/auth?client_id=...&code_challenge=...&code_challenge_method=S256&state=..."
}
```

### `POST /api/v1/oauth/{provider}/callback`
Finalizes code exchange, validates state & PKCE, and stores encrypted credentials.

**Headers:**
- `Authorization: Bearer <oidc_access_token>`

**Request Body:**
```json
{
  "code": "4/0AX4XfWh8...",
  "state": "gAAAAABl..."
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "account": {
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "provider": "google",
    "email_address": "jane@gmail.com",
    "status": "active",
    "scopes": ["gmail.readonly"],
    "connected_at": "2026-11-07T01:20:00Z"
  },
  "message": "Successfully connected Google account jane@gmail.com"
}
```

