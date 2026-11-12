# Staff-Built AI Tools on One Page

For superintendents, directors and boards. From the ACOT 2026 session "Your Staff Are Already Building Apps with AI: A Governance Model That Works" (Kyle Yancey, Virtual Arkansas). Edit it to fit your district before you pass it on.

## The situation

AI coding agents let staff who have never written code build working software: scripts, browser extensions, small web apps. Much of it is useful. Much of it is invisible to IT. Banning it would push it onto personal accounts, where nobody can see it at all.

## The risks

- Keys in code. Passwords and access tokens (often with admin access) typed into scripts. Bots scan public code for keys, so treat any key that goes public as stolen.
- Student data in unvetted tools. Records flowing through AI services nobody reviewed, on personal-account terms.
- One-laptop tools. A tool the department depends on leaves with the person who built it.
- Unreviewed updates. A quick change goes to everyone with no second look.

## What the technology department recommends

1. One place. Every staff-built tool is in the district's code repository, or on the inventory if it can't be.
2. A second person signs off. Anyone can build. A named technical owner approves before it goes to anyone else.
3. Automatic checks. Free scanners check every change for common key formats before it's merged.
4. District-approved AI accounts. Student data goes only into AI accounts covered by a district agreement.
5. No blame for disclosing tools that already exist, if they're listed by a set date.

## What it costs

- Public repositories are free, but anyone can read the code. Most district tools should be private.
- Private, with enforced review: GitHub Team, $4 per person in the organization per month (list, Nov 2026). Keep the organization to builders and reviewers. Example: 12 people x $4 x 12 months = $576 a year.
- Push protection on private repositories (optional): GitHub Secret Protection, $19 per active committer per month (list, Nov 2026). Example: 10 committers = $2,280 a year. The free scanning covers much of this.
- District-approved AI accounts: priced per seat by each vendor, and usually the biggest line. Get quotes.
- Reviewer time: the real cost. Put it in someone's job description.

Check current prices before budgeting.

## What we're asking for

- Send the one-paragraph policy ([policy-template.md](policy-template.md)) to the district's attorney and toward a board agenda.
- Name a technical owner and a backup for staff-built tools, and make review part of their job.
- Decide which AI accounts the district pays for, and which may hold student data.
- Approve a free GitHub organization and one pilot tool.
