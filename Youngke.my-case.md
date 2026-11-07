# Case: Ana, CVS Regional Loss Prevention Manager

> **Individual. Hand in one PDF file**, not this Markdown file: one case for **your team's
> app**, one specific person using it for one real decision, with screenshots of your team's
> **live app**. Upload the PDF to **Brightspace → Hand In Work** before Quiz 11. Your team also
> puts it in Section 2 (*Cases*) of its MVP `validation.pdf`, graded by MVP criteria 6 and 7 in
> `mvp.md` (in your section's repo). Full instructions: Module 11 handout, 11.7 and *What to hand in*. The four
> questions are in 11.1, and how to make the PDF is in 11.4.
>
> **Where to write.** Copy this file into your team's private repo, in any folder your team
> chooses, and rename it for your person, such as `ana-orders.md`. Save screenshots in a folder
> `screenshots/` next to it. Push as you go, so teammates can see your case.
>
> **In class, for Mei,** use `mei-case.md` in your section's repo instead: it is set up for
> copying in your `/class` answers.
>
> **Claim your person first.** Agree as a team who takes which person and decision, or fill in
> part 1, push this file and tell your teammates: the earlier claim keeps it. A case for the same
> person and decision as a teammate's earlier claim does not count. Together, the team's cases
> should cover your main kinds of users and at least one difficult case.
>
> Five parts: **1** the person and the decision; **2** their real situation and their
> alternatives, from at least two sources; **3** the app in use, with live-app screenshots; **4**
> reading the result for their decision; **5** the verdict: prove the app is as good as it gets
> for this person, or break it with a change request. Codex can find sources, take screenshots
> and make the PDF. What the result means for this person, and the verdict, are yours.

<!--
  How to fill it in:
  - All five parts are required. Replace every placeholder that says "Write" or "Paste",
    including the title. Keep the headings. The boxed lines,
    which start with >, may stay in the PDF; these comments do not show in it.
  - Show what you did and what you saw, not only a conclusion: the selections, the numbers on
    the screen, the source and what it says, the check you ran and its result.
  - Make the PDF as in handout 11.4, with the Markdown Preview Enhanced extension installed in
    VS Code: right-click in the file, "Markdown Preview Enhanced: Open Preview to the Side",
    then right-click in the preview, "Export -> Chrome (Puppeteer) -> PDF". Name it for your
    person, such as case-ana-orders.pdf. Open it and check that every screenshot is readable.
    If the export fails, ask Codex to fix it.
-->

## 1. The person and the decision

> **Enough:** a specific person and one decision your app is for, so that a reader who has never
> seen your project can picture it.

<!-- Who they are, with a name you make up and their job or situation; the decision; when it comes up;
     and what they lose if they decide badly. "A store manager" is too general; "Ana, who
     manages a grocery store and decides each Thursday how much fresh produce to order for the
     next week" is a person. A difficult case is welcome: a user the app serves badly, or one at
     the edge of what it is for. Two to four sentences. -->

Ana is the Regional Loss Prevention Manager for CVS Health in Los Angeles. Every quarter, she must decide how to distribute the evening security guard budget across the entire city (all 21 LAPD areas), and ultimately which five reporting districts across those areas get the extra guard (18:00–24:00). If she allocates the budget to the wrong areas, CVS stores face increased shrink and potential danger to employees and customers.

## 2. Their real situation and alternatives

> **Enough:** how this kind of person makes this decision today, what they are trying to
> achieve and what matters to them, and the alternatives they have to your app, from at least
> two sources you read.

<!-- Sources you can open free online: an official rule or government page, job postings, a news
     or trade article, the alternatives' own websites, or a forum where people in that role
     discuss the decision. Say which source each claim comes from.
     Say what matters to this decision that your app's data do not contain, such as a rule, a
     cost, the person's own circumstances or a recent change. Then name their alternatives: other tools or
     websites, other public data, people they can ask, or how they decide now. Part 5 compares
     your app with these. One or two paragraphs. -->


Currently, Ana relies on intuition from store managers and monthly total incident reports. However, these reports do not separate evening risk from daytime risk, nor do they allow her to compare different areas fairly on a single metric. Ana's main alternative is paying for a commercial retail intelligence platform, but those require integrating internal POS data, which is expensive and slow to set up. Another alternative is manually reading LAPD's public crime maps, but those are too aggregated (by Area, not by specific reporting district) and cannot filter by hour. What matters to Ana is a top-down view of all LAPD areas so she can justify her overall quarterly budget allocation to leadership.

**Sources:**

- National Retail Federation. (2026, July 30). *Retailers See Fraud Schemes Evolve as Shoplifting Declines, NRF Study Finds*. https://cdn.nrf.com/media-center/press-releases/retailers-see-fraud-schemes-evolve-as-shoplifting-declines-nrf-study-finds
- CVS Health. (2026). *Asset Protection Coordinator Job Description*. https://jobs.cvshealth.com/

## 3. The app in use

> **Enough:** your team's live link, what the person selects, at least one screenshot **of the
> live app** with the selections visible, and what they see, in your own words.

<!-- Take every screenshot from the live app at its public link, not from the app running on
     your laptop. (Mei's case in class is the exception: its screenshots are of the H-1B
     explorer on your laptop.) One block per screen,
     in the order the person would use them. Insert each screenshot with
     ![what it shows](screenshots/file-name.png). If a selection does not show in the
     screenshot, write it in the line above the image. If a table is cut off, enlarge the window
     or take a second screenshot of the rest. -->

**Live link:** https://cvs-loss-prevention-app-team1.streamlit.app/

**What they select:** 
Ana opens the app and looks at the "Area comparison" bar chart on the left sidebar to compare all 21 LAPD areas. She sees that Hollywood has a significantly higher combined offense count than West LA. She then selects the "Hollywood" LAPD Area from the dropdown to drill down into the specific block-level risks. She leaves the default date window (February 2025 to July 2026).

<!-- Replace this image line with your own screenshot, one line per screenshot. -->
![Screenshot of the app showing Hollywood area selected and the top 10 districts table](screenshots/case-1.png)

**What they see:** 
The app displays a ranked table of the top 10 reporting districts in Hollywood. The top district is `0645`, with a combined 383 evening offenses (172 shoplifting, 211 robbery). The app clearly marks the top five districts as the "priority shortlist". Ana uses both the macro (Area comparison) and micro (Top 10 district table) views to justify her budget.

## 4. Reading the result for their decision

> **Enough:** an answer to each question below, each backed by evidence: a number from the
> data, a rule, a source, or a check you ran.

<!-- Handout 11.1 gives the questions. Questions 1-3 are answered here; question 4 (better off
     than with the alternatives, and what not to use the app for) is part 5. The fourth prompt
     below asks how the person could misread the result, which part 5 then rules out. Handout 11.5 lists nine kinds of number that answer a
     different question: 1 one row per what, 2 which rows belong, 3 the real thing or a stand-in,
     4 a total or a rate, 5 which dates belong, 6 share of whom, 7 same mix, 8 were the groups
     alike before, 9 could it be luck. If a number the person relies on is one of these, name
     the kind, show the evidence, such as the line of code or a count from the data, and say
     what the right number is. For a rate from a small group (kind 9), say how many rows
     stand behind it. Then check whether it holds: compare it with the overall rate, or split
     the data by year. Or say that there are too few rows to tell. Codex can find the code
     behind a number and compute another
     version in a file you run; paste its code and output in the box. -->

**Does the number measure what this person cares about?** 
Yes. The app counts charged offense rows (23C for shoplifting, 120 for robbery) occurring between 18:00 and 23:59. This directly measures the evening risk Ana cares about, allowing her to compare Hollywood fairly against other areas, unlike raw monthly totals that mix daytime vandalism with evening robberies.

**Who is in the rows, and who is not?** 
The rows include all offenses reported to the LAPD within those specific reporting districts. They include both in-store thefts and street crimes. They do not include unreported crimes (which NRF estimates is about 63% of retail theft) or incidents handled entirely by private security without LAPD involvement.

**What outside the data matters to this decision?** 
The dataset lacks CVS store locations. A high-risk district (like `0645`) might not actually have a CVS store in it, or it might have three. Ana must use her internal corporate knowledge to map these districts to actual CVS store addresses. Also, the data doesn't tell her if a specific store already has private security.

**What could they wrongly conclude from it?** 
Ana might conclude that District `0645` needs a guard solely because it has the highest offense count. However, if she doesn't check if a CVS store is actually located there, she might waste the budget on a district with no CVS presence.

```text
I ran an independent check in Python to verify the app's top district count for Hollywood.
import pandas as pd
df = pd.read_csv("data/processed/lapd_nibrs_offenses.csv") 
filtered = df[(df['AREA NAME'] == 'Hollywood') & (df['NIBR Code'].isin(['23C', '120'])) & (df['Time OCC'].between(1800, 2359))]
print(filtered['RPT Dist No'].value_counts().head(1))
Output: 0645    383
The app's display matches the independent calculation, proving the app is not double-counting rows.
```

## 5. The verdict: prove or break

> **Enough:** whether this person is better off with the app than with the alternatives in
> part 2, the app's place among them, and what they must not use it for. Then **either**
> compelling evidence that, for this person, the app is as good as it gets with the data
> available, **or** a change request that makes it better for this case without being made
> only for this case or making other users' answers worse.

<!-- Saying plainly that the app should not be used for some decision is a finding, and counts in
     your favor. So is showing that it holds up: say what you checked and why nothing better is
     possible with the data. A change request can be a new number or view, a label, a warning,
     or removing something misleading; say whom else it affects, such as your teammates' cases
     and the app's other users, and why it does not hurt them. Paste it as it appears in
     change-requests.md, or delete the box if you prove the app. -->


Ana is significantly better off with this app than with her previous alternatives (manual maps or expensive commercial tools). It gives her the exact hour-by-hour, block-by-block data she needs in seconds, for free.

However, to make the app as good as it gets for her specific decision, we should add a change request: Connect reporting districts to CVS stores. Without this, Ana still has to manually cross-reference the district IDs with her internal store list, which leaves room for error.

```markdown
### CR-03: Connect reporting districts to CVS stores

- **From:** Khushi Ahir, 2026-10-23
- **Part:** Download ranked CSV / five-store allocation decision
- **Evidence:** With Hollywood selected, the export contained 10 ranked reporting districts; the top five were 0645, 0638, etc. It had no CVS store IDs or addresses. The manager's decision concerns five stores, but the data only provides districts.
- **Change:** Allow the manager to load or maintain a verified CVS store-to-reporting-district mapping. Show candidate stores alongside ranked districts in the app and export.
- **Priority:** high
- **Status:** open
```
