#!/usr/bin/env python
# -*- coding: utf-8 -*-

import getopt
import os, sys
import fnmatch
import re
import numpy as np
import matplotlib.pyplot as plt
from utils import import_params, get_weights, get_cmap

def usage():
    print("""usage: {} [OPTION...] DIRECTORY...

Show quiver plot of the development of weights over time.

By default the plot is shown for the first and last time step.

options:

  -c          enable continuous mode (time and subplot options are ignored)
  -C CMAP     use CMAP as colormap in continuous mode, see help(colormaps) in
              matplotlib for a list
  -t TIME...  comma-separated list (without space) of timestamps, negative
              numbers are intepreted as counting from the end (as in python)
  -s SUBPLOT  specify subplot layout (e.g. 23 for 2 rows and 3 columns)
  -S STEP     specify time step to use in continous mode
  -T          show experiment path in figure title
  -q          quiet mode, don't show plot, only write PDF
  -w          use winner-take-all instead of weighted sum to calculate
              resulting output
  -h          show this help and exit
""".format(os.path.basename(sys.argv[0])))

def force_fields(ddir, ts, wta, continuous, csteps, subplot, quiet, show_title, cmap):
    params = import_params(ddir)

    try:
        nRows = int(params['nRowsIn'])
        nCols = int(params['nColsIn'])
        nOutputs = int(params['nOutputs'])
        popMinX = float(params['popMinX'])
        popMaxX = float(params['popMaxX'])
        popMinY = float(params['popMinY'])
        popMaxY = float(params['popMaxY'])
    except KeyError, err:
        print('necessary parameter not found: ' + str(err))
        sys.exit(-1)

    nInputs = nRows * nCols

    Wx, Wy = get_weights(ddir, nInputs, nOutputs)
    if Wx is None or Wy is None:
        print("failed to read weights")
        return

    intervalX = (popMaxX - popMinX) / (nOutputs - 1)
    intervalY = (popMaxY - popMinY) / (nOutputs - 1)
    oMovementX = np.arange(popMinX, popMaxX + 1, intervalX)
    oMovementY = np.arange(popMinY, popMaxY + 1, intervalY)

    time = Wx[:,0,0]
    T = len(time)
    [x, y] = np.meshgrid(np.arange(1, nRows + 1), np.arange(1, nCols + 1))

    if continuous:
        ts = range(0, T + 1, csteps)

    fig = plt.figure()

    for i, t in enumerate(ts):
        # use negative indices as in python
        if t < 0:
            t = T + t

        if t >= T:
            t = T - 1
        elif t < 0:
            t = 0

        dx = np.zeros([nInputs, 1])
        dy = np.zeros([nInputs, 1])

        for n in range(nInputs):
            wxt = Wx[t,1:,n]
            wyt = Wy[t,1:,n]

            if not wta:
                oTotalX = wxt.sum()
                oTotalY = wyt.sum()

                dx[n] = np.dot(wxt, oMovementX) / oTotalX
                dy[n] = np.dot(wyt, oMovementY) / oTotalY
            else:
                amx = np.argmax(wxt)
                amy = np.argmax(wyt)

                dx[n] = oMovementX[amx]
                dy[n] = oMovementY[amy]

        # convert to matrix
        dx = dx.reshape(nRows, nCols)
        dy = dy.reshape(nRows, nCols)
        # flip up to down since 0,0 is the input neuron for the upper left
        # corner. Invert x since positive value means movement to the left.
        dx = np.flipud(dx) * (-1.0)
        dy = np.flipud(dy)

        if not continuous:
            if subplot is None:
                s = '1' + str(len(ts)) + str(i + 1)
            else:
                s = subplot + str(i + 1)
        else:
            s = '111'

        ax = fig.add_subplot(int(s))

        c = np.ones((nRows,nCols)) * i

        if not continuous:
            Q = ax.quiver(x, y, dx, dy, units='width', width=0.0035, color='b', edgecolors=('b'))
        else:
            Q = ax.quiver(x, y, dx, dy, units='width', width=0.0035, color=cmap(float(csteps * i) / T))

        ax.axis([0.5, nCols + 0.5, 0.5, nRows + 0.5])
        ax.set_xticks(np.arange(1, nCols + 1, 2))
        ax.set_xticklabels(np.arange(0, nCols, 2), fontsize=8)
        ax.set_yticks(np.arange(1, nRows + 1, 2))
        ax.set_yticklabels(np.arange(0, nRows, 2), fontsize=8)
        ax.set_aspect('equal', 'box')
        ax.set_title("time step {}".format(t), fontsize=12)

    if show_title:
        fig.suptitle(ddir)
    plt.tight_layout()
    plt.subplots_adjust(left=0.125, bottom=0.1, right=0.7, top=0.9,
                            wspace=0.2, hspace=0.3)

    plt.savefig(os.path.join(ddir, 'force_field.pdf'), dpi=300, bbox_inches='tight', pad_inches=0.15)
    if not quiet:
        plt.show()

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "cC:hs:S:t:Tqw")
    except getopt.GetoptError, err:
        print(str(err))
        usage()
        sys.exit(-1)

    if len(args) < 1:
        usage()
        sys.exit(-1)

    # show first and last timestep by default
    ts = [0, -1]

    cmap = None
    continuous = False
    csteps = 10
    subplot = None
    show_title = False
    quiet = False
    wta = False

    for o, a in opts:
        if o == '-c':
            continuous = True
        elif o == '-C':
            cmap = a
        elif o == '-h':
            usage()
            sys.exit(0)
        elif o == '-s':
            subplot = a
        elif o == '-S':
            csteps = int(a)
        elif o == '-t':
            ts = a.split(',')
            if len(ts) < 1:
                print("invalid timestep specification: {}".format(a))
                sys.exit(-1)
        elif o == '-T':
            show_title = True
        elif o == '-q':
            quiet = True
        elif o == '-w':
            wta = True
        else:
            assert False, "unhandled option"

    cmap = get_cmap(cmap, default='Blues')

    for ddir in args:
        force_fields(ddir, np.array(ts, np.int32), wta, continuous, csteps, subplot, quiet, show_title, cmap=cmap)

if __name__ == '__main__':
    main()
