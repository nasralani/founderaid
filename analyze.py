"""founderAid MVP — hypothesis scorecard.
Usage: export the 'events' sheet as CSV (File > Download > CSV), then:
    python3 analyze.py events.csv
Excludes sessions tagged src=team (your own testing).
"""
import csv, json, sys
from collections import Counter, defaultdict

rows = list(csv.DictReader(open(sys.argv[1], encoding="utf-8")))
rows = [r for r in rows if r.get("source") != "team"]
by = defaultdict(list)
for r in rows:
    r["d"] = json.loads(r.get("details") or "{}")
    by[r["session"]].append(r)

def sessions_with(ev):
    return {s for s, evs in by.items() if any(e["event"] == ev for e in evs)}

visits = set(by)
gen = sessions_with("checklist_generated")
tier = sessions_with("tier_click")
paid_tier = {s for s in tier if any(e["event"] == "tier_click" and e["d"].get("tier") in ("launch", "business") for e in by[s])}
emails = sessions_with("email_signup")
links = sessions_with("source_link_click")
survey = [e["d"] for evs in by.values() for e in evs if e["event"] == "survey"]
ratings = Counter(e["d"].get("rating") for evs in by.values() for e in evs if e["event"] == "rating")

founders = [a for a in survey if a.get("q1_started") in ("yes_recent", "yes_older")]
missed = [a for a in founders if a.get("q2_missed") == "yes"]
used = Counter(u for a in survey for u in (a.get("q3_used") or "").split("|") if u)
paid = [a for a in survey if a.get("q5_paid") not in ("", "no", "na", None)]
hours = Counter(a.get("q4_hours") for a in survey)

def pct(a, b): return f"{a}/{b} ({100*a/b:.0f}%)" if b else f"{a}/0"

print("=== FUNNEL ===")
print("Unique visitors:", len(visits))
print("Generated checklist:", pct(len(gen), len(visits)))
print("Clicked an official source link:", pct(len(links), len(gen)))
print("Clicked a paid tier (Launch/Business):", pct(len(paid_tier), len(gen)))
print("Left email:", pct(len(emails), len(gen)))
print("Sources:", dict(Counter(by[s][0]["source"] for s in visits)))
print("\n=== HYPOTHESES ===")
print("H1 Problem — founders who missed/learned late about a requirement:", pct(len(missed), len(founders)), " target >=50%")
print("H2 Alternatives — tools used:", dict(used))
print("   Paid someone for help:", pct(len(paid), len(survey)))
print("   Hours spent:", dict(hours))
print("H3 Value/WTP — paid-tier clicks among checklist users:", pct(len(paid_tier), len(gen)), " target >=30%")
print("   Ratings:", dict(ratings))
print("\nSurvey responses:", len(survey), "| of which actual founders:", len(founders))
print("Sectors:", dict(Counter(e["d"].get("sector") for evs in by.values() for e in evs if e["event"] == "checklist_generated")))
