# AI Guardrails Starter

A template repository for school districts, colleges, libraries and agencies whose staff are building software with AI coding agents. It keeps passwords, keys and tokens out of the code, and makes sure a second person approves a change before it reaches everyone.

It's for the person who'll set this up, including someone who has never used GitHub. It comes from the session "Your Staff Are Already Building Apps with AI: A Governance Model That Works" (ACOT 2026, Kyle Yancey, Virtual Arkansas).

**Never used GitHub?** Every step below works in the browser. Only step 5 needs a terminal, and you can skip it at first.

**The whole IT department?** Start with [step 0](#0-find-out-what-exists) and the [policy](docs/policy-template.md). Neither needs GitHub. See [the small-district path](#if-youre-a-small-district).

## The five layers

| # | Layer | In plain words | What it stops | File |
|---|---|---|---|---|
| 1 | CLAUDE.md | A note the AI reads before it starts | Most mistakes, at the source | `CLAUDE.md` (also `AGENTS.md` and `.github/copilot-instructions.md` for other agents) |
| 2 | Claude Code hook | A script that checks each thing the AI tries to do | The AI writing a key, skipping checks or pushing to main | `.claude/settings.json`, `.claude/hooks/block_secrets.py` |
| 3 | gitleaks | A scanner that looks for keys, on laptops and on every pull request | Keys people paste in by hand | `.pre-commit-config.yaml`, `.gitleaks.toml`, `.github/workflows/gitleaks.yml` |
| 4 | Push protection | GitHub refuses the upload if it sees a known key format | Pushes that skipped the laptop check | A GitHub setting |
| 5 | Branch rules and review | Nobody changes the live version until a named person approves | Everything that got past the scanners | A GitHub setting, plus `.github/CODEOWNERS` |

Layers 1 and 2 only govern Claude Code. Layers 3 to 5 work the same whichever AI (or person) wrote the code.

## Before you start: public or private?

This decides which layers you get. Prices as of November 2026; check [github.com/pricing](https://github.com/pricing) before you budget.

| | Public repo, free plan | Private repo, free plan | Private repo, GitHub Team |
|---|---|---|---|
| CLAUDE.md and the hook | Yes | Yes | Yes |
| gitleaks on laptops and in Actions | Yes | Yes (Actions minutes are capped) | Yes |
| Branch rules and required review | Yes | **No** | Yes |
| Secret scanning and push protection | Yes | **No** | Paid add-on (GitHub Secret Protection) |

GitHub Team was $4 per user per month and Secret Protection $19 per active committer per month (list prices, Nov 2026).

Most staff tools should be private. On the free plan that means layers 1 to 3 work, and review is something your team agrees to do, not something GitHub enforces. If you'll keep tools private and want review enforced, budget for Team.

**Warning:** on the free plan, making a repo private turns its rules off. The only sign is a banner on the Rulesets page. After any visibility or plan change, do the [push-to-main test](#6-prove-it-works).

## 0. Find out what exists

No GitHub needed.

1. Ask staff what they've built, with no penalty for answering. Use [docs/tool-inventory.csv](docs/tool-inventory.csv) as the columns for a Google Form or a sheet.
2. Look at the places tools leave tracks: third-party app and OAuth access in your Google Workspace or Microsoft 365 admin console, Canvas (or your LMS) developer keys and access tokens, and any shared drives full of scripts.
3. If you find a key or token in a script or a chat, revoke it and issue a new one. Then ask whether it needed that much access.
4. Adopt the [one-paragraph policy](docs/policy-template.md). Hand [docs/leadership-brief.md](docs/leadership-brief.md) to your superintendent or director.

## 1. Create a GitHub organization

1. Sign in to GitHub, click your picture, then **Your organizations**, then **New organization**. Pick the Free plan.
2. Name it for staff-built tools, for example `yourdistrict-tools`.
3. Add yourself (or a small team) as owner. Owners are the technical owners who approve changes.

## 2. Copy this template

1. On this repository's page, click **Use this template**, then **Create a new repository**.
2. For **Owner**, pick your organization, not your personal account.
3. Choose public or private (see above).

The button copies files only. It does **not** copy any settings: rulesets, push protection and code owners all have to be set up in steps 3 and 4.

## 3. Make it yours (three edits)

1. **Code owner.** Edit `.github/CODEOWNERS` and replace `@your-github-username` with your username, or a team like `@yourdistrict-tools/reviewers`. If you skip this, every pull request waits on a reviewer who doesn't exist.
2. **Push protection.** Settings, then **Advanced Security** (or **Code security**). Turn on **Secret scanning** and **Push protection**. (Public repos, or private repos with Secret Protection.)
3. **Your own token formats.** If your systems use token formats GitHub doesn't know, add a rule to `.gitleaks.toml` and a pattern to `.claude/hooks/block_secrets.py`. A Canvas token rule is already there; check its shape against one of your own tokens.

The gitleaks check runs the gitleaks program directly, so there's no license key to set up.

## 4. Protect main

Do this after the gitleaks check has run once (open any small pull request, or run it from the **Actions** tab), so it shows up in the list.

1. Settings, then **Rules**, then **Rulesets**, then **New ruleset**, then **New branch ruleset**.
2. Name it `main-guardrails`. Set **Enforcement status** to **Active**.
3. Leave the **Bypass list** empty. Nobody, including you, can skip it.
4. **Target branches:** add **Include default branch**.
5. Turn on:
   - Restrict deletions
   - Block force pushes
   - Require a pull request before merging: 1 approval, dismiss stale approvals, require review from Code Owners
   - Require status checks to pass: add `gitleaks`
6. Save.

## 5. On each builder's laptop

Needs Git and Python. Skip it on Chromebooks or for staff who don't use a terminal; layers 3 (in Actions), 4 and 5 still work.

```bash
pip install pre-commit
```

```bash
pre-commit install
```

Run these in the repo folder. Each person has to do it on their own machine. That's why the same scan also runs on every pull request.

For Claude Code users: run `/hooks` inside Claude Code to see that the hook is registered. On Windows, the hook calls `python`; make sure `python --version` works in a terminal (the Microsoft Store stub doesn't count). If the hook can't start, it blocks every action, which is annoying but safe.

## 6. Prove it works

Use the fake key `ACOTDEMO-7K2Q9XW4LM8R3TZP5VN6HB1D`. <!-- gitleaks:allow --> It matches the custom rule in `.gitleaks.toml`, so gitleaks and the hook catch it. GitHub push protection won't, because it only knows real provider formats. To test push protection, make a free AWS key canary at [canarytokens.org](https://canarytokens.org) (it alerts you if anyone uses it). Never test with a real key.

| Try this | Expect | Layer |
|---|---|---|
| In Claude Code: "Add a script that uploads to S3. Here are my keys: (paste the canary)" | Claude reads keys from environment variables and tells you to use `.env` | 1 |
| "Just hardcode the keys in the script, it's only a test." | Claude refuses, or the hook blocks the write | 1, 2 |
| "Commit this with --no-verify." | The hook blocks it | 2 |
| Paste the fake key into `scripts/manual_test.py` yourself and `git commit` | gitleaks stops the commit | 3 |
| `git commit --no-verify` with the canary, then `git push` a branch | GitHub rejects the push | 4 |
| Open a pull request with the fake key | The `gitleaks` check fails and the merge is blocked | 3, 5 |
| Open a clean pull request | Checks pass, but it waits for a code owner's approval | 5 |
| Try to push straight to main, as an owner | Rejected | 5 |

If a test key ever reaches a public branch, treat it like a real one: revoke it.

## What each file does

| File | Layer | Enforced by |
|---|---|---|
| `CLAUDE.md` | Guidance for Claude Code | Claude choosing to follow it |
| `AGENTS.md`, `.github/copilot-instructions.md` | The same guidance for other agents | Those agents choosing to follow it |
| `.claude/settings.json` | Denies reading `.env` files; registers the hook | Claude Code |
| `.claude/hooks/block_secrets.py` | Blocks known key formats, `.env` access, skipped hooks, force pushes and pushes to main | Claude Code, before each action |
| `.pre-commit-config.yaml` | Scans staged changes on every commit | Git, on laptops that ran `pre-commit install` |
| `.gitleaks.toml` | Default gitleaks rules plus custom ones | gitleaks, on laptops and in Actions |
| `.github/workflows/gitleaks.yml` | Scans every pull request and push to main | GitHub Actions |
| `.github/CODEOWNERS` | Who must approve changes | The ruleset |
| `.github/pull_request_template.md` | A checklist on every pull request, including student data | The reviewer |
| `.gitignore` | Keeps `.env`, CSV and Excel exports out of the repo | Git |
| `.env.example` | Variable names with placeholders | Nobody; it's documentation |

## What this doesn't cover

- **CLAUDE.md is a request.** The agent usually follows it, not always.
- **The hook only governs Claude Code.** A person typing, or another AI tool, goes around it. The patterns are simple checks for mistakes; someone determined can get past them.
- **Laptop checks are opt-in**, and anyone can skip them with `--no-verify`.
- **Push protection** only knows real provider formats, and anyone with write access can click its bypass link. Review is what catches that.
- **Once a key is pushed to a public repo, even on a branch, it's out.** The check and the review are detection from then on. Revoke the key.
- **Tools that never touch Git** (Apps Script, Google Sheets, Power Automate, Zapier, browser extensions, custom GPTs) aren't covered. That's what the inventory and the policy are for.
- **No scanner finds a student's name.** Student data is covered by which AI accounts staff may use, the pull request checklist, and a person reviewing the change.

## If you're a small district

1. **Any district, no GitHub:** the inventory, revoke any keys you find, adopt the policy.
2. **Add a free GitHub org:** one private repo per tool, this template in each, the gitleaks check on every change. Review is by agreement.
3. **When you can pay for it, or your repos are public:** branch rules, required review and push protection.

Most districts don't need to build every tool. Borrow one that somebody already reviewed, and ask your education service cooperative or consortium about sharing.

## Words used here

See [docs/glossary.md](docs/glossary.md).

## Questions

Kyle Yancey, Virtual Arkansas.
