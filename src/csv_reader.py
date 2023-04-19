from pathlib import Path
import re

def coerce(s):
    return_value = None
    try:
        return_value = s.strip() if bool(re.search(r'[a-zA-Z]', s)) else float(s)
    except ValueError as error:
        # print("Conversion Error : ", error)
        return (return_value, False)
    else:
        return (return_value, True)

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
            split_line = line.strip().split(',')
            row = []
            invalid_row = False
            for x in split_line:
                converted_value = coerce(x)
                if converted_value[1] == False:
                    invalid_row = True
                    break
                else:
                    row.append(converted_value[0])

            if invalid_row:
                # print("Skipping invalid input line: ", line)
                continue
            else:
                rows.append(row)

    return rows
