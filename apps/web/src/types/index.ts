export interface EmailAccount {
  id: string;
  provider: "google" | "microsoft";
  email_address: string;
  display_name?: string | null;
  status: "active" | "disconnected" | "expired" | "revoked";
  scopes: string[];
  connected_at: string;
  last_synced_at?: string | null;
}

export interface User {
  id: string;
  email: string;
  full_name?: string | null;
  avatar_url?: string | null;
  is_active: boolean;
  created_at: string;
  email_accounts: EmailAccount[];
}

export interface OAuthStartResponse {
  provider: string;
  authorization_url: string;
}

export interface DisconnectResponse {
  success: boolean;
  message: string;
  email_account_id: string;
}

