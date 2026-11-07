"use client";

import React, { useState } from "react";
import { CheckCircle2, AlertCircle, Trash2, Calendar, Shield, Loader2 } from "lucide-react";
import { EmailAccount } from "@/types";

interface Props {
  accounts: EmailAccount[];
  onDisconnect: (accountId: string) => Promise<void>;
}

export const ConnectedAccountsList: React.FC<Props> = ({ accounts, onDisconnect }) => {
  const [disconnectingId, setDisconnectingId] = useState<string | null>(null);

  const handleDisconnect = async (id: string) => {
    if (!confirm("Are you sure you want to disconnect and revoke this mailbox connection?")) {
      return;
    }
    setDisconnectingId(id);
    try {
      await onDisconnect(id);
    } finally {
      setDisconnectingId(null);
    }
  };

  if (accounts.length === 0) {
    return (
      <div className="border border-dashed border-slate-800 rounded-2xl p-10 text-center bg-slate-900/30">
        <div className="w-12 h-12 rounded-full bg-slate-800 flex items-center justify-center mx-auto mb-3 text-slate-400">
          <Shield className="w-6 h-6" />
        </div>
        <h3 className="text-sm font-medium text-slate-200 mb-1">No mailboxes connected yet</h3>
        <p className="text-xs text-slate-500 max-w-sm mx-auto">
          Connect your Google (Gmail) or Microsoft (Outlook) mailbox below to grant read-only access.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {accounts.map((acc) => {
        const isGoogle = acc.provider === "google";
        const isActive = acc.status === "active";

        return (
          <div
            key={acc.id}
            className="flex flex-col sm:flex-row sm:items-center justify-between p-4 rounded-xl border border-slate-800 bg-slate-900/70 hover:border-slate-700 transition-all gap-4"
          >
            <div className="flex items-start sm:items-center gap-3.5">
              <div
                className={`w-10 h-10 rounded-lg flex items-center justify-center shrink-0 ${
                  isGoogle
                    ? "bg-red-500/10 text-red-400 border border-red-500/20"
                    : "bg-blue-500/10 text-blue-400 border border-blue-500/20"
                }`}
              >
                {isGoogle ? (
                  <svg className="w-5 h-5 fill-current" viewBox="0 0 24 24">
                    <path d="M12.545,10.239v3.821h5.445c-0.712,2.315-2.647,3.972-5.445,3.972c-3.332,0-6.033-2.701-6.033-6.032s2.701-6.032,6.033-6.032c1.498,0,2.866,0.549,3.921,1.453l2.814-2.814C17.503,2.988,15.139,2,12.545,2C7.021,2,2.543,6.477,2.543,12s4.478,10,10.002,10c8.396,0,10.249-7.85,9.426-11.761H12.545z" />
                  </svg>
                ) : (
                  <svg className="w-5 h-5 fill-current" viewBox="0 0 24 24">
                    <path d="M11.55 21H3v-8.55h8.55V21zM21 21h-8.55v-8.55H21V21zm-9.45-9.45H3V3h8.55v8.55zm9.45 0h-8.55V3H21v8.55z" />
                  </svg>
                )}
              </div>

              <div>
                <div className="flex items-center gap-2">
                  <span className="font-medium text-sm text-slate-100">{acc.email_address}</span>
                  <span
                    className={`inline-flex items-center gap-1 text-[11px] font-medium px-2 py-0.5 rounded-full ${
                      isActive
                        ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20"
                        : "bg-slate-700 text-slate-300"
                    }`}
                  >
                    {isActive ? (
                      <CheckCircle2 className="w-3 h-3" />
                    ) : (
                      <AlertCircle className="w-3 h-3" />
                    )}
                    {acc.status}
                  </span>
                </div>

                <div className="flex flex-wrap items-center gap-x-4 gap-y-1 mt-1 text-xs text-slate-400">
                  <span className="capitalize">{acc.provider} mailbox</span>
                  <span className="inline-flex items-center gap-1">
                    <Calendar className="w-3 h-3 text-slate-500" />
                    Connected: {new Date(acc.connected_at).toLocaleDateString()}
                  </span>
                </div>

                {acc.scopes && acc.scopes.length > 0 && (
                  <div className="flex flex-wrap gap-1 mt-2">
                    {acc.scopes.map((scope, idx) => (
                      <span
                        key={idx}
                        className="text-[10px] px-1.5 py-0.5 rounded bg-slate-800 text-slate-400 font-mono"
                      >
                        {scope.split("/").pop()}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            </div>

            <div className="flex items-center sm:self-center">
              <button
                onClick={() => handleDisconnect(acc.id)}
                disabled={disconnectingId === acc.id}
                className="inline-flex items-center gap-1.5 text-xs font-medium text-rose-400/90 hover:text-rose-300 bg-rose-500/10 hover:bg-rose-500/20 border border-rose-500/20 px-3 py-1.5 rounded-lg transition-colors disabled:opacity-50"
              >
                {disconnectingId === acc.id ? (
                  <Loader2 className="w-3.5 h-3.5 animate-spin" />
                ) : (
                  <Trash2 className="w-3.5 h-3.5" />
                )}
                <span>Disconnect</span>
              </button>
            </div>
          </div>
        );
      })}
    </div>
  );
};

