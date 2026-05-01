#!/usr/bin/env python
# coding: utf-8

# # VinDatathon Task 2: Data Preparation & Enrichment
# 
# ## End-to-End Pipeline for Dashboarding
# This notebook is responsible for ingesting all raw operational tables (`sales`, `items`, `returns`, `promos`, `web_traffic`), joining them into a cohesive entity, and engineering business-critical features for the Power BI Dashboard phase. 
# 
# ### Key Engineering Steps:
# 1. **Relational Merging**: Combining transactional data with item master data and return events.
# 2. **Customer Segmentation (RFM)**: Recency, Frequency, and Monetary scoring to identify High-Value vs Churn-Risk customers.
# 3. **Supply Chain Metrics**: Calculating delivery SLAs (`days_to_deliver`) and identifying delayed shipments.
# 4. **Financial Calculations**: Computing explicit `line_gross_profit` and `margin_percentage` per transaction.
# 5. **Data Export**: Outputting the final `tableau_master_dataset.csv` which acts as the single source of truth for the Power BI visualizations.

# # VinDatathon Task 2: Data Preparation & Enrichment
# 
# ## End-to-End Pipeline for Dashboarding
# This notebook is responsible for ingesting all raw operational tables (, , , , ), joining them into a cohesive entity, and engineering business-critical features for the Power BI Dashboard phase. 
# 
# ### Key Engineering Steps:
# 1. **Relational Merging**: Combining transactional data with item master data and return events.
# 2. **Customer Segmentation (RFM)**: Recency, Frequency, and Monetary scoring to identify High-Value vs Churn-Risk customers.
# 3. **Supply Chain Metrics**: Calculating delivery SLAs () and identifying delayed shipments.
# 4. **Financial Calculations**: Computing explicit  and  per transaction.
# 5. **Data Export**: Outputting the final  which acts as the single source of truth for the Power BI visualizations.

# # VinDatathon 2026 — Task 2: Data Preparation for Tableau / Power BI
# 
# **Team / Author:** VinDatathon 2026 Participant  
# **Dataset:** Vietnamese Fashion E-Commerce (Synthetic, 2012–2022)  
# **Goal:** Transform 15 raw CSVs into clean, enriched, analysis-ready tables for business intelligence dashboarding.
# 
# ---
# 
# ## Pipeline Overview
# 
# This notebook executes **Phase 1: Enhanced EDA & Feature Engineering** in 20 structured steps:
# 
# | Step | Output Table | Description |
# |------|-------------|-------------|
# | 1 | *(raw load)* | Load all 15 raw source tables |
# | 2 | `products.csv` | Computed margin & profit per unit |
# | 3 | `dim_geography.csv` | Clean geography dimension |
# | 4 | `dim_promotions.csv` | Clean promotions dimension |
# | 5 | `fact_orders_enriched.csv` | Denormalized fact table with revenue/margin |
# | 6 | `fact_returns_enriched.csv` | Returns with product & order context |
# | 7 | `dim_cust_rfm.csv` | RFM-scored customer segmentation |
# | 8 | `fact_shipments_enriched.csv` | Delivery days, SLA flags |
# | 9 | `fact_sales_daily.csv` | Daily revenue/COGS/margin KPIs |
# | 10 | `fact_inventory.csv` | Inventory value with restock flags |
# | 11 | `fact_web_traffic.csv` | Web session metrics by channel |
# | 12 | `agg_cohort_retention.csv` | Monthly cohort × retention matrix |
# | 13 | `agg_monthly_summary.csv` | Monthly KPI rollup across all domains |
# | 14 | `agg_reviews_summary.csv` | Product reviews aggregated by category |
# | 15 | *(EDA profiling config)* | Statistical profiling setup |
# | 16 | `agg_product_performance.csv` | BCG quadrant + SKU-level KPIs |
# | 17 | `agg_customer_journey.csv` | Full customer lifecycle view |
# | 18 | `agg_promo_effectiveness.csv` | Promotion lift & efficiency analysis |
# | 19 | `agg_channel_funnel.csv` | Traffic → Conversion → Revenue funnel |
# | 20 | `agg_seasonality.csv` | Revenue seasonality by period |
# | **Final** | **`tableau_master_dataset.csv`** | **Master flat join for Tableau / Power BI** |
# 
# ---
# 
# **Output Directory:** `/home/milis/datathon/data/tableu/`
# 

# ## Environment Setup
# 
# Run this cell only if you are on **Google Colab** and need to mount Drive.  
# Skip this cell if running locally — the paths below use absolute local paths.
# 

# ## Imports & Dependencies
# 
# All required libraries are part of the standard data-science stack.  
# Install any missing packages with: `pip install pandas numpy scipy`
# 

# In[1]:


import pandas as pd
import numpy as np
import os
import sys
import io
import warnings
warnings.filterwarnings('ignore')


# In[2]:


import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(style="whitegrid")
print("Visualizations configured.")


# ## Config

# In[3]:


DATA_DIR = '/home/milis/datathon/data/raw'
OUT_DIR  = '/home/milis/datathon/data/tableu'
os.makedirs(OUT_DIR, exist_ok=True)

def load(name, **kw):
    """Load CSV with progress print."""
    path = os.path.join(DATA_DIR, name)
    df = pd.read_csv(path, **kw)
    print(f"  ✓ Loaded {name}: {df.shape[0]:,} rows × {df.shape[1]} cols")
    return df

def save(df, name):
    """Save to tableau_data/ with summary."""
    path = os.path.join(OUT_DIR, name)
    df.to_csv(path, index=False)
    size_mb = os.path.getsize(path) / 1024 / 1024
    print(f"  → Saved {name}: {df.shape[0]:,} rows × {df.shape[1]} cols ({size_mb:.1f} MB)")


# ## STEP 1: Load raw data

# In[4]:


print("STEP 1: Loading raw data")

orders      = load('orders.csv',      parse_dates=['order_date'])
order_items = load('order_items.csv')
payments    = load('payments.csv')
products    = load('products.csv')
customers   = load('customers.csv',   parse_dates=['signup_date'])
geography   = load('geography.csv')
promotions  = load('promotions.csv',  parse_dates=['start_date', 'end_date'])
shipments   = load('shipments.csv',   parse_dates=['ship_date', 'delivery_date'])
returns     = load('returns.csv',     parse_dates=['return_date'])
reviews     = load('reviews.csv',     parse_dates=['review_date'])
inventory   = load('inventory.csv',   parse_dates=['snapshot_date'])
web_traffic = load('web_traffic.csv', parse_dates=['date'])
sales       = load('sales.csv',      parse_dates=['Date'])


# ## STEP 2: dim_products.csv — Products with computed margin

# In[5]:


print("STEP 2: products.csv")

products = products.copy()
products['gross_margin_pct'] = ((products['price'] - products['cogs']) / products['price'] * 100).round(2)
products['profit_per_unit']  = (products['price'] - products['cogs']).round(2)

# Avg rating per product
avg_rating = reviews.groupby('product_id')['rating'].agg(['mean', 'count']).reset_index()
avg_rating.columns = ['product_id', 'avg_rating', 'review_count']
avg_rating['avg_rating'] = avg_rating['avg_rating'].round(2)

# Return stats per product
ret_stats = returns.groupby('product_id').agg(
    total_returns=('return_id', 'count'),
    total_return_qty=('return_quantity', 'sum'),
    total_refund=('refund_amount', 'sum')
).reset_index()

