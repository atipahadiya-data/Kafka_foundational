                ┌─────────────┐
                │Kafka Topics │
                └──────┬──────┘
                       │
                run_pipeline.py
                       │
                   export.py
       ┌───────────────┼───────────────┐
       │               │               │
 Analytics Consumer  Fraud Consumer  Inventory Consumer
       │               │               │
       └───────────────┼───────────────┘
                       │
                       │
            ┌──────────┴──────────┐
            │                     │
        Streamlit             snowflake_export.py



        #### folder structure

        fluxcart-pipeline/
├─ bi_integration/
│  ├─ export.py             # original CSV exporter
│  ├─ data/                 # CSVs written here
│  │  ├─ analytics_summary.csv
│  │  ├─ fraud_alerts.csv
│  │  └─ inventory_summary.csv
├─ snowflake_export/        # new folder for Snowflake integration
│  └─ snowflake_export.py   # reads CSVs and write to snowflake tables


snowflake fluxcart_db architecture :
FLUXCART_DB
│
├── FLUXCART_SCHEMA        (RAW / operational)
│     USER_BEHAVIOR
│     ORDERS
│     PAYMENTS
│
└── FLUXCART_ANALYTICS     (aggregated / BI)
      ANALYTICS_SUMMARY
      INVENTORY_SUMMARY
      FRAUD_ALERTS


Hi Chirantan,

I’m sharing the updated architecture diagram following the Snowflake integration.

The existing flow has been kept unchanged. Snowflake has been integrated specifically for analytics, where data is read from CSV files and inserted into Snowflake for record-keeping and analysis.

Please note that Kafka topics are still not part of the Snowflake integration. 
Implementing this independently was a valuable learning experience :) 

thanks and regards,
Ati



