#!/usr/bin/env python
# -*- coding: utf-8 -*-

import getopt
import os, sys
import numpy as np
import matplotlib.pyplot as plt

def usage():
    print("""usage: {} [OPTION...] DIRECTORY...

Show heat map plot of the number of times an input field has been activated

By default the plot is shown for the first and last time step.

options:

  -c CMAP     use CMAP als colormap, see help(colormaps) in matplotlib for a list
  -t TIME...  comma-separated list (without space) of timestamps, negative
              numbers are intepreted as counting from the end (as in python)
  -s SUBPLOT  specify subplot layout (in matplotlib style, e.g. 23 for 2 rows/3 columns)
  -q          quiet mode, don't show plot, only write PDF
  -h          show this help and exit
""".format(os.path.basename(sys.argv[0])))

def heatmap(ddir, ts, cmap, subplot, quiet):
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

    # set the colormap
    if cmap != None:
        cmap = plt.get_cmap(cmap)
    else:
        cmap = plt.get_cmap('gray_r')

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

        if not subplot is None:
            s = subplot + str(i + 1)
        else:
            s = '1' + str(len(ts)) + str(i + 1)

        ax = fig.add_subplot(int(s))

        p = ax.pcolormesh(x, y, incount, cmap=cmap, rasterized=True)

#        cb = fig.colorbar(p, ax=ax, shrink=0.35, pad=0.2, aspect=10)
#        cb.set_label('# of stimulations')
        ax.set_aspect('equal', 'box')
        ax.set_xticks(np.arange(0.5, nCols + 0.5, 2))
        ax.set_xticklabels(np.arange(0, nCols + 1, 2), fontsize=8)
        ax.tick_params(axis='x', which='both', bottom='off', top='off', labelbottom='on')
        ax.set_yticks(np.arange(0.5, nRows + 0.5, 2))
        ax.set_yticklabels(np.arange(0, nRows + 1, 2), fontsize=8)
        ax.tick_params(axis='y', which='both', left='off', right='off', labelleft='on')
        ax.set_xlim(0, nCols)
        ax.set_ylim(0, nRows)
        ax.set_title("time step {}".format(t, time[t]), fontsize=12)

    fig.suptitle(ddir)
    plt.savefig(os.path.join(ddir, 'heatmap.pdf'), dpi=300, bbox_inches='tight', pad_inches=0.15)
    if not quiet:
        plt.show()

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "c:t:s:qh")
    except getopt.GetoptError, err:
        print(str(err))
        usage()
        sys.exit(-1)

    if len(args) < 1:
        usage()
        sys.exit(-1)

    cm = None
    # show last timestep by default
    ts = [-1]
    subplot = None
    quiet = False

    for o, a in opts:
        if o == '-c':
            cm = a
        elif o == '-t':
            ts = a.split(',')
            if len(ts) < 1:
                print("invalid timestep specification: {}".format(a))
                sys.exit(-1)
        elif o == '-s':
            subplot = a
        elif o == '-q':
            quiet = True
        elif o == '-h':
            usage()
            sys.exit(0)
        else:
            assert False, "unhandled option"

    for arg in args:
        heatmap(arg, np.array(ts, np.int32), cm, subplot, quiet)

if __name__ == '__main__':
    main()
