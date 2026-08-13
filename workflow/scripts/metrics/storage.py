import os
import sys
import pandas as pd

sizes_path = sys.argv[1]

step_sizes = {"gen": [], "sim": [], "digi2raw": [], "hlt": [], "pat": [], "reco": [], "nano": []}

for filename in os.listdir(sizes_path):
    if filename.endswith(".size"):
        step = filename.split("_")[0]
        filepath = os.path.join(sizes_path, filename)

        with open(filepath, "r") as f:
            size = f.readline()
            step_sizes[step].append(int(size[:-2]))

summary_df = {"gen": {}, "sim": {}, "digi2raw": {}, "hlt": {}, "pat": {}, "reco": {}, "nano": {}}
prev = {"sim": "gen", "digi2raw": "sim", "hlt": "digi2raw", "pat": "hlt", "reco": "pat", "nano": "reco"}

for k,v in step_sizes.items():
    summary_df[k]["Total Size"] = sum(v)
    summary_df[k]["Total Size (GBs)"] = sum(v) / (1024**3)
    summary_df[k]["File Count"] = len(v)
    summary_df[k]["Avg File Size"] = summary_df[k]["Total Size"] / summary_df[k]["File Count"]

    if k == "gen":
        summary_df[k]["Peak Storage (GBs)"] = summary_df[k]["Total Size (GBs)"]
    else:
        summary_df[k]["Peak Storage (GBs)"] = (summary_df[k]["Total Size"] + summary_df[prev[k]]["Total Size"]) / (1024**3)


summary = pd.DataFrame.from_dict(summary_df, orient="index")

summary.to_csv("results/reports/sizes.csv")
markdown_summary = summary.to_markdown()

with open("results/reports/sizes.md", "w") as f:
    f.write(markdown_summary)