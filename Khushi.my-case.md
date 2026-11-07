# Case: Maya Chen — Prioritizing Topanga districts for evening security follow-up

## 1. The person and the decision

Maya Chen is a fictional CVS District Asset Protection Manager responsible for stores serving the Topanga area of Los Angeles. At her weekly security review, she must decide which LAPD reporting districts to investigate first before proposing additional evening guard coverage. Her decision is local and tactical, not the citywide quarterly budget allocation handled by Ana in another team case. If she treats district-wide police offense counts as CVS store incidents, she could recommend guards for the wrong locations.

## 2. Their real situation and alternatives

CVS Health's District Asset Protection Leader job listing describes responsibilities connected with preventing losses and coordinating asset protection across stores (Source 1). A CVS Asset Protection Coordinator listing describes store-level loss-prevention work (Source 2). For Maya, the practical decision is not simply which district has the most police reports: she needs to know which CVS stores are actually in that district, which stores have experienced theft or threats, what coverage they already have, and whether an additional guard would be worth the cost. The app does not contain those internal facts.

Without the app, Maya could compare store incident logs and speak to store managers, or manually filter the City of Los Angeles/LAPD public offense dataset (Source 3) by area, time and offense type. Store records are closer to the guard-placement decision, but they do not by themselves show patterns in surrounding reporting districts. Manually aggregating LAPD records could provide that context, but would require more time and care with definitions. Maya's goal is a reliable shortlist for **further local investigation**, not an automatic guard assignment.

**Sources:**

- Source 1: CVS Health, *District Asset Protection Leader* (job listing): https://cvshealth.wd1.myworkdayjobs.com/en-us/cvs_health_careers/job/district-asset-protection-leader--inland-empire-_r1037308
- Source 2: CVS Health, *Asset Protection Coordinator* (job listing): https://cvshealth.wd1.myworkdayjobs.com/en-US/CVS_Health_Careers/job/Asset-Protection-Coordinator_R0936174
- Source 3: City of Los Angeles / LAPD, *LAPD NIBRS Offenses Dataset*: https://data.lacity.org/Public-Safety/LAPD-NIBRS-Offenses-Dataset-2026-to-Present/k7nn-b2ep

## 3. The app in use

**Live link:** https://dso576-project-m1.streamlit.app/

**What Maya selects:** LAPD Areas = **Topanga**; Reporting period = **Most recent complete quarter (July 1–September 30, 2026)**; Ranking measure = **Combined offenses**. She does not upload a verified CVS store-mapping CSV.

![Actual live-app screenshot showing Topanga filters, district ranking and the store-mapping warning](maya-topanga-live-cropped.png)

**What Maya sees:** The table highlights five priority reporting districts in red. District 2156 has 41 shoplifting offense rows and 3 robbery offense rows (**44 combined**). District 2143 has 20 and 1 (**21**); 2114 has 8 and 0 (**8**); 2126 has 1 and 2 (**3**); and 2158 has 2 and 0 (**2**). The bar chart shows the same order. The yellow warning says no verified CVS store mapping is loaded, so no individual CVS store recommendation can be made.

## 4. Reading the result for their decision

**Does the number measure what Maya cares about?** Only partly. The measure is a **total of charged offense rows**, not a rate per CVS store, not a count of distinct police reports, and not a forecast of incidents prevented by a guard. The top district's 44 rows are a useful signal for where to investigate first, but they do not establish that a CVS store there has the greatest need.

**Who is in the rows, and who is not?** In the selected app view, rows concern Topanga reporting districts, shoplifting and robbery offenses, and evening hours (18:00–24:00) in the displayed July–September 2026 period. Other areas, offenses, hours and periods are excluded from this view. The public dataset cannot capture unreported incidents; without verified store mapping, the rows cannot be attributed to particular CVS locations. The app explicitly warns that these are **charged offense rows, not distinct reports**.

**What outside the data matters?** Maya needs verified CVS store addresses mapped to reporting districts, internal loss and incident logs, guard staffing and costs, store hours, and observations from store managers. Even a district with many police offenses may have no CVS store or a store with adequate existing coverage.

**What could Maya wrongly conclude?** She could read the 44 combined offense rows for district 2156 as 44 CVS incidents and immediately assign a guard there. That would mistake a district-wide police count for store-specific evidence and would skip checking whether the relevant store is in that district at all.

**Check run — independently recomputing totals from the screenshot:** This is an arithmetic consistency check of the **live app's displayed shoplifting and robbery columns**, not an independent recount of the underlying source records.

```text
District  Shoplifting  Robbery  Recomputed combined
2156      41           3        44
2143      20           1        21
2114       8           0         8
2126       1           2         3
2158       2           0         2

Top-five total = 44 + 21 + 8 + 3 + 2 = 78
District 2156 exceeds 2143 by 23 offense rows.
```

The recomputed totals agree with the ranking order in the bar chart. This verifies the visible addition and ordering only; it does **not** prove that the underlying source records were counted correctly or that the districts are comparable on a per-store basis. In the absence of verified CVS store counts, a district-level offense **rate per store** cannot be calculated.

## 5. The verdict: prove or break

Maya is better off using the app **alongside** store incident logs and manager input than relying on either alone. Compared with manually grouping LAPD records, the app gives her a quick, understandable Topanga shortlist, with a ranked table, chart and downloadable results. Compared with internal store reports, it adds surrounding district context. It should **not** be used to assign guards to specific CVS stores or blocks, estimate guard effectiveness, or claim that the highest-count district is necessarily the highest-risk store location.

**Verdict: useful for triage, but needs one improvement.** The existing store-mapping warning is appropriate. However, the app could better guide the next step after identifying priority districts without pretending it knows where to place guards.

```markdown
### CR: Add a district investigation checklist to the ranked CSV

- **From:** Maya Chen case (Khushi Ahir), November 2026
- **Part:** Topanga ranked-district export / follow-up workflow
- **Evidence:** With Topanga, Jul–Sep 2026 and Combined offenses selected, the app ranks 2156 first (44 rows), but warns that no verified CVS store mapping is loaded. The ranking does not say which CVS store, if any, should receive a guard.
- **Change:** Offer a downloadable follow-up checklist beside the ranked CSV with the ranked district, offense counts, verified CVS store/district match (blank until checked), store incident history, existing guard coverage, manager confirmation, and next review date. Label it “Investigation only — not a guard placement recommendation.” Keep the current warning.
- **Who benefits:** Any district asset protection manager reviewing local priorities, not only Maya or Topanga.
- **Why it does not harm other users:** It adds an optional investigation workflow without changing the rankings or implying unsupported store-level precision.
- **Priority:** Medium
- **Status:** Proposed; confirm with the team before adding to change-requests.md.
```
