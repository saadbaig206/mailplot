# Vercel Deployment Guide — MailPilot AI Frontend

This document outlines the step-by-step procedure to deploy the MailPilot AI Next.js frontend (`apps/web`) to Vercel within our monorepo architecture.

---

## 1. Monorepo Project Settings on Vercel

When importing the Git repository in Vercel:

1. **Framework Preset**: Select **Next.js**.
2. **Root Directory**:
   - In the project import screen, click **Edit** next to **Root Directory**.
   - Select or enter: `apps/web`
   - Check the box: **Include source files outside of the Root Directory in the Build Cache** (recommended for monorepos).
3. **Build & Development Settings**:
   - **Build Command**: `next build` (or leave default: `npm run build`)
   - **Output Directory**: `.next` (default)
   - **Install Command**: `npm install` (default)

---

## 2. Production Environment Variables

In your Vercel Project Dashboard, navigate to **Settings** -> **Environment Variables** and configure the following:

| Variable Name | Environment | Description | Example Production Value |
|---|---|---|---|
| `NEXT_PUBLIC_API_URL` | Production, Preview | Fully-qualified public URL of your deployed FastAPI backend | `https://api.mailpilot.ai` |
| `NEXT_PUBLIC_APP_URL` | Production, Preview | Public URL of your Vercel deployment | `https://mailpilot.ai` |

> [!IMPORTANT]
> Never set backend secrets (such as `ENCRYPTION_KEY`, `SECRET_KEY`, `GOOGLE_CLIENT_SECRET`, or `MICROSOFT_CLIENT_SECRET`) in Vercel. Those secrets belong exclusively in your backend hosting environment (e.g., Railway, Render, Fly.io, or AWS ECS) and must never be exposed to the client.

---

## 3. Backend CORS & OAuth Redirect Alignment

Once your Vercel deployment URL is generated (e.g. `https://mailpilot-web.vercel.app` or custom domain `https://mailpilot.ai`):

1. **Backend CORS (`ALLOWED_ORIGINS`)**:
   Add your Vercel domains to `ALLOWED_ORIGINS` in your backend environment:
   ```env
   ALLOWED_ORIGINS=https://mailpilot.ai,https://mailpilot-web.vercel.app,http://localhost:3000
   ```

2. **Google Cloud Console Credentials**:
   In Google Cloud Console -> APIs & Services -> Credentials -> OAuth 2.0 Client:
   - **Authorized JavaScript origins**: `https://mailpilot.ai`, `https://mailpilot-web.vercel.app`
   - **Authorized redirect URIs**: `https://api.mailpilot.ai/api/v1/oauth/google/callback`

3. **Microsoft Entra ID (Azure AD)**:
   In Azure Portal -> App Registrations -> Authentication:
   - **Redirect URIs (Web)**: `https://api.mailpilot.ai/api/v1/oauth/microsoft/callback`

---

## 4. Pages Deployed

| Route | Accessibility | Purpose |
|---|---|---|
| `/` | Public | SaaS Landing Page (Features, Security Blueprint, How it works, CTAs) |
| `/privacy` | Public | Privacy Policy (Google Limited Use & Microsoft compliance) |
| `/terms` | Public | Terms of Service |
| `/dashboard` | Authenticated | User Profile, Connected Accounts list, Connect Gmail & Outlook |
| `/oauth/callback` | Callback | Processes OAuth redirect and state verification with Suspense |

