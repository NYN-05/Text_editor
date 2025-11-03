# How to save and push updates

This short guide explains how to save your work locally and push updates to the remote GitHub repository used by this project (`https://github.com/NYN-05/Text_editor.git`). It assumes you're working on Windows using PowerShell (`pwsh.exe`).

## Quick checklist

- Save your files in the editor.
- Open a terminal in the project root (where `.git` lives).
- Check status, stage changes, commit with a clear message, and push.

## Typical commands (PowerShell)

1. Check what changed:

```powershell
git status --porcelain
git status -s
```

2. Review changes if you want:

```powershell
git diff            # unstaged changes
git diff --staged   # staged changes
```

3. Stage files (all files or specific files):

```powershell
git add .                    # stage all changed files
# or
git add path\to\file.ext    # stage a specific file
```

4. Commit with a short, clear message:

```powershell
git commit -m "Short: what changed (scope)"
```

Commit message tips:
- Keep the first line under ~72 characters.
- Use imperative mood: "Add", "Fix", "Update".
- Reference issue or task IDs if you have them.

5. Push to the remote repository:

If you are on `master` and `origin` is already configured:

```powershell
git push origin master
```

If you're working on a feature branch, create and push it:

```powershell
git checkout -b feature/short-description
git push --set-upstream origin feature/short-description
```

6. If there are updates on the remote, fetch and rebase (recommended):

```powershell
git fetch origin
git pull --rebase origin master   # while on master
```

7. If a push fails due to permissions or required authentication:

- Use a GitHub Personal Access Token (PAT) instead of password for HTTPS pushes.
- Or set up SSH keys and change the remote to SSH: `git remote set-url origin git@github.com:NYN-05/Text_editor.git`.

## Common workflows

- Small edits: edit -> git add -> git commit -> git push
- New feature: git checkout -b feature/x -> work -> add/commit -> push -> open PR on GitHub

## Verifying the push

After pushing, you can list remote branches:

```powershell
git ls-remote --heads origin
```

Or open the repo in a browser: https://github.com/NYN-05/Text_editor

## Troubleshooting

- Merge conflicts: follow git's instructions, edit conflicting files, git add, then continue rebase or merge.
- If your local branch is behind, pull first (prefer rebase to keep history linear): `git pull --rebase origin BRANCH`.

## Notes

- This repository currently uses the `master` branch. If you prefer `main`, you can create and push a `main` branch and set it as default on GitHub.
- Keep commits small and descriptive. When in doubt, ask or open a draft PR for feedback.

---

File added by an automated assistant. If you'd like this moved to `CONTRIBUTING.md`, or to include PR/CI instructions, tell me and I will update it.
