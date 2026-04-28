# sampling.py
# Contains stratification logic + random sampling + stratified sampling + adaptive sampling

import pandas as pd
from queries import run_query_pandas


# -----------------------------
# 1. Choose stratification column
# -----------------------------
def get_strat_column(dataset_name):
    if dataset_name == "taxi":
        return "passenger_count"
    elif dataset_name == "retail":
        return "Country"
    elif dataset_name == "tpch":
        return "l_shipmode"
    else:
        raise ValueError(f"Unknown dataset: {dataset_name}")


# -----------------------------
# 2. Uniform random sampling
# -----------------------------
def random_sampling(df, dataset_name, frac=0.1, seed=42):
    sample = df.sample(frac=frac, random_state=seed)
    return run_query_pandas(sample, dataset_name)


# -----------------------------
# 3. Stratified sampling
# -----------------------------
def stratified_sampling(df, dataset_name, frac=0.1, seed=42):
    strat_col = get_strat_column(dataset_name)

    # robustness check
    if strat_col not in df.columns:
        raise ValueError(f"Column '{strat_col}' not found in dataset")

    samples = []

    for _, group in df.groupby(strat_col):
        n = max(1, int(len(group) * frac))  # at least 1 row
        n = min(n, len(group))              # avoid oversampling

        sampled_group = group.sample(n=n, random_state=seed)
        samples.append(sampled_group)

    strat_sample = pd.concat(samples, ignore_index=True)

    return run_query_pandas(strat_sample, dataset_name)


# -----------------------------
# 4. Adaptive sampling 
# -----------------------------
def adaptive_sampling(
    df,
    dataset_name,
    exact_value,
    initial_frac=0.01,
    max_frac=0.5,
    tolerance=0.05,
    seed=42,
    verbose=True   # 👈 NEW (controls printing)
):
    """
    Adaptive sampling:
    - Starts small
    - Doubles sample size until error is acceptable
    """

    frac = initial_frac
    last_estimate = None
    last_error = None

    if verbose:
        print(f"\n[Adaptive] Starting for dataset: {dataset_name}", flush=True)

    while frac <= max_frac:

        # Step 1: sample
        sample = df.sample(frac=frac, random_state=seed)

        # Step 2: estimate
        estimate = run_query_pandas(sample, dataset_name)

        # Step 3: compute relative error safely
        if exact_value == 0 or pd.isna(exact_value):
            error = 0
        else:
            error = abs(estimate - exact_value) / abs(exact_value)

        # Step 4: print progress (FORCE display)
        if verbose:
            print(
                f"[Adaptive][{dataset_name}] frac={frac:.3f} | estimate={estimate:.4f} | error={error:.4f}",
                flush=True
            )

        # Save last values
        last_estimate = estimate
        last_error = error

        # Step 5: stopping condition
        if error < tolerance:
            if verbose:
                print(f"[Adaptive] STOP (tolerance met)\n", flush=True)

            return {
                "estimate": estimate,
                "fraction_used": frac,
                "error": error
            }

        # Step 6: increase sample size
        frac *= 2

    # If max fraction reached
    if verbose:
        print(f"[Adaptive] STOP (max fraction reached)\n", flush=True)

    return {
        "estimate": last_estimate,
        "fraction_used": frac,
        "error": last_error
    }