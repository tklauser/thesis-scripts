# *-* coding: utf-8 -*-
#
# utils.py -- Usefult functions for other scripts
#
# Copyright (C) 2013 Tobias Klauser <tklauser@distanz.ch>

import os
import fnmatch
import re
import numpy as np
import matplotlib.pyplot as plt
from collections import OrderedDict

def import_params(ddir, pfile='params.log', verbose=True):
    if not os.path.isdir(ddir):
        if verbose:
            print("{} is not a directory".format(ddir))
        return None

    p = os.path.join(ddir, pfile)
    if not os.path.isfile(p):
        if verbose:
            print("parameter file {} not found".format(p))
        return None

    f = open(p, 'r')
    labels = f.readline().strip().split(',')
    values = f.readline().strip().split(',')
    f.close()

    if len(labels) == 0 or len(values) == 0:
        if verbose:
            print("no parameters found in {}".format(p))
        return None

    if len(labels) != len(values):
        if verbose:
            print("number of labels doesn't correspond to number of values in {}".format(p))
        return None

    # put parameters into a directory, accessable by parameter name
    return OrderedDict(zip(labels, values))

def get_weights(ddir, nInputs, nOutputs, verbose=True):
    files = os.listdir(ddir)
    xfiles = fnmatch.filter(files, 'weights_x_in*.log')
    yfiles = fnmatch.filter(files, 'weights_y_in*.log')
    nx = len(xfiles)
    ny = len(yfiles)

    if nx == 0 or ny == 0 or nx != ny or nx != nInputs:
        if verbose:
            print("""not enough weight files in your data directory,
                     should be {} (nInputs), but only {}/{} (x/y) found""".format(nInputs, nx, ny))
        return

    # determine size of files for array preallocation
    sx = np.genfromtxt(os.path.join(ddir, xfiles[0]), delimiter=',').shape
    sy = np.genfromtxt(os.path.join(ddir, yfiles[0]), delimiter=',').shape

    # the first column is time
    if sx[1] - 1 != sy[1] - 1 != nOutputs:
        if verbose:
            print("""invalid number of outputs in weight files""")
        return

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

    return Wx, Wy

def save_weights_all(ddir, Wx, Wy, fmt='%1.12f', delim=',', verbose=True):
    np.savetxt(os.path.join(ddir, "weights_all_x.log"), Wx, fmt=fmt, delimiter=delim)
    if verbose:
        print("Weight file for x-axis written to {}".format(os.path.join(ddir, 'weights_all_x.log')))
    np.savetxt(os.path.join(ddir, "weights_all_y.log"), Wy, fmt=fmt, delimiter=delim)
    if verbose:
        print("Weight file for y-axis written to {}".format(os.path.join(ddir, 'weights_all_x.log')))

def get_cmap(cmap, default='gray_r'):
    try:
        cm = plt.get_cmap(cmap)
    except ValueError as e:
        cm = plt.get_cmap(default)

    return cm
