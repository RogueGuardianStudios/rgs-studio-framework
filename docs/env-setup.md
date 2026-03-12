# Environment Setup Guide

Step-by-step instructions for configuring your local
environment before running any framework scripts.

---

## Step 1 — Open your terminal

Open a terminal in the root of the `agent-governance-framework`
repository. This is the folder that contains `framework-core/`,
`state-templates/`, and `environment/`.

If you're using Claude Code, the terminal is already open
in the right place.

---

## Step 2 — Create the .env file

Run this command in your terminal:

```bash
touch .env
```

This creates an empty file called `.env` in the repo root.
You will not see this file in git — it is excluded by
`.gitignore` to prevent secrets from being committed.

---

## Step 3 — Add your API key

Open the `.env` file in any text editor and add the
following line, replacing the placeholder with your
actual Anthropic API key:

```
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

Save the file.

**Alternative — do it from the terminal in one command:**

```bash
echo 'ANTHROPIC_API_KEY=sk-ant-your-key-here' > .env
```

Replace `sk-ant-your-key-here` with your real key.

---

## Step 4 — Verify the file exists

Run:

```bash
cat .env
```

You should see your API key line printed back to you.
If you see nothing, the file is empty — go back to Step 3.

---

## Step 5 — Verify git is ignoring it

Run:

```bash
git status
```

The `.env` file should **not** appear in the output.
If it does appear as an untracked file, check that
`.gitignore` exists in the repo root and contains `.env`.

---

## Where to get an API key

1. Go to https://console.anthropic.com/
2. Sign in or create an account
3. Navigate to **API Keys** in the sidebar
4. Click **Create Key**
5. Copy the key — it starts with `sk-ant-`
6. Paste it into your `.env` file as shown in Step 3

---

## Adding more environment variables

If future scripts require additional variables, add them
on new lines in the same `.env` file:

```
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

See `environment/environment-rules.md` for environment
configuration details.

---

## Troubleshooting

**"Command not found" when running scripts:**
Make sure Python 3 is installed: `python3 --version`

**API key not being picked up:**
Confirm there are no extra spaces around the `=` sign
and no quotes around the value.

**File accidentally committed:**
If `.env` was committed before `.gitignore` was added,
remove it from tracking:

```bash
git rm --cached .env
git commit -m "Remove .env from tracking"
```

The file will remain on disk but stop being tracked.

---

*Document version: 1.0*
*Author: *
