# ============================================================
# PROJECT: E-COMMERCE CUSTOMER VALUE PREDICTION
# COMPONENTS: CLTV + RFM ANALYSIS + SEGMENTATION + VISUALIZATION
# AUTHOR: UDITA GAYEN
# ============================================================

# ---------------------- IMPORT LIBRARIES ----------------------
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------- STEP 1: LOAD DATASET ----------------------
file_path = r"C:\Users\UDITA GAYEN\Downloads\ecommerce_data (1).csv"  
df = pd.read_csv(file_path)

# ---------------------- STEP 2: DATA CLEANING ----------------------
df = df.dropna(subset=['customer_id', 'purchase_amount'])  
df['purchase_amount'] = pd.to_numeric(df['purchase_amount'], errors='coerce')  
df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')  

# ---------------------- STEP 3: CLTV METRICS ----------------------
customer_metrics = df.groupby('customer_id').agg(
    total_revenue=('purchase_amount', 'sum'),
    total_transactions=('purchase_amount', 'count'),
    avg_order_value=('purchase_amount', 'mean')
).reset_index()

total_customers = df['customer_id'].nunique()
purchase_frequency = customer_metrics['total_transactions'].mean() / total_customers
assumed_lifespan_years = 3  # business assumption

# CLTV calculation
customer_metrics['cltv'] = (
    customer_metrics['avg_order_value'] *
    purchase_frequency *
    assumed_lifespan_years
)

# ---------------------- STEP 4: MERGE DEMOGRAPHICS ----------------------
demo_cols = ['customer_id', 'customer_age', 'customer_gender', 'shipping_region', 'loyalty_status']
demographics = df[demo_cols].drop_duplicates(subset='customer_id')
cltv_df = pd.merge(customer_metrics, demographics, on='customer_id', how='left')
cltv_df = cltv_df.sort_values(by='cltv', ascending=False).reset_index(drop=True)

# ---------------------- STEP 5: RFM ANALYSIS ----------------------
recent_date = df['order_date'].max()

rfm = df.groupby('customer_id').agg({
    'order_date': lambda x: (recent_date - x.max()).days,
    'purchase_amount': ['count', 'sum']
})
rfm.columns = ['Recency', 'Frequency', 'Monetary']
rfm = rfm.reset_index()

# Assign scores (1–5)
rfm['R_Score'] = pd.qcut(rfm['Recency'], 5, labels=[5, 4, 3, 2, 1]).astype(int)
rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5]).astype(int)
rfm['M_Score'] = pd.qcut(rfm['Monetary'], 5, labels=[1, 2, 3, 4, 5]).astype(int)
rfm['RFM_Score'] = rfm['R_Score'] + rfm['F_Score'] + rfm['M_Score']

# Merge RFM + CLTV
final_df = pd.merge(cltv_df, rfm, on='customer_id', how='left')

# ---------------------- STEP 6: CUSTOMER SEGMENTATION ----------------------
def segment_customer(row):
    if row['cltv'] > final_df['cltv'].quantile(0.75) and row['RFM_Score'] >= 12:
        return 'High-Value'
    elif row['cltv'] > final_df['cltv'].quantile(0.50) and row['RFM_Score'] >= 9:
        return 'Medium-Value'
    else:
        return 'Low-Value'

final_df['Customer_Segment'] = final_df.apply(segment_customer, axis=1)

# ---------------------- STEP 7: DISPLAY RESULTS ----------------------
print("\n🔝 Top 10 Customers by CLTV:")
print(cltv_df.head(10))

print("\n🏆 Top 10 Customers by RFM Score:")
print(final_df.sort_values(by='RFM_Score', ascending=False).head(10))

print("\n📊 Customer Segmentation Summary:")
print(final_df['Customer_Segment'].value_counts())

# ---------------------- STEP 8: VISUALIZATIONS ----------------------

# 1️⃣ CLTV Distribution
plt.figure(figsize=(10, 5))
plt.hist(cltv_df['cltv'], bins=30, color='teal', edgecolor='black')
plt.title('Customer Lifetime Value (CLTV) Distribution', fontsize=14)
plt.xlabel('CLTV', fontsize=12)
plt.ylabel('Number of Customers', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()

# 2️⃣ Top 10 Customers by CLTV
top_10 = cltv_df.head(10)
plt.figure(figsize=(10, 6))
plt.bar(top_10['customer_id'].astype(str), top_10['cltv'], color='darkorange')
plt.title('Top 10 Customers by CLTV', fontsize=14)
plt.xlabel('Customer ID', fontsize=12)
plt.ylabel('CLTV', fontsize=12)
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()

# 3️⃣ RFM Score Distribution
plt.figure(figsize=(8, 5))
plt.hist(final_df['RFM_Score'], bins=range(3, 16), color='skyblue', edgecolor='black', align='left')
plt.title('RFM Score Distribution', fontsize=14)
plt.xlabel('RFM Score', fontsize=12)
plt.ylabel('Number of Customers', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()

# 4️⃣ Customer Segmentation Pie Chart
plt.figure(figsize=(7, 7))
final_df['Customer_Segment'].value_counts().plot.pie(
    autopct='%1.1f%%', startangle=90, colors=['gold', 'lightgreen', 'lightcoral']
)
plt.title('Customer Segmentation Based on CLTV + RFM', fontsize=14)
plt.ylabel('')
plt.tight_layout()
plt.show()

print("\n✅ Final Analysis Completed Successfully — CLTV, RFM & Segmentation Done!")
