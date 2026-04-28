import pandas as pd
import time

# -----------------------------
# 1. Pandas-based query
# -----------------------------
def run_query_pandas(df, dataset_name):
    if dataset_name == "taxi":
        return df[df["trip_distance"] > 5]["fare_amount"].mean()

    elif dataset_name == "retail":
        filtered = df[df["Quantity"] > 5].copy()
        filtered["total_price"] = filtered["Quantity"] * filtered["UnitPrice"]
        return filtered["total_price"].mean()

    elif dataset_name == "tpch":
        return df[df["l_discount"] < 0.05]["l_extendedprice"].mean()

    else:
        raise ValueError(f"Unknown dataset: {dataset_name}")


# -----------------------------
# 2. SQL query generator
# -----------------------------
def get_exact_sql_query(dataset_name):
    if dataset_name == "taxi":
        return """
        SELECT AVG(fare_amount) AS result
        FROM taxi
        WHERE trip_distance > 5
        """

    elif dataset_name == "retail":
        return """
        SELECT AVG(Quantity * UnitPrice) AS result
        FROM retail
        WHERE Quantity > 5
        """

    elif dataset_name == "tpch":
        return """
        SELECT AVG(l_extendedprice) AS result
        FROM tpch
        WHERE l_discount < 0.05
        """

    else:
        raise ValueError(f"Unknown dataset: {dataset_name}")


# -----------------------------
# 3. Execute SQL query
# -----------------------------
def exact_query_sql(conn, dataset_name):
    query = get_exact_sql_query(dataset_name)

    start = time.time()
    result = pd.read_sql_query(query, conn).iloc[0, 0]
    elapsed = time.time() - start

    return result, elapsed