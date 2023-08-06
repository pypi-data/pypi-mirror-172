import os
import json
import pandas as pd


# root_dir = "/Users/john/Datasets/breast&thyroid/json/rectangle/"
root_dir = "/Users/john/Datasets/breast&thyroid/json/polygon/"
label_path = os.path.join(root_dir, "labels.csv")
df = pd.read_csv(label_path)

for mask_path, label in zip(df["mask_path"], df["label"]):
    mask_path = os.path.join(root_dir, mask_path)
    with open(mask_path) as f:
        json_data = json.load(f)

    json_data["shapes"][0]["label"] = label
    json_data["imageData"] = None

    with open(mask_path, "w") as f:
        json.dump(json_data, f, indent=2)
