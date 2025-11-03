# Deploying to Vercel (Windows PowerShell)

This project is already configured for Vercel serverless Python functions via `vercel.json`. Follow these steps to deploy from your machine.

Prereqs
- Node.js + npm (for the Vercel CLI) or use the Vercel web UI
- Python (for local testing)

Steps (PowerShell)

```powershell
# 1. Install Vercel CLI (global)
npm i -g vercel

# 2. Login to your Vercel account
vercel login

# 3. From the project root deploy (first-time will ask to link to a project)
vercel
# or to deploy to production directly
vercel --prod
```

Notes
- The `vercel.json` routes all requests to `api/index.py` which hosts a Flask app and serves the Jinja template from `templates/`.
- Runtime files are written to `saved_files/` locally, but Vercel is ephemeral. For production, add persistent storage (e.g., S3, Vercel KV, or a database).

Troubleshooting
- If the CLI isn't available on Windows, use the Vercel dashboard and choose "Import Project" to connect your GitHub/GitLab/Bitbucket repo and deploy.
- If Flask routes return errors, check Vercel function logs in the dashboard.

If you want, I can:
- Add a Vercel KV or SQLite example for persistence.
- Create a GitHub Actions workflow for CI/CD that deploys to Vercel on push.
