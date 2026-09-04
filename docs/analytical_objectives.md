# Analytical Objectives — B2B Sales CRM & Pipeline Management

**Platform:** Sales CRM & Pipeline Management Platform  
**Database:** `crm_platform` (PostgreSQL)  
**Schema:** `crm_sales`  
**Purpose:** Formulate core operational and analytical business questions driving the sales pipeline platform, REST API endpoints, and decision-support algorithms.

---

## 1. Pipeline Distribution & Velocity Analysis

1. **How many total opportunities exist in the sales pipeline?**  
   - What is the breakdown by deal stage (Prospecting, Engaging, Won, Lost)?
   - What proportion of deals are currently open (in progress) vs. closed (terminal outcome)?
2. **Where are open deals accumulating?**  
   - How many open opportunities are in initial Prospecting vs. active Engaging?
   - How long have deals been active in their current stage (pipeline aging)?
3. **What is the overall pipeline conversion efficiency?**  
   - What is the closed deal win rate ($\frac{\text{Won}}{\text{Won} + \text{Lost}}$)?
   - How does win conversion vary by product line, sales agent, and enterprise customer sector?

---

## 2. Revenue & Deal Size Analysis

4. **What is the total realized Won revenue across the operational timeframe?**
5. **What is the average and median deal size for closed-won opportunities?**  
   - How do deal sizes differ across product families?
   - Is revenue normally distributed or positively skewed by high-ticket transactions?
6. **Which enterprise accounts generate the highest cumulative revenue?**  
   - What is account revenue concentration (top 10 accounts vs. aggregate)?
   - How do subsidiary account structures correlate with deal values?
7. **Which industry sectors generate the highest revenue and win rates?**  
   - How do Technology, Retail, Finance, Medical, and other sectors perform comparatively?
8. **How do realized close values compare to catalog list prices?**  
   - Are deals closing at standard list price, discounted rates, or bundled premiums?

---

## 3. Sales Team & Representative Performance

9. **Which sales agents drive the highest total won revenue and closed deal count?**
10. **What is each representative's win rate (controlling for deal volume)?**  
    - How do agent win rates compare to the company benchmark of 63.15%?
11. **How does performance distribute across regional sales offices (Central, East, West)?**
12. **How does managerial leadership impact quota delivery?**  
    - Are there performance variances across sales manager cohorts?
13. **Are there sales agents who demonstrate product specialization?**

---

## 4. Sales Cycle & Pipeline Velocity

14. **What is the average engagement-to-close sales cycle length in days?**
15. **How does cycle length differ between Won and Lost opportunities?**  
    - Do lost deals terminate quickly or stall in the pipeline?
16. **How does sales cycle vary by product tier?**  
    - Do high-ticket enterprise products (e.g., GTK 500) experience longer procurement cycles?
17. **Which customer sectors exhibit the shortest conversion cycles?**

---

## 5. Deterministic Opportunity Prioritization (Phase 5 Framework)

18. **How can sales management algorithmically prioritize open opportunities without subjective guesswork?**
19. **What multi-dimensional factors govern open deal priority?**  
    - Product base value score (0–30 pts)
    - Account historical win rate and revenue tier (0–30 pts)
    - Sales agent historical performance tier (0–25 pts)
    - Pipeline stage velocity / aging penalties (0–15 pts)
20. **How are deals segmented into actionable operational tiers?**  
    - **Tier 1 (Critical Focus, 70–100 pts):** High-value, high-propensity opportunities for immediate rep outreach.
    - **Tier 2 (Core Pipeline, 45–69 pts):** Standard active deals advancing through the funnel.
    - **Tier 3 (At-Risk / Low Priority, 0–44 pts):** Stalled, long-tenure, or unassigned opportunities requiring review or disqualification.
21. **How do daily operational work queues route prioritized opportunities to individual reps?**
