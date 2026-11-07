"use client";

import React, { useState } from "react";
import { Loader2 } from "lucide-react";
import { startOAuth } from "../lib/api";

interface Props {
  provider: "google" | "microsoft";
  token: string;
}

export const ConnectButton: React.FC<Props> = ({ provider, token }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const isGoogle = provider === "google";

  const handleConnect = async () => {
    setLoading(true);
    setError(null);
    try {
      const resp = await startOAuth(provider, token);
      if (resp && resp.authorization_url) {
        window.location.href = resp.authorization_url;
      }
    } catch (err: any) {
      setError(err?.message || `Failed to initiate ${provider} connection`);
      setLoading(false);
    }
  };

  return (
    <div>
      <button
        onClick={handleConnect}
        disabled={loading}
        className={`w-full flex items-center justify-center gap-2.5 px-4 py-2.5 rounded-xl font-medium text-sm transition-all shadow-sm ${
          isGoogle
            ? "bg-white hover:bg-slate-100 text-slate-900 border border-slate-200"
            : "bg-[#0078d4] hover:bg-[#006cbd] text-white"
        } disabled:opacity-60 disabled:cursor-not-allowed`}
      >
        {loading ? (
          <Loader2 className="w-4 h-4 animate-spin" />
        ) : isGoogle ? (
          <svg className="w-4 h-4" viewBox="0 0 24 24">
            <path
              fill="#4285F4"
              d="M23.745 12.27c0-.7-.06-1.4-.19-2.07H12v4.51h6.6c-.29 1.52-1.14 2.82-2.4 3.68v3.05h3.88c2.27-2.09 3.665-5.17 3.665-9.17z"
            />
            <path
              fill="#34A853"
              d="M12 24c3.24 0 5.95-1.08 7.93-2.91l-3.88-3.05c-1.08.72-2.45 1.16-4.05 1.16-3.12 0-5.77-2.1-6.72-4.93H1.25v3.15C3.26 21.36 7.33 24 12 24z"
            />
            <path
              fill="#FBBC05"
              d="M5.28 14.27c-.25-.72-.38-1.49-.38-2.27s.13-1.55.38-2.27V6.58H1.25C.45 8.18 0 9.99 0 12s.45 3.82 1.25 5.42l4.03-3.15z"
            />
            <path
              fill="#EA4335"
              d="M12 4.75c1.77 0 3.35.61 4.6 1.8l3.42-3.42C17.95 1.19 15.24 0 12 0 7.33 0 3.26 2.64 1.25 6.58l4.03 3.15c.95-2.83 3.6-4.98 6.72-4.98z"
            />
          </svg>
        ) : (
          <svg className="w-4 h-4 fill-current" viewBox="0 0 24 24">
            <path d="M11.55 21H3v-8.55h8.55V21zM21 21h-8.55v-8.55H21V21zm-9.45-9.45H3V3h8.55v8.55zm9.45 0h-8.55V3H21v8.55z" />
          </svg>
        )}
        <span>Connect {isGoogle ? "Gmail" : "Outlook"}</span>
      </button>

      {error && (
        <p className="text-[11px] text-rose-400 mt-1.5 text-center">{error}</p>
      )}
    </div>
  );
};