products = products.merge(avg_rating, on='product_id', how='left')
products = products.merge(ret_stats, on='product_id', how='left')
products[['review_count', 'total_returns', 'total_return_qty']] = \
    products[['review_count', 'total_returns', 'total_return_qty']].fillna(0).astype(int)
products['total_refund'] = products['total_refund'].fillna(0)

save(products, 'products.csv')


# ## STEP 3: dim_geography.csv — Geography (as-is)

# In[6]:


print("STEP 3: dim_geography.csv")

save(geography, 'dim_geography.csv')


# ## STEP 4: dim_promotions.csv — Promotions (as-is)

# In[7]:


print("STEP 4: dim_promotions.csv")
save(promotions, 'dim_promotions.csv')


# ## STEP 5: fact_orders_enriched.csv — Denormalized fact table

# In[8]:


print("STEP 5: fact.csv (main fact table)")

# Start with order_items as grain (each line item)
fact = order_items.copy()

# Join orders
fact = fact.merge(
    orders[['order_id', 'order_date', 'customer_id', 'zip',
            'order_status', 'payment_method', 'device_type', 'order_source']],
    on='order_id', how='left'
)

# Join products (key fields only, to avoid bloat)
fact = fact.merge(
    products[['product_id', 'product_name', 'category', 'segment', 'size', 'color', 'price', 'cogs']],
    on='product_id', how='left'
)

#  Join payments
fact = fact.merge(
    payments[['order_id', 'payment_value', 'installments']],
    on='order_id', how='left'
)

#  Join geography (region, city)
fact = fact.merge(
    geography[['zip', 'city', 'region']].drop_duplicates(subset='zip'),
    on='zip', how='left'
)

# Computed fields
fact['line_revenue']       = (fact['quantity'] * fact['unit_price']).round(2)
fact['line_cost']          = (fact['quantity'] * fact['cogs']).round(2)
fact['line_gross_profit']  = (fact['line_revenue'] - fact['line_cost']).round(2)
fact['line_margin_pct']    = np.where(
    fact['line_revenue'] > 0,
    (fact['line_gross_profit'] / fact['line_revenue'] * 100).round(2),
    0
)
fact['has_promo']          = (~fact['promo_id'].isna() & (fact['promo_id'] != '')).astype(int)
fact['has_double_promo']   = (~fact['promo_id_2'].isna() & (fact['promo_id_2'] != '')).astype(int)
fact['discount_pct']       = np.where(
    fact['line_revenue'] + fact['discount_amount'] > 0,
    (fact['discount_amount'] / (fact['line_revenue'] + fact['discount_amount']) * 100).round(2),
    0
)

# Date dimensions
fact['order_year']    = fact['order_date'].dt.year
fact['order_month']   = fact['order_date'].dt.month
fact['order_quarter'] = fact['order_date'].dt.quarter
fact['order_dow']     = fact['order_date'].dt.dayofweek  # 0=Mon
fact['order_dow_name']= fact['order_date'].dt.day_name()
fact['order_ym']      = fact['order_date'].dt.to_period('M').astype(str)

save(fact, 'fact.csv')


# ## STEP 6: fact_returns_enriched.csv

# In[9]:


print("STEP 6: fact_ret.csv")

fact_ret = returns.copy()
fact_ret = fact_ret.merge(
    products[['product_id', 'product_name', 'category', 'segment', 'size', 'color', 'price', 'cogs']],
    on='product_id', how='left'
)
fact_ret = fact_ret.merge(
    orders[['order_id', 'order_date', 'customer_id', 'order_source', 'device_type']],
    on='order_id', how='left'
)
# Time to return
fact_ret['days_to_return'] = (fact_ret['return_date'] - fact_ret['order_date']).dt.days
fact_ret['return_year']    = fact_ret['return_date'].dt.year
fact_ret['return_month']   = fact_ret['return_date'].dt.month
fact_ret['return_ym']      = fact_ret['return_date'].dt.to_period('M').astype(str)

save(fact_ret, 'fact_ret.csv')


# ## STEP 7: dim_customers_rfm.csv — RFM Segmentation

# In[10]:


print("STEP 7: dim_cust.csv (RFM Segmentation)")

# Reference date = last order date in dataset + 1 day
ref_date = orders['order_date'].max() + pd.Timedelta(days=1)
print(f"  Reference date for Recency: {ref_date.date()}")

# Compute RFM per customer
rfm = orders.merge(payments[['order_id', 'payment_value']], on='order_id', how='left')
rfm = rfm[rfm['order_status'] != 'cancelled']  # Exclude cancelled

rfm_agg = rfm.groupby('customer_id').agg(
    last_order_date   = ('order_date', 'max'),
    first_order_date  = ('order_date', 'min'),
    frequency         = ('order_id', 'nunique'),
    monetary          = ('payment_value', 'sum'),
    avg_order_value   = ('payment_value', 'mean'),
).reset_index()

rfm_agg['recency_days'] = (ref_date - rfm_agg['last_order_date']).dt.days
rfm_agg['tenure_days']  = (ref_date - rfm_agg['first_order_date']).dt.days
rfm_agg['monetary']     = rfm_agg['monetary'].round(2)
rfm_agg['avg_order_value'] = rfm_agg['avg_order_value'].round(2)

#  RFM Scores (quintiles 1-5)
rfm_agg['R_score'] = pd.qcut(rfm_agg['recency_days'], q=5, labels=[5,4,3,2,1]).astype(int)
rfm_agg['F_score'] = pd.qcut(rfm_agg['frequency'].rank(method='first'), q=5, labels=[1,2,3,4,5]).astype(int)
rfm_agg['M_score'] = pd.qcut(rfm_agg['monetary'].rank(method='first'), q=5, labels=[1,2,3,4,5]).astype(int)
rfm_agg['RFM_score'] = rfm_agg['R_score'] * 100 + rfm_agg['F_score'] * 10 + rfm_agg['M_score']

#  RFM Segment Labels
def rfm_segment(row):
    r, f, m = row['R_score'], row['F_score'], row['M_score']
    if r >= 4 and f >= 4:
        return 'Champions'
    elif r >= 3 and f >= 3:
        return 'Loyal Customers'
    elif r >= 4 and f <= 2:
        return 'New Customers'
    elif r >= 3 and f >= 1 and m >= 3:
        return 'Potential Loyalists'
    elif r <= 2 and f >= 3:
        return 'At Risk'
    elif r <= 2 and f >= 4 and m >= 4:
        return 'Cant Lose Them'
    elif r <= 2 and f <= 2:
        return 'Lost'
    elif r == 3 and f <= 2:
        return 'About To Sleep'
    else:
        return 'Need Attention'

rfm_agg['rfm_segment'] = rfm_agg.apply(rfm_segment, axis=1)

#  Merge with customer demographics
dim_cust = customers.merge(rfm_agg, on='customer_id', how='left')
dim_cust = dim_cust.merge(
    geography[['zip', 'region']].drop_duplicates(subset='zip'),
    on='zip', how='left'
)

# Signup year/month
dim_cust['signup_year']  = dim_cust['signup_date'].dt.year
dim_cust['signup_month'] = dim_cust['signup_date'].dt.month
dim_cust['signup_ym']    = dim_cust['signup_date'].dt.to_period('M').astype(str)

# Fill NAs for customers without orders
dim_cust['frequency']    = dim_cust['frequency'].fillna(0).astype(int)
dim_cust['monetary']     = dim_cust['monetary'].fillna(0)
dim_cust['rfm_segment']  = dim_cust['rfm_segment'].fillna('Never Purchased')

