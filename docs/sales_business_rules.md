# Sales Module — Business Rules & Definitions

**Module:** Sales CRM Analytics  
**Purpose:** Define business logic, pipeline rules, and KPI definitions based on audited data.

---

## 1. What Constitutes an Opportunity?

An **opportunity** is a single sales engagement between a sales agent and a prospective or existing account for a specific product. Each opportunity is uniquely identified by `opportunity_id` and tracks the lifecycle of one potential deal from initial prospecting through to final outcome.

**Key characteristics:**
- One opportunity = one agent + one product + one potential deal
- An opportunity may or may not have an associated account (see section 6)
- An opportunity progresses through stages in a defined order

---

## 2. Deal Stages

The pipeline has **four stages** with a clear progression:

```
Prospecting → Engaging → Won
                       → Lost
```

| Stage | Count | % | Description |
|-------|-------|---|-------------|
| Prospecting | 500 | 5.7% | Initial identification. No engage_date, no close_date, no close_value, account often unknown. |
| Engaging | 1,589 | 18.1% | Active engagement with prospect. Has engage_date. No close_date or close_value yet. Account may or may not be identified. |
| Won | 4,238 | 48.2% | Deal closed successfully. Has engage_date, close_date, and positive close_value. Account is always present. |
| Lost | 2,473 | 28.1% | Deal closed unsuccessfully. Has engage_date, close_date, and close_value = 0. Account is always present. |

**Source:** `data_dictionary.csv` explicitly states: *"Sales pipeline stage (Prospecting > Engaging > Won / Lost)"*

---

## 3. Open vs. Closed Opportunities

| Category | Stages | Count | Has close_date? | Has close_value? |
|----------|--------|-------|-----------------|------------------|
| **Open** | Prospecting, Engaging | 2,089 | No | No |
| **Closed-Won** | Won | 4,238 | Yes | Yes (> 0) |
| **Closed-Lost** | Lost | 2,473 | Yes | Yes (= 0) |

---

## 4. Successful vs. Unsuccessful Outcomes

- **Successful:** `Won` — deal generated revenue
- **Unsuccessful:** `Lost` — deal closed with zero revenue

---

## 5. Opportunity-to-Outcome Observations

For **closed opportunities only** (Won + Lost = 6,711):
- Win rate = 4,238 / 6,711 = **63.1%**
- Loss rate = 2,473 / 6,711 = **36.9%**

If measured against **all opportunities** including open (8,800):
- Won = 48.2%, Lost = 28.1%, Open = 23.7%
- This is NOT a meaningful win rate — open deals have not concluded

**Decision:** Win rate should be calculated from closed deals only.

---

## 6. Missing Account — Business Meaning

| Observation | Detail |
|-------------|--------|
| Total missing account | 1,425 (16.2%) |
| By stage — Prospecting | 337 / 500 (67.4%) |
| By stage — Engaging | 1,088 / 1,589 (68.5%) |
| By stage — Won | 0 / 4,238 (0%) |
| By stage — Lost | 0 / 2,473 (0%) |

**Interpretation:** A missing account means the prospective company has not yet been formally identified or qualified. This is normal in early pipeline stages. By the time a deal closes (Won or Lost), the account is always known.

**Decision:** This is expected CRM behavior, not a data quality error. Do not fabricate accounts for open deals.

---

## 7. Missing close_date — Business Meaning

Missing `close_date` means the opportunity is still open (has not been Won or Lost). Exactly 2,089 rows have missing close_date — matching exactly the combined Prospecting (500) + Engaging (1,589) counts.

**Decision:** This is expected. Do not fabricate close dates.

---

## 8. close_value for Lost Opportunities

All 2,473 Lost deals have `close_value = 0.0`. This makes business sense: a lost deal generates zero revenue.

**Decision:** This is correct and expected. close_value = 0 for Lost deals is a data fact, not a data quality issue.

---

## 9. close_value as Revenue

For Won deals, `close_value` represents the **actual deal revenue** in USD.

| Statistic | Value |
|-----------|-------|
| Mean | $2,360.91 |
| Median | $1,117.00 |
| Min | $38.00 |
| Max | $30,288.00 |
| Std Dev | $2,544.48 |
| Zero values | 0 |

Won deal close_values cluster around product list prices with moderate variation (~1-2% average deviation from catalog price), suggesting real negotiated prices with small discounts or premiums.

**Decision:** close_value for Won deals is reliable revenue data.

---

## 10. Pipeline Value Definition

**Pipeline value** = Sum of `close_value` for Won deals = Total Won Revenue

However, a common CRM metric is "open pipeline value" (potential future revenue). Since open deals (Prospecting + Engaging) have no close_value, we **cannot** calculate a traditional open pipeline value from this dataset.

**What we can calculate:**
- Total Won Revenue: Sum of close_value where deal_stage = Won
- Total Closed Revenue: Same as Won Revenue (Lost = 0)
- Weighted Pipeline: Not calculable without deal probability/expected values for open deals

**Decision:** Report "Total Won Revenue" as the revenue KPI. Do not fabricate pipeline values for open deals.

---

## 11. Win Rate Definition

**Win Rate** = Won / (Won + Lost) = 4,238 / 6,711 = **63.1%**

Denominator includes only closed deals. Open deals (Prospecting + Engaging) are excluded because their outcome is unknown.

**Alternative interpretation:** If the dataset represents a historical snapshot and all deals eventually close, the eventual win rate may differ. We report based on available data.

---

## 12. Sales Cycle Definition

**Sales Cycle** = close_date - engage_date (in days)

Calculable only for closed deals (Won + Lost) that have both dates.

| Metric | All Closed | Won | Lost |
|--------|-----------|-----|------|
| Records | 6,711 | 4,238 | 2,473 |
| Mean | 48.0 days | 51.8 days | 41.5 days |
| Median | 45 days | 57 days | 14 days |
| Min | 1 day | 1 day | 1 day |
| Max | 138 days | 138 days | 138 days |
| Negative cycles | 0 | 0 | 0 |

**Observation:** Lost deals have a shorter median cycle (14 days vs 57 days), suggesting many losses occur quickly. Won deals take longer on average, indicating more sustained engagement is required to win.

---

## 13. Dataset Limitations

| Limitation | Impact |
|-----------|--------|
| **No prospecting dates for Prospecting stage** | Cannot calculate time-in-stage for earliest deals |
| **No expected/weighted deal value for open deals** | Cannot calculate weighted pipeline |
| **No multi-touch tracking** | Each opportunity is a single record — no interaction history |
| **No lead source** | Cannot analyze lead generation channels |
| **No customer contact information** | Cannot tie opportunities to individual buyers |
| **14-month window only** | Cannot analyze year-over-year trends |
| **Snapshot data** | Open deals at time of extraction will never close in this dataset |
| **5 agents with no pipeline activity** | May be new hires, departed agents, or data extraction artifacts |
| **No cost data** | Cannot calculate profitability or cost-to-acquire |
| **No renewal/upsell flag** | Cannot distinguish new business from existing account expansion |
