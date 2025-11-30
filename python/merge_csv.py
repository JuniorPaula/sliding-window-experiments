import pandas as pd
import os

DATA_FOLDER = "../data"
OUTPUT_FILE = f"{DATA_FOLDER}/merged_results.csv"

cpp_csv = f"{DATA_FOLDER}/cpp_results.csv"
go_csv = f"{DATA_FOLDER}/go_results.csv"

print("Loading CSV files...")

df_cpp = pd.read_csv(cpp_csv)
df_go = pd.read_csv(go_csv)

df_cpp.columns = ["n", "algorithm", "time_ns"]
df_go.columns = ["n", "algorithm", "time_ns"]

df_cpp["lang"] = "cpp"
df_go["lang"] = "go"

df_merged = pd.concat([df_cpp, df_go], ignore_index=True)

df_merged = df_merged.sort_values(by=["n", "lang"])

df_merged.to_csv(OUTPUT_FILE, index=False)

print(f"Merged CSV saved at: {OUTPUT_FILE}")
print(df_merged.head(10))
