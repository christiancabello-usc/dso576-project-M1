# Case: Jordan Kim — Prioritizing mobile security-supervisor visits

## 1. The person and the decision

Jordan Kim is the Los Angeles operations supervisor for CVS's contracted security vendor. At the start of each quarter, Jordan uses the exported priority list to decide which LAPD Areas need a mobile supervisor's evening site visits first, so guards assigned to high-priority districts receive training, post-order checks, and incident-report support. A poor decision can leave guards at the busiest locations without oversight and weaken the quality of the incident information CVS relies on. Jordan does not decide CVS's budget or which specific district receives a new guard.

## 2. Their real situation and alternatives

Jordan would normally plan support visits from the security vendor's post orders, guards' incident reports, and calls from CVS store managers. This fits the role: security guards in retail protect people, merchandise, money, and equipment, while California's required guard-training topics include observation, documentation, communication, post orders, site-specific training, and reporting procedures. Jordan's goal is to make sure guards at higher-priority locations receive supervision and support without taking oversight time away from other posts.

The app gives Jordan a faster, consistent way to compare all LAPD Areas using reported evening shoplifting and robbery counts, then identify reporting districts where a supervisory visit may be most useful. However, Jordan must still check the vendor schedule, CVS store locations and hours, guard incident reports, and store-manager concerns before choosing a specific visit. The LAPD source contains reported NIBRS offenses—not CVS-only incidents or proof that a particular guard post needs intervention—and one incident can contain multiple offense records. Jordan's alternatives are reviewing vendor reports and schedules, calling store managers, and filtering the public LAPD data directly.

**Sources:**

- [Security Guards and Gambling Surveillance Officers, U.S. Bureau of Labor Statistics](https://www.bls.gov/ooh/protective-service/security-guards.htm)
- [Security Guard Training, California Bureau of Security and Investigative Services](https://www.bsis.ca.gov/industries/g_train.shtml)

## 3. The app in use

**Live link:** https://dso576-project-m1.streamlit.app/

**What they select:** All 21 LAPD Areas; **Previous 12 months (Aug 2025–Jul 2026)**; and **Robbery first**.

**Screenshot:** Capture the live page after making these selections. It should show all Areas selected in the sidebar, the robbery-first measure, a combined all-districts ranking, the top 10 districts, and the first five highlighted in red.

**What they see:** The app's first five districts are 77th Street 1239 (23 robberies), Central 0162 (22), Rampart 0246 (21), Rampart 0245 (21), and Hollywood 0648 (20). Jordan uses this as a priority route for mobile evening guard-support visits, including post-order checks, training, and incident-report follow-up—not as a decision to add guards or identify a specific CVS store.

## 4. Reading the result for their decision

**Does the number measure what this person cares about?** Partly. The ranking measures reported evening shoplifting and robbery offense rows, which helps Jordan identify districts where contracted guards may need mobile-supervisor support first. For the selected period, the app retains 5,152 qualifying offense rows; 77th Street district 1239 ranks first with 23 robbery offenses and 39 combined offenses. Robbery-first fits Jordan's safety-focused oversight role because retail guards protect people and property and respond to theft and emergencies. However, the number does not directly measure guard performance, CVS-specific incidents, training needs, or whether a supervisor visit will prevent harm. [BLS, *Security Guards and Gambling Surveillance Officers*](https://www.bls.gov/ooh/protective-service/security-guards.htm)

**Who is in the rows, and who is not?** The rows are LAPD-reported offenses in the City of Los Angeles coded as shoplifting (23C) or robbery (120), occurring from 18:00 through 23:59 and from August 1, 2025 through July 31, 2026. They are charged offense rows, not distinct reports, actual crime, or CVS incidents. The data leave out unreported offenses, CVS store locations unless Jordan uploads a verified mapping, guard-post schedules, vendor incident reports, and prior supervisor visits. The LAPD dataset identifies offense records and geography, but it does not identify a CVS store or contracted guard post. [City of Los Angeles, *LAPD NIBRS Offenses Dataset*](https://data.lacity.org/d/k7nn-b2ep)

**What outside the data matters to this decision?** Jordan must check which CVS locations actually have guards, their evening schedules, post orders, recent vendor incident reports, guard training status, store-manager concerns, and the time required to travel between sites. California's guard-training guidance includes site-specific post orders, observation and documentation, communication, emergency response, and reporting procedures—information that is not in LAPD offense data. [California BSIS, *Security Guard Training*](https://www.bsis.ca.gov/industries/g_train.shtml)

**What could they wrongly conclude from it?** Jordan could wrongly conclude that the first-ranked district automatically needs the next supervisory visit. A high robbery count does not prove that a CVS operates there, that a guard is assigned there, or that the guard needs support. Jordan should use the ranking as a starting point for a visit route, then verify vendor and store information before scheduling the visit.

```text
Selection check:
All 21 LAPD Areas
Occurrence dates: 2025-08-01 through 2026-07-31
Evening time: 18:00–23:59
Codes: 23C shoplifting and 120 robbery
Ranking measure: Robbery first

Qualifying charged offense rows: 5,152
Rank 1: 77th Street, RPT Dist 1239 — 16 shoplifting, 23 robbery, 39 combined
```

## 5. The verdict: prove or break

Jordan is better off using the app as a first-pass, citywide triage tool. Compared with manually filtering LAPD's public data or relying only on store-manager calls and vendor reports, the app gives Jordan one consistent, reproducible robbery-first ranking across all Areas and preserves the shoplifting and combined-offense context. It should not be used to assign a guard, evaluate guard performance, claim that a supervisor visit will reduce crime, or choose an individual CVS location without a verified store mapping and vendor scheduling information.

**Verdict: break with a change request.** The app can identify where reported evening offenses are concentrated, but it cannot tell Jordan whether a district has an active guard post or whether that post has recently received supervisory support. Adding an optional, non-personal guard-post and visit-status upload would improve Jordan's routing decision without changing the underlying crime counts or making other users' answers worse.

```markdown
### CR-11: Add guard-post and supervisor-visit context to the combined ranking

- **From:** Christian Cabello, 2026-11-06
- **Part:** Combined district ranking and CSV export
- **Evidence:** Jordan can rank all Areas by robbery-first counts, but the result does not show whether a CVS guard post exists in a district, whether it is staffed during the evening, or when a mobile supervisor last visited. A high-ranked district may therefore receive a visit even when no contracted guard needs support there.
- **Change:** Allow an optional verified upload with Area, reporting district, guard-post identifier, evening-post status, and last supervisor-visit date. Show those fields beside the combined ranking and export them, while leaving offense counts and rankings unchanged when no file is supplied.
- **Priority:** medium
- **Status:** open
```
