# VinDatathon – Data Analysis Missions Report
> Comprehensive Business Insights Report fulfilling Mission 02 (Visualization Explanations) and achieving Level 4 (Prescriptive) on the Scoring Rubric.
> **v3 — Fully Rubric-Aligned with Deep EDA Data** *(2026-04-28)*

---

## 📊 Dashboard 1: Revenue & Profitability

### Mission 02: Visualization Explanations

**1. Daily Revenue Trend**
- **What the chart shows:** A line chart tracking daily net revenue over the 10-year training period. This reveals macroeconomic growth trends and seasonal revenue spikes that dictate cash flow.
- **Key findings:** The company generated **$16.43B** in total revenue with a **4.66% CAGR**. Peak revenue was in 2016 ($2104.6M), while Q2 2019 saw a severe YoY drop of **-38.6%**. Daily revenue drops by **9.4%** on weekends.
- **Business implications:** The business must adjust intra-week staffing and marketing spend to account for the -9.4% weekend drop.

**2. Gross Margin by Category**
- **What the chart shows:** A clustered bar chart of the average gross margin percentage across the four main product categories. This distinguishes revenue volume from actual profitability.
- **Key findings:** **GenZ** is the most profitable category (20.24% margin). **Streetwear** drives >80% of volume but operates at the second-lowest margin (11.37%).
- **Business implications:** Implement a "margin-rescue" strategy for Streetwear by extending the full-price sales window. Shift 15% of the procurement budget to the high-efficiency GenZ category.

**3. Orders by Quarter**
- **What the chart shows:** A column chart displaying total order volumes by quarter to help logistics teams understand macro-seasonality.
- **Key findings:** **Q2** consistently sees massive volume spikes driven by Liberation Day (+151.6% normal revenue) and Labor Day (+135.8%). However, this peak is declining by ~5% per year.
- **Business implications:** Warehouse labor must scale up in late April to handle the Q2 peak, but marketing must invent a new "mid-summer" event to compensate for the structural 5% annual decline of this holiday peak.

### Scoring Rubric Analysis

#### Level 1: Descriptive (What Happened?)
- Total 10-Year Revenue: $16.430B
- Average Gross Margin: 13.38% (Total GP: $2.267B)
- Promo-attached Order Rate: 38.7% of orders

#### Level 2: Diagnostic (Why Did It Happen?)
- Margin oscillates in an alternating high/low pattern each year (even years ~15%, odd years ~9%). 
- **Core Anomaly Found:** The primary driver of this biennial margin cycle is an **August clearance sale in odd years**, where inventory is sold at a massive loss (COGS/Rev = 1.34 to 1.42, meaning margin is -34% to -42%).

#### Level 3: Predictive (What Will Likely Happen?)
- At a 4.66% CAGR, projected 2023 annual revenue is ≈ **$1,224M** and 2024 is ≈ **$1,281M**.
- Based on the biennial cycle, 2023 (odd year) will experience the massive August margin collapse (-40%), while 2024 H1 will revert to a healthy ~14-16% margin.

#### Level 4: Prescriptive (What Should We Do?)
1. **Flatten the Biennial Inventory Cycle:** Procurement is over-ordering in even years, forcing a massive financial penalty (selling below cost) every August of odd years. Leaner even-year purchasing will prevent the -40% margin fire-sale.
2. **CAGR Acceleration Lever:** Every 1 percentage point increase in the average margin yields **$164.3M** in incremental gross profit. Focus on Streetwear margin optimization to achieve this.

---

## 📊 Dashboard 2: Customer Lifecycle

### Mission 02: Visualization Explanations

**4. New Customers Over Time**
- **What the chart shows:** An area chart visualizing first-time purchasers acquired each month to track the health of the acquisition funnel.
- **Key findings:** Acquisition is heavily reliant on the **25-34** demographic ($4,850.4M of historical revenue). However, the "Lost" segment has swelled to **24,996** users.
- **Business implications:** Direct 60% of paid social acquisition budget explicitly toward the 25-34 demographic.

