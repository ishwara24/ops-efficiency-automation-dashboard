# etl_pipeline.py
import pandas as pd
from pathlib import Path
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "branch_files"
OUTPUT_DIR = PROJECT_ROOT / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# configuration
SLA_DELIVERY_DAYS = 5  # change if you want a different SLA

def load_all_csvs(data_dir: Path):
    files = list(data_dir.glob("*.csv"))
    if not files:
        raise FileNotFoundError(f"No CSVs found in {data_dir.resolve()}")
    df_list = []
    for f in files:
        df = pd.read_csv(f)
        df['source_file'] = f.name
        df_list.append(df)
    return pd.concat(df_list, ignore_index=True)

def clean_and_engineer(df: pd.DataFrame):
    # Normalize column names
    df.columns = [c.strip().lower() for c in df.columns]

    expected = ["order_id","branch","region","order_date","dispatch_date","delivery_date",
                "delivery_status","order_value","shipping_cost","items_count"]
    for col in expected:
        if col not in df.columns:
            df[col] = np.nan

    # Parse dates
    for dcol in ["order_date","dispatch_date","delivery_date"]:
        df[dcol] = pd.to_datetime(df[dcol], errors="coerce")

    # Derived metrics
    df["processing_time_days"] = (df["dispatch_date"] - df["order_date"]).dt.days
    df["delivery_time_days"] = (df["delivery_date"] - df["dispatch_date"]).dt.days
    df["total_fulfillment_days"] = (df["delivery_date"] - df["order_date"]).dt.days

    # on_time flag
    df["on_time"] = df["total_fulfillment_days"].le(SLA_DELIVERY_DAYS)
    df["on_time"] = df["on_time"].fillna(False)

    # cost impact proxy
    df["late_flag"] = df["total_fulfillment_days"] > SLA_DELIVERY_DAYS
    df["returned_flag"] = df["delivery_status"].str.lower().eq("returned")
    df["cost_impact"] = 0.0
    df.loc[df["late_flag"], "cost_impact"] += df.loc[df["late_flag"], "order_value"] * 0.02
    df.loc[df["returned_flag"], "cost_impact"] += df.loc[df["returned_flag"], "order_value"] * 0.6

    df = df.dropna(subset=["order_id","order_date"])
    return df

def aggregate_metrics(df: pd.DataFrame):
    branch_agg = df.groupby("branch").agg(
        orders=("order_id","nunique"),
        avg_order_value=("order_value","mean"),
        avg_processing_days=("processing_time_days","mean"),
        avg_delivery_days=("delivery_time_days","mean"),
        avg_fulfillment_days=("total_fulfillment_days","mean"),
        on_time_pct=("on_time", lambda x: 100 * x.sum() / len(x)),
        total_shipping_cost=("shipping_cost","sum"),
        total_cost_impact=("cost_impact","sum")
    ).reset_index()

    region_agg = df.groupby("region").agg(
        orders=("order_id","nunique"),
        avg_order_value=("order_value","mean"),
        on_time_pct=("on_time", lambda x: 100 * x.sum() / len(x)),
        avg_fulfillment_days=("total_fulfillment_days","mean"),
        total_cost_impact=("cost_impact","sum")
    ).reset_index()

    daily = df.groupby(df["order_date"].dt.date).agg(
        orders=("order_id","nunique"),
        avg_fulfillment_days=("total_fulfillment_days","mean"),
        on_time_pct=("on_time", lambda x: 100 * x.sum() / len(x))
    ).reset_index().rename(columns={"order_date":"date"})

    return branch_agg, region_agg, daily

def main():
    raw = load_all_csvs(DATA_DIR)
    cleaned = clean_and_engineer(raw)
    cleaned.to_csv(OUTPUT_DIR / "final_cleaned.csv", index=False)
    branch_agg, region_agg, daily = aggregate_metrics(cleaned)
    branch_agg.to_csv(OUTPUT_DIR / "branch_summary.csv", index=False)
    region_agg.to_csv(OUTPUT_DIR / "region_summary.csv", index=False)
    daily.to_csv(OUTPUT_DIR / "daily_summary.csv", index=False)
    print(f"ETL complete. Check {OUTPUT_DIR.resolve()} for outputs.")

if __name__ == "__main__":
    main()