# Segment distribution
print("\n  RFM Segment distribution:")
print(dim_cust['rfm_segment'].value_counts().to_string())

save(dim_cust, 'dim_cust.csv')


# ## STEP 8: fact_shipments_enriched.csv

# In[11]:


print("STEP 8: fact_ship.csv")

fact_ship = shipments.copy()
fact_ship['delivery_days']     = (fact_ship['delivery_date'] - fact_ship['ship_date']).dt.days
fact_ship['processing_days']   = None  # Will compute after join

# Join order info for processing time
fact_ship = fact_ship.merge(
    orders[['order_id', 'order_date', 'zip', 'order_status']],
    on='order_id', how='left'
)
fact_ship['processing_days'] = (fact_ship['ship_date'] - fact_ship['order_date']).dt.days
fact_ship['total_lead_time'] = (fact_ship['delivery_date'] - fact_ship['order_date']).dt.days

# Join geography for region
fact_ship = fact_ship.merge(
    geography[['zip', 'region', 'city']].drop_duplicates(subset='zip'),
    on='zip', how='left'
)

# Date dims
fact_ship['ship_year']  = fact_ship['ship_date'].dt.year
fact_ship['ship_month'] = fact_ship['ship_date'].dt.month
fact_ship['ship_ym']    = fact_ship['ship_date'].dt.to_period('M').astype(str)

# Delivery performance buckets
fact_ship['delivery_bucket'] = pd.cut(
    fact_ship['delivery_days'],
    bins=[-1, 2, 5, 7, 14, 999],
    labels=['1-2 days', '3-5 days', '6-7 days', '8-14 days', '15+ days']
)

save(fact_ship, 'fact_ship.csv')


# ## STEP 9: fact_sales_daily.csv — Sales with computed fields

# In[12]:


print("STEP 9: fact_sales.csv")

fact_sales = sales.copy()
fact_sales.columns = ['date', 'revenue', 'cogs']
fact_sales['gross_profit']    = (fact_sales['revenue'] - fact_sales['cogs']).round(2)
fact_sales['gross_margin_pct']= (fact_sales['gross_profit'] / fact_sales['revenue'] * 100).round(2)

# Date dimensions
fact_sales['year']         = fact_sales['date'].dt.year
fact_sales['month']        = fact_sales['date'].dt.month
fact_sales['quarter']      = fact_sales['date'].dt.quarter
fact_sales['day_of_week']  = fact_sales['date'].dt.dayofweek
fact_sales['dow_name']     = fact_sales['date'].dt.day_name()
fact_sales['is_weekend']   = (fact_sales['day_of_week'] >= 5).astype(int)
fact_sales['year_month']   = fact_sales['date'].dt.to_period('M').astype(str)

# Rolling averages
fact_sales = fact_sales.sort_values('date')
fact_sales['revenue_ma7']  = fact_sales['revenue'].rolling(7, min_periods=1).mean().round(2)
fact_sales['revenue_ma30'] = fact_sales['revenue'].rolling(30, min_periods=1).mean().round(2)
fact_sales['cogs_ma7']     = fact_sales['cogs'].rolling(7, min_periods=1).mean().round(2)
fact_sales['cogs_ma30']    = fact_sales['cogs'].rolling(30, min_periods=1).mean().round(2)

# YoY growth (compare to same day last year)
fact_sales['revenue_ly'] = fact_sales['revenue'].shift(365)
fact_sales['yoy_growth_pct'] = np.where(
    fact_sales['revenue_ly'] > 0,
    ((fact_sales['revenue'] - fact_sales['revenue_ly']) / fact_sales['revenue_ly'] * 100).round(2),
    np.nan
)
fact_sales.drop(columns=['revenue_ly'], inplace=True)

save(fact_sales, 'fact_sales.csv')


# ## STEP 10: fact_inventory.csv — Inventory (clean)

# In[13]:


print("STEP 10: fact_inventory.csv")

fact_inv = inventory.copy()
# Add inventory value
fact_inv = fact_inv.merge(
    products[['product_id', 'price', 'cogs']].rename(
        columns={'price': 'product_price', 'cogs': 'product_cogs'}
    ),
    on='product_id', how='left'
)
fact_inv['inventory_value_retail'] = (fact_inv['stock_on_hand'] * fact_inv['product_price']).round(2)
fact_inv['inventory_value_cost']   = (fact_inv['stock_on_hand'] * fact_inv['product_cogs']).round(2)

# Inventory health label
def inv_health(row):
    if row['stockout_flag'] == 1:
        return 'Stockout'
    elif row['overstock_flag'] == 1:
        return 'Overstock'
    elif row['reorder_flag'] == 1:
        return 'Reorder Needed'
    else:
        return 'Healthy'

fact_inv['inventory_health'] = fact_inv.apply(inv_health, axis=1)

save(fact_inv, 'fact_inventory.csv')


# ## STEP 11: fact_web_traffic.csv — Web traffic (clean)

# In[14]:


print("STEP 11: fact_web.csv")

fact_web = web_traffic.copy()
fact_web.rename(columns={'date': 'traffic_date'}, inplace=True)
fact_web['year']  = fact_web['traffic_date'].dt.year
fact_web['month'] = fact_web['traffic_date'].dt.month
fact_web['year_month'] = fact_web['traffic_date'].dt.to_period('M').astype(str)

# Pages per session
fact_web['pages_per_session'] = (fact_web['page_views'] / fact_web['sessions']).round(2)

save(fact_web, 'fact_web.csv')


# ## STEP 12: agg_cohort_retention.csv — Cohort Retention Matrix

# In[15]:


print("STEP 12: agg_cohort_retention.csv")
# First purchase month per customer (cohort)
first_order = orders[orders['order_status'] != 'cancelled'].groupby('customer_id')['order_date'].min().reset_index()
first_order.columns = ['customer_id', 'cohort_date']
first_order['cohort_month'] = first_order['cohort_date'].dt.to_period('M')

# All orders with cohort
orders_cohort = orders[orders['order_status'] != 'cancelled'][['order_id', 'customer_id', 'order_date']].copy()
orders_cohort['order_month'] = orders_cohort['order_date'].dt.to_period('M')
orders_cohort = orders_cohort.merge(first_order[['customer_id', 'cohort_month']], on='customer_id')

# Period number (months since cohort)
orders_cohort['period_number'] = (
    (orders_cohort['order_month'].dt.year - orders_cohort['cohort_month'].dt.year) * 12 +
    (orders_cohort['order_month'].dt.month - orders_cohort['cohort_month'].dt.month)
)

# Cohort size
cohort_sizes = orders_cohort.groupby('cohort_month')['customer_id'].nunique().reset_index()
cohort_sizes.columns = ['cohort_month', 'cohort_size']

# Retention counts
retention = orders_cohort.groupby(['cohort_month', 'period_number'])['customer_id'].nunique().reset_index()
retention.columns = ['cohort_month', 'period_number', 'active_customers']

# Merge sizes
retention = retention.merge(cohort_sizes, on='cohort_month')
retention['retention_rate'] = (retention['active_customers'] / retention['cohort_size'] * 100).round(2)

# Convert period to string for Tableau
retention['cohort_month'] = retention['cohort_month'].astype(str)

# Limit to first 24 months for readability
retention = retention[retention['period_number'] <= 24]

save(retention, 'agg_cohort_retention.csv')


# ## STEP 13: agg_monthly_summary.csv — Monthly KPI rollup

# In[16]:


