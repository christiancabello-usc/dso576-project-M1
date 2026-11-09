## 4. Tests

*What protects the app from mistakes? Section author: Amy (Yutong Wu). Tests added: `tests/test_mvp_validation.py`. Checked on commit `8fc57b1` plus that file, November 8, 2026.*

### 4.1 Summary: what the tests guarantee

Our users act on four things the screen shows: the **Area totals** (shoplifting, robbery, combined), the **ranked top-10 districts** with the red top five, the **selected period and measure**, and the **exported CSV** they take to leadership. The tests guarantee that, for every selection a user can make, these numbers are counted from exactly the rows the captions promise, add up consistently, are ranked by the measure the user chose, and are exported with everything needed to reproduce them.

```bash
python -m pytest -q        # from the repo root; pytest.ini sets the paths
```

```text
...............x......................................                   [100%]
53 passed, 1 xfailed in 4.63s
```

That is **22 tests from the starting build** (the professor's build of our one-shot prompt) plus **32 we added**. The one *xfail* is a test of a promise the app does not yet keep; it documents a real bug the tests found (4.5).

### 4.2 Properties that must always hold, and what tests them

Each property is tested in up to three ways: a **small example worked out by hand**, a **cross-check** (the same number found another way), and an **invariant** checked on every screen a user can reach. ★ marks tests our team added.

**P1. Evening = 18:00–23:59, and the period includes its first and last day** (the caption under every result).

- *Hand-worked:* 18:00 and 23:59 in, 17:59 and 00:00 out; 23:59:59 on the last day in, Jan 31 and Aug 1 out (`test_filter.py`).
- ★ *Cross-check:* every Area × every period recounted in SQLite, with SQL's own time and date comparisons, equals the app (`test_area_totals_match_independent_sql`).

**P2. Combined = shoplifting + robbery; counts are whole and never negative.**

- *Hand-worked:* 2 shoplifting + 1 robbery in district 0101 → combined 3 (`test_rank.py`).
- ★ *Invariant:* holds on all **189 screens** a user can reach: 21 Areas × 3 periods × 3 measures (`test_invariants_for_every_area_period_and_measure`).

**P3. The Area total and the district table count the same rows**: nothing lost or double-counted between them.

- ★ *Cross-check:* for Central, Topanga and Hollywood, sum of all districts = Area total = number of filtered rows (`test_area_totals_equal_sum_of_all_district_counts`).
- ★ *Invariant:* the top-10 sum never exceeds the Area total, on all 189 screens.

**P4. The ranking follows the measure the user picked, and ties break the same way every time.**

- *Hand-worked:* equal counts → 0102 before 0103; weighted: 1 shoplifting + 1 robbery × 3 = 4 beats 2 shoplifting (`test_rank.py`).
- ★ *Hand-worked:* district 0102 with 2 robberies is first under *Robbery first* and last under *Combined offenses* (`test_robbery_first_orders_by_robbery_then_combined`).
- ★ *Invariant:* rows sorted by the selected measure, ranks 1…n, at most 10 rows, no district twice, on all 189 screens.

**P5. The numbers quoted in our cases are what the data give.**

- ★ *Cross-check against the live app:* Central, Aug 2025 – Jul 2026 = 103 / 221 / **324**; district **0161 = 59 + 10 = 69**, the values on the live app in Case 5 (`test_central_twelve_months_matches_live_app`).

**P6. A store mapping adds stores but never changes counts, and a bad file is refused with a clear reason.**

- ★ *Hand-worked:* "161" → "0161" and " Central " → "Central"; a file without `rpt_dist_no` is refused with that column named; two stores in 0161 → count 2, district 0163 → "No verified CVS store mapped"; counts stay 69 and 31.

**P7. The export lets a reader reproduce the ranking.**

- *Hand-worked:* Areas and dates are recorded (`test_app.py`).
- ★ *Hand-worked:* ranking measure and evening window are recorded, "0161" keeps its leading zero, and a UTF-8 BOM makes Excel show "18:00–24:00" correctly (`test_export_records_measure_window_and_opens_in_excel`).

**P8. Period labels match their dates.**

- ★ *Previous 12 months* = Aug 1, 2025 – Jul 31, 2026, and every period ends on the last complete month.
- ★ *Most recent complete quarter* covers three months: **fails today** (strict xfail, CR-13, see 4.5).

**P9. Bad data or bad settings stop loudly, never silently.**

- *Hand-worked:* a duplicate offense ID stops the load; invalid dates and times are counted, not guessed (`test_data.py`); a misspelled Area, a start before Feb 2025, or an end before the start is rejected (`test_setup.py`).
- *End-to-end:* the real app opens on Topanga without error, and empty data shows a message instead of crashing (`test_app.py`).

### 4.3 What we added beyond the starting build, and why these matter most

The starting build tested each piece of code on tiny tables (P1, P4, P9 and part of P2, P7). We read it against what our users actually rely on and found four gaps:

1. **No test tied any number to the real data.** A test can pass on a 5-row table and the screen can still be wrong on 35,798 rows. P5 pins the exact numbers our cases quote, and the invariant test (P2–P4) checks **every** screen a user can reach, not one example. This matters most because a manager presents these numbers to leadership.
2. **No independent recount.** Every original check reused the app's own pandas logic. The SQL cross-check (P1) recounts every Area for every period with a different tool and different time/date comparisons, so a shared mistake in our filter would be caught.
3. **Features built from change requests had no tests:** *Robbery first* (CR-01), store mapping and candidate stores (CR-03 / CR-04), the measure and window in the export. These are exactly what our cases use: Jordan's robbery-first route, and the store mapping that every case says is needed before choosing a store.
4. **Labels were never checked against what they label.** The caption, period and measure are how users know what a number means; P7 and P8 check them.

### 4.4 Do the tests catch real mistakes?

A test that has never failed proves little. We broke the code on purpose, one realistic mistake at a time, ran both suites, and restored the code:

| Deliberate mistake | Starting build's 22 tests | Our 32 tests |
|---|---|---|
| Evening window ends at 22:59 instead of 23:59 | 2 fail | 2 fail |
| Store mapping no longer pads "161" to "0161" (every store would show as unmapped) | **all pass** | 1 fails |
| *Robbery first* secretly sorts by combined offenses | **all pass** | 1 fails |
| Export drops the `ranking_measure` column | **all pass** | 1 fails |
| Unmapped districts lose their "No verified CVS store mapped" label | **all pass** | 1 fails |
| Last day of the period dropped | 1 fails | 2 fail |
| Robbery weighted × 2 instead of × 3 | 1 fails | 17 fail |

Four of seven mistakes passed the starting build unnoticed; our tests catch all seven.

### 4.5 A real bug the tests found (CR-13)

`test_most_recent_quarter_covers_three_months` fails on the current code: the option *Most recent complete quarter (Jul–Jul 2026)* covers **Jul 1 – Jul 31, 2026 only**, because `period_options` in `src/view.py` starts at the first month of the calendar quarter that contains the last complete month (July). The live app shows the same dates (`screenshots/amy-3-quarter-is-july-only.png`). It matters for the quarterly decisions in our cases, and the Topanga example in Section 1 reads this option as three months. We filed CR-13 and kept the test as a **strict xfail**: the suite stays green, the bug stays visible, and the suite turns red if the bug is fixed without removing the marker.

### 4.6 What the tests do not guarantee

- **That the live app runs the same code and data.** Tests run on the repository. On Nov 8, 2026 we checked by hand that the live app shows the P5 numbers; after any redeploy this check must be repeated.
- **That LAPD's data are complete or correct.** Tests check our counting of LAPD's rows, not the rows themselves (Section 3).
- **Visual details**: red highlighting, chart colours and the warning banner are checked in screenshots, not by assertions.
- **That a ranking answers a user's question.** Correct counting cannot tell whether the 18:00–24:00 measure fits a decision; Section 2 shows where it does not (Case 5).
