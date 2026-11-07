import React from "react";
import Link from "next/link";
import { FileText, AlertTriangle, ArrowLeft, Mail, Scale } from "lucide-react";
import { Header } from "../../components/Header";
import { Footer } from "../../components/Footer";

export default function TermsOfServicePage() {
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
            <Scale className="w-4 h-4" />
            <span>Terms & Conditions</span>
          </div>
          <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
            Terms of Service
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
            These Terms of Service outline the rules and regulations for using the MailPilot AI platform. Variables designated with <strong className="text-amber-100 font-mono">[CONFIRMATION REQUIRED]</strong> require your verification and input prior to production deployment.
          </p>
        </div>

        {/* Content Body */}
        <article className="prose prose-invert prose-sm max-w-none space-y-8 text-slate-300 leading-relaxed text-xs sm:text-sm">
          {/* Section 1 */}
          <section className="space-y-3">
            <h2 className="text-base sm:text-lg font-bold text-white border-b border-slate-800 pb-2">
              1. Acceptance of Terms
            </h2>
            <p>
              By accessing, registering for, or using the MailPilot AI service (the &quot;Service&quot;), provided by MailPilot AI (&quot;Company&quot;, &quot;we&quot;, &quot;us&quot;, or &quot;our&quot;), you acknowledge that you have read, understood, and agree to be bound by these Terms of Service (&quot;Terms&quot;). If you do not agree to these Terms, you must not access or use the Service.
            </p>
            <div className="p-3 rounded-lg bg-slate-900 border border-slate-800 font-mono text-xs text-amber-300">
              [CONFIRMATION REQUIRED: Legal Entity Name and Form of Incorporation: e.g., MailPilot AI Inc., a Delaware Corporation]
            </div>
          </section>

          {/* Section 2 */}
          <section className="space-y-3">
            <h2 className="text-base sm:text-lg font-bold text-white border-b border-slate-800 pb-2">
              2. Description of the Service
            </h2>
            <p>
              MailPilot AI is an email management and productivity software-as-a-service application. In its current release (Phase 1: Foundation and Authentication), the Service provides:
            </p>
            <ul className="list-disc list-inside space-y-1.5 pl-2 text-slate-400">
              <li>OpenID Connect (OIDC) user authentication.</li>
              <li>Multi-account OAuth 2.0 connection architecture for Google (Gmail) and Microsoft (Outlook) mailboxes.</li>
              <li>Server-side encrypted credential storage.</li>
              <li>Connected mailbox management, status verification, and token revocation.</li>
            </ul>
            <p className="text-xs text-slate-400">
              Phase 1 is strictly read-only and does not send outbound emails or persist email message bodies. Future features and enhancements are subject to change.
            </p>
          </section>

          {/* Section 3 */}
          <section className="space-y-3">
            <h2 className="text-base sm:text-lg font-bold text-white border-b border-slate-800 pb-2">
              3. User Accounts and Security
            </h2>
            <p>
              You must provide accurate and complete information when authenticating with the Service. You are solely responsible for maintaining the confidentiality of your session tokens, credentials, and all activities that occur under your account. You agree to immediately notify us of any unauthorized use of your account or security breach.
            </p>
          </section>

          {/* Section 4 */}
          <section className="space-y-3">
            <h2 className="text-base sm:text-lg font-bold text-white border-b border-slate-800 pb-2">
              4. Third-Party Mailbox Providers & API Compliance
            </h2>
            <p>
              To use MailPilot AI, you may grant the Service permission to connect to your third-party email accounts via official OAuth 2.0 endpoints:
            </p>
            <ul className="list-disc list-inside space-y-1.5 pl-2 text-slate-400">
              <li>
                <strong className="text-slate-200">Google APIs:</strong> Your use of Google integration is governed by Google&apos;s Terms of Service and the Google API Services User Data Policy, including Limited Use requirements.
              </li>
              <li>
                <strong className="text-slate-200">Microsoft Identity Platform:</strong> Your use of Microsoft integration is governed by Microsoft&apos;s Service Agreement and Microsoft Graph API terms.
              </li>
            </ul>
            <p className="text-xs text-slate-400">
              We are not responsible for the availability, uptime, or policies of third-party email providers.
            </p>
          </section>

          {/* Section 5 */}
          <section className="space-y-3">
            <h2 className="text-base sm:text-lg font-bold text-white border-b border-slate-800 pb-2">
              5. Acceptable Use Policy
            </h2>
            <p>You agree not to use the Service to:</p>
            <ul className="list-disc list-inside space-y-1.5 pl-2 text-slate-400">
              <li>Violate any applicable local, state, national, or international laws.</li>
              <li>Access or attempt to access another user&apos;s account, data, or connected mailboxes.</li>
              <li>Interfere with, disrupt, reverse engineer, or circumvent the security controls of the Service.</li>
              <li>Probe, scan, or test the vulnerability of our systems or networks without authorization.</li>
              <li>Transmit unsolicited mass email (spam) or malicious software.</li>
            </ul>
          </section>

          {/* Section 6 */}
          <section className="space-y-3">
            <h2 className="text-base sm:text-lg font-bold text-white border-b border-slate-800 pb-2">
              6. Intellectual Property
            </h2>
            <p>
              The Service, including its code, architecture, designs, trademarks, and documentation, is the proprietary property of MailPilot AI and is protected by intellectual property laws. You retain full ownership of your email content and mailbox data.
            </p>
          </section>

          {/* Section 7 */}
          <section className="space-y-3">
            <h2 className="text-base sm:text-lg font-bold text-white border-b border-slate-800 pb-2">
              7. Disclaimers & Limitation of Liability
            </h2>
            <p>
              THE SERVICE IS PROVIDED ON AN &quot;AS IS&quot; AND &quot;AS AVAILABLE&quot; BASIS WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED. TO THE MAXIMUM EXTENT PERMITTED BY LAW, WE DISCLAIM ALL WARRANTIES, INCLUDING MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT.
            </p>
            <p>
              IN NO EVENT SHALL MAILPILOT AI BE LIABLE FOR ANY INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES ARISING OUT OF OR IN CONNECTION WITH YOUR USE OF THE SERVICE.
            </p>
          </section>

          {/* Section 8 */}
          <section className="space-y-3">
            <h2 className="text-base sm:text-lg font-bold text-white border-b border-slate-800 pb-2">
              8. Termination & Disconnection
            </h2>
            <p>
              You may terminate your use of the Service at any time by disconnecting your email accounts and discontinuing access. We reserve the right to suspend or terminate accounts that violate these Terms or pose a security risk to our infrastructure.
            </p>
          </section>

          {/* Section 9 */}
          <section className="space-y-3">
            <h2 className="text-base sm:text-lg font-bold text-white border-b border-slate-800 pb-2">
              9. Governing Law & Dispute Resolution
            </h2>
            <p>
              These Terms shall be governed by and construed in accordance with the laws of the specified jurisdiction, without regard to conflict of law principles.
            </p>
            <div className="p-3 rounded-lg bg-slate-900 border border-slate-800 font-mono text-xs text-amber-300">
              [CONFIRMATION REQUIRED: Governing Jurisdiction and Dispute Resolution Forum: e.g. State of Delaware, USA, with binding arbitration in New Castle County, Delaware]
            </div>
          </section>

          {/* Section 10 */}
          <section className="space-y-3">
            <h2 className="text-base sm:text-lg font-bold text-white border-b border-slate-800 pb-2">
              10. Contact Us
            </h2>
            <p>
              If you have any questions about these Terms, please contact us:
            </p>
            <div className="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-2 text-xs">
              <div className="flex items-center gap-2 text-white font-semibold">
                <Mail className="w-4 h-4 text-indigo-400" />
                <span>Legal & Inquiries</span>
              </div>
              <div className="font-mono text-amber-300">
                [CONFIRMATION REQUIRED: Official Legal Inquiries Email: e.g. legal@mailpilot.ai]
              </div>
            </div>
          </section>
        </article>
      </main>

      <Footer />
    </div>
  );
}

