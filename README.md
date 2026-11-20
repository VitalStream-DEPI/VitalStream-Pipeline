# MedStream

A data engineering pipeline and machine learning project for diabetes risk prediction using patient health records.

## Overview
This repository contains the end-to-end workflow for processing clinical diabetes data. The pipeline cleans raw patient records, performs exploratory analysis, loads the prepared records into an embedded analytical warehouse (DuckDB), trains classification models to predict diabetes risk, and provides an interactive clinical web dashboard.

## Dataset
We use the diabetes prediction dataset containing 100,000 patient records across 9 features:
- `gender`: Female or Male
- `age`: Patient age in years
- `hypertension`: High blood pressure diagnosis (0 = no, 1 = yes)
- `heart_disease`: Heart condition history (0 = no, 1 = yes)
- `smoking_history`: Patient smoking status
- `bmi`: Body Mass Index
- `HbA1c_level`: Glycated hemoglobin test result
- `blood_glucose_level`: Fasting blood sugar level
- `diabetes`: Target label (0 = non-diabetic, 1 = diabetic)

## Project Structure
```text
MedStream/
├── data/
│   ├── raw/                  # Source CSV files
│   └── processed/            # Cleaned data ready for modeling
├── models/                   # Exported trained ML models (.pkl)
├── notebooks/                # Jupyter notebooks for interactive analysis
├── EDA.ipynb                 # Visualizations and feature distributions
├── MedStream.ipynb           # Data cleaning and transformation pipeline
├── data_warehouse.ipynb      # DuckDB table setup and SQL queries
├── model_training.ipynb      # AI model training (Random Forest & Logistic Regression)
├── app.py                    # Interactive clinical web dashboard (Streamlit)
├── requirements.txt          # Required Python packages
└── README.md
```

## Setup & Execution
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run notebooks in order:
   - `MedStream.ipynb`: Cleans raw records, drops duplicates, and exports `diabetes_cleaned.csv`.
   - `EDA.ipynb`: Checks summary stats, class distributions, and correlation values.
   - `data_warehouse.ipynb`: Stores cleaned records in DuckDB (`patients_analytics` table).
   - `model_training.ipynb`: Queries data from DuckDB, trains Random Forest (97.2% accuracy), and exports `models/diabetes_model.pkl`.
3. Launch Interactive Clinical Dashboard:
   ```bash
   py -m streamlit run app.py
   ```
