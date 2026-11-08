# CVS Evening Loss-Prevention Navigator — Team MVP Validation

## Introduction

The CVS Evening Loss-Prevention Navigator is a decision-support app for asset protection managers reviewing evening shoplifting and robbery patterns across Los Angeles. Its purpose is to help managers narrow down which LAPD areas and reporting districts deserve closer investigation before deciding where to focus limited security resources. The app uses public LAPD offense data, not internal CVS loss records. It is available at https://dso576-project-m1.streamlit.app/. It should improve the **first step** of the decision—identifying places to investigate—without pretending that public district totals can identify the best individual CVS store for a guard.

## 1. Design: Why this is the right app for our users

### 1.1 Users, situation, and decision

Our primary users are CVS district and regional asset protection leaders. Their job is not simply to look at crime charts. They must identify emerging problems, coordinate with store and field leaders, assess loss-prevention priorities, and decide where security attention and resources are justified. CVS Health's District Asset Protection Leader job description specifically discusses using reporting tools to identify priorities, analyzing trends, coordinating outside security agencies, and balancing shrinkage and financial performance [1]. CVS's Asset Protection Coordinator description also emphasizes monitoring store activity and working with store leadership [2]. These responsibilities explain why our users need an understandable way to compare areas and investigate local conditions.

A regional leader might use the app to compare multiple LAPD areas before a planning meeting. A district leader might select Topanga and use its reporting-district ranking to decide which locations require follow-up with store managers. In both cases, the app supports prioritization; it does not make the final decision to assign a guard. That decision also needs verified CVS locations, store-level incident records, staffing and costs, and manager input.

### 1.2 Features and design decisions

**LAPD area selection.** The sidebar lets managers select the geographic area they are responsible for. This prevents a district manager from having to interpret a citywide list when the immediate decision concerns only one area. It also supports regional users who need to compare different areas.

**Reporting-period selection.** Managers can choose a defined time window, including the most recent complete quarter. A complete-quarter option makes it easier to compare consistent reporting periods instead of drawing conclusions from an unfinished month. The selected dates are visible, so a reader knows what time period the results represent.

**Ranking measure.** The app offers a measure such as combined shoplifting and robbery offenses. The selected measure is visible alongside the results, reducing ambiguity about what the ranking means. The app must not describe that measure as the number of distinct incidents or as a store-level risk score: LAPD's NIBRS data may record multiple offenses within one incident [3].

**Top 10 reporting-district table and red top-five highlighting.** A ranked table turns a large public dataset into a manageable investigation shortlist. It preserves the individual shoplifting and robbery columns rather than showing only one combined number, and the red highlighting helps users quickly locate the first five districts. These are priority districts for review, not automatically recommended guard posts.

**Bar chart.** The chart makes differences between reporting districts easier to see than a table alone. For example, in the live Topanga view for July–September 2026, reporting district 2156 shows 41 shoplifting offense rows and 3 robbery offense rows (44 combined), compared with 21 combined for district 2143. This difference makes 2156 a reasonable first place to investigate, but not necessarily the right CVS store for a guard.

**Downloadable ranked CSV.** Managers can export the same ranked results for follow-up discussions and documentation. This is useful when decisions involve several store leaders rather than only the person viewing the dashboard.

**Optional verified CVS store mapping and explicit warning.** The app allows a verified store-mapping CSV to be uploaded. When no mapping is present, it warns that area totals are not offenses per CVS store and that individual store recommendations cannot be made. This is one of our most important design safeguards: a district's police offense count is not evidence that a particular CVS store experienced those offenses.

**Evening focus and data caveats.** The app focuses on offenses occurring from 6 p.m. to midnight, matching the proposed evening-security decision. It identifies counts as charged offense rows rather than distinct reports and notes the excluded January 2025 reporting period. These qualifications matter because the underlying LAPD source changed reporting systems and NIBRS can represent multiple offenses for a single incident [3].

### Live-app evidence: Topanga example

The screenshot below is from the **publicly deployed app**, with **Topanga**, **July 1–September 30, 2026**, and **Combined offenses** selected. It shows the ranking table, bar chart, CSV download, and warning that no verified CVS store mapping is loaded. The screenshot is evidence of these visible features, not independent validation of the underlying offense dataset.

![Live deployed Topanga view showing selections, ranked districts, chart, and store-mapping warning](maya-topanga-live-cropped.png)

*Figure 1. Public Streamlit MVP, Topanga selection (captured November 6, 2026). Source: https://dso576-project-m1.streamlit.app/.*

### 1.3 Alternatives considered and features deliberately excluded

We could have shown the entire public dataset in a large table or built a more complex geographic dashboard. Instead, we prioritized filters, district rankings, and a chart that a manager can interpret quickly. A large raw-data view would require more analysis by the user before reaching a practical shortlist. A detailed map could be valuable later, but it might also imply more location precision than the current CVS mapping supports.

We also did not provide automatic recommendations for individual CVS stores or blocks. The app does not have verified store-level incident histories or a complete verified mapping between CVS stores and LAPD reporting districts by default. Recommending a particular store based only on district totals would be misleading. Similarly, we did not add predictive crime forecasts, automated guard scheduling, or return-on-investment calculations. Those would require additional evidence about future risk, store hours, guard costs, and the effect of security interventions; the public offense counts alone cannot support them.

These omissions are intentional design limits, not simply missing visuals. They keep the MVP aligned with what its data can actually establish.

### 1.4 Overall design defense

The design fits the user's workflow: choose the relevant area and period, see an interpretable district ranking, compare the offense categories, export a shortlist, and then verify local conditions before making a security decision. Its most important strength is the distinction between **district-level investigation priorities** and **store-level guard assignments**. The app provides a quicker starting point than manually filtering the LAPD dataset, while its warning makes clear where human judgment and internal CVS evidence are still necessary.

The design is not complete for every asset-protection decision. A future version could add a documented investigation checklist tied to verified CVS locations and store incident data. For this MVP, however, we prefer a transparent, limited recommendation over an apparently precise answer the data cannot justify.

### Evidence and sources

[1] CVS Health, *District Asset Protection Leader* (job description): https://cvshealth.wd1.myworkdayjobs.com/en-us/cvs_health_careers/job/district-asset-protection-leader--inland-empire-_r1037308

[2] CVS Health, *Asset Protection Coordinator* (job description): https://cvshealth.wd1.myworkdayjobs.com/en-US/CVS_Health_Careers/job/Asset-Protection-Coordinator_R0936174

[3] City of Los Angeles, *LAPD NIBRS Offenses Dataset*: https://data.lacity.org/d/k7nn-b2ep

[4] Team's public MVP: https://dso576-project-m1.streamlit.app/

*The screenshot documents one deployed Topanga view; it does not independently verify every selectable app state or establish which features were explicitly discussed and rejected during team planning. Confirm the latter with teammates before final submission.*
