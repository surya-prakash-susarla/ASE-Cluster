import sys
import math
import collections

from test import *
from cli import initialize_from_cli, print_help
from globals import global_options, K_HELP, K_START_ACTION

def generate_results() -> int:
    n = 2
    return_value = xpln_with_n_iterations(n)
    print(return_value)
    return 0

def __main__() -> int:
    initialize_from_cli()

    if global_options[K_HELP]:
        print_help()
        return 0

    return generate_results()


sys.exit(__main__())
