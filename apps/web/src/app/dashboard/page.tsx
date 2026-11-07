"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import {
  KeyRound,
  RefreshCw,
  AlertCircle,
  Mail,
  CheckCircle2,
  Lock,
  Layers,
  ArrowLeft,
} from "lucide-react";
import { Navbar } from "../../components/Navbar";
import { ConnectedAccountsList } from "../../components/ConnectedAccountsList";
import { ConnectButton } from "../../components/ConnectButton";
import { disconnectEmailAccount, fetchEmailAccounts, fetchMe } from "../../lib/api";
import { EmailAccount, User } from "../../types";

export default function DashboardPage() {
  const [token, setToken] = useState<string>("");
  const [user, setUser] = useState<User | null>(null);
  const [accounts, setAccounts] = useState<EmailAccount[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [tokenInput, setTokenInput] = useState<string>("");

  // Load token from localStorage on mount
  useEffect(() => {
    const saved = localStorage.getItem("mailpilot_jwt");
    if (saved) {
      setToken(saved);
      loadUserData(saved);
    }
  }, []);

  const loadUserData = async (activeToken: string) => {
    setLoading(true);
    setError(null);
    try {
      const userData = await fetchMe(activeToken);
      setUser(userData);
      const accountsData = await fetchEmailAccounts(activeToken);
      setAccounts(accountsData);
    } catch (err: any) {
      setError(err?.message || "Failed to authenticate with backend API");
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  const handleApplyToken = (newToken: string) => {
    if (!newToken.trim()) return;
    localStorage.setItem("mailpilot_jwt", newToken.trim());
    setToken(newToken.trim());
    loadUserData(newToken.trim());
  };

  const handleLogout = () => {
    localStorage.removeItem("mailpilot_jwt");
    setToken("");
    setUser(null);
    setAccounts([]);
  };

  const handleDisconnect = async (accountId: string) => {
    if (!token) return;
    await disconnectEmailAccount(accountId, token);
    // Refresh accounts list
    const updated = await fetchEmailAccounts(token);
    setAccounts(updated);
  };

  return (
    <div className="min-h-screen bg-slate-950 flex flex-col">
      <Navbar user={user} onLogout={handleLogout} />

      <main className="flex-1 max-w-6xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
        <div className="flex items-center justify-between">
          <Link
            href="/"
            className="inline-flex items-center gap-1.5 text-xs text-slate-400 hover:text-white transition-colors"
          >
            <ArrowLeft className="w-3.5 h-3.5" />
            <span>Back to Home</span>
          </Link>
          <div className="flex items-center gap-3 text-xs text-slate-400">
            <Link href="/privacy" className="hover:text-slate-200">
              Privacy Policy
            </Link>
            <span>&bull;</span>
            <Link href="/terms" className="hover:text-slate-200">
              Terms of Service
            </Link>
          </div>
        </div>

        {/* Authentication Panel */}
        {!user ? (
          <div className="max-w-xl mx-auto my-12 p-8 rounded-2xl border border-slate-800 bg-slate-900/80 shadow-2xl backdrop-blur-xl">
            <div className="w-12 h-12 rounded-xl bg-indigo-600/20 text-indigo-400 flex items-center justify-center mb-4 border border-indigo-500/20">
              <KeyRound className="w-6 h-6" />
            </div>
            <h2 className="text-xl font-bold text-white mb-2">Application Sign-In</h2>
            <p className="text-sm text-slate-400 mb-6">
              Phase 1 authenticates via your managed OIDC Identity Provider. Provide your Bearer access token to access the dashboard.
            </p>

            <div className="space-y-4">
              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1.5">
                  OIDC Bearer Access Token
                </label>
                <textarea
                  rows={3}
                  value={tokenInput}
                  onChange={(e) => setTokenInput(e.target.value)}
                  placeholder="eyJhbGciOiJSUzI1NiIsImtpZCI6..."
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs font-mono text-slate-200 placeholder-slate-600 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>

              {error && (
                <div className="p-3 rounded-lg bg-rose-500/10 border border-rose-500/20 flex items-center gap-2 text-xs text-rose-400">
                  <AlertCircle className="w-4 h-4 shrink-0" />
                  <span>{error}</span>
                </div>
              )}

              <button
                onClick={() => handleApplyToken(tokenInput)}
                disabled={!tokenInput.trim() || loading}
                className="w-full py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-medium text-sm transition-all shadow-lg shadow-indigo-600/20 disabled:opacity-50"
              >
                {loading ? "Validating Token with Backend..." : "Authenticate & Continue"}
              </button>
            </div>
          </div>
        ) : (
          <>
            {/* User Profile Banner */}
            <div className="p-6 rounded-2xl border border-slate-800 bg-slate-900/60 backdrop-blur-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div className="flex items-center gap-4">
                <div className="w-14 h-14 rounded-2xl bg-indigo-600/20 text-indigo-400 flex items-center justify-center border border-indigo-500/30 text-xl font-bold">
                  {user.email.charAt(0).toUpperCase()}
                </div>
                <div>
                  <h1 className="text-lg font-bold text-white">
                    {user.full_name || "Authorized User"}
                  </h1>
                  <p className="text-xs text-slate-400 font-mono">{user.email}</p>
                  <div className="flex items-center gap-2 mt-1.5">
                    <span className="inline-flex items-center gap-1 text-[11px] font-medium text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-2 py-0.5 rounded-full">
                      <CheckCircle2 className="w-3 h-3" />
                      Tenant Verified
                    </span>
                    <span className="text-[11px] text-slate-500">
                      ID: {user.id.substring(0, 8)}...
                    </span>
                  </div>
                </div>
              </div>

              <div className="flex items-center gap-2 self-start md:self-center">
                <button
                  onClick={() => loadUserData(token)}
                  className="inline-flex items-center gap-1.5 text-xs text-slate-400 hover:text-slate-200 bg-slate-800 hover:bg-slate-700 border border-slate-700 px-3 py-2 rounded-lg transition-colors"
                >
                  <RefreshCw className={`w-3.5 h-3.5 ${loading ? "animate-spin" : ""}`} />
                  <span>Sync Accounts</span>
                </button>
              </div>
            </div>

            {/* Mailbox Connection Controls */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {/* Connect Actions Card */}
              <div className="p-6 rounded-2xl border border-slate-800 bg-slate-900/60 space-y-4">
                <div className="flex items-center gap-2 text-white font-semibold text-sm">
                  <Mail className="w-4 h-4 text-indigo-400" />
                  <h3>Connect Mailbox</h3>
                </div>
                <p className="text-xs text-slate-400">
                  Connect email accounts via official OAuth 2.0 with PKCE and encrypted token storage.
                </p>

                <div className="space-y-3 pt-2">
                  <ConnectButton provider="google" token={token} />
                  <ConnectButton provider="microsoft" token={token} />
                </div>

                <div className="pt-4 border-t border-slate-800/80 space-y-2">
                  <div className="flex items-center gap-1.5 text-[11px] font-medium text-slate-400">
                    <Lock className="w-3.5 h-3.5 text-slate-500" />
                    <span>Security Blueprint</span>
                  </div>
                  <ul className="text-[10px] text-slate-500 space-y-1 list-disc list-inside">
                    <li>Read-only scopes: <code className="text-slate-400">gmail.readonly</code> & <code className="text-slate-400">Mail.Read</code></li>
                    <li>S256 PKCE Code Challenge</li>
                    <li>Tokens encrypted with AES-256-GCM / Fernet</li>
                    <li>Never exposed to browser</li>
                  </ul>
                </div>
              </div>

              {/* Connected Accounts Section */}
              <div className="md:col-span-2 p-6 rounded-2xl border border-slate-800 bg-slate-900/60 space-y-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2 text-white font-semibold text-sm">
                    <Layers className="w-4 h-4 text-indigo-400" />
                    <h3>Connected Email Accounts ({accounts.length})</h3>
                  </div>
                  <span className="text-xs text-slate-400">Tenant Isolated</span>
                </div>

                <ConnectedAccountsList
                  accounts={accounts}
                  onDisconnect={handleDisconnect}
                />
              </div>
            </div>
          </>
        )}
      </main>

      <footer className="border-t border-slate-900 py-6 text-center text-xs text-slate-600">
        MailPilot AI &mdash; Phase 1: Foundation and Authentication &bull; Neon Serverless PostgreSQL Ready
      </footer>
    </div>
  );
}

