import sys
import math
import collections

from test import *
from cli import initialize_from_cli, print_help
from globals import global_options, K_HELP, K_START_ACTION

def generate_results() -> int:
    print("Begin generating results")
    n = 20
    return_value = xpln_with_n_iterations(n)
    return 0

#### MAIN
def __main__() -> int:
    initialize_from_cli()

    if global_options[K_HELP]:
        print_help()
        return 0

    return generate_results()

sys.exit(__main__())