print("STEP 13: agg_monthly_summary.csv")

# Monthly sales
monthly_sales = fact_sales.groupby('year_month').agg(
    revenue       = ('revenue', 'sum'),
    cogs          = ('cogs', 'sum'),
    gross_profit  = ('gross_profit', 'sum'),
    avg_daily_rev = ('revenue', 'mean'),
    days_in_month = ('revenue', 'count'),
).reset_index()
monthly_sales['gross_margin_pct'] = (monthly_sales['gross_profit'] / monthly_sales['revenue'] * 100).round(2)

# Monthly orders
orders_monthly = orders.copy()
orders_monthly['year_month'] = orders_monthly['order_date'].dt.to_period('M').astype(str)
mo = orders_monthly.groupby('year_month').agg(
    total_orders     = ('order_id', 'nunique'),
    unique_customers = ('customer_id', 'nunique'),
    cancelled_orders = ('order_status', lambda x: (x == 'cancelled').sum()),
).reset_index()
mo['cancel_rate_pct'] = (mo['cancelled_orders'] / mo['total_orders'] * 100).round(2)

# Monthly returns
returns_monthly = returns.copy()
returns_monthly['year_month'] = returns_monthly['return_date'].dt.to_period('M').astype(str)
mr = returns_monthly.groupby('year_month').agg(
    total_returns = ('return_id', 'count'),
    total_refund  = ('refund_amount', 'sum'),
).reset_index()

# Merge all
monthly = monthly_sales.merge(mo, on='year_month', how='left')
monthly = monthly.merge(mr, on='year_month', how='left')
monthly['total_returns'] = monthly['total_returns'].fillna(0).astype(int)
monthly['total_refund']  = monthly['total_refund'].fillna(0)
monthly['return_rate_pct'] = np.where(
    monthly['total_orders'] > 0,
    (monthly['total_returns'] / monthly['total_orders'] * 100).round(2),
    0
)
monthly['aov'] = (monthly['revenue'] / monthly['total_orders']).round(2)

# Revenue growth MoM
monthly = monthly.sort_values('year_month')
monthly['revenue_prev'] = monthly['revenue'].shift(1)
monthly['mom_growth_pct'] = np.where(
    monthly['revenue_prev'] > 0,
    ((monthly['revenue'] - monthly['revenue_prev']) / monthly['revenue_prev'] * 100).round(2),
    np.nan
)
monthly.drop(columns=['revenue_prev'], inplace=True)

save(monthly, 'agg_monthly_summary.csv')


# ## STEP 14: agg_reviews_summary.csv — Reviews aggregated

# In[17]:


print("STEP 14: agg_reviews_summary.csv")

reviews_enriched = reviews.merge(
    products[['product_id', 'category', 'segment']],
    on='product_id', how='left'
)
reviews_enriched['review_ym'] = reviews_enriched['review_date'].dt.to_period('M').astype(str)

# Monthly avg rating by category
rev_summary = reviews_enriched.groupby(['review_ym', 'category']).agg(
    avg_rating    = ('rating', 'mean'),
    review_count  = ('review_id', 'count'),
    pct_5_star    = ('rating', lambda x: (x == 5).mean() * 100),
    pct_1_star    = ('rating', lambda x: (x == 1).mean() * 100),
).reset_index()
rev_summary['avg_rating'] = rev_summary['avg_rating'].round(2)
rev_summary['pct_5_star'] = rev_summary['pct_5_star'].round(2)
rev_summary['pct_1_star'] = rev_summary['pct_1_star'].round(2)

save(rev_summary, 'agg_reviews_summary.csv')


# ## STEP 15: Advanced EDA Configuration & Statistical Profiling
# 
# Sets up helper utilities for outlier detection (Z-score, IQR) and
# cross-table relationship validation used in Steps 16–20.
# 

# In[18]:


import os
import numpy as np
from scipy import stats

OUT_DIR = '/home/milis/datathon/data/tableu'
os.makedirs(OUT_DIR, exist_ok=True)

def save_eda_csv(df, name):
    df.to_csv(os.path.join(OUT_DIR, name), index=False)
    print(f'Saved {name} with shape {df.shape}')


# ## STEP 16: agg_product_performance.csv

# In[19]:


def build_product_performance(fact_orders, products, fact_returns):
    perf = fact_orders.groupby('product_id').agg(
        total_revenue   = ('line_revenue', 'sum'),
        total_qty       = ('quantity', 'sum'),
        total_orders    = ('order_id', 'nunique'),
        avg_margin_pct  = ('line_margin_pct', 'mean'),
        avg_discount_pct= ('discount_pct', 'mean'),
        promo_order_rate= ('has_promo', 'mean'),
    ).reset_index()
    ret_by_product = fact_returns.groupby('product_id').agg(
        return_count = ('return_id', 'count'),
        return_qty   = ('return_quantity', 'sum'),
        avg_days_to_return = ('days_to_return', 'mean'),
    ).reset_index()
    perf = perf.merge(ret_by_product, on='product_id', how='left')
    perf['return_rate'] = (perf['return_count'] / perf['total_orders']).fillna(0).round(4)
    perf = perf.merge(products[['product_id','product_name','category','segment',
                                     'avg_rating','gross_margin_pct']], on='product_id', how='left')
    perf['revenue_pct_rank'] = perf['total_revenue'].rank(pct=True)
    median_revenue = perf['total_revenue'].median()
    median_margin  = perf['avg_margin_pct'].median()
    def bcg_label(row):
        hi_rev  = row['total_revenue'] > median_revenue
        hi_marg = row['avg_margin_pct'] > median_margin
        if hi_rev and hi_marg:   return 'Star'
        elif hi_rev:             return 'Cash Cow'
        elif hi_marg:            return 'Question Mark'
        else:                    return 'Dog'
    perf['bcg_quadrant'] = perf.apply(bcg_label, axis=1)
    return perf

agg_product_performance = build_product_performance(fact, products, fact_ret)
save_eda_csv(agg_product_performance, 'agg_product_performance.csv')


# ## STEP 17: agg_customer_journey.csv

# In[20]:


def build_customer_journey(customers, orders, payments, dim_cust):
    journey = customers[['customer_id', 'signup_date', 'acquisition_channel']].copy()
    order_agg = orders[orders['order_status'] != 'cancelled'].groupby('customer_id').agg(
        first_order_date = ('order_date', 'min'),
        last_order_date  = ('order_date', 'max'),
        total_orders     = ('order_id', 'nunique'),
    ).reset_index()
    journey = journey.merge(order_agg, on='customer_id', how='left')
    journey['days_to_first_order'] = (journey['first_order_date'] - journey['signup_date']).dt.days
    journey['converted'] = journey['first_order_date'].notna().astype(int)
    all_orders_sorted = orders[orders['order_status'] != 'cancelled'].sort_values(['customer_id', 'order_date'])
    all_orders_sorted['prev_order_date'] = all_orders_sorted.groupby('customer_id')['order_date'].shift(1)
    all_orders_sorted['inter_order_days'] = (all_orders_sorted['order_date'] - all_orders_sorted['prev_order_date']).dt.days
    avg_gap = all_orders_sorted.groupby('customer_id')['inter_order_days'].mean().round(1).reset_index()
    avg_gap.columns = ['customer_id', 'avg_inter_order_days']
    journey = journey.merge(avg_gap, on='customer_id', how='left')
    journey = journey.merge(dim_cust[['customer_id','rfm_segment','monetary','R_score','F_score','M_score']], on='customer_id', how='left')
    return journey

