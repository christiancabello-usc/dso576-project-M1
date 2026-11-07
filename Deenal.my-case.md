# Case: Rita — CVS Wilshire Store Manager's Security Request

## 1. The person and the decision

Rita is the on-site general manager of a CVS store in the Wilshire area of Los Angeles. At her next store safety review, she must decide whether to submit a request for additional evening security coverage for her own store. If she requests coverage without sufficient evidence, the store may incur unnecessary costs; if she fails to request it when needed, employees and customers may face avoidable safety concerns. Rita can request extra security, but approval and deployment may depend on CVS leadership.

## 2. Their real situation and alternatives

Rita's decision starts with what she sees at her store: employee concerns, incidents reported to management, inventory losses, customer complaints, and current guard coverage. CVS Health's asset-protection roles show that preventing losses and coordinating store safety are ongoing operational responsibilities (Source 1). Retail-industry reporting from the National Retail Federation also documents the importance of theft and violence concerns in retail settings (Source 2). Neither source establishes that Rita's specific store needs a guard; that must be checked locally.

Without the app, Rita could review internal incident logs, speak with employees and district asset-protection staff, or manually inspect public LAPD crime data (Source 3). Internal records describe her own store more directly, but may miss broader neighborhood patterns. The app adds a faster view of surrounding reporting-district offenses, although those are not the same as CVS incidents and cannot determine the benefit or cost of hiring a guard.

**Sources:**

- Source 1: CVS Health, *Asset Protection Coordinator* (career listing): https://jobs.cvshealth.com/
- Source 2: National Retail Federation, *Retailers See Fraud Schemes Evolve as Shoplifting Declines, NRF Study Finds* (2026): https://cdn.nrf.com/media-center/press-releases/retailers-see-fraud-schemes-evolve-as-shoplifting-declines-nrf-study-finds
- Source 3: City of Los Angeles / LAPD, *LAPD NIBRS Offenses Dataset*: https://data.lacity.org/Public-Safety/LAPD-NIBRS-Offenses-Dataset-2026-to-Present/k7nn-b2ep

## 3. The app in use

**Live link:** https://dso576-project-m1.streamlit.app/

**What Rita selects:** Rita opens the public app and chooses the LAPD area that covers her Wilshire CVS location, after checking the store's actual reporting-district boundary. She selects the most recent complete reporting period and **Combined offenses** to review evening shoplifting and robbery patterns. **Important:** “Wilshire area” is not enough to identify her exact LAPD reporting district; the store's address and boundary must be verified first.

**Screenshot to insert:** Capture the live app with the verified LAPD area, reporting period, ranking measure, and district table visible. Save the image beside this Markdown file and replace the placeholder below with its actual path.

![Live-app screenshot of Rita's verified LAPD area and evening district ranking — INSERT ACTUAL SCREENSHOT](screenshots/rita-wilshire-live.png)

**What Rita sees:** The app provides a ranked view of evening shoplifting and robbery offense rows for the selected reporting districts. Rita can identify districts worth investigating, but the ranking does not prove that any particular CVS store experienced those incidents. **Record the actual top district, shoplifting count, robbery count, and combined count from the live screenshot here before submission.** Do not substitute numbers from Hollywood or Topanga.

## 4. Reading the result for their decision

**Does the number measure what Rita cares about?** Partly. The app's combined offense count summarizes police offense rows in a reporting district during the selected hours and dates. Rita needs to decide whether *her specific CVS store* warrants extra guard coverage. District-wide totals are context, not a store-level risk rate, a forecast, or a measure of security effectiveness.

**Who is in the rows, and who is not?** The selected rows cover the chosen LAPD area, reporting districts, time window, and included shoplifting/robbery offenses. They exclude other offenses, unreported events, and store-specific events that do not appear in police data. A charged offense row is not necessarily a distinct police report, and it is not necessarily a CVS incident.

**What outside the data matters?** Rita should check her store's exact reporting district, internal incident history, employee concerns, opening hours, current coverage, guard costs, and CVS approval policies. The app cannot tell her whether the store has already hired guards or whether a guard would prevent a particular number of incidents.

**What could Rita wrongly conclude?** She might interpret a high-ranked district as proof that her store needs security immediately, even if the store is outside that district or its own incident logs show a different pattern. Conversely, a low district count does not prove that her store is safe.

**Check to complete against the live app:** After recording the selected district's displayed counts, recompute `shoplifting + robbery = combined` and check that the ranked table orders the displayed totals correctly. Write the actual numbers and result below. This is a display-consistency check only, not an independent recount of the source data.

```text
Verified LAPD area: [enter]
Verified reporting district containing CVS store: [enter]
Selected dates: [enter]
Shoplifting rows: [enter]
Robbery rows: [enter]
Recomputed combined rows: [enter]
Displayed combined rows: [enter]
Check result: [enter]
```

## 5. The verdict: prove or break

Rita is better off using the app **together with** her store's incident logs and employee reports than using district rankings or internal observations alone. The app makes surrounding evening offense patterns easier to inspect than manually aggregating police data. It should **not** be used by itself to approve a guard, attribute district offenses to CVS, or claim that added security will reduce incidents.

**Verdict: useful context, but the single-store request workflow needs improvement.** A store manager needs a clear way to connect a district-level pattern to the specific location she manages and to document the evidence for a request.

```markdown
### CR: Add a store-level security request evidence checklist

- **From:** Deenal — Rita CVS Wilshire store manager case, November 2026
- **Part:** Ranked district results / follow-up decision
- **Evidence:** The app ranks LAPD reporting districts by evening offense rows, but the ranking alone does not verify which district contains Rita's CVS or whether that store has experienced incidents.
- **Change:** Add an optional downloadable checklist for store managers: verified store address and reporting district, selected period, district offense counts, store incident log summary, employee concerns, existing coverage, requested hours, and approval status. Label it “Evidence for review — not an automatic security recommendation.”
- **Who benefits:** CVS store managers and district asset-protection staff preparing or evaluating local security requests.
- **Why it does not harm other users:** It adds an optional store-level follow-up without changing the app's existing district rankings or overstating the precision of police data.
- **Priority:** Medium
- **Status:** Proposed; confirm with the team before adding to change-requests.md.
```
