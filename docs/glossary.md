# Words used here

| Word | Plain meaning |
|---|---|
| Repository (repo) | A project folder, with the full history of every change |
| Commit | A saved snapshot of the changes |
| Push | Uploading commits to GitHub |
| Branch | A draft copy where someone works without touching the live version |
| Main | The live version |
| Pull request (PR) | A request to merge a branch into main, where someone reviews it |
| Code owner | The person or team who must approve changes |
| Check / CI / Actions | Automatic scans GitHub runs on its own servers for every pull request |
| Pre-commit | A check that runs on your own computer before a commit is saved |
| Hook (Claude Code) | A script Claude Code runs before each action it takes, which can block the action |
| CLAUDE.md / AGENTS.md | Instructions the AI agent reads at the start of each session |
| gitleaks | A free scanner that looks for passwords, keys and tokens |
| Push protection | GitHub refusing an upload that contains a known key format |
| Ruleset | GitHub settings that protect main (require review, require checks) |
| Bypass list | Who is allowed to skip a ruleset. Leave it empty. |
| `.env` | A local file that holds real keys. It's never committed. |
| Canary token | A fake credential that alerts you when someone tries to use it |
