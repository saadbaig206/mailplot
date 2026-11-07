"use client";

import React, { Suspense, useEffect, useState } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import { CheckCircle2, AlertCircle, Loader2 } from "lucide-react";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

function OAuthCallbackContent() {
  const searchParams = useSearchParams();
  const router = useRouter();

  const [status, setStatus] = useState<"processing" | "success" | "error">("processing");
  const [message, setMessage] = useState<string>("Finalizing secure OAuth connection...");

  useEffect(() => {
    const code = searchParams.get("code");
    const state = searchParams.get("state");
    const provider = searchParams.get("provider") || "google";
    const errorParam = searchParams.get("error");

    if (errorParam) {
      setStatus("error");
      setMessage(`OAuth authorization rejected: ${errorParam}`);
      return;
    }

    if (!code || !state) {
      setStatus("error");
      setMessage("Missing authorization code or state parameter.");
      return;
    }

    const token = localStorage.getItem("mailpilot_jwt");
    if (!token) {
      setStatus("error");
      setMessage("Missing active application session token. Please sign in to MailPilot first.");
      return;
    }

    async function completeOAuth() {
      try {
        const resp = await fetch(`${API_BASE}/api/v1/oauth/${provider}/callback`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({ code, state }),
        });

        const data = await resp.json();
        if (!resp.ok) {
          throw new Error(data.detail || "Failed to finalize OAuth connection");
        }

        setStatus("success");
        setMessage(data.message || `Successfully connected your ${provider} account!`);
        setTimeout(() => {
          router.push("/dashboard");
        }, 2000);
      } catch (err: any) {
        setStatus("error");
        setMessage(err.message || "An unexpected error occurred during OAuth finalization.");
      }
    }

    completeOAuth();
  }, [searchParams, router]);

  return (
    <div className="max-w-md w-full p-8 rounded-2xl border border-slate-800 bg-slate-900/80 shadow-2xl text-center space-y-4">
      {status === "processing" && (
        <div className="space-y-3">
          <Loader2 className="w-10 h-10 text-indigo-400 animate-spin mx-auto" />
          <h2 className="text-base font-semibold text-white">Connecting Mailbox</h2>
          <p className="text-xs text-slate-400">{message}</p>
        </div>
      )}

      {status === "success" && (
        <div className="space-y-3">
          <div className="w-12 h-12 rounded-full bg-emerald-500/10 text-emerald-400 flex items-center justify-center mx-auto border border-emerald-500/20">
            <CheckCircle2 className="w-6 h-6" />
          </div>
          <h2 className="text-base font-semibold text-white">Connection Verified!</h2>
          <p className="text-xs text-slate-400">{message}</p>
          <p className="text-[11px] text-slate-500">Redirecting to dashboard...</p>
        </div>
      )}

      {status === "error" && (
        <div className="space-y-3">
          <div className="w-12 h-12 rounded-full bg-rose-500/10 text-rose-400 flex items-center justify-center mx-auto border border-rose-500/20">
            <AlertCircle className="w-6 h-6" />
          </div>
          <h2 className="text-base font-semibold text-white">Connection Failed</h2>
          <p className="text-xs text-rose-400">{message}</p>
          <button
            onClick={() => router.push("/dashboard")}
            className="mt-4 px-4 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs font-medium text-slate-200 transition-colors"
          >
            Back to Dashboard
          </button>
        </div>
      )}
    </div>
  );
}

export default function OAuthCallbackPage() {
  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center p-4">
      <Suspense
        fallback={
          <div className="p-8 text-center text-slate-400">
            <Loader2 className="w-8 h-8 animate-spin mx-auto mb-2 text-indigo-400" />
            <p className="text-xs">Loading callback...</p>
          </div>
        }
      >
        <OAuthCallbackContent />
      </Suspense>
    </div>
  );
}
