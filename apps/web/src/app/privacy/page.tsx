import React from "react";
import Link from "next/link";
import { Shield, AlertTriangle, ArrowLeft, Mail, Lock, ExternalLink } from "lucide-react";
import { Header } from "../../components/Header";
import { Footer } from "../../components/Footer";

export default function PrivacyPolicyPage() {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col selection:bg-indigo-500 selection:text-white">
      <Header />

      <main className="flex-1 max-w-4xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-12 md:py-20">
        <div className="mb-8">
          <Link
            href="/"
            className="inline-flex items-center gap-1.5 text-xs text-slate-400 hover:text-white transition-colors mb-4"
          >
            <ArrowLeft className="w-3.5 h-3.5" />
            <span>Back to Home</span>
          </Link>
          <div className="flex items-center gap-2 text-indigo-400 text-xs font-semibold mb-2">
            <Shield className="w-4 h-4" />
            <span>Transparency & Trust</span>
          </div>
          <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
            Privacy Policy
          </h1>
          <p className="text-xs text-slate-400 mt-2">
            Last updated: November 7, 2026 &bull; MailPilot AI Phase 1
          </p>
        </div>

        {/* Legal Disclaimer / Operator Confirmation Notice */}
        <div className="p-4 rounded-xl bg-amber-500/10 border border-amber-500/20 text-amber-300 text-xs leading-relaxed space-y-2 mb-10">
          <div className="flex items-center gap-2 font-semibold">
            <AlertTriangle className="w-4 h-4 shrink-0 text-amber-400" />
            <span>Notice: Administrative & Legal Confirmation Required</span>
          </div>
          <p className="text-[11px] text-amber-200/90">
            This Privacy Policy accurately documents the active Phase 1 technical architecture. Sections containing placeholder variables for your legal entity, specific AI model vendors, and privacy contact emails are highlighted with <strong className="text-amber-100 font-mono">[CONFIRMATION REQUIRED]</strong> tags and require your confirmation before public production release.
          </p>
        </div>

        {/* Content Body */}
        <article className="prose prose-invert prose-sm max-w-none space-y-8 text-slate-300 leading-relaxed text-xs sm:text-sm">
          {/* Section 1 */}
          <section className="space-y-3">
            <h2 className="text-base sm:text-lg font-bold text-white border-b border-slate-800 pb-2">
              1. Introduction & Operating Entity
            </h2>
            <p>
              MailPilot AI (&quot;we&quot;, &quot;our&quot;, or &quot;us&quot;) operates the MailPilot AI email management software-as-a-service application. We are committed to safeguarding your privacy and ensuring complete transparency regarding how your email accounts, authentication credentials, and personal information are handled.
            </p>
            <div className="p-3 rounded-lg bg-slate-900 border border-slate-800 font-mono text-xs text-amber-300">
              [CONFIRMATION REQUIRED: Legal Entity Name, Registration Number, and Operating Jurisdiction: e.g., MailPilot AI Inc., Delaware, USA]
            </div>
          </section>

          {/* Section 2 */}
          <section className="space-y-3">
            <h2 className="text-base sm:text-lg font-bold text-white border-b border-slate-800 pb-2">
              2. Information We Collect
            </h2>
            <p>
              MailPilot AI collects only the minimum information necessary to authenticate users and securely connect their authorized mailboxes:
            </p>
            <ul className="list-disc list-inside space-y-1.5 pl-2 text-slate-400">
              <li>
                <strong className="text-slate-200">Application Identity Information:</strong> When you log into MailPilot AI through our managed OpenID Connect (OIDC) provider, we receive your unique subject identifier (<code className="text-indigo-300">sub</code>), primary email address, full name (if provided), and profile picture URL.
              </li>
              <li>
                <strong className="text-slate-200">Connected Mailbox Metadata:</strong> When you connect a Google or Microsoft mailbox, we store the mailbox email address, display name, connection status, and granted permission scopes.
              </li>
              <li>
                <strong className="text-slate-200">Encrypted OAuth Credentials:</strong> We store provider access tokens and refresh tokens. These tokens are encrypted at rest using server-side authenticated symmetric cryptography (AES-256 / Fernet).
              </li>
              <li>
                <strong className="text-slate-200">Security Audit Logs:</strong> We maintain immutable audit records of account logins, connection attempts, state verifications, and disconnections, including timestamps, sanitized event types, and client IP addresses for security monitoring.
              </li>
              <li>
                <strong className="text-slate-200">Email Body Contents in Phase 1:</strong> <span className="text-emerald-400 font-semibold">We do NOT store or persist the body content of your emails in Phase 1.</span>
              </li>
            </ul>
          </section>

          {/* Section 3 */}
          <section className="space-y-3">
            <h2 className="text-base sm:text-lg font-bold text-white border-b border-slate-800 pb-2">
              3. How Gmail and Outlook Data is Accessed and Used
            </h2>
            <p>
              MailPilot AI accesses mailbox data strictly via official OAuth 2.0 application programming interfaces (APIs) provided by Google and Microsoft:
            </p>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 my-3">
              <div className="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-2">
                <h3 className="font-semibold text-white text-xs flex items-center gap-2">
                  <span className="w-2 h-2 rounded-full bg-red-400" />
                  Google (Gmail) Integration
                </h3>
                <p className="text-xs text-slate-400">
                  Requested Scope: <code className="text-indigo-300 font-mono">https://www.googleapis.com/auth/gmail.readonly</code>.
                </p>
                <p className="text-xs text-slate-400">
                  Used solely to read email metadata (headers, subject, sender, date) and message threads to support classification and organization. We do not request permissions to compose, send, delete, or modify emails in Phase 1.
                </p>
              </div>

              <div className="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-2">
                <h3 className="font-semibold text-white text-xs flex items-center gap-2">
                  <span className="w-2 h-2 rounded-full bg-blue-400" />
                  Microsoft (Outlook) Integration
                </h3>
                <p className="text-xs text-slate-400">
                  Requested Scopes: <code className="text-indigo-300 font-mono">Mail.Read</code> and <code className="text-indigo-300 font-mono">offline_access</code>.
                </p>
                <p className="text-xs text-slate-400">
                  Used solely to read mailbox metadata and messages via Microsoft Graph. MailPilot AI does not request mail write or mailbox administrator permissions in Phase 1.
                </p>
              </div>
            </div>

            {/* Google Limited Use Disclosure */}
            <div className="p-4 rounded-xl bg-indigo-950/40 border border-indigo-800/40 space-y-2">
              <h4 className="text-xs font-bold text-indigo-300 flex items-center gap-2">
                <Lock className="w-4 h-4 text-indigo-400" />
                Google API Services User Data Policy Compliance
              </h4>
              <p className="text-xs text-slate-300">
                MailPilot AI&apos;s use and transfer to any other app of information received from Google APIs will adhere to the{" "}
                <a
                  href="https://developers.google.com/terms/api-services-user-data-policy"
                  target="_blank"
                  rel="noreferrer"
                  className="text-indigo-400 underline hover:text-indigo-300 inline-flex items-center gap-1"
                >
                  Google API Services User Data Policy
                  <ExternalLink className="w-3 h-3" />
                </a>
                , including the Limited Use requirements.
              </p>
            </div>
          </section>

          {/* Section 4 */}
          <section className="space-y-3">
            <h2 className="text-base sm:text-lg font-bold text-white border-b border-slate-800 pb-2">
              4. Data Storage, Encryption & Security Architecture
            </h2>
            <p>
              We implement comprehensive defense-in-depth measures to protect your credentials and data:
            </p>
            <ul className="list-disc list-inside space-y-1.5 pl-2 text-slate-400">
              <li>
                <strong className="text-slate-200">Authenticated Symmetric Encryption:</strong> All OAuth access and refresh tokens are encrypted at rest using AES-256 authenticated symmetric encryption (Fernet / AES-256-GCM) with tamper verification. Plaintext tokens are never stored in the database.
              </li>
              <li>
                <strong className="text-slate-200">Zero Token Exposure:</strong> Access and refresh tokens are never exposed to your browser, never serialized in client responses, and never logged in server telemetry.
              </li>
              <li>
                <strong className="text-slate-200">PKCE & Signed State:</strong> All authorization flows enforce RFC 7636 Proof Key for Code Exchange (<code className="text-indigo-300">S256</code>) and HMAC-signed, confidential, single-use state tokens to prevent cross-site request forgery (CSRF) and code interception.
              </li>
              <li>
                <strong className="text-slate-200">Tenant Isolation:</strong> Application data is partitioned per user. Database queries strictly filter by verified authentication claims, preventing cross-tenant access.
              </li>
            </ul>
          </section>

          {/* Section 5 */}
          <section className="space-y-3">
            <h2 className="text-base sm:text-lg font-bold text-white border-b border-slate-800 pb-2">
              5. Artificial Intelligence (AI) Processing & Third-Party Models
            </h2>
            <div className="p-3 rounded-lg bg-emerald-500/10 border border-emerald-500/20 text-emerald-300 text-xs">
              <strong>Phase 1 Operating Reality:</strong> In Phase 1, MailPilot AI implements foundation, authentication, and mailbox connection plumbing only. <span className="underline">No email contents are transmitted to or processed by artificial intelligence models in Phase 1.</span>
            </div>
            <p>
              For future phases introducing AI summarization, triage, and reply drafting, processing will adhere to the following strict criteria:
            </p>
            <ul className="list-disc list-inside space-y-1.5 pl-2 text-slate-400">
              <li>
                <strong className="text-slate-200">No Model Training:</strong> Your email data, metadata, or drafts will never be used to train, retrain, or improve foundational AI models.
              </li>
              <li>
                <strong className="text-slate-200">Human-In-The-Loop:</strong> All generated email responses require your explicit review and manual approval before any outbound action can be taken.
              </li>
            </ul>
            <div className="p-3 rounded-lg bg-slate-900 border border-slate-800 font-mono text-xs text-amber-300">
              [CONFIRMATION REQUIRED: Specific Third-Party AI Vendor (e.g. Anthropic Claude, OpenAI, or Google Cloud Vertex AI), Data Processing Addendum (DPA) status, and zero-data-retention agreement details for future phases]
            </div>
          </section>

          {/* Section 6 */}
          <section className="space-y-3">
            <h2 className="text-base sm:text-lg font-bold text-white border-b border-slate-800 pb-2">
              6. Data Retention, Account Disconnection & Deletion
            </h2>
            <p>
              You maintain full ownership of your mailbox connections and data:
            </p>
            <ul className="list-disc list-inside space-y-1.5 pl-2 text-slate-400">
              <li>
                <strong className="text-slate-200">Immediate Disconnection & Revocation:</strong> You can disconnect any connected Gmail or Outlook account at any time directly from the dashboard. Disconnecting sends an automated revocation request to the provider (such as Google&apos;s token revocation endpoint) and permanently deletes the encrypted credentials from our database.
              </li>
              <li>
                <strong className="text-slate-200">User Account Deletion:</strong> If you delete your MailPilot AI account, all associated connected accounts and credentials are deleted immediately via cascading database constraints.
              </li>
            </ul>
            <div className="p-3 rounded-lg bg-slate-900 border border-slate-800 font-mono text-xs text-amber-300">
              [CONFIRMATION REQUIRED: Exact Retention Window for Security Audit Logs: e.g. 90 days or 180 days for audit_events]
            </div>
          </section>

          {/* Section 7 */}
          <section className="space-y-3">
            <h2 className="text-base sm:text-lg font-bold text-white border-b border-slate-800 pb-2">
              7. Contact Information
            </h2>
            <p>
              If you have any questions, concerns, or requests regarding this Privacy Policy or your data, please contact our privacy and data protection officer:
            </p>
            <div className="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-2 text-xs">
              <div className="flex items-center gap-2 text-white font-semibold">
                <Mail className="w-4 h-4 text-indigo-400" />
                <span>Privacy & Security Office</span>
              </div>
              <div className="font-mono text-amber-300">
                [CONFIRMATION REQUIRED: Official Privacy Support Email: e.g. privacy@mailpilot.ai or support@mailpilot.ai]
              </div>
              <div className="font-mono text-amber-300">
                [CONFIRMATION REQUIRED: Physical Mailing Address for Legal Notices]
              </div>
            </div>
          </section>
        </article>
      </main>

      <Footer />
    </div>
  );
}

