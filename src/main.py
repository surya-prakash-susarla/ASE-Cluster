import sys
import math
import collections
import pathlib

from test import *
from cli import initialize_from_cli, print_help
from globals import global_options, K_HELP, K_START_ACTION, K_FILE

def generate_results() -> int:
    # Iterate through files in the data path.
    files = pathlib.Path('../etc/data/').iterdir()

    for f in files:
        print('\n'*2 + '<'*10 + '='*15 + '>'*10)
        print("Currently processing file : ", f)
        global_options[K_FILE] = f
        test_xpln20()
        print('<'*10 + '='*15 + '>'*10 + '\n'*2)

    return 0

def __main__() -> int:
    initialize_from_cli()

    if global_options[K_HELP]:
        print_help()
        return 0

    return generate_results()


sys.exit(__main__())
