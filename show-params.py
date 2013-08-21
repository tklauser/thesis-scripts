#!/usr/bin/env python
# *-* coding: utf-8 -*-
#
# show-params.py -- Show drobot experiment parametes in human-readable form
#
# Copyright (C) 2013 Tobias Klauser <tklauser@distanz.ch>

import getopt
import os, sys

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

    p = os.path.join(d, params_file)
    if not os.path.isfile(p):
        return 

    f = open(p, 'r')
    labels = f.readline().strip().split(',')
    values = f.readline().strip().split(',')
    f.close()

    if len(labels) == 0 or len(values) == 0:
        print("no parameters found in {}".format(p))
        return

    if len(labels) != len(values):
        print("number of labels doesn't correspond to number of values in {}".format(p))
        return

    print("experiment {}".format(d))
    for i, l in enumerate(labels):
        print("  {:<25}: {}".format(l, values[i]))
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
