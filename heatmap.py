#!/usr/bin/env python
# -*- coding: utf-8 -*-

import getopt
import os, sys
import numpy as np
import matplotlib.pyplot as plt

def usage():
    print("""usage: {} [OPTION...] DIRECTORY

Show heat map plot of the number of times an input field has been activated

By default the plot is shown for the first and last time step.

options:

  -t TIME...  comma-separated list (without space) of timestamps, negative
              numbers are intepreted as counting from the end (as in python)
  -h          show this help and exit
""".format(os.path.basename(sys.argv[0])))

def heatmap(ddir, ts):
    # TODO: move directory checking and parameter reading into class used by
    # this script and force_fields.py
    if not os.path.isdir(ddir):
        print("{} is not a directory".format(ddir))
        return

    p = os.path.join(ddir, 'params.log')
    if not os.path.isfile(p):
        print("parameter file {} not found".format(p))
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

    # put parameters into a directory, accessable by parameter name
    params = dict(zip(labels, values))

    if not ('nRowsIn' in params and 'nColsIn' in params):
        print("not all necessary parameters available in the parameter file")
        return

    nRows = int(params['nRowsIn'])
    nCols = int(params['nColsIn'])

    indata = np.genfromtxt(os.path.join(ddir, 'in.log'), delimiter=',')

    time = indata[:,0]
    T = len(time)
    indata = indata[:,1:]
    [x, y] = np.meshgrid(np.arange(0, nRows + 1), np.arange(0, nCols + 1))

    fig = plt.figure()

    for i, t in enumerate(ts):
        # use negative indices as in python
        if t < 0:
            t = T + t

        if t >= T:
            t = T - 1
        elif t < 1:
            t = 1

        incount = indata[0:t,:].sum(axis=0)
        incount = incount.reshape(nRows,nCols)
        incount = np.flipud(incount)

        s = '1' + str(len(ts)) + str(i + 1)
        ax = fig.add_subplot(int(s))

        p = ax.pcolormesh(x, y, incount)
        ax.set_aspect('equal')
        fig.colorbar(p, ax=ax, shrink=0.35, pad=0.1, aspect=10)
        ax.set_title("time step {}".format(t, time[t]))

    plt.show()
def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "t:h")
    except getopt.GetoptError, err:
        print(str(err))
        usage()
        sys.exit(-1)

    if len(args) < 1:
        usage()
        sys.exit(-1)

    # show last timestep by default
    ts = [-1]

    for o, a in opts:
        if o == '-t':
            ts = a.split(',')
            if len(ts) < 1:
                print("invalid timestep specification: {}".format(a))
                sys.exit(-1)
        elif o == '-h':
            usage()
            sys.exit(0)
        else:
            assert False, "unhandled option"

    heatmap(args[0], np.array(ts, np.int32))

if __name__ == '__main__':
    main()
