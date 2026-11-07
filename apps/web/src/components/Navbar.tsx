"use client";

import React from "react";
import { Mail, ShieldCheck, User as UserIcon } from "lucide-react";
import { User } from "@/types";

interface NavbarProps {
  user: User | null;
  onLogout: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({ user, onLogout }) => {
  return (
    <header className="border-b border-slate-800 bg-slate-900/60 backdrop-blur-md sticky top-0 z-50">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 to-violet-500 flex items-center justify-center shadow-lg shadow-indigo-500/20">
            <Mail className="w-5 h-5 text-white" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-bold text-lg tracking-tight text-white">MailPilot AI</span>
              <span className="text-[10px] uppercase font-semibold px-2 py-0.5 rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
                Phase 1
              </span>
            </div>
            <p className="text-xs text-slate-400">Foundation & Auth</p>
          </div>
        </div>

        <div className="flex items-center gap-4">
          {user ? (
            <div className="flex items-center gap-3">
              <div className="flex items-center gap-2.5 px-3 py-1.5 rounded-lg bg-slate-800/80 border border-slate-700">
                {user.avatar_url ? (
                  <img src={user.avatar_url} alt={user.email} className="w-6 h-6 rounded-full" />
                ) : (
                  <div className="w-6 h-6 rounded-full bg-indigo-600/30 text-indigo-400 flex items-center justify-center text-xs font-semibold">
                    <UserIcon className="w-3.5 h-3.5" />
                  </div>
                )}
                <div className="text-left hidden sm:block">
                  <div className="text-xs font-medium text-slate-200">{user.full_name || user.email}</div>
                  <div className="text-[10px] text-slate-400">{user.email}</div>
                </div>
              </div>
              <button
                onClick={onLogout}
                className="text-xs text-slate-400 hover:text-slate-200 transition-colors px-2 py-1"
              >
                Sign out
              </button>
            </div>
          ) : (
            <div className="flex items-center gap-1.5 text-xs text-amber-400/90 bg-amber-500/10 border border-amber-500/20 px-2.5 py-1 rounded-md">
              <ShieldCheck className="w-3.5 h-3.5" />
              <span>Authentication Required</span>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};

