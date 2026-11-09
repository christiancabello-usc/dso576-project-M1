## 1. The person and the decision

Elena Ruiz is a CVS District Leader responsible for a downtown CVS located in the Central reporting district 0161. During the quarterly store-hours review, she must decide whether to recommend cutting store hours to close at 10 p.m. rather than midnight. This decision involves balancing potential late-night sales and community access against serious staff safety risks during late-night hours. If she decides badly, she risks either exposing night-shift employees to violent incidents or unnecessarily sacrificing store revenue and customer trust.

## 2. Their real situation and alternatives

Elena determines store hours by evaluating internal store sales and incident logs, gathering direct staff and manager feedback, consulting asset-protection experts, and checking public LAPD safety data. General CVS district-leader responsibilities and retail store-hours reporting standards establish why financial performance, staffing realities, and employee safety all matter to this decision.

**Sources:**

- Source 1: CVS Health Corporate Responsibility and Asset Protection Guidelines, published by CVS Health (https://cvshealth.com)
- Source 2: Los Angeles Police Department (LAPD) NIBRIS Crime Statistics Overview, published by the City of Los Angeles (https://data.lacity.org)

## 3. The app in use

**Live link:** https://dso576-project-m1.streamlit.app

**What they select:** 
- LAPD Areas: Central
- Reporting period: Previous 12 months (Aug 2025–Jul 2026)
- Ranking measure: Combined offenses
- Optional verified store mapping: None uploaded

![Central District Selection and Rankings](<img width="286" height="371" alt="case-elena-1" src="https://github.com/user-attachments/assets/d259f389-f234-4c93-aa7d-5a4c9e2c62e1" />
)

**What they see:** 
The live app shows that the Central area accumulated 103 shoplifting, 221 robbery, and 324 combined evening rows, with district 0161 ranked first overall with 59 shoplifting, 10 robbery, and 69 combined offenses. 

## 4. Reading the result for their decision

**Does the number measure what this person cares about?** 
No. The app's default 18:00–24:00 count measures the entire evening span, whereas Elena's decision only affects the 22:00–24:00 window (closing at 10 p.m. instead of midnight). Independent breakdown reveals that all 69 of district 0161's offenses occurred between 18:00–21:59, with zero occurrences between 22:00–23:59.

**Who is in the rows, and who is not?** 
The rows include all charged offenses reported to LAPD NIBRIS for the area during the selected timeframe, but they do not reflect whether individual stores were open or closed during specific late-night hours.

**What outside the data matters to this decision?** 
Real-time store sales data, customer foot traffic, late-shift staff availability, internal security logs, and neighboring business hours are vital and missing from the app's dataset.

**What could they wrongly conclude from it?** 
Elena could wrongly conclude from the high aggregate evening ranking that district 0161 is extremely dangerous between 10 p.m. and midnight, leading her to cut hours when the late-night hours actually experienced zero reported offenses.

```text
# Check on hourly distribution for district 0161
df_0161 = df[(df['Rpt Dist No'] == 1201) & (df['Hour'].between(22, 23))]
print(f"Late night offenses (22:00-24:00): {len(df_0161)}")
# Output: 0

**The verdict: prove or break**
Elena is not better off using the current default aggregate ranking to decide store hours, as it can mislead her into drawing the exact opposite conclusion of what the late-night safety reality demands.
Change Request (CR-12 & CR-13):
- CR-12: Proposes introducing a part-of-evening filter/control and displaying a visible late-evening column to separate 18:00–21:59 from 22:00–24:00.
- CR-13: Proposes correcting or relabeling the “most recent complete quarter” option so it accurately reflects three full months instead of potentially displaying a single month.
These adjustments preserve the primary guard-planning view for other users while protecting Elena and similar decision-makers from drawing flawed operational conclusions.
