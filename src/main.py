import sys
import math
import collections
import pathlib
import numpy as np
from test import *
from cli import initialize_from_cli, print_help
from globals import global_options, K_HELP, K_START_ACTION, K_FILE
import pandas as pd
from data import Data

def print_corr():
    data = Data(global_options[K_FILE])
    cells = [x.cells for x in data.rows]
    cells = np.array(cells)
    cells = np.delete(cells, [x.at for x in data.cols.x], axis = 1)
    cells = pd.DataFrame(cells)
    print(cells.corr())
    

def generate_results() -> int:
    # Iterate through files in the data path.
    files = pathlib.Path('../etc/data/').iterdir()
    files = list(files)
    print("files : ", files)
    # ONLY USE BELOW WHEN DEBUGGING:
    # files = pathlib.Path('etc/data').iterdir()
    # ONLY USE ABOVE WHEN DEBUGGING:
    skip = 1

    k_def = 0
    k_hpo = 1
    k_abl = 2

    mode = k_def

    break_at_end = False
    for f in files:
        if skip > 0:
            skip -= 1
            continue
        else:
            break_at_end = True
        print('\n'*2 + '<'*10 + '='*15 + '>'*10)
        print("Currently processing file : ", f)
        global_options[K_FILE] = f
        iterations = 1
        print_corr()
        if mode == k_def:
            test_xpln(iterations)
        elif mode == k_hpo:
            test_hpo()
            # HPO test only on one file
            break
        else:
            test_abl()
            # ABL test only on one file
            break

        print('<'*10 + '='*15 + '>'*10 + '\n'*2)

        if break_at_end:
            print("braeking")
            break

    return 0

def __main__() -> int:
    initialize_from_cli()

    if global_options[K_HELP]:
        print_help()
        return 0

    return generate_results()


sys.exit(__main__())