agg_customer_journey = build_customer_journey(customers, fact, payments, dim_cust)
save_eda_csv(agg_customer_journey, 'agg_customer_journey.csv')


# ## STEP 18: agg_promo_effectiveness.csv

# In[21]:


def build_promo_effectiveness(fact_orders, promotions):
    promo_orders = fact_orders[fact_orders['has_promo'] == 1].copy()
    no_promo     = fact_orders[fact_orders['has_promo'] == 0].copy()
    promo_agg = promo_orders.groupby('promo_id').agg(
        promo_order_count   = ('order_id', 'nunique'),
        promo_revenue       = ('line_revenue', 'sum'),
        promo_avg_basket    = ('line_revenue', lambda x: x.groupby(promo_orders.loc[x.index, 'order_id']).sum().mean()),
        promo_avg_margin    = ('line_margin_pct', 'mean'),
        promo_avg_discount  = ('discount_pct', 'mean'),
        unique_customers    = ('customer_id', 'nunique'),
    ).reset_index()
    promo_agg = promo_agg.merge(promotions[['promo_id','promo_type','discount_value','applicable_category']], on='promo_id', how='left')
    no_promo_aov = no_promo.groupby(['category','order_id'])['line_revenue'].sum().groupby(level=0).mean().reset_index()
    no_promo_aov.columns = ['applicable_category', 'baseline_aov']
    promo_agg = promo_agg.merge(no_promo_aov, on='applicable_category', how='left')
    promo_agg['discount_cost'] = (promo_agg['promo_revenue'] * promo_agg['promo_avg_discount'] / 100)
    promo_agg['revenue_per_discount_unit'] = (promo_agg['promo_revenue'] / promo_agg['discount_cost'].replace(0, np.nan)).round(2)
    return promo_agg

agg_promo_effectiveness = build_promo_effectiveness(fact, promotions)
save_eda_csv(agg_promo_effectiveness, 'agg_promo_effectiveness.csv')


# ## STEP 19: agg_channel_funnel.csv

# In[22]:


def build_channel_funnel(fact_web, fact_orders, payments):
    web_monthly = fact_web.groupby(['year_month', 'traffic_source']).agg(
        sessions        = ('sessions', 'sum'),
        page_views      = ('page_views', 'sum'),
        avg_bounce_rate = ('bounce_rate', 'mean'),
    ).reset_index()
    fact_orders['year_month'] = fact_orders['order_date'].dt.to_period('M').astype(str)
    order_monthly = fact_orders.groupby(['year_month', 'order_source']).agg(
        orders     = ('order_id', 'nunique'),
        revenue    = ('line_revenue', 'sum'),
        customers  = ('customer_id', 'nunique'),
    ).reset_index().rename(columns={'order_source': 'traffic_source'})
    funnel = web_monthly.merge(order_monthly, on=['year_month', 'traffic_source'], how='outer')
    funnel['actual_conv_rate'] = (funnel['orders'] / funnel['sessions'] * 100).round(4)
    funnel['revenue_per_session'] = (funnel['revenue'] / funnel['sessions']).round(2)
    funnel['cac_proxy'] = (funnel['revenue'] / funnel['customers']).round(2)
    return funnel

agg_channel_funnel = build_channel_funnel(fact_web, fact, payments)
save_eda_csv(agg_channel_funnel, 'agg_channel_funnel.csv')


# ## STEP 20: agg_seasonality.csv

# In[23]:


def build_seasonality(fact_sales):
    seas = fact_sales[['date','revenue','gross_margin_pct','year','month','quarter']].copy()
    seas['week_of_year'] = seas['date'].dt.isocalendar().week.astype(int)
    seas['day_of_week']  = seas['date'].dt.dayofweek
    seas['is_weekend']   = (seas['day_of_week'] >= 5).astype(int)
    vn_holidays = {(1, 1): 'New Year', (1, 27): 'Tet_eve', (1, 29): 'Tet', (4, 30): 'Liberation', (5, 1): 'Labor', (9, 2): 'National Day'}
    def is_holiday(row):
        key = (row['date'].month, row['date'].day)
        return vn_holidays.get(key, 'Normal')
    seas['holiday_type'] = seas.apply(is_holiday, axis=1)
    monthly_avg = seas.groupby('month')['revenue'].mean().rename('monthly_avg_revenue')
    seas = seas.merge(monthly_avg, on='month', how='left')
    seas['seasonality_index'] = (seas['revenue'] / seas['monthly_avg_revenue']).round(4)
    return seas

agg_seasonality = build_seasonality(fact_sales)
save_eda_csv(agg_seasonality, 'agg_seasonality.csv')


# ## Visualizations: Module A - Revenue & Sales Dynamics

# In[ ]:


print("Generating Module A Visualizations...")
# A1: Full Revenue Timeline with Rolling Average
plt.figure(figsize=(14, 6))
sns.lineplot(data=fact_sales, x='date', y='revenue', alpha=0.5, label='Daily Revenue')
sns.lineplot(data=fact_sales, x='date', y='revenue_ma30', color='red', label='30-Day Moving Avg')
plt.title('A1: Full Revenue Timeline (2012-2022)')
plt.ylabel('Revenue')
plt.legend()
plt.tight_layout()
plt.show()

# A2: Revenue vs. COGS Gap (Gross Profit)
monthly_sales = fact_sales.groupby('year_month').agg({'revenue':'sum', 'cogs':'sum'}).reset_index()
plt.figure(figsize=(14, 6))
plt.fill_between(monthly_sales['year_month'], monthly_sales['revenue'], alpha=0.4, color='green', label='Gross Profit')
plt.fill_between(monthly_sales['year_month'], monthly_sales['cogs'], alpha=0.8, color='red', label='COGS')
plt.plot(monthly_sales['year_month'], monthly_sales['revenue'], color='green', linewidth=1)
plt.title('A2: Revenue vs. COGS Gap (Gross Profit)')
plt.xticks(monthly_sales['year_month'][::12], rotation=45)
plt.legend()
plt.tight_layout()
plt.show()

# A3: Monthly Seasonality Heatmap
heatmap_data = fact_sales.pivot_table(index='year', columns='month', values='revenue', aggfunc='mean')
plt.figure(figsize=(12, 8))
sns.heatmap(heatmap_data, cmap='YlGnBu', annot=False)
plt.title('A3: Monthly Seasonality Heatmap (Avg Daily Revenue)')
plt.tight_layout()
plt.show()

# A6: Revenue Decomposition (Price x Quantity)
yearly_vol = fact.groupby('order_year').agg(total_quantity=('quantity','sum'), avg_price=('unit_price','mean')).reset_index()
fig, ax1 = plt.subplots(figsize=(12, 6))
ax2 = ax1.twinx()
ax1.bar(yearly_vol['order_year'], yearly_vol['total_quantity'], alpha=0.6, color='blue', label='Total Quantity')
ax2.plot(yearly_vol['order_year'], yearly_vol['avg_price'], color='red', marker='o', linewidth=2, label='Avg Unit Price')
ax1.set_ylabel('Total Quantity', color='blue')
ax2.set_ylabel('Avg Unit Price', color='red')
plt.title('A6: Revenue Decomposition (Price vs Volume)')
plt.tight_layout()
plt.show()


# ## Visualizations: Module B - Customer Intelligence

# In[ ]:


