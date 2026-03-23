"""
snowflake_export.py — Read existing CSVs and push to Snowflake
run pip3 install confluent-kafka snowflake-connector-python pandas
Terminal 1: python3 run_pipeline.py           # runs producer + consumers
Terminal 2: python3 bi_integration/export.py        # writes CSVs
Terminal 3: python3 snowflake_export/snowflake_export.py      # reads CSVs, writes to Snowflake
Terminal 4: streamlit run streamlit_dashboard.py  # dashboard reads CSVs
"""

import os, time, pandas as pd
import snowflake.connector
from datetime import datetime

# CSV paths (same as export.py)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "bi_integration", "data")

ANALYTICS_CSV = os.path.join(DATA_DIR, "analytics_summary.csv")
FRAUD_CSV     = os.path.join(DATA_DIR, "fraud_alerts.csv")
INVENTORY_CSV = os.path.join(DATA_DIR, "inventory_summary.csv")

EXPORT_INTERVAL_SECONDS = 60  # how often to check CSVs

# Snowflake connection
def get_snowflake_connection():
    return snowflake.connector.connect(
        user="FLUXCART_USER",
        password="StrongPassword123!",
        account="YYWQTSL-DN79138",
        warehouse="FLUXCART_WH",
        database="FLUXCART_DB",
        schema="FLUXCART_ANALYTICS",
        role="FLUXCART_ROLE"
    )

# Function to upsert data from DataFrame to Snowflake
def write_snowflake(table, df: pd.DataFrame):
    if df.empty:
        return
    conn = get_snowflake_connection()
    cur = conn.cursor()
    cols = list(df.columns)
    placeholders = ",".join(["%s"]*len(cols))
    query = f"INSERT INTO {table} ({','.join(cols)}) VALUES ({placeholders})"
    data = [tuple(row) for row in df.to_numpy()]
    cur.executemany(query, data)
    conn.commit()
    cur.close()
    conn.close()
    print(f"[Snowflake] Wrote {len(df)} rows to {table}")

# Track last processed rows to avoid duplicates
last_rows = {"analytics":0, "fraud":0, "inventory":0}

def main():
    print("[Snowflake Export] Started...")
    global last_rows
    while True:
        try:
            # ----------------- Analytics -----------------
            if os.path.exists(ANALYTICS_CSV):
                df = pd.read_csv(ANALYTICS_CSV)
                new_rows = df.iloc[last_rows["analytics"]:]
                write_snowflake("ANALYTICS_SUMMARY", new_rows)
                last_rows["analytics"] = len(df)

            # ----------------- Fraud -----------------
            if os.path.exists(FRAUD_CSV):
                df = pd.read_csv(FRAUD_CSV)
                new_rows = df.iloc[last_rows["fraud"]:]
                write_snowflake("FRAUD_ALERTS", new_rows)
                last_rows["fraud"] = len(df)

            # ----------------- Inventory -----------------
            if os.path.exists(INVENTORY_CSV):
                df = pd.read_csv(INVENTORY_CSV)
                new_rows = df.iloc[last_rows["inventory"]:]
                write_snowflake("INVENTORY_SUMMARY", new_rows)
                last_rows["inventory"] = len(df)

        except Exception as e:
            print(f"[Snowflake Export] Error: {e}")

        time.sleep(EXPORT_INTERVAL_SECONDS)

if __name__ == "__main__":
    main()