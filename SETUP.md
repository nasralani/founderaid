# founderAid MVP — setup (≈15 min)

## 1. Response logging (Google Sheet)
1. Create a Google Sheet "founderAid MVP data" and share it with the team.
2. Extensions → Apps Script → paste `apps-script.gs` → Save.
3. Deploy → New deployment → Web app → Execute as **Me**, Access **Anyone** → Deploy → authorise.
4. Copy the `/exec` URL into `index.html`: `captureUrl: "https://script.google.com/.../exec"`.
5. Optional: change prices in `CONFIG.prices` to your team's agreed tiers.

## 2. Host it (free, public link)
- **Netlify Drop:** go to app.netlify.com/drop and drag the `founderaid-mvp` folder in. Done.
- **Or GitHub Pages:** new repo → upload `index.html` → Settings → Pages → deploy from `main`.

## 3. Share with tracked links
Add `?src=` so you can tell channels apart:
- `…/?src=linkedin` · `…/?src=reddit` · `…/?src=facebook` · `…/?src=network`
- `…/?src=class` (classmates — report separately as convenience sample)
- `…/?src=team` (your own testing — excluded from analysis)

## 4. Analyse
Sheet → File → Download → CSV, then:
`python3 analyze.py events.csv`
It prints the funnel and an H1/H2/H3 scorecard for the slides.

## What gets logged
visit · checklist_generated (inputs) · source_link_click · rating · feedback_text · survey (5 answers) · tier_click · email_signup.
No names. Email only if the user volunteers it — delete emails before sharing data.

## H4 accuracy test (no users needed)
Generate checklists for 5 business types; check each step against BizPaL and the linked official pages. Record correct / missing / wrong per step.