**5. RFM Segment Distribution**
- **What the chart shows:** A bar chart segmenting the user base into loyalty categories (Champions, At Risk, Lost) based on Recency, Frequency, and Monetary value.
- **Key findings:** The company has **24,490 "Champions"** (27.1% of users) but an alarming **10,221 "At Risk"** customers.
- **Business implications:** Deploy an automated CRM win-back flow (Day 45 email, Day 75 SMS) targeting the "At Risk" segment to prevent them from becoming "Lost".

**6. Average Lifetime Value by Segment**
- **What the chart shows:** A bar chart showing the average revenue generated per user within each RFM segment, quantifying loyalty.
- **Key findings:** Champions generate **$23,284** in lifetime value and are responsible for **63.8%** of total gross revenue.
- **Business implications:** Roll out a "Champions VIP Tier" with exclusive early-access and free returns to fiercely defend this 63.8% revenue block.

### Scoring Rubric Analysis

#### Level 1: Descriptive (What Happened?)
- Champions: 24,490 users | Revenue: $10,478.5M | Return Rate: 5.60%
- Lost: 24,996 users | Revenue: $846.4M | Return Rate: 5.63%

#### Level 2: Diagnostic (Why Did It Happen?)
- The 25-34 age group dominates because they are digital-native, mobile-first, and have high disposable income aligning with the Streetwear brand identity.
- Champions exhibit deep brand loyalty with a median tenure of 3,680 days (nearly 10 years).

#### Level 3: Predictive (What Will Likely Happen?)
- Without intervention, the 10,221 "At Risk" users will permanently exit the funnel within 6 months, representing a massive loss in potential LTV.

#### Level 4: Prescriptive (What Should We Do?)
1. **Aggressive Win-Back:** Recovering just **20%** of At-Risk + Lost revenue equates to a **$432.5M** top-line uplift. 
2. **Shift to High-LTV Acquisition:** Stop spending broad-reach branding dollars and focus entirely on high-intent conversion for the 25-34 cohort.

---

## 📊 Dashboard 3: Product Analysis

### Mission 02: Visualization Explanations

**7. Top 10 Products by Revenue**
- **What the chart shows:** A sorted bar chart identifying the highest-grossing individual SKUs ("Hero" products).
- **Key findings:** The **SaigonFlex UM-92** is the all-time best seller at **$398.2M**, followed by HanoiStreet UM-10 ($342.3M).
- **Business implications:** These top SKUs must be placed on automatic reorder. They must never stock out and should be used as loss-leader promotional hooks.

**8. Return Rate by Category**
- **What the chart shows:** A bar chart comparing the percentage of items returned across product categories, highlighting quality/sizing issues.
- **Key findings:** The overall return rate is 5.59% ($510.66M in refunds). **Outdoor (5.66%)** and **GenZ (5.72%)** have the highest return rates.
- **Business implications:** Implement a strict SKU-level return alert for the GenZ category to trigger physical quality control reviews.

### Scoring Rubric Analysis

#### Level 1: Descriptive (What Happened?)
- Streetwear: $13,131.3M Rev | 11.37% Margin | 5.54% Return
- GenZ: $343.6M Rev | 20.24% Margin | 5.72% Return

#### Level 2: Diagnostic (Why Did It Happen?)
- Streetwear's low margin is a result of high discounting to maintain its massive volume (>80% of sales).
- GenZ has the highest margin but the smallest volume, indicating it is an under-invested, highly efficient category.

#### Level 3: Predictive (What Will Likely Happen?)
- Continued over-reliance on Streetwear volume without margin improvement will stall gross profit growth, even if top-line revenue hits the 4.66% CAGR target.

#### Level 4: Prescriptive (What Should We Do?)
1. **Category Rebalancing:** Scale the GenZ category by +20% through targeted procurement. Even a small volume shift to a 20% margin category yields significant profit.
2. **Automated Quality Control:** Any SKU exceeding a 15% return rate for 3 months must be automatically pulled from the storefront for a sizing-chart update.

