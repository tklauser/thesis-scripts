#!/usr/bin/env python
# *-* coding: utf-8 -*-
#
# show-params.py -- Show drobot experiment parametes in human-readable form
#
# Copyright (C) 2013 Tobias Klauser <tklauser@distanz.ch>

import getopt
import os, sys
from params import import_params

LEARNING_RULES = {
        0: 'Oja',
        1: 'Hebbian Covariance',
        2: 'McMillen',
        3: 'Learning by Mistakes',
}

OUTPUT_FUNCTIONS = {
        0: 'linear',
        1: 'sigmoid',
}

def usage():
    print("""usage: {} [OPTION...] DIRECTORY...

Show drobot experiment parameters in human-readable form for chosen directories.

options:

  -R  recursive mode
  -h  show this help and exit""".format(os.path.basename(sys.argv[0])))

def show_params(d, params_file, recursive):
    if not os.path.isdir(d):
        return

    if recursive:
        for dd in os.listdir(d):
            dd = os.path.join(d, dd)
            if os.path.isdir(dd):
                show_params(dd, params_file, recursive)

    params = import_params(d, params_file)

    print("experiment {}".format(d))
    linear = False
    for l, v in params.items():
        if l == 'time':
            continue
        elif l == 'learningRule':
            v = LEARNING_RULES[int(params[l])]
        elif l == 'outputFn':
            v = OUTPUT_FUNCTIONS[int(params[l])]
            if v == 'linear':
                linear = True
        else:
            v = params[l]

        if l == 'sigmoidBeta' and linear:
            continue

        print("  {:<25}: {}".format(l, v))
    print("")

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "Rh")
    except getopt.GetoptError, err:
        print(str(err))
        usage()
        sys.exit(-1)

    if len(args) < 1:
        usage()
        sys.exit(-1)

    recursive = False
    params_file = 'params.log'

    for o, a in opts:
        if o == '-R':
            recursive = True
        elif o == '-h':
            usage()
            sys.exit(0)
        else:
            assert False, "unhandled option"

    for d in args:
        show_params(d, params_file, recursive)

if __name__ == '__main__':
    main()
