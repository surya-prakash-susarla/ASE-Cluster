from sym import Sym
from num import Num
from utils import rand, rint, rnd, show, show_tree, tree, value, xpln, showRule, selects, ysNums, xpln_improved
from data import Data, rep_cols, rep_rows, rep_grid, rep_place, transpose, cliffsDelta, bootstrap
from csv import get_csv_rows
from collections import OrderedDict
from globals import *
from data import diffs

import copy


def test_xpln():
    data = Data(global_options[K_FILE])
    best, rest, evals = data.sway()
    rule, most = xpln(data, best, rest)
    print('*'*10)
    print("rule from xpln : ", rule)
    for r in rule:
        print(showRule(r))
    return True


def test_global_options() -> bool:
    print(global_options)
    return True


def test_rand() -> bool:
    global_options[K_SEED] = 1
    max_range = 1000
    t = []
    for i in range(1, max_range):
        t.append(rand(hi=100))
    global_options[K_SEED] = 1
    u = []
    for i in range(1, max_range):
        u.append(rand(hi=100))
    return (t == u)


def test_some() -> bool:
    global_options[K_MAX] = 32
    num1 = Num()
    for i in range(1, 10000):
        num1.add(i)
    print(num1.has)
    print('length : ', len(num1.has))
    return True


def test_clone() -> bool:
    data = Data(global_options[K_FILE])
    data2 = data.clone(data.rows)
    print(data.stats())
    print(data2.stats())
    return True


def test_dist() -> bool:
    data = Data(global_options[K_FILE])
    num = Num()
    for row in data.rows:
        num.add(data.dist(row, data.rows[0]))
    num.print()
    return True


def test_cliffs() -> bool:
    if (False == cliffsDelta([8, 7, 6, 2, 5, 8, 7, 3], [8, 7, 6, 2, 5, 8, 7, 3])):
        print("False")
    else:
        print("1")

    if (True == cliffsDelta([8, 7, 6, 2, 5, 8, 7, 3], [9, 9, 7, 8, 10, 9, 6])):
        print("True")
    else:
        print("2")

    t1 = []
    t2 = []
    for i in range(1000):
        random_number = rand()
        t1.append(random_number)
    for i in range(1000):
        random_number = rand()
        t2.append(random_number**0.5)

    if (cliffsDelta(t1, t1)):
        print("3")
    else:
        print("False")
    if (cliffsDelta(t1, t2)):
        print("True")
    else:
        print("4")
    diff = False
    j = 1.0
    while (diff == False):
        t3 = []
        for i in t1:
            t3.append(i*j)
        diff = cliffsDelta(t1, t3)
        print('>', rnd(j), diff)
        j = j*1.025
    return True


def test_tree() -> bool:
    show_tree(tree(Data()))
    return True


def test_sway() -> bool:
    data = Data(global_options[K_FILE])
    best, rest, evals = data.sway()
    print("\n all ", data.stats())
    print("    ",   data.stats(is_mid=False))
    print("\nbest", best.stats())
    print("    ",   best.stats(is_mid=False))
    print("\nrest", rest.stats())
    print("    ",   rest.stats(is_mid=False))
    print("\n all ~= best?", diffs(best.cols.y, data.cols.y))
    print("best ~= rest?", diffs(best.cols.y, rest.cols.y))
    return True


def test_bins() -> bool:
    data = Data(global_options[K_FILE])
    best, rest, evals = data.sway()
    rowss = {}
    rowss['best'] = best.rows
    rowss['rest'] = rest.rows
    b4 = None

    for t in (data.bins(data.cols.x, rowss)):
        for k in t:
            if k.txt != b4:
                print(" ")
            b4 = k.txt
            print(k.txt, k.min, k.max, rnd(
                value(k.y.has, len(best.rows), len(rest.rows), "best")), end=' ')
            for col in k.y.has:
                print(col, ":", k.y.has[col], end=' ')
            print("\n")

    return True


def test_num() -> bool:
    num = Num()
    nums = [1, 1, 1, 1, 2, 2, 3]
    for i in nums:
        num.add(i)
    return 11/7 == num.mid() and 0.787 == rnd(num.div())


