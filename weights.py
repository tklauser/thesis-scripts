#!/usr/bin/env python
# -*- coding: utf-8 -*-

import getopt
import os, sys
import numpy as np
import matplotlib.pyplot as plt
from utils import import_params, get_weights, get_cmap

def usage():
    print("""usage: {} [OPTION...] DIRECTORY...

By default the plot is shown for the first and last time step.

options:

  -c CMAP     use CMAP als colormap, see help(colormaps) in matplotlib for a list
  -t TIME...  comma-separated list (without space) of timestamps, negative
              numbers are intepreted as counting from the end (as in python)
  -T          show experiment path in figure title
  -q          quiet mode, don't show plot, only write PDF
  -h          show this help and exit
""".format(os.path.basename(sys.argv[0])))

def plot_one(t, x, y, W, nInputs, nOutputs, fig, s, cmap):
    ax = fig.add_subplot(int(s))
    ax.set_xlabel('inputs', fontsize=8)
    ax.set_ylabel('outputs', fontsize=8)

    p = ax.pcolormesh(x, y, W[t,:,:], cmap=cmap, rasterized=True)

    cb = fig.colorbar(p, ax=ax, shrink=0.9, pad=0.1, aspect=10)
    cb.ax.tick_params(labelsize=8)
    cb.solids.set_edgecolor('face')

    ax.set_aspect('equal', 'box')
    ax.set_xticks(np.arange(0.5, nInputs + 0.5, 5))
    ax.set_xticklabels(np.arange(0, nInputs + 1, 5), fontsize=8)
    ax.tick_params(axis='x', which='both', bottom='off', top='off', labelbottom='on')
    ax.set_yticks(np.arange(0.5, nOutputs + 0.5, 2))
    ax.set_yticklabels(np.arange(0, nOutputs + 1, 2), fontsize=8)
    ax.tick_params(axis='y', which='both', left='off', right='off', labelleft='on')
    ax.set_xlim(0, nInputs)
    ax.set_ylim(0, nOutputs)
    ax.set_title("time step {}".format(t), fontsize=12)

def weights(ddir, ts, quiet, show_title, cmap):
    params = import_params(ddir)

    try:
        nRows = int(params['nRowsIn'])
        nCols = int(params['nColsIn'])
        nOutputs = int(params['nOutputs'])
    except KeyError, err:
        print('necessary parameter not found: ' + str(err))
        sys.exit(-1)

    nInputs = nRows * nCols

    Wx, Wy = get_weights(ddir, nInputs, nOutputs)
    if Wx is None or Wy is None:
        print("failed to read weights")
        return

    time = Wx[:,0,0]
    T = len(time)
    # omit time 
    Wx = Wx[:,1:,:]
    Wy = Wy[:,1:,:]

    [x, y] = np.meshgrid(np.arange(0, nInputs + 1), np.arange(0, nOutputs + 1))

    figx = plt.figure()
    figy = plt.figure()

    N = len(ts)

    for i, t in enumerate(ts):
        # use negative indices as in python
        if t < 0:
            t = T + t

        if t >= T:
            t = T - 1
        elif t < 0:
            t = 0

        s = str(N) + '1' + str(i + 1)
        plot_one(t, x, y, Wx, nInputs, nOutputs, figx, s, cmap)
        plot_one(t, x, y, Wy, nInputs, nOutputs, figy, s, cmap)

    if not quiet:
        plt.show()

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "c:t:Tqh")
    except getopt.GetoptError, err:
        print(str(err))
        usage()
        sys.exit(-1)

    if len(args) < 1:
        usage()
        sys.exit(-1)

    cmap = None
    # show last timestep by default
    ts = [-1]
    show_title = False
    quiet = False

    for o, a in opts:
        if o == '-c':
            cmap = a
        elif o == '-t':
            ts = a.split(',')
            if len(ts) < 1:
                print("invalid timestep specification: {}".format(a))
                sys.exit(-1)
        elif o == '-T':
            show_title = True
        elif o == '-q':
            quiet = True
        elif o == '-h':
            usage()
            sys.exit(0)
        else:
            assert False, "unhandled option"

    for ddir in args:
        weights(ddir, np.array(ts, np.int32), quiet, show_title, get_cmap(cmap))

if __name__ == '__main__':
    main()