print("Generating Module B Visualizations...")
# B1: Customer Acquisition Timeline
signup_monthly = customers['signup_date'].dt.to_period('M').value_counts().sort_index().reset_index()
signup_monthly.columns = ['month', 'signups']
signup_monthly['cumulative_signups'] = signup_monthly['signups'].cumsum()
fig, ax1 = plt.subplots(figsize=(14, 6))
ax2 = ax1.twinx()
ax1.bar(signup_monthly['month'].astype(str), signup_monthly['signups'], alpha=0.5, color='purple', label='New Signups')
ax2.plot(signup_monthly['month'].astype(str), signup_monthly['cumulative_signups'], color='black', linewidth=2, label='Cumulative Signups')
ax1.set_xticks(signup_monthly['month'].astype(str)[::12])
ax1.set_xticklabels(signup_monthly['month'].astype(str)[::12], rotation=45)
plt.title('B1: Customer Acquisition Timeline')
plt.tight_layout()
plt.show()

# B4: Cohort Retention Heatmap
retention = pd.read_csv('/home/milis/datathon/data/tableu/agg_cohort_retention.csv')
ret_pivot = retention.pivot(index='cohort_month', columns='period_number', values='retention_rate')
plt.figure(figsize=(16, 10))
sns.heatmap(ret_pivot.iloc[::3, :24], cmap='Blues', annot=False, vmin=0, vmax=100)
plt.title('B4: Cohort Retention Heatmap (%) - Sampled Quarterly Cohorts')
plt.ylabel('Cohort Month')
plt.xlabel('Months Since Signup')
plt.tight_layout()
plt.show()

# B5: RFM Segmentation Scatter Plot
plt.figure(figsize=(10, 8))
sns.scatterplot(data=dim_cust.sample(min(10000, len(dim_cust))), x='frequency', y='monetary', hue='R_score', palette='RdYlGn', alpha=0.6)
plt.title('B5: RFM Scatter Plot (Frequency vs Monetary, colored by Recency Score)')
plt.xscale('log')
plt.yscale('log')
plt.tight_layout()
plt.show()


# ## Visualizations: Module C - Product & Inventory

# In[ ]:


print("Generating Module C Visualizations...")
# C2: Margin Distribution Boxplot by Category
plt.figure(figsize=(12, 6))
sns.boxplot(data=products, x='category', y='gross_margin_pct')
plt.title('C2: Margin Distribution by Category')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# C4: Stockout Rate by Category
inv_cat = fact_inv.merge(products[['product_id','category']], on='product_id')
inv_cat['snapshot_month'] = inv_cat['snapshot_date'].dt.to_period('M').astype(str)
stockout_cat = inv_cat.groupby(['snapshot_month', 'category'])['stockout_flag'].mean().reset_index()
plt.figure(figsize=(14, 6))
sns.lineplot(data=stockout_cat, x='snapshot_month', y='stockout_flag', hue='category')
plt.title('C4: Monthly Stockout Rate by Category')
plt.xticks(stockout_cat['snapshot_month'].unique()[::12], rotation=45)
plt.ylabel('Stockout Rate')
plt.tight_layout()
plt.show()


# ## Visualizations: Modules D, E, F - Operations & Funnel

# In[ ]:


print("Generating Module D, E, F Visualizations...")
# D3: Promotion Revenue Bar Chart
promo_eff = pd.read_csv('/home/milis/datathon/data/tableu/agg_promo_effectiveness.csv')
plt.figure(figsize=(12, 6))
sns.barplot(data=promo_eff.sort_values('promo_revenue', ascending=False).head(10), x='promo_id', y='promo_revenue')
plt.title('D3: Top 10 Promotions by Revenue Generated')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# E1: Traffic Source Mix Area Chart
traffic_mix = fact_web.groupby(['year_month', 'traffic_source'])['sessions'].sum().unstack().fillna(0)
traffic_mix.plot(kind='area', stacked=True, figsize=(14, 6), colormap='Set2')
plt.title('E1: Traffic Source Mix Over Time')
plt.ylabel('Sessions')
plt.tight_layout()
plt.show()

# F1: Delivery Time Histogram
plt.figure(figsize=(10, 6))
sns.histplot(data=fact_ship, x='delivery_days', bins=30, kde=True, color='teal')
plt.title('F1: Delivery Time Distribution')
plt.xlim(0, 20)
plt.tight_layout()
plt.show()


# ## STEP 21: G1 - Price Inflation Signal

# ## Visualizations: Module A - Revenue & Sales Dynamics

# In[ ]:


print("Generating Module A Visualizations...")
# A1: Full Revenue Timeline with Rolling Average
plt.figure(figsize=(14, 6))
sns.lineplot(data=fact_sales, x='date', y='revenue', alpha=0.5, label='Daily Revenue')
sns.lineplot(data=fact_sales, x='date', y='revenue_ma30', color='red', label='30-Day Moving Avg')
plt.title('A1: Full Revenue Timeline (2012-2022)')
plt.ylabel('Revenue')
plt.legend()
plt.tight_layout()
plt.show()

# A2: Revenue vs. COGS Gap (Gross Profit)
monthly_sales = fact_sales.groupby('year_month').agg({'revenue':'sum', 'cogs':'sum'}).reset_index()
plt.figure(figsize=(14, 6))
plt.fill_between(monthly_sales['year_month'], monthly_sales['revenue'], alpha=0.4, color='green', label='Gross Profit')
plt.fill_between(monthly_sales['year_month'], monthly_sales['cogs'], alpha=0.8, color='red', label='COGS')
plt.plot(monthly_sales['year_month'], monthly_sales['revenue'], color='green', linewidth=1)
plt.title('A2: Revenue vs. COGS Gap (Gross Profit)')
plt.xticks(monthly_sales['year_month'][::12], rotation=45)
plt.legend()
plt.tight_layout()
plt.show()

# A3: Monthly Seasonality Heatmap
heatmap_data = fact_sales.pivot_table(index='year', columns='month', values='revenue', aggfunc='mean')
plt.figure(figsize=(12, 8))
sns.heatmap(heatmap_data, cmap='YlGnBu', annot=False)
plt.title('A3: Monthly Seasonality Heatmap (Avg Daily Revenue)')
plt.tight_layout()
plt.show()

# A6: Revenue Decomposition (Price x Quantity)
yearly_vol = fact.groupby('order_year').agg(total_quantity=('quantity','sum'), avg_price=('unit_price','mean')).reset_index()
fig, ax1 = plt.subplots(figsize=(12, 6))
ax2 = ax1.twinx()
ax1.bar(yearly_vol['order_year'], yearly_vol['total_quantity'], alpha=0.6, color='blue', label='Total Quantity')
ax2.plot(yearly_vol['order_year'], yearly_vol['avg_price'], color='red', marker='o', linewidth=2, label='Avg Unit Price')
ax1.set_ylabel('Total Quantity', color='blue')
ax2.set_ylabel('Avg Unit Price', color='red')
plt.title('A6: Revenue Decomposition (Price vs Volume)')
plt.tight_layout()
plt.show()


# ## Visualizations: Module B - Customer Intelligence

# In[ ]:


print("Generating Module B Visualizations...")
# B1: Customer Acquisition Timeline
signup_monthly = customers['signup_date'].dt.to_period('M').value_counts().sort_index().reset_index()
signup_monthly.columns = ['month', 'signups']
signup_monthly['cumulative_signups'] = signup_monthly['signups'].cumsum()
fig, ax1 = plt.subplots(figsize=(14, 6))
ax2 = ax1.twinx()
ax1.bar(signup_monthly['month'].astype(str), signup_monthly['signups'], alpha=0.5, color='purple', label='New Signups')
ax2.plot(signup_monthly['month'].astype(str), signup_monthly['cumulative_signups'], color='black', linewidth=2, label='Cumulative Signups')
ax1.set_xticks(signup_monthly['month'].astype(str)[::12])
ax1.set_xticklabels(signup_monthly['month'].astype(str)[::12], rotation=45)
plt.title('B1: Customer Acquisition Timeline')
plt.tight_layout()
plt.show()

