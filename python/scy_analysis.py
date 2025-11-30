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
# Helper: decide log scale
# =====================================================================
def should_use_log(values):
  vmin = max(min(values), 1)
  vmax = max(values)
  return vmax / vmin > 100

# =====================================================================
# Plot save helper
# =====================================================================
def save_plot(filename):
  path = f"{OUTPUT_FOLDER}/{filename}"
  plt.savefig(path, dpi=180)
  print(f"Graph saved in: {path}")
  plt.close()

# =====================================================================
# LOAD MERGED CSV
# =====================================================================
print("Loading merged CSV...")

df = pd.read_csv(DATA_FILE)

print("Data loaded!\n")

# =====================================================================
# UNIVERSAL COMPARATIVE PLOT
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
# === STATISTICS FUNCTIONS ============================================
# =====================================================================

def speedup(a, b):
  """How many times b is faster than a."""
  return a / b

def percent_gain(a, b):
  """Percentage improvement from a to b."""
  return (a - b) / a * 100

def diff(a, b):
  """Absolute difference."""
  return a - b

def asymptotic_ratio(n1, t1, n2, t2):
  """
  Experimental ratio using t(n2)/t(n1).
  If ~n2/n1 → O(n)
  If ~(n2/n1)^2 → O(n²)
  """
  return (t2 / t1) / (n2 / n1)

def loglog_slope(n_values, t_values):
  """
  Computes the slope of log(t) vs log(n).
  slope ≈ 1 → linear
  slope ≈ 2 → quadratic
  """
  logn = np.log(n_values)
  logt = np.log(t_values)
  slope, _ = np.polyfit(logn, logt, 1)
  return slope

# =====================================================================
# === SCIENTIFIC SUMMARY =============================================
# =====================================================================

def scientific_summary(df):
  print("\n========================= RESUMO CIENTÍFICO =========================\n")

  langs = ["cpp", "go"]
  algos = ["naive", "sliding"]

  for lang in langs:
    for algo in algos:
      subset = df[(df["lang"] == lang) & (df["algorithm"].str.contains(algo))]

      n_vals = np.array(subset["n"])
      t_vals = np.array(subset["time_ns"])

      slope = loglog_slope(n_vals, t_vals)

      print(f"📌 {lang.upper()} — {algo.upper()}")
      print(f"   ➜ log-log slope ≈ {slope:.3f}")
      if slope > 1.4:
        print("   ⟶ Confirmado empiricamente: O(n²)\n")
      else:
        print("   ⟶ Confirmado empiricamente: O(n)\n")

  print("====================================================================\n")

scientific_summary(df)
