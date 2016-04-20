#!/usr/bin/env python
# -*- coding: utf-8 -*-

import getopt
import os, sys
import fnmatch
import re
import numpy as np
import matplotlib.pyplot as plt
from utils import import_params, get_cmap

def usage():
    print("""usage: {} [OPTION...] DIRECTORY...

Show plot of development of network output.

  -C CMAP     use CMAP as colormap in continuous mode, see help(colormaps) in
              matplotlib for a list
  -q          quiet mode, don't show plot, only write PDF
  -h          show this help and exit
""".format(os.path.basename(sys.argv[0])))

def plot_output(ddir, quiet, cmap):
    params = import_params(ddir)

    try:
        nRows = int(params['nRowsIn'])
        nCols = int(params['nColsIn'])
        nOutputs = int(params['nOutputs'])
    except KeyError, err:
        print('necessary parameter not found: ' + str(err))
        sys.exit(-1)

    nInputs = nRows * nCols

    # XXX: get this from the files themselves
    T = 5

    outputs = np.zeros([T, nOutputs, nInputs])

    fig, axes = plt.subplots(1, nInputs, sharex=True, sharey=True)

    for i in range(nInputs):
        tmp = np.genfromtxt(os.path.join(ddir, "out_x_in_{}.log".format(i)), delimiter=',')
        outputs[:,:,i] = tmp[:,1:]

    for i in range(nInputs):
        for t in range(T):
            ax = axes[i]
            ax.set_title("input {}".format(i))
            ax.plot(outputs[t,:,i], color=cmap(float(0.2 + t) / T))
            ax.set_xlim(0.0, float(nOutputs - 1))
            ax.set_ylim(-1.5, 1.5)
            ax.set_aspect(5, 'box-forced')

    plt.show()

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "C:hq")
    except getopt.GetoptError, err:
        print(str(err))
        usage()
        sys.exit(-1)

    if len(args) < 1:
        usage()
        sys.exit(-1)

    cmap = None
    quiet = False

    for o, a in opts:
        if o == '-C':
            cmap = a
        elif o == '-h':
            usage()
            sys.exit(0)
        elif o == '-q':
            quiet = True
        else:
            assert False, "unhandled option"

    cmap = get_cmap(cmap, default='Blues')

    for ddir in args:
        plot_output(ddir, quiet, cmap=cmap)

if __name__ == '__main__':
    main()