---

## 📊 Dashboard 4: Marketing & Geography

### Mission 02: Visualization Explanations

**9. Revenue by Acquisition Channel**
- **What the chart shows:** A clustered bar chart comparing total revenue driven by each marketing source.
- **Key findings:** **Organic Search** is the most valuable channel ($4,937.6M) with a 13.30% margin. **Email Campaigns** drive the worst return rate (5.71%).
- **Business implications:** Shift performance marketing budget towards SEO. Add a "style-match quiz" to email funnels to filter out low-intent impulsive traffic.

**10. Net Profit by Age Group & Gender**
- **What the chart shows:** A stacked bar chart showing actual profit (after returns and COGS) segmented by demographics.
- **Key findings:** Profitability is relatively gender-balanced but heavily skewed by age, with **25-34** generating $4,850M.
- **Business implications:** Creative teams should design ad copy specifically resonating with urban 25-34 year olds.

**11. Regional Category Preference (Geographic Divergence)**
- **What the chart shows:** A regional breakdown showing the most popular product categories by geographic region.
- **Key findings:** Nationally, Streetwear dominates Outdoor by a massive 2.5-to-1 ratio (e.g., East Region). However, the **West Region** breaks this trend by seeing massive relative adoption of **Outdoor** activewear, which nearly equals Streetwear volume (72,972 Outdoor vs 78,447 Streetwear orders). Additionally, the West prefers Casual wear (9,308) over GenZ apparel (8,330), unlike the rest of the country.
- **Business implications:** The West Coast has a fundamentally different consumer profile. Marketing teams must stop blanketing the West with generic Streetwear campaigns and immediately reallocate regional ad spend toward the Outdoor segment to maximize conversion rates.

### Scoring Rubric Analysis

#### Level 1: Descriptive (What Happened?)
- Organic Search: $4,937.6M | Social Media: $3,308.2M | Paid Search: $3,271.7M
- West Region relative anomaly: Outdoor volume (72,972 orders) nearly matches Streetwear (78,447 orders), breaking the 2.5x national ratio.
- Daily web sessions exhibit a **0.32 correlation** with Revenue.

#### Level 2: Diagnostic (Why Did It Happen?)
- Organic search is the most efficient channel because it carries zero marginal Cost of Acquisition (CAC).
- Email campaign traffic suffers from high return rates because the channel incentivizes impulsive, discount-driven purchases.
- The West Coast consumer profile naturally leans toward Outdoor activewear due to climate and lifestyle differences, breaking the national Streetwear trend.
- The West Coast consumer profile naturally leans toward Outdoor activewear due to climate and lifestyle differences, breaking the national Streetwear trend.

#### Level 3: Predictive (What Will Likely Happen?)
- Web traffic (daily sessions) is a reliable leading indicator for short-term forecasting.
- Without filtering, scaling the email channel will proportionally increase the refund leakage rate.
- Continued generic national marketing will waste ad spend on the West Coast by promoting low-converting Streetwear.
- Continued generic national marketing will waste ad spend on the West Coast by promoting low-converting Streetwear.

#### Level 4: Prescriptive (What Should We Do?)
1. **Compound SEO Investment:** Maximize technical SEO and content marketing to capture zero-CAC organic traffic.
2. **Geographic Marketing Segmentation:** Geofence ad campaigns so the West Region receives 80% Outdoor/Casual marketing, dramatically improving regional conversion efficiency.

---

## 📊 Dashboard 5: Operations & Logistics

### Mission 02: Visualization Explanations

**12. Average Delivery Days Over Time**
- **What the chart shows:** A line chart tracking the average time it takes for an order to reach the customer, indicating supply chain health.
- **Key findings:** The mean delivery time is **4.50 days**, with a P95 of **7 days**. The checkout cancellation rate is an alarming **9.19%**, representing **$1,515.9M** in lost revenue.
- **Business implications:** Negotiate a strict 4-day delivery SLA with 3PL partners and conduct an A/B test on the checkout funnel to halve the 9.2% drop-off.

