# Deploying to Netlify

This file explains how this repository is prepared for Netlify and how to deploy it.

What I added
- `netlify.toml` — configuration that tells Netlify to publish the static site from the `templates/` folder and where local functions live for `netlify dev`.

Quick steps to deploy

1. Go to https://app.netlify.com and sign in (or create an account).
2. Click "Add new site" → "Import an existing project" → "GitHub" and authorize Netlify if needed.
3. Select the repository `NYN-05/Text_editor`.
4. In the deploy settings, set the Publish directory to `templates` (the `netlify.toml` already specifies this). Leave the Build command empty if your site is static.
5. Click "Deploy site". Netlify will build and publish the site and create a URL.

Testing locally

- Install Netlify CLI: `npm install -g netlify-cli` (requires Node.js).
- Run `netlify dev` in the project root to preview the site locally and test Functions (JS/Go functions supported by default).

About server/API code in this repo

- This repository contains `api/index.py` which is designed for Vercel-style Python serverless functions. Netlify's Functions environment runs Node.js (JavaScript) or Go by default. To run Python functions on Netlify you must use a build plugin or an adapter.
- If you'd like, I can:
  - Convert a small example API endpoint to a Netlify JS function (place under `netlify/functions/`) so you can test serverless behavior immediately, or
  - Add instructions and CI for deploying the Python API elsewhere (e.g., a small Flask app on Render or Heroku) and proxy requests from the Netlify site.

Files relevant to Netlify
- `netlify.toml` — Netlify configuration (publish directory + dev functions path)
- `templates/` — static site content (publish directory)

After connecting the repo, Netlify will auto-deploy on pushes to `master`.
