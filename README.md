# Approximate Query Processing using Sampling Techniques

## Overview
This project implements and evaluates Approximate Query Processing (AQP) techniques for analytical queries.

Instead of scanning entire datasets, AQP uses sampling methods to estimate query results, significantly improving performance while maintaining acceptable accuracy. The project compares exact query execution with sampling-based approaches to analyze the trade-off between speed and accuracy.

The following methods are implemented:
- Exact Query Execution (baseline)
- Uniform Random Sampling
- Stratified Sampling
- Adaptive Sampling (optional extension)

---

## Objectives
The primary objectives of this project are:
- To reduce query execution time using sampling techniques  
- To evaluate trade-offs between accuracy and performance  
- To compare different sampling strategies across datasets  
- To analyze how error changes with varying sample sizes  

---

## Datasets
The experiments are conducted on the following datasets:
- NYC Taxi Dataset  
- Online Retail Dataset  
- TPC-H Lineitem Dataset  

Note: Datasets are not included in this repository due to size constraints.

---

## Technologies Used
- Python  
- Pandas  
- NumPy  
- SQLite  
- Matplotlib  

---

## Methodology

### Exact Query Execution
Executes SQL queries on the full dataset to obtain the ground truth.

### Uniform Random Sampling
Selects a random subset of data and scales the result to estimate the full dataset.

### Stratified Sampling
Divides the dataset into groups (strata) and samples each group proportionally to improve accuracy.

### Adaptive Sampling (Optional)
Dynamically adjusts the sample size based on error thresholds.

---

## Evaluation Metrics
Performance is evaluated using the following metrics:
- Runtime (execution time)  
- Absolute error  
- Relative error  
- Speedup over exact query execution  

---

## How to Run

### Prerequisites
Ensure that the following are installed:
- Python 3.9 or higher  
- Git (optional)
-Install dependencies 
pip install pandas numpy matplotlib
-import sqlite3
- Add Dataset Files
--Create a folder named data/ and place the dataset files inside: taxi.csv, retail.csv, lineitem.csv
- ensure the dataset paths in config.py match the file names
-Run the project from main.py
-view results 
After execution, results are saved in the output/ directory.

## Generated files include:

-results.csv (full experiment results)
-clean_comparison.csv (formatted comparison table)
-summary_table.csv (aggregated metrics)

## Result interpretation
-Sampling significantly reduces query execution time
-Stratified sampling produces lower error than uniform random sampling
-Increasing sample size improves accuracy
-There is a clear trade-off between speed and accuracy

## Contributors
-Olumide Adebisi
-Onyiyechi Agu
-Fortress Ezeuchenne

