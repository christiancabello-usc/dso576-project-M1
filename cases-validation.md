# 2. Cases: does the app help real people with real decisions?

## Scope and evidence used in every case

The [CVS Evening Loss-Prevention Navigator](https://dso576-project-m1.streamlit.app/) is a first-pass investigation tool. It ranks **charged LAPD offense rows** for shoplifting (NIBRS 23C) and robbery (120) that occurred from 18:00 through 23:59. It is not a count of distinct police reports, CVS incidents, actual crime, individual-store risk, or the effect of a guard. The current committed source snapshot has 471,285 offense rows with unique offense IDs; the app ships a privacy-minimized subset of the two included offense codes.

The five cases below cover regional, district, store, vendor-supervision, and deliberately difficult store-hours decisions. All use the live app where their saved screenshot and selection remain reproducible. Cases marked **refresh before final PDF** contain screenshots or numbers recorded against an earlier app/data state and must be rerun on the current live app before submission.

| Persona | Decision | App role | Verdict |
| --- | --- | --- | --- |
| Ana, regional loss-prevention manager | Which areas/districts deserve quarterly guard-budget investigation | Citywide prioritization | Useful triage; not a store assignment |
| Maya, district asset-protection manager | Which Topanga districts to investigate before proposing coverage | Local district shortlist | Useful triage; not a CVS-store recommendation |
| Rita, Wilshire store manager | Whether to request additional security for one store | Context for a local request | Incomplete without verified store evidence |
| Jordan, vendor operations supervisor | Where to send mobile evening support visits | Cross-Area supervisory routing | Useful first pass; needs post/visit context |
| Elena, district leader | Whether one Central CVS should close at 10 p.m. | Difficult edge case | Not fit for this question without an hour split |

## Case 1 — Ana: regional quarterly allocation

### Person, situation, and alternatives

Ana is CVS Health's Regional Loss Prevention Manager in Los Angeles. Each quarter she must decide where to focus a limited evening-security budget and explain the resulting investigation shortlist to leadership. She currently combines store-manager intuition and monthly reports; those alternatives can blur daytime and evening patterns or require manual public-data work. The app gives a common definition of evening shoplifting and robbery across LAPD Areas and reporting districts. Retail asset-protection work also depends on store information and operational judgment, not a public count alone. [National Retail Federation retail-security context](https://cdn.nrf.com/media-center/press-releases/retailers-see-fraud-schemes-evolve-as-shoplifting-declines-nrf-study-finds) and [the LAPD NIBRS source](https://data.lacity.org/d/k7nn-b2ep) provide the external context.

### App in use and interpretation

Ana should select all 21 Areas, a stated comparison period, and a visible ranking measure; the sidebar comparison and the combined district list then give her a reproducible starting point for leadership discussion. The number measures where qualifying **reported offense rows** are concentrated, not loss dollars, CVS exposure, or the expected benefit of a guard. Rows include district-wide police offenses, including non-CVS locations; they omit unreported crime, CVS store locations, current guard posts, store hours, and internal shrink.

Ana must not conclude that the top district automatically receives a guard. She must first verify whether CVS operates in the district, the number of affected stores, internal incident patterns, existing coverage, and cost. The optional verified store-mapping upload helps connect a district to candidate stores but does not replace those checks.

**Verdict:** Ana is better off with the app for a transparent, citywide investigation shortlist than with manual public-data filtering alone. It is not sufficient to allocate guards to individual stores. The saved Ana case's Hollywood screenshot, older app URL, and reported values are **refresh before final PDF** evidence; they refer to a prior deployment/data state and should not be presented as current live-app results.

## Case 2 — Maya Chen: Topanga district follow-up

### Person, situation, and alternatives

Maya is a fictional CVS District Asset Protection Manager for stores served by the Topanga area. In her weekly review she must decide which reporting districts to investigate before recommending possible additional evening guard coverage. Asset-protection roles involve preventing losses and coordinating with stores, but her real decision also requires verified store locations, internal incident logs, current coverage, costs, and manager observations. Relevant sources are CVS's [District Asset Protection Leader listing](https://cvshealth.wd1.myworkdayjobs.com/en-us/cvs_health_careers/job/district-asset-protection-leader--inland-empire-_r1037308), [Asset Protection Coordinator listing](https://cvshealth.wd1.myworkdayjobs.com/en-US/CVS_Health_Careers/job/Asset-Protection-Coordinator_R0936174), and the [LAPD NIBRS dataset](https://data.lacity.org/d/k7nn-b2ep).

### App in use and interpretation

Maya selects Topanga, a named period, and Combined offenses, without assuming that a reporting district is a CVS store. The app displays a ranked table and chart with shoplifting, robbery, and combined charged-offense rows; it warns when no verified CVS mapping is loaded. Those counts are useful context for where to ask store managers questions, but are not a per-store rate, distinct incident count, or guard-effectiveness estimate.

The decision can be harmed if Maya treats district rows as CVS incidents or assigns a guard before confirming a CVS location and its internal evidence. She should use the app alongside store records, manager input, staffing information, and the optional mapping. A display-consistency check should recompute `shoplifting + robbery = combined` for the selected live table.

**Verdict:** Maya is better off with the app as a Topanga investigation shortlist, not as an automatic guard-placement system. Her saved July–September 2026 screenshot and numbers are **refresh before final PDF**: the current course snapshot ends July 2026 and the current “most recent complete quarter” label must be reviewed before use.

## Case 3 — Rita: single-store security request

### Person, situation, and alternatives

Rita is the on-site general manager of a CVS store in the Wilshire area. At a store-safety review she must decide whether to request additional evening coverage for that one location. She begins with employee concerns, internal incidents, loss, customer complaints, existing coverage, and the cost/approval process. The app can supplement those records with surrounding public-offense context; it cannot show that an offense happened at Rita's CVS. Sources include CVS's [Asset Protection Coordinator listing](https://jobs.cvshealth.com/), the [National Retail Federation's retail-security reporting](https://cdn.nrf.com/media-center/press-releases/retailers-see-fraud-schemes-evolve-as-shoplifting-declines-nrf-study-finds), and the [LAPD NIBRS dataset](https://data.lacity.org/d/k7nn-b2ep).

### App in use and interpretation

Rita must first verify her store's LAPD reporting district, then select its Area, an explicit period, and Combined offenses. The resulting district rank is context only: the rows are public offense records for shoplifting and robbery during the selected evening period, not store-level incidents or a prediction that a guard will work. A high district rank can coexist with no CVS store in the district; a low rank can coexist with a serious store-specific problem.

**Verdict:** Rita is better off only when she combines the app with exact location verification, store incident history, employee concerns, hours, current coverage, and costs. The saved Rita case intentionally leaves its screenshot and district values blank, so it is **not final evidence** until a verified live selection and screenshot are added. Its proposed follow-up is an optional store-request evidence checklist that preserves the ranking while documenting the required local checks.

## Case 4 — Jordan Kim: vendor-supervisor route

### Person, situation, and alternatives

Jordan is the Los Angeles operations supervisor for CVS's contracted security vendor. At the start of a quarter, he prioritizes evening mobile-supervisor visits so guards receive training, post-order checks, and incident-report support. Guards protect people and property, but their work includes observation, documentation, communication, and site-specific procedures; those operational facts are not in LAPD records. [BLS's security-guard profile](https://www.bls.gov/ooh/protective-service/security-guards.htm) and [California BSIS training guidance](https://www.bsis.ca.gov/industries/g_train.shtml) support that context.

### App in use and interpretation

Jordan selects all 21 Areas, **Previous 12 months (Aug 2025–Jul 2026)**, and **Robbery first**. The app returns one combined cross-Area top-10 list. In the committed course snapshot, the filter retains 5,152 qualifying charged-offense rows: 77th Street district 1239 is first with 16 shoplifting rows, 23 robbery rows, and 39 combined rows. The next four robbery-first rows are Central 0162 (22 robberies), Rampart 0246 (21), Rampart 0245 (21), and Hollywood 0648 (20).

This ranking measures a public geographic signal relevant to routing support, but not a guard's performance, a CVS-specific incident, an active post, a post's staffing, or the value of a supervisory visit. Jordan must check vendor schedules, post orders, guard reports, store locations and hours, past visits, travel time, and manager concerns before making a route.

**Verdict:** Jordan is better off with the repeatable citywide triage list than with manual filtering alone, but must not use it to assign a guard or infer that a high-ranked district automatically needs a visit. Proposed CR-11 is an optional, non-personal upload of guard-post and supervisor-visit status; it would add routing context without changing the public-offense ranking.

## Case 5 — Elena Ruiz: difficult store-hours edge case

### Person, situation, and alternatives

Elena is a fictional CVS District Leader responsible for a downtown CVS in Central reporting district 0161. At a quarterly store-hours review she must decide whether to recommend closing at 10 p.m. rather than midnight. Her decision trades late-night sales and customer access against staff safety. She uses store sales and incident logs, staff and manager input, asset-protection advice, and public LAPD data. CVS district-leader responsibilities and reporting on retail store-hours changes establish why sales, staffing, and safety all matter; see the sources in [Amy's full case](Amy.my-case.md).

### App in use and interpretation

Elena selected Central, Previous 12 months (Aug 2025–Jul 2026), Combined offenses, and no store mapping. The live app showed Central with 103 shoplifting, 221 robbery, and 324 combined evening rows; district 0161 was ranked first with 59 shoplifting, 10 robbery, and 69 combined rows. The source case independently split the same qualifying rows: all 69 of 0161's rows occurred from 18:00–21:59, with zero from 22:00–23:59. Across Central, only 81 of 324 rows were after 10 p.m., and 79 were robberies.

The app's default 18:00–24:00 count therefore does **not** measure the decision Elena is considering: closing only changes 22:00–24:00. A low late count can also mean that stores are closed, not that the period is safe. Sales, customers, late-shift staffing, internal incidents, and neighboring-store hours remain essential.

**Verdict:** Elena is not better off using the current default ranking to decide store hours; it can direct her toward the opposite conclusion. CR-12 proposes a part-of-evening control and a visible late-evening column. CR-13 proposes correcting or relabeling the “most recent complete quarter” option, which currently can display July only rather than three months. These changes preserve the default guard-planning view while preventing a misleading use for Elena and other users.

## Cross-case conclusion

The app is useful when a manager needs a transparent, reproducible **district-level investigation priority** for evening shoplifting and robbery. It is not a store-level risk score, a guard-placement recommendation, a causal estimate of guard impact, or a tool for decisions about narrower hours without an appropriate filter. Across all five cases, the necessary complements are verified CVS locations, internal incident and loss records, store hours, staff and manager input, current guard coverage, schedules, costs, and relevant vendor information. The difficult Elena case shows why a correct count can still answer the wrong decision question.

Before exporting `validation.pdf`, refresh the marked Ana, Maya, and Rita live-app evidence. Use screenshots captured from the published app with the selections visible and replace any superseded URL, period, or count.
