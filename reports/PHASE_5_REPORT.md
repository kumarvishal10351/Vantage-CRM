# PHASE 5 REPORT — Interpretable CRM Opportunity Prioritization

**Phase:** 5 — Interpretable CRM Opportunity Prioritization Framework  
**Date:** 2026-08-31  
**Status:** COMPLETED & VERIFIED (All 10 Automated Tests Passed; Open Pipeline Scored & Persisted)  
**Database:** `crm_platform` (Schema: `crm_sales`)  
**Output Dataset:** `data/processed/crm_sales/prioritized_open_opportunities.csv`  

---

## 1. Executive Summary & Governance Declarations

Following the empirical findings in Phase 4C, sales leadership established that the historical CRM dataset does not contain sufficient pre-outcome signal for reliable machine learning Win/Lost forecasting (ROC-AUC ~0.50–0.54). 

Phase 5 implemented an **interpretable, deterministic, rule-based CRM Prioritization Framework** for all **2,089 active open opportunities** (`Prospecting` and `Engaging`).

### Critical Governance Statements:
- **"The CRM Priority Score is an operational prioritization index. It is not a probability of winning, forecast, expected revenue, or predictive model."**
- **Operational Business Rules:** The scoring weights and thresholds are **OPERATIONAL BUSINESS RULES**, not statistically optimized predictive weights.
- **Resource Allocation Focus:** **"Tier 1 opportunities receive higher operational attention based on the selected business-priority rules."** They are NOT more likely to win.
- **Observable Factor Scope:** **"The framework prioritizes observable opportunity-management factors but does not estimate probability of conversion."**

---

## 2. Prioritization Framework Architecture

The framework calculates an additive composite priority score across four observable pre-outcome CRM dimensions:

$$\text{CRM Priority Score} = \text{Stage Points } (10\text{--}30) + \text{Product Points } (10\text{--}30) + \text{Account Points } (5\text{--}25) + \text{Age Points } (5\text{--}15)$$

### Point Allocation Matrix:
| Dimension | High Tier (Max Points) | Medium Tier | Low Tier | Unassigned / Base | Max Points |
|:---|:---|:---|:---|:---|:---:|
| **1. Deal Lifecycle Stage** | `Engaging` (**30 pts**) | — | `Prospecting` (**10 pts**) | — | **30** |
| **2. Product Catalog Value** | High Value $\ge \$4\text{k}$ (**30 pts**) | Medium Value \$1k–\$4k (**20 pts**) | Low Value $<\$1\text{k}$ (**10 pts**) | — | **30** |
| **3. Account Strategic Scale**| Enterprise $\ge \$2.5\text{B}$ / 5k emp (**25 pts**) | Mid-Market (**15 pts**) | Commercial / Small (**10 pts**) | Unassigned Account (**5 pts**) | **25** |
| **4. Engagement Age & Urgency**| Recent $\le 90$ days (**15 pts**) | Aging $91–180$ days (**10 pts**) | Stalled $> 180$ days (**5 pts**) | Unengaged Prospect (**5 pts**) | **15** |
| **Total Composite Score** | | | | | **100** |

> **Non-Causal Attribute Clarification:**
> - Product price represents **catalog value**, NOT estimated deal value.
> - Account tier represents **analytical strategic scale**, NOT account quality.
> - Engagement age represents **operational aging/urgency**, NOT stage velocity.
> - **None of these attributes imply causal effects on winning.**

---

## 3. Current Open Pipeline Prioritization Results ($N = 2,089$)

All 2,089 active open opportunities were scored without missing values:

```text
Open Pipeline Prioritization Distribution (N=2,089):
Tier 1 — High Priority (&ge; 75 pts):   [========] 20.49% (428 Deals)
Tier 2 — Medium Priority (55-74 pts): [====================] 49.45% (1,033 Deals)
Tier 3 — Lower Priority (&lt; 55 pts):   [============] 30.06% (628 Deals)
```

| Priority Tier | Score Range | Open Deals | % of Open Pipeline | Engaging Count | Prospecting Count | Action Plan |
|:---|:---:|---:|---:|---:|---:|:---|
| **Tier 1 — High Priority** | $\ge 75$ | **428** | **20.49%** | 428 | 0 | **Immediate Manager Review & Deal-Desk Support** |
| **Tier 2 — Medium Priority**| $55 - 74$ | **1,033** | **49.45%** | 972 | 61 | **Standard Rep Follow-Up Cadence** |
| **Tier 3 — Lower Priority** | $< 55$ | **628** | **30.06%** | 189 | 439 | **Routine Monitoring & SDR Lead Qualification** |
| **Total Active Pipeline** | **25 - 100** | **2,089** | **100.00%** | **1,589** | **500** | Full Open Universe |

*Note on Stage Composition:* Tier 1 is intentionally dominated by Engaging opportunities (428) because lifecycle stage carries the largest fixed score component (30 pts), ensuring management focuses immediately on active customer conversations.

---

## 4. Sales Operations & Management Breakdowns

