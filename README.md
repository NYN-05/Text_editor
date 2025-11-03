# Minimal Flask app ready for Vercel

This repository contains a tiny Flask + Jinja app packaged as a Vercel Python serverless function.

Files:
- `api/index.py` - Flask WSGI app entrypoint used by Vercel
- `templates/index.html` - Jinja2 template rendered by Flask
- `requirements.txt` - Python dependencies
- `vercel.json` - Vercel configuration

Quick local run (Windows PowerShell):

```powershell
# create venv
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python api/index.py
```

Deploy to Vercel (recommended):

1. Install the Vercel CLI: `npm i -g vercel` or use the web UI.
2. From the project root run:

```powershell
vercel login
vercel --prod
```

Vercel will detect the `vercel.json` and use the `@vercel/python` runtime to deploy `api/index.py`.

Test locally (once the app is running):

```powershell
# From a separate PowerShell window
curl http://127.0.0.1:5000/
```

Persistence note
----------------

The editor saves files to a local `saved_files/` directory in the project. This works for local development and persistent servers. However, Vercel and other serverless providers use ephemeral file systems: files written at runtime are not guaranteed to persist across invocations, builds, or deployments.

If you need persistent storage in production, consider:
- Using an object store (S3, Cloud Storage) for files
- Using a simple database (SQLite on a persistent volume, PostgreSQL)
- Using Vercel KV or another key-value service for small items

If you'd like, I can add a SQLite backend or an example that saves to S3/Vercel KV and update the UI accordingly.

