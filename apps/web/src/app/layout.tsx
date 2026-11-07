import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "MailPilot AI — SaaS Email Management Platform",
  description: "Secure, multi-user AI email management with Gmail and Outlook integration.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-slate-950 text-slate-100 antialiased min-h-screen">
        {children}
      </body>
    </html>
  );
}

