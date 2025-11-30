import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# =====================================================================
# General plot settings
# =====================================================================
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['figure.figsize'] = (11, 6)
plt.rcParams['font.size'] = 12

# =====================================================================
# Paths
# =====================================================================
DATA_FILE = "../data/merged_results.csv"
OUTPUT_FOLDER = "../docs/charts"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# =====================================================================
# Helpers
# =====================================================================
def should_use_log(values):
  vmin = max(min(values), 1)
  vmax = max(values)
  return vmax / vmin > 100


def save_plot(filename):
  path = f"{OUTPUT_FOLDER}/{filename}"
  plt.savefig(path, dpi=180)
  print(f"Graph saved in: {path}")
  plt.close()


def speedup(a, b):
  """How many times b is faster than a (a/b)."""
  return a / b


def percent_gain(a, b):
  """Percentage improvement from a to b."""
  return (a - b) / a * 100.0


def loglog_slope(n_values, t_values):
  """Slope of log(t) vs log(n).  ~1 => O(n), ~2 => O(n²)."""
  logn = np.log(n_values)
  logt = np.log(t_values)
  slope, _ = np.polyfit(logn, logt, 1)
  return slope


# =====================================================================
# Load merged CSV
# =====================================================================
print("Loading merged CSV...")
df = pd.read_csv(DATA_FILE)
print("Data loaded!\n")


# =====================================================================
# General all-algorithms plot
# =====================================================================
def plot_all_algorithms(df):
  plt.title("Comparação Geral — C++ e Go (Naive vs Sliding)")
  plt.xlabel("Tamanho do input (n)")
  plt.ylabel("Tempo (ns)")

  groups = df.groupby(["lang", "algorithm"])
  for (lang, algo), subset in groups:
    label = f"{lang.upper()} {algo}"
    plt.plot(subset["n"], subset["time_ns"], marker="o", label=label)

  if should_use_log(df["time_ns"]):
    plt.yscale("log")

  plt.legend()
  save_plot("all_algorithms.png")


plot_all_algorithms(df)


# =====================================================================
# LOG-LOG plot (x e y em log) — asymptotic behavior
# =====================================================================
def plot_loglog(df):
  plt.title("Log-Log — C++ e Go (Naive vs Sliding)")
  plt.xlabel("log(n)")
  plt.ylabel("log(tempo ns)")

  groups = df.groupby(["lang", "algorithm"])
  for (lang, algo), subset in groups:
    n = subset["n"].values
    t = subset["time_ns"].values
    label = f"{lang.upper()} {algo}"
    plt.plot(n, t, marker="o", label=label)

  plt.xscale("log")
  plt.yscale("log")
  plt.legend()
  save_plot("all_algorithms_loglog.png")


plot_loglog(df)


# =====================================================================
# SPEEDUP: naive / sliding for linguage
# =====================================================================
def plot_speedup(df):
  for lang in ["cpp", "go"]:
    naive = df[(df["lang"] == lang) & (df["algorithm"].str.contains("naive"))]
    sliding = df[(df["lang"] == lang) & (df["algorithm"].str.contains("sliding"))]

    if naive.empty or sliding.empty:
      print(f"Sem dados suficientes para speedup de {lang.upper()} (pulando)")
      continue

    naive = naive.sort_values("n")
    sliding = sliding.sort_values("n")

    # make sure both have the same 'n' values
    merged = pd.merge(
      naive[["n", "time_ns"]],
      sliding[["n", "time_ns"]],
      on="n",
      suffixes=("_naive", "_sliding"),
    )

    merged["speedup"] = speedup(
      merged["time_ns_naive"], merged["time_ns_sliding"]
    )

    plt.plot(merged["n"], merged["speedup"], marker="o")
    plt.title(f"Speedup Naive/Sliding — {lang.upper()}")
    plt.xlabel("Tamanho do input (n)")
    plt.ylabel("Speedup (naive_time / sliding_time)")
    plt.yscale("log")  # speedup usually varies widely
    save_plot(f"speedup_{lang}.png")


plot_speedup(df)


# =====================================================================
# Gain percentual: what percent faster is sliding vs naive
# =====================================================================
def plot_percent_gain(df):
  for lang in ["cpp", "go"]:
    naive = df[(df["lang"] == lang) & (df["algorithm"].str.contains("naive"))]
    sliding = df[(df["lang"] == lang) & (df["algorithm"].str.contains("sliding"))]

    if naive.empty or sliding.empty:
      print(f"Sem dados suficientes para percent gain de {lang.upper()} (pulando)")
      continue

    naive = naive.sort_values("n")
    sliding = sliding.sort_values("n")

    merged = pd.merge(
      naive[["n", "time_ns"]],
      sliding[["n", "time_ns"]],
      on="n",
      suffixes=("_naive", "_sliding"),
    )

    merged["percent_gain"] = percent_gain(
      merged["time_ns_naive"], merged["time_ns_sliding"]
    )

    plt.plot(merged["n"], merged["percent_gain"], marker="o")
    plt.title(f"Ganho Percentual — {lang.upper()} (Sliding vs Naive)")
    plt.xlabel("Tamanho do input (n)")
    plt.ylabel("Ganho (%)")
    save_plot(f"percent_gain_{lang}.png")


plot_percent_gain(df)


# =====================================================================
# Scientific summary: empirical complexity analysis
# =====================================================================
def scientific_summary(df):
  print("\n========================= RESUMO CIENTÍFICO =========================\n")

  langs = ["cpp", "go"]
  algos = ["naive", "sliding"]

  for lang in langs:
    for algo in algos:
      subset = df[(df["lang"] == lang) & (df["algorithm"].str.contains(algo))]

      if len(subset) < 2:
        print(f"Sem dados suficientes para {lang.upper()} - {algo.upper()} (skip)\n")
        continue

      n_vals = subset["n"].values
      t_vals = subset["time_ns"].values

      if any(t_vals <= 0):
        print(f"Valores inválidos (<=0) para {lang. upper()} - {algo.upper()} (skip)\n")
        continue

      slope = loglog_slope(n_vals, t_vals)

      print(f"{lang.upper()} — {algo.upper()}")
      print(f"   ➜ slope log-log ≈ {slope:.3f}")
      if slope > 1.4:
        print("   ⟶ Confirmado empiricamente: O(n²)\n")
      else:
        print("   ⟶ Confirmado empiricamente: O(n)\n")

  print("====================================================================\n")


scientific_summary(df)

print("Analysis finished.")