### A. Priority Tier by Account Strategic Scale
- **Enterprise Accounts:** 152 Tier 1 deals (66.1% of all open enterprise deals).
- **Mid-Market Accounts:** 82 Tier 1 deals (29.2% of all open mid-market deals).
- **Unassigned Accounts:** 157 Tier 1 deals, 742 Tier 2 deals, 526 Tier 3 deals.

### B. Priority Tier by Product Catalog Value Tier
- **High Value Products ($\ge \$4,000$):** 296 Tier 1 deals (69.2% of Tier 1 volume).
- **Medium Value Products (\$1,000–\$3,999):** 95 Tier 1 deals, 418 Tier 2 deals.
- **Low Value Products (<\$1,000):** 37 Tier 1 deals, 419 Tier 2 deals, 402 Tier 3 deals.

### C. Top 5 Sales Representatives by Tier 1 Workload
| Sales Representative | Tier 1 Deals | Tier 2 Deals | Tier 3 Deals | Total Open Pipeline |
|:---|---:|---:|---:|---:|
| **Darcel Schlecht** | **52** | 79 | 36 | **167** |
| **Cassey Cress** | **29** | 43 | 26 | **98** |
| **Kary Hendrixson** | **27** | 44 | 22 | **93** |
| **Daniell Hammack** | **23** | 30 | 17 | **70** |
| **Zane Levy** | **23** | 39 | 24 | **86** |

---

## 5. Retrospective Diagnostic on Historical Closed Deals ($N = 6,711$)

The scoring rules were applied retrospectively to the 6,711 closed deals to evaluate historical outcome distributions.

> **Methodological Clarification:**
> The retrospective closed-deal analysis is a **diagnostic check only and was NOT used to optimize the scoring weights**.

| Priority Tier | Closed Deals Evaluated | Won Deals | Lost Deals | Retrospective Win Rate (%) |
|:---|---:|---:|---:|---:|
| **Tier 1 — High Priority** | 871 | 552 | 319 | **63.38%** |
| **Tier 2 — Medium Priority** | 4,197 | 2,627 | 1,570 | **62.59%** |
| **Tier 3 — Lower Priority** | 1,643 | 1,059 | 584 | **64.46%** |
| **Total Supervised Population** | **6,711** | **4,238** | **2,473** | **63.15%** |

### Retrospective Diagnostic Finding:
> **"Retrospective results show that the priority tiers do not meaningfully separate historical Won/Lost outcomes. Leakage prevention was established separately through feature restrictions and automated validation."**

---

## 6. Automated Test Suite Verification (`tests/test_phase5_priority_framework.py`)

All 10 automated test cases passed cleanly:

```text
============================= test session starts =============================
platform win32 -- Python 3.14.3, pytest-9.0.2, pluggy-1.6.0
rootdir: C:\Users\kumar\Desktop\CRM
collected 10 items

tests/test_phase5_priority_framework.py::test_open_opportunity_population_count PASSED [ 10%]
tests/test_phase5_priority_framework.py::test_no_closed_records_in_scoring PASSED [ 20%]
tests/test_phase5_priority_framework.py::test_no_prohibited_outcome_fields PASSED [ 30%]
tests/test_phase5_priority_framework.py::test_priority_score_range_validity PASSED [ 40%]
tests/test_phase5_priority_framework.py::test_every_record_has_one_tier PASSED [ 50%]
tests/test_phase5_priority_framework.py::test_deterministic_scoring_reproducibility PASSED [ 60%]
tests/test_phase5_priority_framework.py::test_engagement_age_calculation PASSED [ 70%]
tests/test_phase5_priority_framework.py::test_account_tier_calculation PASSED [ 80%]
tests/test_phase5_priority_framework.py::test_product_tier_calculation PASSED [ 90%]
tests/test_phase5_priority_framework.py::test_persisted_dataset_and_retrospective PASSED [100%]

======================= 10 passed in 3.44s =======================
```

---

## 7. Persisted Deliverables & Governance Compliance

| Artifact File | Description |
|:---|:---|
| `src/prioritization/crm_priority.py` | Production prioritization engine and scoring pipeline. |
| `tests/test_phase5_priority_framework.py` | 10-check automated test suite. |
| `data/processed/crm_sales/prioritized_open_opportunities.csv` | 2,089 scored and categorized active open opportunities. |
| `docs/crm_priority_framework.md` | Comprehensive operational methodology and playbook. |
| `reports/PHASE_5_REPORT.md` | This Phase 5 summary report. |

---

### Strict Restriction Compliance Confirmation
- [x] No ML model trained or optimized against historical outcomes
- [x] No win/loss outcome fields or post-outcome timestamps used
- [x] Zero synthetic opportunities, labels, or fabricated open deal values created
- [x] Scores are explicitly designated as CRM Priority Scores, never probabilities
- [x] Scoring engine (`src/prioritization/crm_priority.py`) and outputs remained untouched
- [x] Database schema and raw CSV datasets remained completely untouched
- [x] All 10 unit and integration tests passed

---

**Phase 5 documentation corrections are complete, verified, and aligned with governance rules. Halting execution as instructed.**
