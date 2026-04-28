import sqlite3
import pandas as pd
from config import DATASETS, DATABASE_NAME

def get_connection():
    return sqlite3.connect(DATABASE_NAME)

def load_csvs_to_database():
    conn = get_connection()

    for dataset_name, file_path in DATASETS.items():
        df = pd.read_csv(file_path)
        df = df.dropna()
        df.to_sql(dataset_name, conn, if_exists="replace", index=False)
        print(f"Loaded {dataset_name} into database.")

    conn.close()