# GitHub first, deployment second

## 1. Add these files to the existing project root

Copy the following from this kit into the root of `kinyarwanda-sentiment-classifier/`:

- `.gitignore`
- `README.md` (keep a backup of your existing README first if it contains important notes)
- `app.py` (keep a copy of the current app first; this version works locally with the saved model and can use `MODEL_REPO_ID` after deployment)
- `requirements.txt`
- `requirements-dev.txt` (for reproducing notebooks and experiments)
- `MODEL_HOSTING.md`
- `scripts/upload_model_to_hub.py`
- `scripts/clear_notebook_outputs.py`

Do not copy this ZIP into the project or upload your model directory/raw data to GitHub.

## 2. Clear notebook outputs before publishing

From Terminal:

```bash
cd ~/Downloads/kinyarwanda-sentiment-classifier
python scripts/clear_notebook_outputs.py notebooks
```

This makes backup copies to `notebooks_backup_before_clear_outputs/`. Inspect them locally if you need old outputs. Clearing outputs prevents saved tweet examples from being embedded in notebooks; the backup folder should remain local and not be committed.

## 3. Create an empty GitHub repository

On GitHub, create a repository named `kinyarwanda-sentiment-classifier`. For a public portfolio project choose Public, after checking what files will be published. Do not initialize it with a README, license, or `.gitignore`, because you have an existing local project.

## 4. Initialize and push

In Terminal (from your project root):

```bash
git init
git branch -M main
git status --short
```

Inspect this status list. It should NOT contain `data/`, `models/`, virtual environments, `.env`, `.streamlit/secrets.toml`, or raw-text test error CSVs. If any of those appear, stop and fix `.gitignore` before proceeding.

Then stage and commit:

```bash
git add .
git status --short
git commit -m "Add Kinyarwanda sentiment classification project"
```

Add the remote URL from the empty GitHub repository page, replacing USERNAME with your account:

```bash
git remote add origin https://github.com/USERNAME/kinyarwanda-sentiment-classifier.git
git push -u origin main
```

GitHub may ask you to authenticate in your browser. Never paste a password or access token into this chat.

If `git init` says the project is already a repository, do not initialize again; inspect `git status` and `git remote -v` first.
