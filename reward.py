#!/usr/bin/env python
# -*- coding: utf-8 -*-

import getopt
import os, sys
import numpy as np
import matplotlib.pyplot as plt
from params import import_params

def usage():
    print("""usage: {} [OPTION...] DIRECTORY...

Show development of reward and cummulative reward.

options:

  -T          show experiment path in figure title
  -q          quiet mode, don't show plot, only write PDF
  -h          show this help and exit
""".format(os.path.basename(sys.argv[0])))

def reward(ddir, quiet, show_title):
    rewards = np.genfromtxt(os.path.join(ddir, 'reward.log'), delimiter=',')

    time = rewards[:,0]
    T = len(time)
    rewards = rewards[:,1:]

    r = np.zeros(T)

    fig = plt.figure()

    for t in range(T):
        r[t] = rewards[0:t,:].sum(axis=0)

    t = range(len(time))

    plt.plot(t, r)

    if show_title:
        fig.suptitle(ddir)
    plt.savefig(os.path.join(ddir, 'reward.pdf'), dpi=300, bbox_inches='tight', pad_inches=0.15)
    if not quiet:
        plt.show()

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "Tqh")
    except getopt.GetoptError, err:
        print(str(err))
        usage()
        sys.exit(-1)

    if len(args) < 1:
        usage()
        sys.exit(-1)

    show_title = False
    quiet = False

    for o, a in opts:
        if o == '-T':
            show_title = True
        elif o == '-q':
            quiet = True
        elif o == '-h':
            usage()
            sys.exit(0)
        else:
            assert False, "unhandled option"

    for arg in args:
        reward(arg, quiet, show_title)

if __name__ == '__main__':
    main()
