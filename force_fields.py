#!/usr/bin/env python
# -*- coding: utf-8 -*-

import getopt
import os, sys
import fnmatch
import re
import numpy as np
import matplotlib.pyplot as plt

def usage():
    print("""usage: {} [OPTION...] DIRECTORY

Show quiver plot of the development of weights over time.

By default the plot is shown for the first and last time step.

options:

  -t TIME...  comma-separated list (without space) of timestamps, negative
              numbers are intepreted as counting from the end (as in python)
  -h          show this help and exit
""".format(os.path.basename(sys.argv[0])))

def force_fields(ddir, ts):
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

    if not ('nRowsIn' in params and 'nColsIn' in params and 'nOutputs' in params
            and 'popMinX' in params and 'popMaxX' in params
            and 'popMinY' in params and 'popMaxY' in params):
        print("not all necessary parameters available in the parameter file")
        return

    nRows = int(params['nRowsIn'])
    nCols = int(params['nColsIn'])
    nInputs = nRows * nCols
    nOutputs = int(params['nOutputs'])
    popMinX = float(params['popMinX'])
    popMaxX = float(params['popMaxX'])
    popMinY = float(params['popMinY'])
    popMaxY = float(params['popMaxY'])

    files = os.listdir(ddir)
    xfiles = fnmatch.filter(files, 'weights_x_in*.log')
    yfiles = fnmatch.filter(files, 'weights_y_in*.log')
    nx = len(xfiles)
    ny = len(yfiles)

    if nx == 0 or ny == 0 or nx != ny or nx != nInputs:
        print("""not enough weight files in your data directory,
                 should be {} (nInputs), but only {}/{} (x/y) found""".format(nInputs, nx, ny))
        return

    # determine size of files for array preallocation
    sx = np.genfromtxt(os.path.join(ddir, xfiles[0]), delimiter=',').shape
    sy = np.genfromtxt(os.path.join(ddir, yfiles[0]), delimiter=',').shape

    # TODO: plausibility checks on sx, sy wrt nOutputs

    Wx = np.zeros([sx[0], nOutputs + 1, nx])
    Wy = np.zeros([sy[0], nOutputs + 1, ny])

    # files don't necessarily get listed in numerically correct order, thus
    # extract index number from the file name
    pattern = re.compile('weights_x_in_(\d+).*\.log')
    for i in range(nx):
        n = int(pattern.match(xfiles[i]).group(1))
        Wx[:,:, n] = np.genfromtxt(os.path.join(ddir, xfiles[i]), delimiter=',')

    pattern = re.compile('weights_y_in_(\d+).*\.log')
    for i in range(ny):
        n = int(pattern.match(yfiles[i]).group(1))
        Wy[:,:, n] = np.genfromtxt(os.path.join(ddir, yfiles[i]), delimiter=',')

    intervalX = (popMaxX - popMinX) / (nOutputs - 1)
    intervalY = (popMaxY - popMinY) / (nOutputs - 1)
    oMovementX = np.arange(popMinX, popMaxX + 1, intervalX)
    oMovementY = np.arange(popMinY, popMaxY + 1, intervalY)

    time = Wx[:,0,0]
    T = len(time)

    for t in ts:
        # use negative indices as in python
        if t < 0:
            t = T + t 

        if t >= T:
            t = T - 1
        elif t < 0:
            t = 0

        plt.figure()

        dx = np.zeros([nx, 1])
        dy = np.zeros([ny, 1])

        for i in range(nx):
            wxt = Wx[t,1:,i]
            wyt = Wy[t,1:,i]

            oTotalX = wxt.sum()
            oTotalY = wyt.sum()

            dx[i] = np.dot(wxt, oMovementX) / oTotalX
            dy[i] = np.dot(wyt, oMovementY) / oTotalY

        # convert to matrix
        dx = dx.reshape(nRows, nCols)
        dy = dy.reshape(nRows, nCols)
        # flip up to down since 0,0 is the input neuron for the upper left
        # corner. Invert x since positive value means movement to the left.
        dx = np.flipud(dx) * (-1.0)
        dy = np.flipud(dy)

        [x, y] = np.meshgrid(np.arange(1, nRows + 1), np.arange(1, nCols + 1))
        Q = plt.quiver(x, y, dx, dy, units='width', width=0.005, color='b')
        plt.axis([0, nCols + 1, 0, nRows + 1])
        plt.axes().set_aspect('equal', 'box')
        plt.title("step {} (t={})".format(t, time[t]))

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

    # show first and last timestep by default
    ts = [0, -1]

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

    force_fields(args[0], np.array(ts, np.int32))

if __name__ == '__main__':
    main()