# B4: Cohort Retention Heatmap
retention = pd.read_csv('/home/milis/datathon/data/tableu/agg_cohort_retention.csv')
ret_pivot = retention.pivot(index='cohort_month', columns='period_number', values='retention_rate')
plt.figure(figsize=(16, 10))
sns.heatmap(ret_pivot.iloc[::3, :24], cmap='Blues', annot=False, vmin=0, vmax=100)
plt.title('B4: Cohort Retention Heatmap (%) - Sampled Quarterly Cohorts')
plt.ylabel('Cohort Month')
plt.xlabel('Months Since Signup')
plt.tight_layout()
plt.show()

# B5: RFM Segmentation Scatter Plot
plt.figure(figsize=(10, 8))
sns.scatterplot(data=dim_cust.sample(min(10000, len(dim_cust))), x='frequency', y='monetary', hue='R_score', palette='RdYlGn', alpha=0.6)
plt.title('B5: RFM Scatter Plot (Frequency vs Monetary, colored by Recency Score)')
plt.xscale('log')
plt.yscale('log')
plt.tight_layout()
plt.show()


# ## Visualizations: Module C - Product & Inventory

# In[ ]:


print("Generating Module C Visualizations...")
# C2: Margin Distribution Boxplot by Category
plt.figure(figsize=(12, 6))
sns.boxplot(data=products, x='category', y='gross_margin_pct')
plt.title('C2: Margin Distribution by Category')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# C4: Stockout Rate by Category
inv_cat = fact_inv.merge(products[['product_id','category']], on='product_id')
inv_cat['snapshot_month'] = inv_cat['snapshot_date'].dt.to_period('M').astype(str)
stockout_cat = inv_cat.groupby(['snapshot_month', 'category'])['stockout_flag'].mean().reset_index()
plt.figure(figsize=(14, 6))
sns.lineplot(data=stockout_cat, x='snapshot_month', y='stockout_flag', hue='category')
plt.title('C4: Monthly Stockout Rate by Category')
plt.xticks(stockout_cat['snapshot_month'].unique()[::12], rotation=45)
plt.ylabel('Stockout Rate')
plt.tight_layout()
plt.show()


# ## Visualizations: Modules D, E, F - Operations & Funnel

# In[ ]:


print("Generating Module D, E, F Visualizations...")
# D3: Promotion Revenue Bar Chart
promo_eff = pd.read_csv('/home/milis/datathon/data/tableu/agg_promo_effectiveness.csv')
plt.figure(figsize=(12, 6))
sns.barplot(data=promo_eff.sort_values('promo_revenue', ascending=False).head(10), x='promo_id', y='promo_revenue')
plt.title('D3: Top 10 Promotions by Revenue Generated')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# E1: Traffic Source Mix Area Chart
traffic_mix = fact_web.groupby(['year_month', 'traffic_source'])['sessions'].sum().unstack().fillna(0)
traffic_mix.plot(kind='area', stacked=True, figsize=(14, 6), colormap='Set2')
plt.title('E1: Traffic Source Mix Over Time')
plt.ylabel('Sessions')
plt.tight_layout()
plt.show()

# F1: Delivery Time Histogram
plt.figure(figsize=(10, 6))
sns.histplot(data=fact_ship, x='delivery_days', bins=30, kde=True, color='teal')
plt.title('F1: Delivery Time Distribution')
plt.xlim(0, 20)
plt.tight_layout()
plt.show()


# In[24]:


print("STEP 21: G1 - Price Inflation Signal")
price_by_year = (
    order_items
    .merge(orders[["order_id","order_date"]], on="order_id")
    .assign(year=lambda df: df["order_date"].dt.year)
    .merge(products[["product_id", "category", "price"]], on="product_id")
)

price_trend = price_by_year.groupby(["category", "year"]).agg(
    median_sold_price=('unit_price', 'median'),
    base_catalog_price=('price', 'median')
).reset_index()

price_trend['inflation_gap'] = price_trend['median_sold_price'] - price_trend['base_catalog_price']

save_eda_csv(price_trend, 'agg_price_inflation.csv')

plt.figure(figsize=(12, 6))
sns.lineplot(data=price_trend, x='year', y='median_sold_price', hue='category', marker='o')
plt.title('G1: Median Sold Unit Price by Category Over Time (Inflation Signal)')
plt.ylabel('Median Sold Price')
plt.xlabel('Year')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()


# ## STEP 22: G2 - Demand Shock Events

# In[25]:


print("STEP 22: G2 - Demand Shock Events")
daily_orders = orders[orders['order_status'] != 'cancelled'].groupby('order_date').size().reset_index(name='daily_order_count')
daily_orders['rolling_mean_30'] = daily_orders['daily_order_count'].rolling(30, min_periods=1).mean()
daily_orders['rolling_std_30'] = daily_orders['daily_order_count'].rolling(30, min_periods=1).std().fillna(0)

daily_orders['is_shock'] = daily_orders['daily_order_count'] > (daily_orders['rolling_mean_30'] + 3 * daily_orders['rolling_std_30'])

save_eda_csv(daily_orders[daily_orders['is_shock']], 'agg_demand_shocks.csv')

plt.figure(figsize=(14, 6))
plt.plot(daily_orders['order_date'], daily_orders['daily_order_count'], label='Daily Orders', alpha=0.6)
plt.plot(daily_orders['order_date'], daily_orders['rolling_mean_30'], label='30-Day Moving Avg', color='orange')
shock_points = daily_orders[daily_orders['is_shock']]
plt.scatter(shock_points['order_date'], shock_points['daily_order_count'], color='red', label='Demand Shock (>3σ)', zorder=5)
plt.title('G2: Demand Shock Events (Daily Orders)')
plt.legend()
plt.tight_layout()
plt.show()


# ## STEP 23: G3 - Customer LTV by Cohort x Channel

# In[26]:


print("STEP 23: G3 - Customer LTV by Cohort x Channel")

cust_ltv = customers[['customer_id', 'signup_date', 'acquisition_channel']].copy()
cust_ltv['cohort_yq'] = cust_ltv['signup_date'].dt.to_period('Q').astype(str)

order_rev = fact.groupby(['customer_id', 'order_date'])['line_revenue'].sum().reset_index()
order_rev = order_rev.merge(cust_ltv[['customer_id', 'signup_date']], on='customer_id')
order_rev['days_since_signup'] = (order_rev['order_date'] - order_rev['signup_date']).dt.days

ltv_3m = order_rev[order_rev['days_since_signup'] <= 90].groupby('customer_id')['line_revenue'].sum().reset_index(name='ltv_3m')
ltv_12m = order_rev[order_rev['days_since_signup'] <= 365].groupby('customer_id')['line_revenue'].sum().reset_index(name='ltv_12m')
ltv_total = order_rev.groupby('customer_id')['line_revenue'].sum().reset_index(name='ltv_total')

cust_ltv = cust_ltv.merge(ltv_3m, on='customer_id', how='left')
cust_ltv = cust_ltv.merge(ltv_12m, on='customer_id', how='left')
cust_ltv = cust_ltv.merge(ltv_total, on='customer_id', how='left').fillna(0)

