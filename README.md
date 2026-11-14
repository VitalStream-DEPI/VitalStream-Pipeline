# MedStream — Diabetes Prediction Pipeline 🩺📊

> **DEPI Graduation Project** — End-to-End Medical Data Engineering & Machine Learning Pipeline for Diabetes Prediction.

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Dataset](https://img.shields.io/badge/Dataset-Diabetes_Prediction_100k-green.svg)](#)

---

## 📌 Project Overview
**MedStream** is a complete medical data pipeline designed to ingest, clean, explore, and predict diabetes risk among patients using demographic, lifestyle, and clinical indicators.

---

## 🔬 Dataset Overview (`diabetes_prediction_dataset.csv`)
The dataset contains **100,000 patient records** and **9 features**:

| Feature | Type | Description |
| :--- | :--- | :--- |
| `gender` | Categorical | Female / Male |
| `age` | Numeric | Patient age (years) |
| `hypertension` | Binary (0/1) | 0: No high blood pressure, 1: High blood pressure |
| `heart_disease` | Binary (0/1) | 0: No heart disease, 1: Has heart disease |
| `smoking_history` | Categorical | never, current, former, No Info |
| `bmi` | Numeric | Body Mass Index |
| `HbA1c_level` | Numeric | Glycated hemoglobin level |
| `blood_glucose_level` | Numeric | Blood glucose level (mg/dL) |
| **`diabetes`** | **Target (0/1)** | **0: No Diabetes, 1: Diagnosed with Diabetes** |

---

## 🗂️ Project Directory Structure

```text
MedStream/
├── data/
│   ├── raw/                  # Raw dataset (diabetes_prediction_dataset.csv)
│   └── processed/            # Cleaned data (diabetes_cleaned.csv)
├── notebooks/                # Exploratory & cleaning notebooks
│   └── MedStream.ipynb       # Main interactive cleaning notebook
├── src/                      # Source code (pipelines, models)
├── tests/                    # Unit tests
├── inspect_dataset.py        # Dataset verification script
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

---

## 🚀 Quick Start & How to Run

### 1. Test dataset inspection:
```bash
py inspect_dataset.py
```

### 2. Run Data Cleaning in Notebook:
Open `MedStream.ipynb` in VS Code and click **Run All**. The cleaned dataset will automatically be created at:
`data/processed/diabetes_cleaned.csv`.