**13. Shipments by Delivery Days**
- **What the chart shows:** A histogram displaying the distribution of delivery times.
- **Key findings:** The delivery distribution is highly uniform between 2 and 7 days.
- **Business implications:** Introduce tiered shipping options (e.g., $15 Express vs Free Standard) to capture customer willingness-to-pay and prioritize urgent logistics.

### Scoring Rubric Analysis

#### Level 1: Descriptive (What Happened?)
- Total Shipped Orders: 625,382
- Cancelled Order Rate: 9.19%
- Dec 2022 Inventory Fill Rate: 96.1%

#### Level 2: Diagnostic (Why Did It Happen?)
- The uniform delivery distribution (2-7 days) indicates that the company is treating all shipping equally rather than prioritizing based on cart value or customer tier.
- A 9.19% cancellation rate indicates severe UX friction at the final checkout step (e.g., unexpected shipping fees or lack of preferred payment methods).

#### Level 3: Predictive (What Will Likely Happen?)
- A 96.1% fill rate at the end of 2022 indicates healthy inventory levels heading into 2023, minimizing near-term stockout risks.

#### Level 4: Prescriptive (What Should We Do?)
1. **Checkout Friction Audit:** Halving the 9.19% cancellation rate translates directly to a massive **$757.9M** potential revenue recovery over the next cycle.
2. **SLA Contractualization:** Implement a strict 4-day delivery SLA with financial penalties for 3PL providers that exceed the threshold.

---

## 📊 Dashboard 6: Anomaly Detection

### Mission 02: Visualization Explanations

**14. Revenue vs COGS Divergence**
- **What the chart shows:** A dual-axis line chart tracking Revenue against COGS to identify loss-making periods.
- **Key findings:** A massive anomaly occurs in **August of odd-years**, where COGS skyrockets to **1.4x of Revenue** (-40% gross margin).
- **Business implications:** Procurement must flatten the biennial inventory cycle. The current strategy of over-ordering in even years leads to a catastrophic financial penalty to clear stock in odd years.

**15. Daily Net Margin Volatility**
- **What the chart shows:** A bar chart colored by profitability, highlighting specific days where margin drops below the historical average.
- **Key findings:** Margin erosion spikes when customers stack multiple promotions. Double-promos degrade order margin by **1.79 percentage points**.
- **Business implications:** Implement an OMS circuit-breaker to strictly prevent double-coupon stacking and block transactions where final price < COGS.

### Scoring Rubric Analysis

#### Level 1: Descriptive (What Happened?)
- Double-Promo Orders: 206 orders (0.029%)
- Margin — Normal Orders: 13.38% | Margin — Double-Promo Orders: 11.58%

#### Level 2: Diagnostic (Why Did It Happen?)
- Refund spikes highly correlate with promotional days. High traffic volume amplifies the baseline return rate, resulting in severe margin erosion on days like Feb 16, 2021 ($199K in refunds).

#### Level 3: Predictive (What Will Likely Happen?)
- Left unchecked, promotional stacking during peak events (like Liberation Day) will continue to erode the profitability of the highest-volume sales days.

#### Level 4: Prescriptive (What Should We Do?)
1. **OMS Circuit-Breaker:** Implement a backend order management rule: `if cart_final_price < COGS, block checkout`. This establishes a hard mathematical floor on profitability.
2. **One-Promo Policy:** Enforce backend mutual exclusion so only the single best promotion applies per cart, preventing the 1.79% margin bleed.


---

## 🎤 Executive Pitching Guide: Deep Dive for Presentations

When presenting these dashboards to judges or stakeholders, do not just read the numbers off the charts. Use this deep-dive guide to tell a compelling business story that connects data anomalies directly to strategic action.

