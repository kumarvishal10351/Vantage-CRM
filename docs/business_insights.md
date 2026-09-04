# Business Insights — Phase 3 SQL Analytics

**Phase:** 3 — CRM SQL Analytics & KPI Layer  
**Generated From:** Validated SQL queries against `crm_platform` PostgreSQL database  
**Date:** 2026-08-30

> **Interpretive Framework:** All insights below are **descriptive observations** from a single dataset snapshot. Correlation does not imply causation. Each insight includes a limitation statement. These are starting points for further investigation, not definitive business conclusions.

---

## Sales CRM Insights (crm_sales)

---

### Insight 1: The Pipeline Has a 63.15% Win Rate

- **Observation:** 4,238 of 6,711 closed deals were Won, yielding a win rate of 63.15%.
- **Supporting Metric:** Win Rate = 4,238 / (4,238 + 2,473) = 63.15%
- **Business Interpretation:** Nearly two-thirds of deals that reach a conclusion are successful. This suggests the sales team is reasonably effective at converting engaged prospects. However, 2,089 open deals (23.7% of total) have unknown outcomes.
- **Limitation:** This is a point-in-time snapshot (Oct 2016 – Dec 2017). The open deals will never close in this dataset, so the true lifetime win rate may differ.

---

### Insight 2: Lost Deals Close Faster Than Won Deals

- **Observation:** Lost deals have a median sales cycle of 14 days vs. 57 days for Won deals (average: 41.5 vs. 51.8 days).
- **Supporting Metric:** Median cycle — Lost: 14 days; Won: 57 days
- **Business Interpretation:** Many losses occur quickly — prospects who will not convert are identified and disqualified early. Won deals require sustained engagement, suggesting that persistence and relationship-building are important for conversion.
- **Limitation:** The dataset does not capture why deals are lost quickly (lack of fit, budget, timing, etc.). Some quick losses may represent good pipeline discipline rather than failure.

---

### Insight 3: Three Products Drive 83% of Revenue

- **Observation:** GTX Pro (35.09%), GTX Plus Pro (26.28%), and MG Advanced (22.15%) collectively contribute 83.52% of total Won revenue ($10,005,534).
- **Supporting Metric:** GTX Pro: $3,510,578 | GTX Plus Pro: $2,629,651 | MG Advanced: $2,216,387
- **Business Interpretation:** Revenue concentration is high. The business is heavily dependent on three mid-to-high-priced products. Lower-priced products (MG Special, GTX Basic) generate high deal volume but minimal revenue share.
- **Limitation:** This reflects revenue, not profitability. Lower-priced products may have higher margins or serve as entry points for upselling.

---

### Insight 4: Win Rates Are Remarkably Consistent Across Products

- **Observation:** Win rates range from 60.00% (GTK 500) to 64.84% (MG Special) — a spread of less than 5 percentage points across all 7 products.
- **Supporting Metric:** Lowest: GTK 500 at 60.00% (but only 25 closed deals); Highest: MG Special at 64.84% (1,223 closed deals)
- **Business Interpretation:** Product type does not strongly differentiate win likelihood. Sales effectiveness appears driven by factors other than which product is being sold.
- **Limitation:** GTK 500 has only 25 closed deals — its 60.00% win rate is statistically unreliable. All other products have 745+ closed deals.

---

### Insight 5: Regional Performance Is Balanced

- **Observation:** Win rates across the three regional offices are within 1.4 percentage points: West (63.94%), East (63.02%), Central (62.56%).
- **Supporting Metric:** Won deals — Central: 1,629; West: 1,438; East: 1,171
- **Business Interpretation:** No region significantly underperforms. The higher volume in Central is proportional to its larger agent count (11 agents) vs. the other regions.
- **Limitation:** This does not account for market size differences, competitive landscape, or quota achievement per region.

---

### Insight 6: Revenue of ~$10 Million Across 4,238 Won Deals

- **Observation:** Total Won revenue is $10,005,534 with an average deal size of $2,360.91 and a median of $1,117.00.
- **Supporting Metric:** Mean $2,360.91 vs. Median $1,117.00 | Min $38 | Max $30,288
- **Business Interpretation:** The large mean-median gap indicates revenue is positively skewed — a smaller number of large deals (e.g., GTX Pro, GTK 500) pull the average up, while most deals are smaller. Both measures should be tracked.
- **Limitation:** This is 14 months of data. No cost data is available, so profitability is unknown.

---

### Insight 7: Open Pipeline Is Not Monetizable

- **Observation:** 2,089 open opportunities (500 Prospecting + 1,589 Engaging) have no close_value, and no probability or expected value field exists.
- **Supporting Metric:** NULL close_value for 100% of open deals
- **Business Interpretation:** Monetary pipeline value cannot be reported from this dataset. Open pipeline can only be tracked by opportunity count and stage.
- **Limitation:** This is a dataset design limitation, not a data quality issue. In a production CRM, opportunity value would typically be available.

---

## Key Caveats

1. **No causation claims.** All observations describe associations in the data. Controlled experiments or longitudinal studies would be needed to establish causation.
2. **Sales data spans 14 months only.** Trends may not generalize to other periods.
3. **Open pipeline outcome uncertainty.** The 2,089 open opportunities represent in-flight pipeline whose ultimate outcomes are unobserved in the snapshot.

