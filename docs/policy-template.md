# A one-paragraph policy

A starting point, written for a school district. Swap "district" and "superintendent" for your own organization's terms, change anything else to fit, and have your attorney check it against FERPA, state privacy law and your board policy before it goes to the board.

> Staff may use AI tools the district has approved to build software for district work. Any tool that uses district credentials, reads or stores student or staff records, or is used by anyone besides the person who built it is listed in the district's tool inventory, kept where the district can see it (code goes in the district's code repository), and approved by a technical owner the superintendent names before it goes into use and before each change goes out. Passwords, keys and tokens are never written into code or pasted into an AI tool. Student and staff records go only into AI accounts the district has approved for that data. Staff who built such tools before this policy list them in the inventory by [date]. Listing a tool won't by itself lead to discipline, and the technology department will help bring it in.

## Why each part is there

- "Uses district credentials, reads or stores student or staff records, or is used by anyone besides the person who built it." This is the scope. A teacher's personal flashcard script is out; a grade export is in.
- "Listed in the district's tool inventory." Covers tools that can't live in a code repository (Apps Script, Power Automate, browser extensions, custom GPTs). See [tool-inventory.csv](tool-inventory.csv).
- "Kept where the district can see it." If it's in the district's organization, IT can see it, and it survives the builder leaving. The policy doesn't name a product, so it doesn't need a board vote when you change tools.
- "A technical owner the superintendent names." A second person signs off. Name a person and a backup, and make review part of their job. One-person department? The technical owner can't approve their own tools; name a reviewer at your co-op or another district for those.
- "Never pasted into an AI tool." Pasting a key or a student list into an AI chat sends it to the AI provider.
- "By [date]" and "won't by itself lead to discipline." Without a no-blame line, staff stop telling you what they've built, and the tools stay invisible. "By itself" is there on purpose: it doesn't excuse deliberate misuse of data, and it doesn't change the district's duty to report a breach.
