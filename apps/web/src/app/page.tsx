import React from "react";
import Link from "next/link";
import {
  ShieldCheck,
  Lock,
  Mail,
  ArrowRight,
  CheckCircle2,
  Sparkles,
  Inbox,
  Cpu,
  Layers,
  Database,
  KeyRound,
  FileText,
  UserCheck,
} from "lucide-react";
import { Header } from "../components/Header";
import { Footer } from "../components/Footer";

  export default function LandingPage() {
    return (
      <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col selection:bg-indigo-500 selection:text-white">
        <Header />

        <main className="flex-1">
          {/* Hero Section */}
          <section className="relative overflow-hidden pt-20 pb-24 md:pt-32 md:pb-36 border-b border-slate-900">
            <div className="absolute inset-0 bg-[radial-gradient(ellipse_80%_80%_at_50%_-20%,rgba(99,102,241,0.15),rgba(255,255,255,0))] pointer-events-none" />

            <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 text-center relative z-10">
              <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-xs font-semibold mb-8 animate-fade-in">
                <Sparkles className="w-3.5 h-3.5 text-indigo-400" />
                <span>Phase 1 Verified: Foundation, Multi-Tenant Auth & OAuth Connections</span>
              </div>

              <h1 className="text-4xl sm:text-6xl lg:text-7xl font-extrabold tracking-tight text-white max-w-4xl mx-auto leading-[1.1]">
                Intelligent Email Management with <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 via-violet-400 to-pink-400">Zero-Compromise Security</span>
              </h1>

              <p className="mt-6 text-base sm:text-lg text-slate-400 max-w-2xl mx-auto leading-relaxed">
                Connect your Gmail and Outlook mailboxes with least-privilege, read-only permissions. Built from the ground up for strict tenant isolation, authenticated AES-256 token encryption, and human-in-the-loop control.
              </p>

              <div className="mt-10 flex flex-col sm:flex-row items-center justify-center gap-4">
                <Link
                  href="/dashboard"
                  className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-7 py-3.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-sm shadow-xl shadow-indigo-600/25 transition-all hover:scale-[1.02]"
                >
                  <span>Launch MailPilot Dashboard</span>
                  <ArrowRight className="w-4 h-4" />
                </Link>
                <Link
                  href="/#security"
                  className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-7 py-3.5 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-200 font-medium text-sm transition-colors"
                >
                  <ShieldCheck className="w-4 h-4 text-emerald-400" />
                  <span>Security Architecture</span>
                </Link>
              </div>

              {/* Trust Badges Bar */}
              <div className="mt-16 pt-8 border-t border-slate-900 grid grid-cols-2 sm:grid-cols-4 gap-6 max-w-4xl mx-auto text-left">
                <div className="flex items-start gap-3">
                  <CheckCircle2 className="w-5 h-5 text-indigo-400 shrink-0 mt-0.5" />
                  <div>
                    <h4 className="text-xs font-semibold text-white">Read-Only Scopes</h4>
                    <p className="text-[11px] text-slate-500">gmail.readonly & Mail.Read</p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <Lock className="w-5 h-5 text-emerald-400 shrink-0 mt-0.5" />
                  <div>
                    <h4 className="text-xs font-semibold text-white">Encrypted Tokens</h4>
                    <p className="text-[11px] text-slate-500">AES-256 authenticated ciphertext</p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <KeyRound className="w-5 h-5 text-violet-400 shrink-0 mt-0.5" />
                  <div>
                    <h4 className="text-xs font-semibold text-white">PKCE & Signed State</h4>
                    <p className="text-[11px] text-slate-500">RFC 7636 replay resistance</p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <UserCheck className="w-5 h-5 text-amber-400 shrink-0 mt-0.5" />
                  <div>
                    <h4 className="text-xs font-semibold text-white">Tenant Isolated</h4>
                    <p className="text-[11px] text-slate-500">Zero cross-tenant leakage</p>
                  </div>
                </div>
              </div>
            </div>
          </section>

                    {/* Features Preview Section */}
                    <section id="features" className="py-20 md:py-28 max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
                      <div className="text-center max-w-3xl mx-auto mb-16">
                        <h2 className="text-xs uppercase font-bold tracking-widest text-indigo-400 mb-3">Product Roadmap</h2>
                        <h3 className="text-3xl sm:text-4xl font-bold text-white tracking-tight">
                          A Modern SaaS Engine for Email Overload
                        </h3>
                        <p className="mt-4 text-sm text-slate-400">
                          Phase 1 establishes the rock-solid authentication and OAuth foundation. Subsequent phases introduce real-time processing and AI-assisted workflows.
                        </p>
                      </div>

                        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                          {/* Feature 1 */}
                          <div className="p-8 rounded-2xl border border-slate-800/80 bg-slate-900/40 hover:border-slate-700 transition-all flex flex-col justify-between">
                            <div>
                              <div className="w-12 h-12 rounded-xl bg-indigo-500/10 text-indigo-400 flex items-center justify-center mb-6 border border-indigo-500/20">
                                <Inbox className="w-6 h-6" />
                              </div>
                              <div className="flex items-center gap-2 mb-2">
                                <h4 className="text-base font-semibold text-white">Multi-Provider OAuth</h4>
                                <span className="text-[10px] font-semibold px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">Phase 1 Active</span>
                              </div>
                              <p className="text-xs text-slate-400 leading-relaxed">
                                Connect personal or enterprise Google Workspace and Microsoft 365 Outlook accounts side-by-side using official OAuth 2.0 with PKCE.
                              </p>
                            </div>
                            <div className="mt-6 pt-4 border-t border-slate-800 text-[11px] text-slate-500">
                              Supports multiple accounts per user with single-click revocation.
                            </div>
                          </div>

                              {/* Feature 2 */}
                              <div className="p-8 rounded-2xl border border-slate-800/80 bg-slate-900/40 hover:border-slate-700 transition-all flex flex-col justify-between">
                                <div>
                                  <div className="w-12 h-12 rounded-xl bg-violet-500/10 text-violet-400 flex items-center justify-center mb-6 border border-violet-500/20">
                                    <Cpu className="w-6 h-6" />
                                  </div>
                                  <div className="flex items-center gap-2 mb-2">
                                    <h4 className="text-base font-semibold text-white">AI Urgency & Triage</h4>
                                    <span className="text-[10px] font-semibold px-2 py-0.5 rounded bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">Phase 2 Planned</span>
                                  </div>
                                  <p className="text-xs text-slate-400 leading-relaxed">
                                    Automatic classification of incoming mail into urgent, important, and promotional categories so executives never miss critical customer correspondence.
                                  </p>
                                </div>
                                <div className="mt-6 pt-4 border-t border-slate-800 text-[11px] text-slate-500">
                                  Zero automated sending without explicit human review.
                                </div>
                              </div>

                                {/* Feature 3 */}
                                <div className="p-8 rounded-2xl border border-slate-800/80 bg-slate-900/40 hover:border-slate-700 transition-all flex flex-col justify-between">
                                  <div>
                                    <div className="w-12 h-12 rounded-xl bg-pink-500/10 text-pink-400 flex items-center justify-center mb-6 border border-pink-500/20">
                                      <Layers className="w-6 h-6" />
                                    </div>
                                      <div className="flex items-center gap-2 mb-2">
                                        <h4 className="text-base font-semibold text-white">Contextual Drafts</h4>
                                        <span className="text-[10px] font-semibold px-2 py-0.5 rounded bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">Phase 2 Planned</span>
                                      </div>
                                      <p className="text-xs text-slate-400 leading-relaxed">
                                        Generate context-aware reply drafts matching your tone and organizational knowledge. Accept spoken audio instructions and approve before sending.
                                      </p>
                                    </div>
                                      <div className="mt-6 pt-4 border-t border-slate-800 text-[11px] text-slate-500">
                                        No email bodies stored or persisted in Phase 1.
                                      </div>
                                    </div>
                                  </div>
                                </section>

                                      {/* Security Deep Dive Section */}
                                      <section id="security" className="py-20 md:py-28 bg-slate-900/30 border-y border-slate-900">
                                        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
                                          <div className="text-center max-w-3xl mx-auto mb-16">
                                            <h2 className="text-xs uppercase font-bold tracking-widest text-emerald-400 mb-3">Enterprise Grade Security</h2>
                                            <h3 className="text-3xl sm:text-4xl font-bold text-white tracking-tight">
                                              Architected For Maximum Confidentiality
                                            </h3>
                                            <p className="mt-4 text-sm text-slate-400">
                                              We designed MailPilot AI to exceed security best practices from day one. You own your data, and credentials never sit unprotected in memory or storage.
                                            </p>
                                          </div>

                                          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                                            <div className="p-8 rounded-2xl border border-slate-800 bg-slate-950/70 space-y-4">
                                              <div className="flex items-center gap-3">
                                                <div className="w-10 h-10 rounded-lg bg-emerald-500/10 text-emerald-400 flex items-center justify-center border border-emerald-500/20">
                                                  <Lock className="w-5 h-5" />
                                                </div>
                                                <div>
                                                  <h4 className="text-sm font-semibold text-white">Authenticated Token Encryption at Rest</h4>
                                                  <p className="text-xs text-slate-400">AES-256-GCM / Fernet Cryptography</p>
                                                </div>
                                              </div>
                                                <p className="text-xs text-slate-400 leading-relaxed">
                                                  OAuth access and refresh tokens are encrypted using an authenticated symmetric key before persistence. A database compromise yields only undecryptable ciphertext. Tokens are never logged and never exposed in client API responses.
                                                </p>
                                            </div>

                                              <div className="p-8 rounded-2xl border border-slate-800 bg-slate-950/70 space-y-4">
                                                <div className="flex items-center gap-3">
                                                  <div className="w-10 h-10 rounded-lg bg-indigo-500/10 text-indigo-400 flex items-center justify-center border border-indigo-500/20">
                                                    <ShieldCheck className="w-5 h-5" />
                                                  </div>
                                                  <div>
                                                    <h4 className="text-sm font-semibold text-white">Single-Use Signed State & PKCE</h4>
                                                    <p className="text-xs text-slate-400">RFC 7636 S256 Challenge & Anti-CSRF</p>
                                                  </div>
                                                </div>
                                                <p className="text-xs text-slate-400 leading-relaxed">
                                                  Every OAuth initiation generates high-entropy code verifiers and SHA-256 challenge digests. OAuth state tokens are signed, encrypted, and bound to the authenticated user ID with a strict 10-minute expiration and anti-replay protection.
                                                </p>
                                              </div>

                                                  <div className="p-8 rounded-2xl border border-slate-800 bg-slate-950/70 space-y-4">
                                                    <div className="flex items-center gap-3">
                                                      <div className="w-10 h-10 rounded-lg bg-violet-500/10 text-violet-400 flex items-center justify-center border border-violet-500/20">
                                                        <FileText className="w-5 h-5" />
                                                      </div>
                                                      <div>
                                                        <h4 className="text-sm font-semibold text-white">Google & Microsoft Least Privilege</h4>
                                                        <p className="text-xs text-slate-400">Strict Read-Only Permission Bounds</p>
                                                      </div>
                                                    </div>
                                                    <p className="text-xs text-slate-400 leading-relaxed">
                                                      MailPilot AI requests only the bare minimum read scopes required: <code className="text-indigo-300">gmail.readonly</code> for Gmail and <code className="text-indigo-300">Mail.Read</code> for Outlook. No write, modify, or send permissions are requested in Phase 1.
                                                    </p>
                                                  </div>

                                                        <div className="p-8 rounded-2xl border border-slate-800 bg-slate-950/70 space-y-4">
                                                          <div className="flex items-center gap-3">
                                                            <div className="w-10 h-10 rounded-lg bg-pink-500/10 text-pink-400 flex items-center justify-center border border-pink-500/20">
                                                              <Database className="w-5 h-5" />
                                                            </div>
                                                            <div>
                                                              <h4 className="text-sm font-semibold text-white">Tenant Isolation & Immediate Revocation</h4>
                                                              <p className="text-xs text-slate-400">Zero-Trust Identity Derivation</p>
                                                            </div>
                                                          </div>
                                                          <p className="text-xs text-slate-400 leading-relaxed">
                                                            All database queries enforce user tenancy derived strictly from validated JWT claims. Users can disconnect mailboxes at any time, which invalidates tokens with provider revocation endpoints and purges local credentials.
                                                          </p>
                                                        </div>
                                                      </div>
                                                    </div>
                                                  </section>

                                                  {/* How It Works Section */}
                                                  <section id="how-it-works" className="py-20 md:py-28 max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
                                                    <div className="text-center max-w-3xl mx-auto mb-16">
                                                      <h2 className="text-xs uppercase font-bold tracking-widest text-indigo-400 mb-3">Workflow</h2>
                                                      <h3 className="text-3xl sm:text-4xl font-bold text-white tracking-tight">
                                                        Simple, Safe & Transparent
                                                      </h3>
                                                      <p className="mt-4 text-sm text-slate-400">
                                                        Three steps to a clean, prioritized, AI-assisted inbox.
                                                      </p>
                                                    </div>

                                                    <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                                                      <div className="text-center space-y-4 p-6 rounded-2xl bg-slate-900/30 border border-slate-800/80">
                                                        <div className="w-12 h-12 rounded-full bg-indigo-600/20 text-indigo-400 flex items-center justify-center mx-auto text-lg font-bold border border-indigo-500/30">
                                                          1
                                                        </div>
                                                        <h4 className="text-base font-semibold text-white">Connect Your Mailbox</h4>
                                                        <p className="text-xs text-slate-400">
                                                          Sign in with Google or Microsoft through secure OAuth 2.0 with PKCE. We never see your password.
                                                        </p>
                                                      </div>

                                                    <div className="text-center space-y-4 p-6 rounded-2xl bg-slate-900/30 border border-slate-800/80">
                                                      <div className="w-12 h-12 rounded-full bg-violet-600/20 text-violet-400 flex items-center justify-center mx-auto text-lg font-bold border border-violet-500/30">
                                                        2
                                                      </div>
                                                      <h4 className="text-base font-semibold text-white">Triage & Summary</h4>
                                                      <p className="text-xs text-slate-400">
                                                        Read-only analysis prioritizes urgent emails and extracts actionable takeaways without human inbox fatigue.
                                                      </p>
                                                    </div>

                                                    <div className="text-center space-y-4 p-6 rounded-2xl bg-slate-900/30 border border-slate-800/80">
                                                      <div className="w-12 h-12 rounded-full bg-pink-600/20 text-pink-400 flex items-center justify-center mx-auto text-lg font-bold border border-pink-500/30">
                                                        3
                                                      </div>
                                                      <h4 className="text-base font-semibold text-white">Review & Approve</h4>
                                                      <p className="text-xs text-slate-400">
                                                        Review suggested replies or spoken directives. Nothing is sent without your explicit click and approval.
                                                      </p>
                                                    </div>
                                                </div>
                                              </section>

                                              {/* Final CTA */}
                                              <section className="py-20 bg-gradient-to-b from-slate-950 via-indigo-950/30 to-slate-950 border-t border-slate-900 text-center">
                                                <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
                                                  <h3 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
                                                    Ready to Upgrade Your Email Workflow?
                                                  </h3>
                                                  <p className="mt-4 text-sm text-slate-400 max-w-xl mx-auto">
                                                    Access the Phase 1 dashboard to connect and manage your Gmail and Outlook accounts with enterprise-level security.
                                                  </p>
                                                  <div className="mt-8 flex justify-center">
                                                    <Link
                                                      href="/dashboard"
                                                      className="inline-flex items-center gap-2 px-8 py-3.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-sm shadow-xl shadow-indigo-600/30 transition-all hover:scale-105"
                                                    >
                                                      <span>Launch MailPilot Dashboard</span>
                                                      <ArrowRight className="w-4 h-4" />
                                                    </Link>
                                                  </div>
                                                </div>
                                              </section>
                                            </main>

                                            <Footer />
                                          </div>
                                          );
}
