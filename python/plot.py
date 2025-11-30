import pandas as pd
import matplotlib.pyplot as plt
import os

# =====================================================================
# General plot settings
# =====================================================================
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 12

# =====================================================================
# Paths
# =====================================================================
DATA_FOLDER = "../data"
OUTPUT_FOLDER = "../docs/charts"

cpp_csv = f"{DATA_FOLDER}/cpp_results.csv"
go_csv = f"{DATA_FOLDER}/go_results.csv"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# =====================================================================
# Helper: checks if values span multiple orders of magnitude
# =====================================================================
def should_use_log(values):
  """
  Decide automaticamente se o eixo Y deve usar escala logarítmica.
  Se o maior valor for 100x maior que o menor → usa log.
  """
  vmin = max(min(values), 1)   # evita log(0)
  vmax = max(values)

  return vmax / vmin > 100


# =====================================================================
# Save plot function
# =====================================================================
def save_plot(filename):
    path = f"{OUTPUT_FOLDER}/{filename}"
    plt.savefig(path, dpi=180)
    print(f"Graph saved in: {path}")
    plt.close()


# =====================================================================
# Load Data
# =====================================================================
print("Loading CSVs...")

df_cpp = pd.read_csv(cpp_csv)
df_go = pd.read_csv(go_csv)

# Normalize headers
df_cpp.columns = ["n", "algorithm", "time_ns"]
df_go.columns = ["n", "algorithm", "time_ns"]

df_cpp["lang"] = "cpp"
df_go["lang"] = "go"

df_all = pd.concat([df_cpp, df_go], ignore_index=True)

print("Data loaded successfully.")


# =====================================================================
# Individual plot per language
# =====================================================================
def plot_by_lang(df, lang):
  subset = df[df["lang"] == lang]

  naive = subset[subset["algorithm"].str.contains("naive")]
  sliding = subset[subset["algorithm"].str.contains("sliding")]

  plt.plot(naive["n"], naive["time_ns"], marker="o", label="Naive (O(n²))")
  plt.plot(sliding["n"], sliding["time_ns"], marker="o", label="Sliding (O(n))")

  plt.title(f"{lang.upper()} - Desempenho dos Algoritmos")
  plt.xlabel("Tamanho do input (n)")
  plt.ylabel("Tempo (ns)")
  plt.legend()

  # decide automatically if log scale is needed
  all_values = list(naive["time_ns"]) + list(sliding["time_ns"])
  if should_use_log(all_values):
      plt.yscale("log")

  save_plot(f"{lang}_naive_vs_sliding.png")


print("Generating individual language plots...")
plot_by_lang(df_all, "cpp")
plot_by_lang(df_all, "go")


# =====================================================================
# Comparative plot (Sliding)
# =====================================================================
def plot_comparison_sliding(df):
  sliding = df[df["algorithm"].str.contains("sliding")]

  cpp = sliding[sliding["lang"] == "cpp"]
  go = sliding[sliding["lang"] == "go"]

  plt.plot(cpp["n"], cpp["time_ns"], marker="o", label="C++ Sliding")
  plt.plot(go["n"], go["time_ns"], marker="o", label="Go Sliding")

  plt.title("C++ vs Go (Sliding Window)")
  plt.xlabel("Tamanho do input (n)")
  plt.ylabel("Tempo (ns)")
  plt.legend()

  all_values = list(cpp["time_ns"]) + list(go["time_ns"])
  if should_use_log(all_values):
      plt.yscale("log")

  save_plot("cpp_vs_go_sliding.png")


print("Generating comparative sliding window plot...")
plot_comparison_sliding(df_all)


# =====================================================================
# Comparative plot (Naive)
# =====================================================================
def plot_comparison_naive(df):
  naive = df[df["algorithm"].str.contains("naive")]

  cpp = naive[naive["lang"] == "cpp"]
  go = naive[naive["lang"] == "go"]

  plt.plot(cpp["n"], cpp["time_ns"], marker="o", label="C++ Naive")
  plt.plot(go["n"], go["time_ns"], marker="o", label="Go Naive")

  plt.title("C++ vs Go (Naive)")
  plt.xlabel("Tamanho do input (n)")
  plt.ylabel("Tempo (ns)")
  plt.legend()

  all_values = list(cpp["time_ns"]) + list(go["time_ns"])
  if should_use_log(all_values):
      plt.yscale("log")

  save_plot("cpp_vs_go_naive.png")


print("Generating comparative naive plot...")
plot_comparison_naive(df_all)


print("\nAll plots generated successfully!")
