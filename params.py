# *-* coding: utf-8 -*-
#
# show-params.py -- Show drobot experiment parametes in human-readable form
#
# Copyright (C) 2013 Tobias Klauser <tklauser@distanz.ch>

import os
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
