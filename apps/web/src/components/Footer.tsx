import React from "react";
import Link from "next/link";
import { Mail, Shield, ExternalLink } from "lucide-react";

export const Footer: React.FC = () => {
  return (
    <footer className="border-t border-slate-800 bg-slate-950 text-slate-400 text-xs">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-10">
          {/* Column 1: Brand */}
          <div className="space-y-3 md:col-span-2">
            <div className="flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-indigo-600 to-violet-500 flex items-center justify-center text-white">
                <Mail className="w-4 h-4" />
              </div>
              <span className="font-bold text-base text-white tracking-tight">MailPilot AI</span>
            </div>
            <p className="text-xs text-slate-400 max-w-md leading-relaxed">
              Multi-user AI email management SaaS platform. Connect your Gmail and Outlook mailboxes with least-privilege, read-only permissions, authenticated server-side token encryption, and human-in-the-loop review.
            </p>
            <div className="flex items-center gap-2 pt-1 text-[11px] text-slate-500">
              <Shield className="w-3.5 h-3.5 text-emerald-400" />
              <span>Phase 1 Architecture: Read-Only Scopes &bull; Zero Plaintext Token Storage</span>
            </div>
          </div>

          {/* Column 2: Navigation */}
          <div className="space-y-2">
            <h4 className="text-xs font-semibold text-slate-200 uppercase tracking-wider">Product</h4>
            <ul className="space-y-1.5 text-xs">
              <li>
                <Link href="/dashboard" className="hover:text-white transition-colors">
                  Dashboard
                </Link>
              </li>
              <li>
                <Link href="/#features" className="hover:text-white transition-colors">
                  Features
                </Link>
              </li>
              <li>
                <Link href="/#security" className="hover:text-white transition-colors">
                  Security Architecture
                </Link>
              </li>
              <li>
                <Link href="/#how-it-works" className="hover:text-white transition-colors">
                  How It Works
                </Link>
              </li>
            </ul>
          </div>

          {/* Column 3: Legal & Compliance */}
          <div className="space-y-2">
            <h4 className="text-xs font-semibold text-slate-200 uppercase tracking-wider">Legal & Trust</h4>
            <ul className="space-y-1.5 text-xs">
              <li>
                <Link href="/privacy" className="hover:text-white transition-colors flex items-center gap-1">
                  <span>Privacy Policy</span>
                </Link>
              </li>
              <li>
                <Link href="/terms" className="hover:text-white transition-colors flex items-center gap-1">
                  <span>Terms of Service</span>
                </Link>
              </li>
              <li>
                <a
                  href="https://developers.google.com/terms/api-services-user-data-policy"
                  target="_blank"
                  rel="noreferrer"
                  className="hover:text-white transition-colors inline-flex items-center gap-1 text-slate-500 hover:text-slate-300"
                >
                  <span>Google User Data Policy</span>
                  <ExternalLink className="w-3 h-3" />
                </a>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom bar */}
        <div className="pt-8 border-t border-slate-900 flex flex-col sm:flex-row items-center justify-between gap-4 text-[11px] text-slate-500">
          <p>&copy; {new Date().getFullYear()} MailPilot AI. All rights reserved.</p>
          <div className="flex items-center gap-6">
            <Link href="/privacy" className="hover:text-slate-300 transition-colors">
              Privacy
            </Link>
            <Link href="/terms" className="hover:text-slate-300 transition-colors">
              Terms
            </Link>
            <Link href="/dashboard" className="hover:text-slate-300 transition-colors">
              App
            </Link>
          </div>
        </div>
      </div>
    </footer>
  );
};

