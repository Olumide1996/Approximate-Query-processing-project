import time
import numpy as np
import pandas as pd

from config import TRIALS, SAMPLE_FRACTIONS
from sampling import random_sampling, stratified_sampling, adaptive_sampling
from queries import exact_query_sql


def run_experiment(df, dataset_name, conn):
    exact_result, exact_time = exact_query_sql(conn, dataset_name)
    results = []

    for frac in SAMPLE_FRACTIONS:
        rand_errors = []
        strat_errors = []
        rand_times = []
        strat_times = []

        # NEW: store actual results
        rand_results = []
        strat_results = []

        adaptive_errors = []
        adaptive_times = []
        adaptive_fracs = []
        adaptive_results = []  # optional (for completeness)

        for trial in range(TRIALS):

            # -----------------------------
            # Random sampling
            # -----------------------------
            start = time.time()
            rand_result = random_sampling(df, dataset_name, frac, trial)
            rand_time = time.time() - start

            # -----------------------------
            # Stratified sampling
            # -----------------------------
            start = time.time()
            strat_result = stratified_sampling(df, dataset_name, frac, trial)
            strat_time = time.time() - start

            # -----------------------------
            # Store actual results (NEW)
            # -----------------------------
            rand_results.append(rand_result)
            strat_results.append(strat_result)

            # -----------------------------
            # Errors
            # -----------------------------
            rand_error = abs(rand_result - exact_result)
            strat_error = abs(strat_result - exact_result)

            rand_errors.append(rand_error)
            strat_errors.append(strat_error)
            rand_times.append(rand_time)
            strat_times.append(strat_time)

            # -----------------------------
            # Adaptive sampling
            # -----------------------------
            start = time.time()

            adaptive_output = adaptive_sampling(
                df,
                dataset_name,
                exact_result
            )

            adaptive_time = time.time() - start

            adaptive_result = adaptive_output["estimate"]
            adaptive_error = adaptive_output["error"]
            used_frac = adaptive_output["fraction_used"]

            adaptive_errors.append(adaptive_error)
            adaptive_times.append(adaptive_time)
            adaptive_fracs.append(used_frac)
            adaptive_results.append(adaptive_result)

        # -----------------------------
        # Save results (UPDATED)
        # -----------------------------
        results.append({
            "dataset": dataset_name,
            "fraction": frac,
            "exact_result": exact_result,
            "exact_time": exact_time,

            # NEW: actual outputs (VERY IMPORTANT FOR DEFENSE)
            "random_result_mean": np.mean(rand_results),
            "strat_result_mean": np.mean(strat_results),
            "adaptive_result_mean": np.mean(adaptive_results),

            # Errors
            "random_error_mean": np.mean(rand_errors),
            "random_error_std": np.std(rand_errors),

            "strat_error_mean": np.mean(strat_errors),
            "strat_error_std": np.std(strat_errors),

            # Times
            "random_time_mean": np.mean(rand_times),
            "random_time_std": np.std(rand_times),

            "strat_time_mean": np.mean(strat_times),
            "strat_time_std": np.std(strat_times),

            # Adaptive results
            "adaptive_error_mean": np.mean(adaptive_errors),
            "adaptive_error_std": np.std(adaptive_errors),
            "adaptive_time_mean": np.mean(adaptive_times),
            "adaptive_fraction_mean": np.mean(adaptive_fracs),
        })

    return results