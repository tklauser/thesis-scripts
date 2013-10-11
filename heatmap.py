#!/usr/bin/env python
# -*- coding: utf-8 -*-

import getopt
import os, sys
import numpy as np
import matplotlib.pyplot as plt
from utils import import_params, get_cmap

def usage():
    print("""usage: {} [OPTION...] DIRECTORY...

Show heat map plot of the number of times an input field has been activated

By default the plot is shown for the first and last time step.

options:

  -C CMAP     use CMAP as colormap, see help(colormaps) in matplotlib for a list
  -t TIME...  comma-separated list (without space) of timestamps, negative
              numbers are intepreted as counting from the end (as in python)
  -s SUBPLOT  specify subplot layout (in matplotlib style, e.g. 23 for 2 rows/3 columns)
  -T          show experiment path in figure title
  -q          quiet mode, don't show plot, only write PDF
  -h          show this help and exit
""".format(os.path.basename(sys.argv[0])))

def heatmap(ddir, ts, subplot, quiet, show_title, cmap=None):
    params = import_params(ddir)

    try:
        nRows = int(params['nRowsIn'])
        nCols = int(params['nColsIn'])
    except KeyError, err:
        print('necessary parameter not found: ' + str(err))
        sys.exit(-1)

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

        if subplot is None:
            s = '1' + str(len(ts)) + str(i + 1)
        else:
            s = subplot + str(i + 1)

        ax = fig.add_subplot(int(s))

        p = ax.pcolormesh(x, y, incount, cmap=cmap, rasterized=True)

        cb = fig.colorbar(p, ax=ax, shrink=0.8, pad=0.1, aspect=10)
        cb.ax.tick_params(labelsize=8)
        cb.solids.set_edgecolor('face')
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

    if show_title:
        fig.suptitle(ddir)
    plt.savefig(os.path.join(ddir, 'heatmap.pdf'), dpi=300, bbox_inches='tight', pad_inches=0.15)
    if not quiet:
        plt.show()

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "C:t:s:Tqh")
    except getopt.GetoptError, err:
        print(str(err))
        usage()
        sys.exit(-1)

    if len(args) < 1:
        usage()
        sys.exit(-1)

    # show last timestep by default
    ts = [-1]

    cmap = None
    subplot = None
    show_title = False
    quiet = False

    for o, a in opts:
        if o == '-C':
            cmap = a
        elif o == '-t':
            ts = a.split(',')
            if len(ts) < 1:
                print("invalid timestep specification: {}".format(a))
                sys.exit(-1)
        elif o == '-s':
            subplot = a
        elif o == '-T':
            show_title = True
        elif o == '-q':
            quiet = True
        elif o == '-h':
            usage()
            sys.exit(0)
        else:
            assert False, "unhandled option"

    cmap = get_cmap(cmap)

    for arg in args:
        heatmap(arg, np.array(ts, np.int32), subplot, quiet, show_title, cmap=cmap)

if __name__ == '__main__':
    main()
