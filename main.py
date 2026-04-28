import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# ensures plots display properly in VS Code
plt.switch_backend('TkAgg')

from config import DATASETS, DATABASE_NAME, OUTPUT_RESULTS
from database import load_csvs_to_database
from experiments import run_experiment


def main():
    os.makedirs("output", exist_ok=True)

    print("Step 1: Loading CSV files into SQLite database...")
    load_csvs_to_database()

    conn = sqlite3.connect(DATABASE_NAME)

    all_results = []

    for dataset_name, file_path in DATASETS.items():
        print(f"Step 2: Running experiments for {dataset_name}...")

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        df = pd.read_csv(file_path).dropna()
        dataset_results = run_experiment(df, dataset_name, conn)
        all_results.extend(dataset_results)

    results_df = pd.DataFrame(all_results)

    # -----------------------------
    # Speedup calculations
    # -----------------------------
    results_df["random_speedup"] = results_df["exact_time"] / results_df["random_time_mean"]
    results_df["strat_speedup"] = results_df["exact_time"] / results_df["strat_time_mean"]

    # -----------------------------
    # Relative error
    # -----------------------------
    results_df["random_relative_error"] = (
        results_df["random_error_mean"] / results_df["exact_result"]
    )

    results_df["strat_relative_error"] = (
        results_df["strat_error_mean"] / results_df["exact_result"]
    )

    # -----------------------------
    # FINAL RESULTS TABLE
    # -----------------------------
    print("\n================ FINAL RESULTS TABLE ================\n")

    final_table = results_df[[
        "dataset",
        "fraction",
        "exact_result",
        "random_result_mean",
        "strat_result_mean",
        "random_error_mean",
        "strat_error_mean",
        "random_relative_error",
        "strat_relative_error",
        "random_time_mean",
        "strat_time_mean",
        "random_speedup",
        "strat_speedup"
    ]].round(4)

    print(final_table)

    # =====================================================
    # CLEAN COMPARISON TABLE
    # =====================================================
    print("\n================ CLEAN COMPARISON TABLE ================\n")

    rows = []

    for _, row in results_df.iterrows():

        rows.append({
            "dataset": row["dataset"],
            "fraction": row["fraction"],
            "method": "Exact",
            "result": row["exact_result"],
            "runtime": row["exact_time"],
            "abs_error": 0,
            "rel_error": 0
        })

        rows.append({
            "dataset": row["dataset"],
            "fraction": row["fraction"],
            "method": "Random",
            "result": row["random_result_mean"],
            "runtime": row["random_time_mean"],
            "abs_error": row["random_error_mean"],
            "rel_error": row["random_error_mean"] / abs(row["exact_result"])
        })

        rows.append({
            "dataset": row["dataset"],
            "fraction": row["fraction"],
            "method": "Stratified",
            "result": row["strat_result_mean"],
            "runtime": row["strat_time_mean"],
            "abs_error": row["strat_error_mean"],
            "rel_error": row["strat_error_mean"] / abs(row["exact_result"])
        })

    clean_df = pd.DataFrame(rows).round(4)

    print(clean_df)

    # SAVE CLEAN TABLE
    clean_df.to_csv("output/clean_comparison.csv", index=False)
    print("Clean comparison table saved to output/clean_comparison.csv")

    # =====================================================
    # 🔥 SUMMARY TABLE (NEW)
    # =====================================================
    print("\n================ SUMMARY TABLE ================\n")

    summary_df = clean_df.groupby(["dataset", "method"]).agg({
        "abs_error": "mean",
        "runtime": "mean",
        "rel_error": "mean"
    }).reset_index().round(4)

    print(summary_df)

    # SAVE SUMMARY TABLE
    summary_df.to_csv("output/summary_table.csv", index=False)
    print("Summary table saved to output/summary_table.csv")

    # -----------------------------
    # Save results
    # -----------------------------
    results_df.to_csv(OUTPUT_RESULTS, index=False)
    print(f"\nResults saved to {OUTPUT_RESULTS}")

    results_df.to_sql("experiment_results", conn, if_exists="replace", index=False)
    print("Results also saved into SQLite database table: experiment_results")

    conn.close()

    # -----------------------------
    # Plotting
    # -----------------------------
    print("\nGenerating plots...")

    for dataset in results_df["dataset"].unique():
        df_plot = results_df[results_df["dataset"] == dataset]

        plt.figure()
        plt.plot(df_plot["fraction"], df_plot["random_error_mean"], marker="o", label="Random")
        plt.plot(df_plot["fraction"], df_plot["strat_error_mean"], marker="o", label="Stratified")

        plt.xlabel("Sample Fraction")
        plt.ylabel("Absolute Error")
        plt.title(f"Error vs Sample Size ({dataset})")
        plt.legend()

        save_path = f"output/{dataset}_error_plot.png"
        plt.savefig(save_path)
        print(f"Saved plot: {save_path}")

        plt.show(block=True)

    print("\nDone.")
    print(results_df)


if __name__ == "__main__":
    main()