import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta

out_dir = Path("../branch_files")  
out_dir.mkdir(parents=True, exist_ok=True)

np.random.seed(42)
branches = ["North_A", "North_B", "South_A", "West_A", "East_A"]
regions = {"North_A":"North","North_B":"North","South_A":"South","West_A":"West","East_A":"East"}

n_orders_per_file = 250
start_date = datetime(2025, 10, 1)

for b in branches:
    rows = []
    for i in range(n_orders_per_file):
        order_id = f"{b[:3].upper()}-{1000+i}"
        order_date = start_date + timedelta(days=int(np.random.exponential(5)))
        processing_delay_days = max(0, int(np.random.normal(2, 2)))
        delivery_delay_days = processing_delay_days + max(0, int(np.random.normal(2,2)))
        dispatch_date = order_date + timedelta(days=processing_delay_days)
        delivery_date = dispatch_date + timedelta(days=delivery_delay_days)
        delivery_status = np.random.choice(["Delivered","Returned","In Transit"], p=[0.9,0.05,0.05])
        order_value = round(np.random.uniform(100, 5000),2)
        shipping_cost = round(order_value * np.random.uniform(0.02, 0.08),2)
        rows.append({
            "order_id": order_id,
            "branch": b,
            "region": regions[b],
            "order_date": order_date.strftime("%Y-%m-%d"),
            "dispatch_date": dispatch_date.strftime("%Y-%m-%d"),
            "delivery_date": delivery_date.strftime("%Y-%m-%d"),
            "delivery_status": delivery_status,
            "order_value": order_value,
            "shipping_cost": shipping_cost,
            "items_count": np.random.randint(1,6)
        })
    df = pd.DataFrame(rows)
    df.to_csv(out_dir / f"{b}_orders.csv", index=False)

print("Sample branch files created in ./branch_files/ (relative to project root)")
