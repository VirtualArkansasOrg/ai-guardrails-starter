# Staff-built AI tools: a one-page brief

For superintendents, directors and boards. From the ACOT 2026 session "Your Staff Are Already Building Apps with AI: A Governance Model That Works" (Kyle Yancey, Virtual Arkansas).

## The situation

AI coding agents let staff who have never written code build working software: scripts, browser extensions, small web apps. Much of it is useful. Most of it is invisible to IT. Banning it would push it onto personal accounts, where nobody can see it at all.

## The risks

- **Keys in code.** Passwords and access tokens (often admin-level) typed into scripts. Once one is public, strangers try it within minutes or hours.
- **Student data in unvetted tools.** Records flowing through AI services nobody reviewed, on personal-account terms.
- **One-laptop tools.** A tool the department depends on leaves with the person who built it.
- **Unreviewed updates.** A quick change goes to everyone with no second look.

## What we recommend

1. **One place.** Every staff-built tool that matters lives in the district's GitHub organization.
2. **A second person signs off.** Anyone can build. A named technical owner approves before it ships.
3. **Automatic checks.** Free scanners catch keys before they're saved or merged.
4. **District-managed AI accounts.** Student data goes only into AI accounts with terms the district controls.
5. **No penalty** for bringing in tools that already exist.

## What it costs

- Public repositories: free.
- Private repositories with enforced review: GitHub Team, $4 per user per month (Nov 2026 list price), for the people who build and review.
- Push protection on private repositories: GitHub Secret Protection, $19 per active committer per month (Nov 2026 list price). Optional; free scanning covers much of the gap.
- The real cost is reviewer time: someone has to own the reviews.

Check current prices before budgeting.

## What we're asking for

- Adopt the one-paragraph policy ([policy-template.md](policy-template.md)).
- Name a technical owner (a person or small team) who approves staff-built tools.
- Decide which AI accounts the district pays for, and which may hold student data.
- Approve a free GitHub organization and one pilot tool.
