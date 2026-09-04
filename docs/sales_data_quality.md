# Sales Module — Data Quality Decisions

**Module:** Sales CRM Analytics  
**Purpose:** Document every known data quality issue with an explicit, defensible decision.

---

## Issue 1: "technolgy" Typo in accounts.csv

**Finding:** The `sector` column in `accounts.csv` contains `"technolgy"` (12 rows) which is clearly a misspelling of `"technology"`.

**Is it an error?** Yes — obvious typo. No legitimate sector called "technolgy" exists.

**Should it be corrected?** Yes.

**Could correction distort the analysis?** No. This is a simple spelling correction that makes the data usable. The original value cannot be a valid category for reporting or grouping.

**Decision:** Correct `"technolgy"` to `"technology"` during data cleaning. Document the correction. The original raw file will be preserved unmodified in `data/raw/`.

---

## Issue 2: "GTXPro" vs "GTX Pro" Product Name Mismatch

**Finding:** `sales_pipeline.csv` uses `"GTXPro"` (no space, 1,480 occurrences) while `products.csv` uses `"GTX Pro"` (with space). This breaks the referential integrity between the two tables.

**Is it an error?** Yes — it is a data entry inconsistency. The product catalog (`products.csv`) is the authoritative source for product names.

**Should it be corrected?** Yes — standardize to `"GTX Pro"` (matching the products catalog).

**Could correction distort the analysis?** No. This is purely a naming standardization. The 1,480 pipeline rows clearly refer to the same product. No analytical meaning changes.

**Decision:** Rename `"GTXPro"` to `"GTX Pro"` in the pipeline data during cleaning. This restores referential integrity with the products table.

---

## Issue 3: 1,425 Opportunities Without Accounts

**Finding:** 1,425 opportunities (16.2%) have a null `account` value. Breakdown:
- Prospecting: 337 / 500 (67.4%)
- Engaging: 1,088 / 1,589 (68.5%)
- Won: 0 / 4,238 (0%)
- Lost: 0 / 2,473 (0%)

**Is it an error?** No. This is expected CRM behavior. In early pipeline stages, the target company may not yet be identified or qualified. By closure, the account is always known.

**Should it be corrected?** No. Do NOT fabricate account names for open deals.

**Could correction distort the analysis?** Yes — imputing accounts for early-stage deals would create false associations and skew account-level metrics.

**Decision:** Retain null accounts as-is. When computing account-level metrics (revenue, opportunities), use only records where account is not null. Document that open-deal analytics exclude unidentified accounts.

---

## Issue 4: 5 Sales Agents With No Pipeline Opportunities

**Finding:** Five agents in `sales_teams.csv` have zero records in `sales_pipeline.csv`:
- Carl Lin (West, manager: Summer Sewald)
- Carol Thompson (West, manager: Celia Rouche)
- Elizabeth Anderson (East, manager: Cara Losch)
- Mei-Mei Johns (Central, manager: Melvin Marxen)
- Natalya Ivanova (East, manager: Rocco Neubert)

**Is it an error?** Uncertain. They could be:
- New hires who haven't yet generated pipeline
- Departed agents whose deals were reassigned
- Non-selling roles erroneously included in the sales team list
- Artifacts of data extraction timing

**Should it be corrected?** No — they are legitimate team members in the source data.

**Could correction (removal) distort the analysis?** Yes — removing them changes team sizes and manager span-of-control metrics.

**Decision:** Retain all 35 agents in the sales_teams table. When computing agent performance metrics (won revenue, deals closed), these 5 agents will naturally show zero. Reports should note that 30 of 35 agents have pipeline activity in the dataset period.

---

## Issue 5: 500 Missing engage_date Values

**Finding:** All 500 Prospecting-stage opportunities have null `engage_date`.

**Is it an error?** No. Per the data dictionary, `engage_date` is the *"Date in which the Engaging deal stage was initiated."* Prospecting-stage deals have not yet engaged, so this field is correctly null.

**Should it be corrected?** No. Do NOT fabricate engagement dates.

**Decision:** Retain as null. These represent genuinely pre-engagement opportunities.

---

## Issue 6: 2,089 Missing close_date Values

**Finding:** 2,089 opportunities have null `close_date`:
- Prospecting: 500 (100%)
- Engaging: 1,589 (100%)

All Won and Lost deals have close_dates.

**Is it an error?** No. Open deals have not closed yet. The data dictionary states `close_date` is the *"Date in which the deal was Won or Lost"*.

**Should it be corrected?** No. Do NOT fabricate close dates.

**Decision:** Retain as null. Sales cycle calculations should use only closed deals (Won + Lost).

---

## Issue 7: 2,089 Missing close_value Values

**Finding:** Same 2,089 opportunities (Prospecting + Engaging) have null `close_value`.

**Is it an error?** No. Open deals have not generated revenue outcomes. close_value is only meaningful for closed deals.

**Should it be corrected?** No. Do NOT impute close_values for open deals.

**Could imputation distort the analysis?** Yes — assigning estimated values would create false revenue projections without any basis.

**Decision:** Retain as null. Revenue analytics should use only Won deals. Counts of open pipeline should use row counts, not fabricated dollar values.

---

## Additional Observation: "Philipines" in accounts.csv

**Finding:** `office_location` contains `"Philipines"` which is likely a misspelling of `"Philippines"`.

**Decision:** Correct to `"Philippines"` during data cleaning. Cosmetic correction — does not affect analytical results.

---

## Summary of Decisions

| Issue | Decision | Action |
|-------|----------|--------|
| "technolgy" typo | **Correct** | Fix to "technology" |
| "GTXPro" mismatch | **Correct** | Standardize to "GTX Pro" |
| 1,425 null accounts | **Retain** | Expected for early-stage deals |
| 5 inactive agents | **Retain** | Keep in team roster, note in reports |
| 500 null engage_date | **Retain** | Correct for Prospecting stage |
| 2,089 null close_date | **Retain** | Correct for open deals |
| 2,089 null close_value | **Retain** | Correct for open deals |
| "Philipines" typo | **Correct** | Fix to "Philippines" |