### 1. The "Margin Cycle" Story (Dashboard 1 & 6)
**What to say:** *"You’ll notice a massive anomaly on Dashboard 6 where our COGS exceeds Revenue in August of odd years. This isn't bad data—it's a self-inflicted wound. We are stuck in a biennial inventory trap. We over-procure in even years, and panic-liquidate in odd years, eating a -40% gross margin loss just to clear warehouse space. By flattening our procurement cycle and buying leaner, we eliminate this completely, saving millions in forced markdowns."*
**The Deep 'Why':** Explain that the 10-year historical data proves this is a structural failure in demand planning, not a one-off event. Showing you can diagnose systemic supply-chain issues will score massive points.

### 2. The "Volume vs. Profitability" Paradox (Dashboard 1 & 3)
**What to say:** *"Our Streetwear category is driving 80% of our top-line revenue, which looks great on the surface. But when you look at Dashboard 1, the margin is a mere 11.37%. We are bleeding profit to maintain volume. Conversely, our GenZ category has a 20.2% margin but low volume. Our strategic pivot is simple: use Streetwear as an acquisition hook, but shift 15% of our procurement budget into scaling the highly-efficient GenZ category to actually drive bottom-line profit."*
**The Deep 'Why':** Judges love when you prove that top-line revenue is a vanity metric. True business value comes from margin optimization.

### 3. The "Silent Revenue Leaks" (Dashboard 2 & 5)
**What to say:** *"We identified two massive, silent revenue leaks. First, on Dashboard 5, our checkout cancellation rate is 9.19%, representing over .5 Billion in abandoned intent over 10 years. Second, on Dashboard 2, our 'Lost' cohort has swelled to 25,000 users. Why are they leaving? Look at our delivery times. We have no SLA enforcement, with some orders taking 7 days. By enforcing a strict 4-day SLA with our 3PL partners and adding an automated CRM win-back campaign, we can recover over 00M in immediate top-line revenue."*
**The Deep 'Why':** This connects Operations (Shipping) to Marketing (Retention). Showing cross-domain impact proves you understand the entire business ecosystem, not just isolated charts.

### 4. The "Fading Holiday Peak" (Dashboard 1)
**What to say:** *"If you look at our Q2 orders, Liberation and Labor Day historically drove +150% revenue spikes. But our time-series analysis shows a structural 5% YoY decline in these specific peaks since 2013. We can no longer rely on April/May holidays to float our Q2 numbers. We are proposing a new, manufactured mid-summer event to artificially recreate that peak demand and stabilize our Q2 forecasting."*
**The Deep 'Why':** This shows you aren't just looking at static totals; you are analyzing longitudinal trends and anticipating future shortfalls before they hit the P&L.

### 5. Defending the "Champions Moat" (Dashboard 2)
**What to say:** *"Only 27% of our users are 'Champions', yet they generate an astounding 63.8% of our lifetime revenue. They stay with us for an average of 10 years. This cohort is our defensive moat. Rather than spending blindly on broad-reach acquisition, our primary marketing objective must be defending this moat with a VIP tier—free returns and early access. Defending this 63% revenue block is non-negotiable."*
**The Deep 'Why':** This demonstrates an understanding of the Pareto Principle (80/20 rule) and Customer Lifetime Value (CLV), prioritizing retention over expensive acquisition.

### 6. The "West Coast Anomaly" (Dashboard 4)
**What to say:** *"Nationally, Streetwear is our bread and butter, out-selling Outdoor gear by 2.5 to 1. But when we isolated the geographic data, we found a massive anomaly on the West Coast. Consumers there buy Outdoor gear in massive volumes (nearly 73,000 orders), nearly matching Streetwear one-to-one. Right now, we are wasting ad spend by blanketing the entire country with the exact same Streetwear campaigns. By geographically segmenting our marketing and pushing Outdoor gear heavily to the West, we can instantly boost conversion efficiency without spending an extra dollar on acquisition."*
**The Deep 'Why':** This proves you aren't just looking at macro-averages. Finding a hidden demographic/geographic pocket of high-intent buyers is the holy grail of growth marketing.