def test_sym() -> bool:
    sym = Sym()
    symbols = ["a", "a", "a", "a", "b", "b", "c"]
    for s in symbols:
        sym.add(s)
    return ("a" == sym.mid() and 1.379 == rnd(sym.div()))


def test_read_from_csv():
    rows = get_csv_rows(global_options[K_FILE])
    total_rows = len(rows)
    total_columns = len(rows[0])
    return total_columns*total_rows == 8*399


def test_half():
    data = Data(global_options[K_FILE])
    left, right, A, B, mid, c = data.half()
    print(len(left), len(right), len(data.rows))
    print(A.cells, c)
    print(mid)
    print(B.cells)
    return True


def xpln_with_n_iterations(n):
    rules = Num()

    out = {'all': None, 'sway': None, 'xpln': None,
           'ztop': None, 'sway_1': None, 'xpln_1': None}

    for i in range(n):
        print('*'*20)
        print("Iteration : ", i+1)
        data = Data(global_options[K_FILE])
        best, rest, evals = data.sway()
        best1, rest1, evals = data.sway_improved()
        print('total number of rows : ', len(data.rows))
        print('number of best : ', len(best.rows))
        print('number of rest : ', len(rest.rows))
        print('number of best improved : ', len(best1.rows))
        print('number of rest improved : ', len(rest1.rows))
        # skipping print from original source of xpln20
        rule, most = xpln(data, best, rest)
        rule1, most1 = xpln_improved(data, best1, rest1)

        def generate_sway_data(out, data, best, label):
            if out[label] == None:
                out[label] = {}
                for col in data.cols.y:
                    out[label][col.txt] = Num(col.at, col.txt)
            ysNums(out[label], best)

        def generate_xpln_data(out, data, data1, label):
            if out[label] == None:
                out[label] = {}
                for col in data.cols.y:
                    out[label][col.txt] = Num(col.at, col.txt)
            ysNums(out[label], data1)

        if len(rule) > 0 and len(rule1) > 0:
            print("Rule : {}\nMost: {}".format(rule, most))
            rules.add(len(rule))
            print("Using rule : ", rule[0])
            print("Using second rule : ", rule1[0])
            data1 = data.clone(data.rows)
            data1 = data1.clone(selects(rule[0], data.rows))
            data2 = data.clone(data.rows)
            data2 = data2.clone(selects(rule1[0], data.rows))
            if out['all'] == None:
                out['all'] = {}
                for col in data.cols.y:
                    out['all'][col.txt] = Num(col.at, col.txt)
            ysNums(out['all'], data)

            generate_sway_data(out, data, best, 'sway')
            generate_sway_data(out, data, best1, 'sway_1')
            generate_xpln_data(out, data, data1, 'xpln')
            generate_xpln_data(out, data, data2, 'xpln_1')

            if out['ztop'] == None:
                out['ztop'] = {}
                for col in data.cols.y:
                    out['ztop'][col.txt] = Num(col.at, col.txt)

            tmp, _ = data.betters(len(best.rows))
            top = data.clone(data.rows)
            top = top.clone(tmp)
            ysNums(out['ztop'], top)

            print('-'*20)
    return out, rules


def test_xpln(n=20):
    out, rules = None, None
    while out == None:
        out, rules = xpln_with_n_iterations(n)
    header = ["all", "sway", "sway_1", "xpln", "xpln_1", "ztop"]

    vars = sorted(list(out["all"].keys()))

    for col_name in vars:
        print("&"+str(col_name), end=' ')
    for k in header:
        nums = out[k]

        print("\n" + str(k), end=' ')
        for x in vars:

            num = nums[x]
            print(' & ' + str(rnd(num.mid(), 2)), end='')

    def fun(x):
        if (x):
            return '='
        return '≠'

    print('\n.')
    for col_name in vars:
        print("&"+str(col_name), end=' ')

    for h in header:
        print("\nall to " + str(h), end=' ')
        for v in vars:
            t1 = out['all'][v].has
            t2 = out[h][v].has

            b_return = bootstrap(t1, t2)
            c_return = cliffsDelta(t1, t2)

            print("&" + str(fun(b_return and c_return)), end='')

    if rules.n > 0:
        print("\n rule size " + "mu " + str(rules.mid()) +
              " std " + str(rnd(rules.div())))
