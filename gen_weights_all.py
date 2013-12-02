#!/usr/bin/env python
# -*- coding: utf-8 -*-

import getopt
import os, sys
import numpy as np
from utils import import_params, get_weights, save_weights_all

def usage():
    print("""usage: {} [OPTION...] DIRECTORY...

Generate weights_x_all.log and weights_y_all.log from the weight per input files.

options:

  -h          show this help and exit
""".format(os.path.basename(sys.argv[0])))

def gen_weights_all(ddir):
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
    # take most recent values, strip time and transpose so we can write column wise (like eigen)
    Wx, Wy = Wx[-1,1:,:].T, Wy[-1,1:,:].T
    # use final value and reshape to row vector
    Wx, Wy = np.squeeze(Wx[-1,1:,:].reshape(1,-1)), np.squeeze(Wy.reshape(1,-1))
    save_weights_all(ddir, Wx, Wy)
    print("Weight files written to {}".format(ddir))

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h")
    except getopt.GetoptError, err:
        print(str(err))
        usage()
        sys.exit(-1)

    if len(args) < 1:
        usage()
        sys.exit(-1)

    for o, a in opts:
        if o == '-h':
            usage()
            sys.exit(0)
        else:
            assert False, "unhandled option"

    for ddir in args:
        gen_weights_all(ddir)

if __name__ == '__main__':
    main()
