import { DisconnectResponse, EmailAccount, OAuthStartResponse, User } from "../types";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export class ApiError extends Error {
  status: number;
  constructor(message: string, status: number) {
    super(message);
    this.status = status;
    this.name = "ApiError";
  }
}

async function request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const url = `${API_BASE}${endpoint}`;
  const response = await fetch(url, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
  });

  if (!response.ok) {
    let errorDetail = "API request failed";
    try {
      const errorJson = await response.json();
      errorDetail = errorJson.detail || errorDetail;
    } catch {
      errorDetail = await response.text();
    }
    throw new ApiError(errorDetail, response.status);
  }

  return response.json() as Promise<T>;
}

export async function fetchMe(token: string): Promise<User> {
  return request<User>("/api/v1/me", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
}

export async function fetchEmailAccounts(token: string): Promise<EmailAccount[]> {
  return request<EmailAccount[]>("/api/v1/email-accounts", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
}

export async function startOAuth(
  provider: "google" | "microsoft",
  token: string
): Promise<OAuthStartResponse> {
  return request<OAuthStartResponse>(`/api/v1/oauth/${provider}/start`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
}

export async function disconnectEmailAccount(
  accountId: string,
  token: string
): Promise<DisconnectResponse> {
  return request<DisconnectResponse>(`/api/v1/email-accounts/${accountId}`, {
    method: "DELETE",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
}

