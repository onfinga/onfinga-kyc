# Onfinga KYC – Progress Tracker

📆 **Last Updated:** 2025-09-07

---

## ✅ Completed Milestones

### Phase 1: Backend Core (Flask + PostgreSQL)
- Set up Flask backend with factory pattern (`create_app`).
- Configured SQLAlchemy, Flask-Migrate, and PostgreSQL connection.
- Created models:
  - `User`
  - `KYCSession`
  - `KYCSubmission`
- Implemented migrations and upgraded database schema.
- Built core routes:
  - `/kyc/start` → Start new KYC session
  - `/kyc/status/<session_id>` → Get KYC status
  - `/kyc/update/<session_id>` → Approve/Reject KYC
  - `/kyc/list` → List all sessions for a user
- Added stricter validation, structured error codes, and error handling.

### Phase 2: Admin Panel
- Integrated **Flask-Admin**.
- Secured it with **Basic Auth** (`SecureModelView`).
- Added filtering, searching, and restricted actions in the admin panel.
- Confirmed panel working at `/admin`.

### Phase 3: Frontend MVP (React + Vite)
- Bootstrapped React frontend inside `/frontend`.
- Implemented components:
  - `StartKYC.jsx` → Starts a new session
  - `CheckStatus.jsx` → Polls and displays session status
  - `UpdateStatus.jsx` → Approve/Reject status for testing
- Styled with `App.css`.
- Verified integration with backend.

### Phase 4: Repo & Deployment
- Initialized GitHub repo: [onfinga-kyc](https://github.com/onfinga/onfinga-kyc).
- Created `.env` and added to `.gitignore`.
- Added `requirements.txt` for backend dependencies.
- Started preparing `render.yaml` for deployment.

---

## 🚧 In Progress

- Migration fixes for `user_id` foreign key refactor.
- Deployment pipeline setup on Render.

---

## 🎯 Next Milestones

1. **Deployment**
   - Debug Render build pipeline.
   - Ensure `requirements.txt` + `render.yaml` configured properly.
   - Deploy backend + frontend.

2. **MVP Validation**
   - End-to-end flow: user email → KYC session → admin approval → frontend reflects status.
   - Add basic frontend error handling.

---

## 📌 Notes

- Placeholder user in DB: `placeholder@onfinga.com`.
- Admin credentials in `.env`:
  - `ADMIN_USERNAME=admin`
  - `ADMIN_PASSWORD=supersecret123`
- Known bug: React UI shows white text on white background for session IDs (fixed via styling).

---

## Milestone A — Backend Hardening ✅ (Completed)
**Date:** 2025-09-05  

- Enforce stricter input validation (user_id/email) ✅  
- Error handling & 404s for missing sessions ✅  
- Structured error codes returned by all endpoints ✅  
- HTTPS in production via Render’s managed TLS ✅  

**Notes:**  
- `/kyc/start` now validates input and supports email→user mapping.  
- All endpoints return `{ error, code }` consistently for failures.  
- No code-based redirects needed; Render terminates TLS at the edge.  

---

## Milestone B — Environment Cleanup ✅ (Completed)
**Date:** 2025-09-05  

- Added `.env.example` to repo.  
- Added `.gitignore` rules for Python, frontend, and OS junk.  
- Removed hardcoded fallbacks from `config.py`.  

**Notes:**  
- Project is now environment-agnostic: no accidental secrets in repo.  
- `.env.example` guides devs to set up `.env` locally.  
- Safer for deployment on Render and when collaborating.  

---

## 🏷️ Git Tags

- `milestone-backend-hardening`
- `milestone-ssh-setup`
- `milestone-env-cleanup`
