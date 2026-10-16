from pathlib import Path
import pandas as pd

DATA_PATH = Path("data/raw")

files = sorted(DATA_PATH.rglob("*.csv*"))
print("عدد الملفات:", len(files))

for file_path in files:
    print("\n" + "=" * 60)
    print("File:", file_path.name)
    df = pd.read_csv(file_path, nrows=5)
    print("Columns:", df.columns.tolist())