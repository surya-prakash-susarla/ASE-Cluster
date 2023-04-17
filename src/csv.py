from pathlib import Path
import re

def coerce(s):
    s = s.strip() if bool(re.search(r'[a-zA-Z]', s)) else float(s)
    return s

def get_csv_rows(filepath: str) -> []:
    filepath = Path(filepath)
    does_file_exist = filepath.exists()
    is_csv_suffix = (filepath.suffix == '.csv') 
    if not does_file_exist or not is_csv_suffix:
        print("File path does not exist OR File not csv, given path: ", filepath.absolute())
        return

    rows = []
    with open(filepath.absolute(), 'r', encoding='utf-8') as file:
        for row_no, line in enumerate(file):
            row = list(map(coerce, line.strip().split(',')))
            rows.append(row)

    return rows
