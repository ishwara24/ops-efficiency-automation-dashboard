# ops-efficiency-automation-dashboard
Operations Efficiency &amp; Automation — Python ETL + Power BI dashboard

# Operations Efficiency & Automation Dashboard

**TL;DR — What this is (15 seconds)**  
A compact, end-to-end operations analytics project that automates ingestion of daily branch order files (Python ETL), produces a cleaned master dataset, and exposes business-ready KPIs and drilldowns in a Power BI dashboard. Built to demonstrate automation + analytics + business impact for operations-focused analyst roles.

![dashboard screenshot](dashboard.png)

---

## Why this project matters 
Operations teams lose time and margin due to manual data merging, inconsistent file formats, late deliveries and returns. This project shows how to turn multiple daily CSVs from branches into a single, repeatable pipeline and a visual product that answers: *Which branches/regions are causing delays? How much are late deliveries costing? Are operational changes improving fulfillment times?* all with a fast, reproducible workflow.

---

## Highlights
- **Automated ETL**: Python script merges multiple branch CSVs, normalizes schema, parses dates and engineers metrics (processing time, fulfillment days, on-time flag, cost impact).
- **Power BI Dashboard**: Clean executive KPIs + region/branch visualizations + order-level drilldown for root-cause analysis.
- **Business impact**: Identified top-delay branches and estimated an **₹112.6K** cost impact from late deliveries/returns in sample data.
- **Quick reproducibility**: Full pipeline runs locally and produces `output/final_cleaned.csv` ready for BI consumption.

---


---

## Quick-start (run locally in 5 minutes)

### Clone the repo:

git clone https://github.com/ishwara24/ops-efficiency-automation-dashboard
cd ops-dashboard-project
(Optional) Create and activate a Python virtual environment:

python -m venv venv
# Windows (cmd)
venv\Scripts\activate.bat
# macOS/Linux
# source venv/bin/activate
Install dependencies:

pip install -r requirements.txt
Generate sample files (optional, already included):

python code\generate_sample_branch_files.py
Run the ETL pipeline:

python code\etl_pipeline.py
Outputs will be generated in output/final_cleaned.csv and summary files.

Open PowerBI/Operations_Dashboard.pbix (or Operations_Dashboard.pdf) in Power BI Desktop.

Key Files Explained
code/generate_sample_branch_files.py
Creates reproducible synthetic branch CSVs for testing.

code/etl_pipeline.py
Reads all CSVs, cleans them, engineers operational metrics (total_fulfillment_days, on_time, cost_impact), and exports cleaned + aggregated CSVs.

output/final_cleaned.csv
Final master table used for Power BI analysis.

PowerBI/Operations_Dashboard.pbix
Power BI report containing KPIs, regional performance, branch analysis, and drilldown pages.

Author
Ishwara Sinha
📧 Email: ishwarasinha24@gmail.com
🔗 LinkedIn: https://linkedin.com/in/ishwara-sinha
💻 GitHub: https://github.com/ishwara24
✍️ Hashnode Blog: https://hashnode.com/691ddb2ebab204c3911d84cd/dashboard

