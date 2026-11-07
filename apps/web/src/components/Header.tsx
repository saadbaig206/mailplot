"use client";

import React, { useState } from "react";
import Link from "next/link";
import { Mail, ArrowRight, Menu, X, Shield } from "lucide-react";

export const Header: React.FC = () => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <header className="border-b border-slate-800/80 bg-slate-950/80 backdrop-blur-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Brand */}
        <Link href="/" className="flex items-center gap-3 group">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 to-violet-500 flex items-center justify-center shadow-lg shadow-indigo-500/20 group-hover:scale-105 transition-transform">
            <Mail className="w-5 h-5 text-white" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-bold text-lg tracking-tight text-white group-hover:text-indigo-300 transition-colors">
                MailPilot AI
              </span>
              <span className="text-[10px] uppercase font-semibold px-2 py-0.5 rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
                Phase 1
              </span>
            </div>
            <p className="text-[11px] text-slate-400">Intelligent Email SaaS</p>
          </div>
        </Link>

        {/* Desktop Nav */}
        <nav className="hidden md:flex items-center gap-6 text-sm text-slate-300 font-medium">
          <Link href="/#features" className="hover:text-white transition-colors">
            Features
          </Link>
          <Link href="/#security" className="hover:text-white transition-colors flex items-center gap-1.5">
            <Shield className="w-3.5 h-3.5 text-indigo-400" />
            Security
          </Link>
          <Link href="/#how-it-works" className="hover:text-white transition-colors">
            How It Works
          </Link>
          <Link href="/privacy" className="hover:text-white transition-colors text-slate-400 hover:text-slate-200">
            Privacy
          </Link>
          <Link href="/terms" className="hover:text-white transition-colors text-slate-400 hover:text-slate-200">
            Terms
          </Link>
        </nav>

        {/* Action Button */}
        <div className="hidden md:flex items-center gap-3">
          <Link
            href="/dashboard"
            className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold shadow-lg shadow-indigo-600/20 transition-all hover:scale-[1.02]"
          >
            <span>Open Dashboard</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        {/* Mobile menu toggle */}
        <button
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          className="md:hidden p-2 text-slate-400 hover:text-white"
          aria-label="Toggle Menu"
        >
          {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
        </button>
      </div>

      {/* Mobile Nav dropdown */}
      {mobileMenuOpen && (
        <div className="md:hidden border-b border-slate-800 bg-slate-900/95 px-4 pt-3 pb-6 space-y-3">
          <Link
            href="/#features"
            onClick={() => setMobileMenuOpen(false)}
            className="block py-1.5 text-sm text-slate-300 hover:text-white"
          >
            Features
          </Link>
          <Link
            href="/#security"
            onClick={() => setMobileMenuOpen(false)}
            className="block py-1.5 text-sm text-slate-300 hover:text-white"
          >
            Security & Compliance
          </Link>
          <Link
            href="/#how-it-works"
            onClick={() => setMobileMenuOpen(false)}
            className="block py-1.5 text-sm text-slate-300 hover:text-white"
          >
            How It Works
          </Link>
          <Link
            href="/privacy"
            onClick={() => setMobileMenuOpen(false)}
            className="block py-1.5 text-sm text-slate-300 hover:text-white"
          >
            Privacy Policy
          </Link>
          <Link
            href="/terms"
            onClick={() => setMobileMenuOpen(false)}
            className="block py-1.5 text-sm text-slate-300 hover:text-white"
          >
            Terms of Service
          </Link>
          <div className="pt-2">
            <Link
              href="/dashboard"
              onClick={() => setMobileMenuOpen(false)}
              className="w-full flex items-center justify-center gap-2 py-2.5 rounded-xl bg-indigo-600 text-white text-xs font-semibold shadow-md"
            >
              <span>Launch Dashboard</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>
        </div>
      )}
    </header>
  );
};

