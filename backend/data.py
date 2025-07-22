import sqlite3
import pandas as pd
import os

# Absolute path to DB
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ecommerce.db'))

# File paths
ad_sales_csv = os.path.join(os.path.dirname(__file__), 'Product-Level Ad Sales and Metrics (mapped) - Product-Level Ad Sales and Metrics (mapped).csv')
total_sales_csv = os.path.join(os.path.dirname(__file__), 'Product-Level Total Sales and Metrics (mapped) - Product-Level Total Sales and Metrics (mapped).csv')
eligibility_csv = os.path.join(os.path.dirname(__file__), 'Product-Level Eligibility Table (mapped) - Product-Level Eligibility Table (mapped).csv')

def import_ad_sales():
    df = pd.read_csv(ad_sales_csv)
    df = df.rename(columns={'item_id': 'product_id'})

    # Compute CPC if not present
    if 'cpc' not in df.columns:
        df['cpc'] = df['ad_spend'] / df['clicks']
    
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        for _, row in df.iterrows():
            cursor.execute("""
                INSERT OR REPLACE INTO Product_Level_Ad_Sales_Metrics
                (date, product_id, ad_spend, clicks, impressions, cpc)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                row['date'],
                row['product_id'],
                row['ad_spend'],
                row['clicks'],
                row['impressions'],
                row['cpc']
            ))
        conn.commit()
    print(f'✅ Ad sales data imported: {len(df)} rows')


def import_total_sales():
    df = pd.read_csv(total_sales_csv)
    df = df.rename(columns={
        'item_id': 'product_id',
        'total_units_ordered': 'units_sold'
    })

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        for _, row in df.iterrows():
            cursor.execute("""
                INSERT OR REPLACE INTO Product_Level_Total_Sales_Metrics
                (date, product_id, total_sales, units_sold)
                VALUES (?, ?, ?, ?)
            """, (
                row['date'],
                row['product_id'],
                row['total_sales'],
                row['units_sold']
            ))
        conn.commit()
    print(f'✅ Total sales data imported: {len(df)} rows')

def import_eligibility():
    df = pd.read_csv(eligibility_csv)
    df = df.rename(columns={'item_id': 'product_id'})
    df['eligibility'] = df['eligibility'].map({'TRUE': 1, 'FALSE': 0})

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        for _, row in df.iterrows():
            cursor.execute("""
                INSERT OR REPLACE INTO Product_Eligibility
                (eligibility_datetime_utc, product_id, eligibility, message)
                VALUES (?, ?, ?, ?)
            """, (
                row['eligibility_datetime_utc'],
                row['product_id'],
                row['eligibility'],
                row['message']
            ))
        conn.commit()
    print(f'✅ Eligibility data imported: {len(df)} rows')

def main():
    import_ad_sales()
    import_total_sales()
    import_eligibility()
    print('🎉 All CSV data imported successfully.')

if __name__ == '__main__':
    main()
