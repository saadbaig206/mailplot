# MailPilot AI — Security Architecture & Threat Model (Phase 1)

## 1. Security Principles

MailPilot AI enforces a defense-in-depth posture:
1. **Zero-Trust Client Identity**: Endpoints never trust a user ID or tenant identifier supplied by the browser. All identities are derived from cryptographically verified authentication claims.
2. **Authenticated Encryption at Rest**: Provider tokens (OAuth access & refresh) are never stored in plaintext. They are encrypted using authenticated cryptography before hitting the database.
3. **Least Privilege**: Mailbox permissions in Phase 1 request read-only access only (`gmail.readonly` and `Mail.Read`).
4. **Mandatory PKCE**: Proof Key for Code Exchange (RFC 7636) with SHA-256 (`S256`) is enforced on both Google and Microsoft OAuth flows.
5. **State Confidentiality & Replay Protection**: OAuth `state` is single-use, time-limited, and cryptographically protected.
6. **Auditing**: All security events (logins, account links, revocation, disconnects, failures) are logged to `audit_events`.

---

## 2. Threat Modeling & Mitigations

| Threat | Risk | Mitigation |
|---|---|---|
| **Database Compromise (Token Leakage)** | High | Tokens are encrypted with a 32-byte secret key using authenticated symmetric encryption (`Fernet` / `AES-256-GCM`). A stolen database dump contains only ciphertext. |
| **CSRF / Authorization Code Injection** | High | Single-use, time-limited, authenticated `state` parameter bound to the initiating user's ID. Mismatched or replayed states reject with HTTP 400. |
| **Authorization Code Interception** | High | PKCE with `code_challenge_method=S256`. The authorization server will not issue tokens without the original high-entropy `code_verifier`. |
| **Cross-Tenant Account Access** | Critical | Every query enforces `WHERE email_accounts.user_id = current_user.id`. User B attempting to view, modify, or disconnect User A's mailbox receives HTTP 404. |
| **Open Redirect Vulnerability** | Medium | Redirect URIs are strictly validated against registered endpoints. The browser callback redirects to configured, domain-whitelisted origin paths. |
| **Token Exposure in API Responses** | High | Response schemas explicitly exclude `encrypted_access_token` and `encrypted_refresh_token`. Only non-sensitive metadata (email, provider, status, scopes) is serialized. |
| **JWT Spoofing / Tampering** | Critical | RS256 signature verification against managed OIDC JWKS. Rejects unsigned, HS256 (in prod), or expired tokens. |

---

## 3. Disconnect & Revocation

When a user disconnects an email account via `DELETE /api/v1/email-accounts/{id}`:
1. Ownership is strictly verified against `current_user.id`.
2. The encrypted refresh or access token is decrypted server-side.
3. A revocation request is dispatched to the provider's revocation endpoint (`oauth2.googleapis.com/revoke` for Google).
4. The database record is deleted (which cascades to `oauth_connections`).
5. An audit event `oauth.disconnected` is recorded.

