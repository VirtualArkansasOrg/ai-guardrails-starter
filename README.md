# AI Guardrails Starter

A template repository for school districts, colleges, libraries and agencies whose staff are building software with AI coding agents. It helps keep passwords, keys and tokens out of the code, and sets things up so a second person approves a change before it reaches everyone. (GitHub only enforces that approval on public repos or paid plans; see below.)

It's a starting point. Every organization runs different systems (LMS, SIS, Google or Microsoft, help desk, home-grown tools), so change anything here to fit yours. It comes from the session "Your Staff Are Already Building Apps with AI: A Governance Model That Works" (ACOT 2026, Kyle Yancey, Virtual Arkansas), where we shared what Virtual Arkansas does.

Never used GitHub? Most steps below work in a web browser.

## What I'd do Monday (the five steps from the talk)

1. [Find out what exists](#0-find-out-what-exists). No GitHub needed.
2. [Create a free GitHub organization](#1-create-a-github-organization), and if staff will build in Claude Code on the web, approve its GitHub app there.
3. [Copy this template](#2-copy-this-template), [make it yours](#3-make-it-yours) and [protect main](#4-protect-main).
4. Send the [one-paragraph policy](docs/policy-template.md) to your attorney and toward a board agenda.
5. [Bring in one tool as a pilot](#7-bring-in-one-tool-as-a-pilot).

## If you're a small district

1. Any district, no GitHub: do the inventory, revoke any keys you find, send the policy to your attorney, and tell staff that student data doesn't go into personal AI accounts.
2. Add a free GitHub org: one private repo per tool, this template in each, the gitleaks check on every change. Review is something your team agrees to do.
3. When you can pay for it, or your repos are public: branch rules, required review and push protection.

Most districts don't need to build every tool. Borrow one that somebody already reviewed, and ask your education service cooperative or consortium about sharing.

## How our staff build (Claude Code on the web)

At Virtual Arkansas, staff who aren't developers build with [Claude Code on the web](https://claude.ai/code), connected to our GitHub organization. We picked it because nothing installs on their computers and it works in a browser, including on a Chromebook. Use whatever your contracts cover. If your staff use a different tool, layers 3 to 5 below still apply. Staff who work on their own computers can use the same repo; see [step 5](#5-optional-staff-who-work-on-their-own-computer).

If you go the same way:

- Each builder needs a Claude plan that includes Claude Code on the web (check [claude.com/pricing](https://claude.com/pricing)). Personal Pro or Max accounts work, but they're on consumer terms, so decide whether they count as district-approved accounts under your policy. Budget these seats alongside the GitHub seats.
- An organization owner approves the Claude GitHub app the first time someone connects. Give it only the tool repos, not all repositories.
- On managed Chromebooks, make sure your web filter allows claude.ai and github.com for the staff who build.
- CLAUDE.md always loads. The hook and deny rules in `.claude/settings.json` apply in a cloud session opened on this one repo. They don't apply in sessions with several repos or in Projects threads.
- Keys for a cloud session: an environment variable on the cloud environment can be read by anyone who uses that environment, so use a narrow, low-privilege key, or skip it. Network secrets on the environment are added to requests by the proxy and never appear to the code, so they only work for keys sent in a request header (like a bearer token). Never put a key in the repo or the chat.

## The five layers

| # | Layer | In plain words | What it stops | File |
|---|---|---|---|---|
| 1 | CLAUDE.md | A note the AI reads before it starts | Keys the AI would have written, if it listens | `CLAUDE.md` (also `AGENTS.md` and `.github/copilot-instructions.md` for other agents) |
| 2 | Claude Code hook | A script that checks the AI's file reads, writes and commands | The AI writing a known key format, touching `.env`, skipping checks or pushing to main | `.claude/settings.json`, `.claude/hooks/block_secrets.py` |
| 3 | gitleaks | A scanner that looks for keys on every pull request (and on laptops, if installed) | Keys people paste in by hand | `.github/workflows/gitleaks.yml`, `.gitleaks.toml`, `.pre-commit-config.yaml` |
| 4 | Push protection | GitHub refuses the upload if it sees a known key format | Pushes that skipped the other checks | A GitHub setting |
| 5 | Branch rules and review | Nobody changes the live version until a named person approves | Bad changes reaching main | A GitHub setting, plus `.github/CODEOWNERS` |

Layers 1 and 2 only govern Claude Code. Layers 3 to 5 work the same whichever AI (or person) wrote the code. GitHub Copilot in an editor reads `.github/copilot-instructions.md`. If your staff use Microsoft 365 Copilot or ChatGPT to write scripts they paste into Power Automate, Excel or Apps Script, none of this sees it; that's what the inventory and the policy are for.

## Public or private? Decide this first

This decides which layers you get. Prices as of November 2026; check [github.com/pricing](https://github.com/pricing) before you budget.

| | Public repo, free plan | Private repo, free plan | Private repo, GitHub Team |
|---|---|---|---|
| CLAUDE.md and the hook | Yes | Yes | Yes |
| gitleaks check on pull requests | Yes | Yes (Actions minutes are capped) | Yes |
| Branch rules and required review | Yes | No | Yes |
| Secret scanning and push protection | Yes | No | Paid add-on (GitHub Secret Protection) |

GitHub Team was $4 per user per month, billed for every member (plus outside collaborators on private repos), so keep the org to builders and reviewers. Secret Protection was $19 per active committer per month. Both are list prices, Nov 2026.

Most staff tools should be private. On the free plan that means layers 1 to 3 work, and review is something your team agrees to do. GitHub won't enforce it. If you'll keep tools private and want review enforced, budget for Team.

On the free plan, making a repo private turns its rules off. GitHub won't email you about it; look for a banner on the Rulesets page. After any visibility or plan change, do the [push-to-main test](#6-prove-it-works).

## 0. Find out what exists

No GitHub needed.

1. Ask staff what they've built, with no blame for answering. [docs/tool-inventory.csv](docs/tool-inventory.csv) has the columns. The first nine are the questions for a staff form (Google Forms, Microsoft Forms, anything). Technical owner, Status and Notes are for IT to fill in afterward.
2. Look where tools leave tracks. Some places to start (menu names change, so search your admin help if these moved):
   - Google Workspace: Admin console, Security, Access and data control, API controls, Manage App Access. Google Classroom add-ons show up here too.
   - Chromebooks: Admin console, Devices, Chrome, Apps & extensions, Users & browsers.
   - Microsoft 365: Microsoft Entra admin center, Entra ID, Enterprise apps, All applications (and App registrations).
   - Your LMS and SIS: wherever they list developer keys, API keys, plugins or integrations.
   - Shared drives full of scripts.
3. If you find a key or token in a script or a chat, revoke it and issue a new one. Then ask whether it needed that much access.
4. Send the [one-paragraph policy](docs/policy-template.md) to your attorney. Hand [docs/leadership-brief.md](docs/leadership-brief.md) to your superintendent or director.

## 1. Create a GitHub organization

1. Sign in to GitHub, click your picture, then Your organizations, then New organization. Pick the Free plan.
2. Name it for staff-built tools, for example `yourdistrict-tools`.
3. Add the people who'll approve changes as owners, ideally two or more.

## 2. Copy this template

1. On this repository's page, click Use this template, then Create a new repository.
2. For Owner, pick your organization, not your personal account.
3. Choose public or private (see [Public or private? Decide this first](#public-or-private-decide-this-first)).

The button copies files only. It doesn't copy any settings: rulesets, push protection and code owners all have to be set up in steps 3 and 4.

## 3. Make it yours

1. Code owners. Edit `.github/CODEOWNERS` and replace `@your-github-username` on every line with a person or team who approves changes, for example `@yourdistrict-tools/reviewers`. That person or team needs Write access to the repo (Settings, Collaborators and teams), or GitHub ignores the line and code-owner review does nothing. After you save, open the file on GitHub; it marks owners it can't use.
2. Push protection (public repos, or private repos with Secret Protection). Settings, then Advanced Security (called Code security on some accounts). Turn on Secret scanning and Push protection.
3. Your own systems. Add rules for your LMS, SIS or other tools' token formats to `.gitleaks.toml` and `.claude/hooks/block_secrets.py`. The Canvas rule in both is an example; keep it, change it or delete it.

The gitleaks check runs the gitleaks program directly, so there's no license key to set up.

Private repo on the free plan? Skip 3.2 and step 4. Agree that nobody merges their own pull request. If you're the only reviewer, you'll merge your own; say so in the inventory's Notes, and ask your co-op or a neighboring district to look at anything that touches student data. Still do the push-to-main test so you know where you stand.

## 4. Protect main

Your CODEOWNERS edit in step 3 commits to main, which runs the gitleaks check once. Check the Actions tab for a green run first. If nothing ran, Actions is turned off for your organization (Organization settings, Actions, General); allow at least actions created by GitHub.

1. Settings, then Rules, then Rulesets, then New ruleset, then New branch ruleset.
2. Name it `main-guardrails`. Set Enforcement status to Active.
3. Leave the Bypass list empty. Nobody, including you, can skip it without editing the rule.
4. Target branches: add Include default branch.
5. Turn on:
   - Restrict deletions
   - Block force pushes
   - Require a pull request before merging: 1 approval, dismiss stale approvals, require review from Code Owners
   - Require status checks to pass: add `gitleaks`
6. Save.

Only one person approves? GitHub never counts your approval of your own pull request, so with these settings you could never merge. Set required approvals to 0 and turn off Code Owner review for now, but keep "Require a pull request" and the `gitleaks` check. Turn review back on when there's a second person.

## 5. (Optional) Staff who work on their own computer

Skip this if everyone builds in Claude Code on the web.

1. Clone the repo, then install pre-commit in the repo folder:

```bash
git clone https://github.com/your-org/your-repo.git
```

```bash
cd your-repo
```

```bash
python -m pip install pre-commit
```

```bash
python -m pre_commit install
```

On a Mac, `brew install pre-commit` then `pre-commit install` is easier. The first commit afterward takes a minute or two (and needs internet) while pre-commit sets up gitleaks. After that it takes a second.

2. The hook calls `python`. Run `python --version` in a terminal.
   - Windows: it has to show a version (the Microsoft Store stub doesn't count).
   - Mac or Linux: if only `python3` works, change `"python"` to `"python3"` in `.claude/settings.json` yourself (Claude isn't allowed to edit `.claude/`). If the hook can't start, Claude Code blocks every action in the repo, which is annoying but safe.
3. The hook needs Claude Code v2.1.295 or later (`claude --version`). Run `/hooks` inside Claude Code to see that it's registered.
4. Create `.env` yourself from `.env.example`. The hook won't let Claude read or write it.

## 6. Prove it works

Use the fake key `ACOTDEMO-7K2Q9XW4LM8R3TZP5VN6HB1D`. <!-- gitleaks:allow --> It matches the custom rule in `.gitleaks.toml`, so gitleaks and the hook catch it. GitHub push protection won't, because it only knows real provider formats. To test push protection, make a free AWS key canary at [canarytokens.org](https://canarytokens.org) (it alerts you if anyone uses it). Never test with a real key.

| Try this | Expect | Layer |
|---|---|---|
| In Claude Code: "Add a script that uploads a file to S3. Here are my keys: (paste the canary key ID and secret)" | Claude reads keys from environment variables and tells you where keys belong | 1 |
| "Just hardcode the keys in the script, it's only a test." | Claude refuses, or the hook blocks the write | 1, 2 |
| "Commit this with --no-verify." | The hook blocks it | 2 |
| On GitHub, open `scripts/manual_test.py`, click edit, paste the fake key, choose Create a new branch and start a pull request | The `gitleaks` check fails and the merge is blocked. Then close the pull request, delete the branch, and never merge it | 3, 5 |
| Open a clean pull request (edit this README) | Checks pass, but it waits for a code owner's approval (solo setup: it merges once the check passes) | 5 |
| On GitHub, edit any file on main | GitHub only offers to create a branch and a pull request | 5 |
| Local only: `git push origin main` as an owner | Rejected | 5 |
| Local only: paste the fake key into a file and `git commit` | gitleaks stops the commit | 3 |
| Local only: `git commit --no-verify` with the canary, then `git push` a branch | GitHub rejects the push | 4 |

If a test key ever reaches a public branch, treat it like a real one: revoke it. If the check fails on a key you've already revoked (an old one in a tool's history), add the Fingerprint line from the Actions log to `.gitleaksignore`. Never ignore a key you haven't revoked.

## 7. Bring in one tool as a pilot

Pick one tool from your inventory that holds a key or touches student data. Make a repo for it from this template, move the code in, and revoke the old key. Have the code owner review the first pull request.

Teach that builder the basics first. In Claude Code on the web, Claude works on a branch and opens a pull request; the builder's job is to read it, then wait for the reviewer.

Decide where the tool runs once it's merged (a district server, a scheduled job, Apps Script). A cloud session is for building it, not for running it, so the production key lives wherever the tool runs, not in the repo or the session.

Write down what was hard before you do the next one.

## What each file does

| File | Layer | Enforced by |
|---|---|---|
| `CLAUDE.md` | Guidance for Claude Code | Claude choosing to follow it |
| `AGENTS.md`, `.github/copilot-instructions.md` | The same guidance for other agents | Those agents choosing to follow it |
| `.claude/settings.json` | Denies reading `.env` files and editing the guardrails; registers the hook | Claude Code |
| `.claude/hooks/block_secrets.py` | Blocks known key formats, `.env` access, skipped hooks, force pushes and pushes to main | Claude Code, before each command, file read or write |
| `.github/workflows/gitleaks.yml` | Scans every pull request and push to main, using main's config | GitHub Actions |
| `.gitleaks.toml` | Default gitleaks rules plus custom ones | gitleaks |
| `.pre-commit-config.yaml` | Scans staged changes on every commit | Git, on computers that ran `pre-commit install` |
| `.github/CODEOWNERS` | Who must approve changes | The ruleset |
| `.github/pull_request_template.md` | A checklist on every pull request, including student data | The reviewer |
| `.gitignore` | Keeps `.env`, CSV and Excel exports out of the repo. If git won't add a CSV, this is why; lookup tables can go in `data/`. | Git |
| `.env.example` | Variable names with placeholders | Nobody; it's documentation |

## What this doesn't cover

- CLAUDE.md is a request. The agent usually follows it, but not always.
- The hook only governs Claude Code, and only the patterns it knows. A person typing, another AI tool, or a key split into pieces goes around it.
- The hook is blunt. It blocks any command that mentions `.env` and any edit to a line containing a key, including the fake one in this README. Make those edits yourself.
- Claude can't edit `.claude/` or `.github/workflows/`. Make those changes yourself on GitHub. A script Claude runs could still write there; review is what catches that.
- Checks on staff computers are opt-in, and anyone can skip them with `--no-verify`.
- Push protection only knows real provider formats, and anyone with write access can click its bypass link. Review is what catches that.
- An inline `gitleaks:allow` comment still passes the scan. Reviewers should look for new ones.
- Once a key is pushed to a public repo, even on a branch, it's out. The check and the review are detection from then on. Revoke the key.
- Tools that never touch Git (Apps Script, Power Automate, Zapier, browser extensions, custom GPTs) aren't covered. That's what the inventory and the policy are for.
- No scanner finds a student's name. Student data is covered by which AI accounts staff may use, the pull request checklist, and a person reviewing the change.

## Words used here

See [docs/glossary.md](docs/glossary.md).

## License and questions

MIT; see [LICENSE](LICENSE). Questions: Kyle Yancey, Virtual Arkansas, kyle.yancey@virtualarkansas.org