channel_ltv = cust_ltv.groupby(['cohort_yq', 'acquisition_channel']).agg(
    avg_ltv_3m=('ltv_3m', 'mean'),
    avg_ltv_12m=('ltv_12m', 'mean'),
    avg_ltv_total=('ltv_total', 'mean'),
    customer_count=('customer_id', 'nunique')
).reset_index()

save_eda_csv(channel_ltv, 'agg_cohort_channel_ltv.csv')

plt.figure(figsize=(14, 6))
sns.lineplot(data=channel_ltv, x='cohort_yq', y='avg_ltv_12m', hue='acquisition_channel', marker='s')
plt.title('G3: Average 12-Month LTV by Acquisition Channel and Cohort Quarter')
plt.xticks(rotation=45)
plt.ylabel('12-Month LTV')
plt.tight_layout()
plt.show()


# ## STEP 24: G4 - Margin Erosion from Discounting

# In[27]:


print("STEP 24: G4 - Margin Erosion from Discounting")
fact_margin = fact.copy()
fact_margin['gross_revenue'] = fact_margin['quantity'] * fact_margin['unit_price']
fact_margin['quarter'] = fact_margin['order_date'].dt.to_period('Q').astype(str)

margin_erosion = fact_margin.groupby(['category', 'quarter']).agg(
    net_revenue=('line_revenue', 'sum'),
    gross_revenue=('gross_revenue', 'sum'),
    total_cogs=('line_cost', 'sum')
).reset_index()

margin_erosion['effective_margin_pct'] = ((margin_erosion['net_revenue'] - margin_erosion['total_cogs']) / margin_erosion['gross_revenue'] * 100).round(2)
margin_erosion['discount_rate_overall'] = ((margin_erosion['gross_revenue'] - margin_erosion['net_revenue']) / margin_erosion['gross_revenue'] * 100).round(2)

save_eda_csv(margin_erosion, 'agg_margin_erosion.csv')

fig, axes = plt.subplots(1, 2, figsize=(16, 6))
sns.lineplot(data=margin_erosion, x='quarter', y='effective_margin_pct', hue='category', ax=axes[0])
axes[0].set_title('Effective Margin % Over Time')
axes[0].tick_params(axis='x', rotation=45)

sns.lineplot(data=margin_erosion, x='quarter', y='discount_rate_overall', hue='category', ax=axes[1], legend=False)
axes[1].set_title('Effective Discount Depth % Over Time')
axes[1].tick_params(axis='x', rotation=45)

plt.suptitle('G4: Margin Erosion from Discounting')
plt.tight_layout()
plt.show()


# ## STEP 25: G5 & G6 - Payment Concentration & Mobile Conversion Gap

# In[28]:


print("STEP 25: G5 & G6 - Payment & Device Risks")

device_payment = fact.groupby(['order_year', 'device_type', 'payment_method']).agg(
    revenue=('line_revenue', 'sum'),
    orders=('order_id', 'nunique')
).reset_index()
device_payment['aov'] = device_payment['revenue'] / device_payment['orders']

save_eda_csv(device_payment, 'agg_payment_device_risk.csv')

plt.figure(figsize=(10, 5))
sns.barplot(data=device_payment, x='order_year', y='aov', hue='device_type')
plt.title('G6: Average Order Value by Device Type (Mobile Gap)')
plt.ylabel('AOV')
plt.tight_layout()
plt.show()


# ## STEP 26: G7 - Seasonal Inventory Misalignment

# In[29]:


print("STEP 26: G7 - Seasonal Inventory Misalignment")
inv_monthly = inventory.copy()
inv_monthly['year_month'] = inv_monthly['snapshot_date'].dt.to_period('M').astype(str)

stockout_trend = inv_monthly.groupby('year_month')['stockout_flag'].mean().reset_index(name='stockout_rate')
monthly_rev = fact_sales.groupby('year_month')['revenue'].sum().reset_index()

misalignment = stockout_trend.merge(monthly_rev, on='year_month')
save_eda_csv(misalignment, 'agg_inventory_misalignment.csv')

fig, ax1 = plt.subplots(figsize=(14, 6))
ax2 = ax1.twinx()
ax1.bar(misalignment['year_month'], misalignment['stockout_rate'], color='lightcoral', alpha=0.6, label='Stockout Rate')
ax2.plot(misalignment['year_month'], misalignment['revenue'], color='navy', marker='o', label='Revenue')

ax1.set_xlabel('Month')
ax1.set_ylabel('Stockout Rate', color='red')
ax2.set_ylabel('Revenue', color='navy')

# Fix tick spacing
n_ticks = 12
ticks = misalignment['year_month'][::len(misalignment)//n_ticks]
ax1.set_xticks(ticks.index)
ax1.set_xticklabels(ticks.values, rotation=45)

plt.title('G7: Inventory Misalignment (Revenue vs Stockouts)')
plt.tight_layout()
plt.show()


# ## FINAL STEP: Create Power BI Master Dataset

# In[30]:


# =============================================================================
# FINAL STEP: Build powerbi_master_dataset.csv
# =============================================================================
print("FINAL STEP: Building powerbi_master_dataset.csv")

OUTPUT_CSV = os.path.join(OUT_DIR, 'powerbi_master_dataset.csv')

print("Loading enriched tables...")
fact_orders   = pd.read_csv(os.path.join(OUT_DIR, 'fact.csv'), low_memory=False)
dim_cust      = pd.read_csv(os.path.join(OUT_DIR, 'dim_cust.csv'), low_memory=False)
fact_ship     = pd.read_csv(os.path.join(OUT_DIR, 'fact_ship.csv'), low_memory=False)
fact_ret      = pd.read_csv(os.path.join(OUT_DIR, 'fact_ret.csv'), low_memory=False)

print("Joining customer RFM data...")
cust_cols = ['customer_id', 'gender', 'age_group', 'acquisition_channel', 'tenure_days', 'R_score', 'F_score', 'M_score', 'rfm_segment']
master = fact_orders.merge(dim_cust[cust_cols], on='customer_id', how='left')

print("Joining shipment data...")
ship_cols = ['order_id', 'delivery_days', 'processing_days', 'shipping_fee', 'total_lead_time', 'delivery_bucket']
fact_ship_dedup = fact_ship[ship_cols].drop_duplicates(subset=['order_id'])
master = master.merge(fact_ship_dedup, on='order_id', how='left')

print("Joining returns data...")
ret_agg = (fact_ret[['order_id', 'product_id', 'return_reason', 'return_quantity', 'refund_amount']]
    .groupby(['order_id', 'product_id'])
    .agg({'return_quantity': 'sum', 'refund_amount': 'sum', 'return_reason': 'first'})
    .reset_index())
master = master.merge(ret_agg, on=['order_id', 'product_id'], how='left')

master['is_returned'] = master['return_quantity'].notna().astype(int)
master['return_quantity'] = master['return_quantity'].fillna(0)
master['refund_amount'] = master['refund_amount'].fillna(0)
master['net_revenue_after_returns'] = master['line_revenue'] - master['refund_amount']

print(f"\nMaster Dataset Shape: {master.shape[0]:,} rows × {master.shape[1]} columns")

master.to_csv(OUTPUT_CSV, index=False)
size_mb = os.path.getsize(OUTPUT_CSV) / 1e6
print(f"\n Saved: {OUTPUT_CSV} ({size_mb:.1f} MB)")

