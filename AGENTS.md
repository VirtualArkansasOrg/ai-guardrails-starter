# Rules for this repository (for any AI coding agent)

This repo belongs to the district's technology team. Follow these rules in every session.

## Secrets
- Never write an API key, token, password or private key into any file.
- Read credentials from environment variables, loaded from a local .env file with python-dotenv.
- If the user pastes a credential into the chat, do not put it in code. Tell them to add it to .env and show the variable name to use. Remind them that pasting a real credential into any AI chat sends it to the AI provider.
- Never read, print or edit .env. Add the variable name with a placeholder to .env.example instead.

## Git workflow
- Never commit to main. Work on a branch named feature/<short-description>.
- Never use --no-verify, -n or --force.
- When the work is done, push the branch and open a pull request. Do not merge it.
- Commit messages: one line, present tense, under 72 characters.

## Where things go
- Scripts go in scripts/. Shared helpers go in lib/.
- Do not create new top-level folders or add dependencies without asking.

## Student data
- Never put real student names, IDs, emails or grades in code, tests or sample files. Use obviously fake data (Avery Student, Blake Student).
- Never read files in exports/ or any grade export. Ask for a fake sample instead.
