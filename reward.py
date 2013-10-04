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

  -c          show histogram with count of positive and negative rewards
  -T          show experiment path in figure title
  -q          quiet mode, don't show plot, only write PDF
  -h          show this help and exit
""".format(os.path.basename(sys.argv[0])))

def reward(ddir, do_count, quiet, show_title):
    rewards = np.genfromtxt(os.path.join(ddir, 'reward.log'), delimiter=',')

    time = rewards[:,0]
    rewards = rewards[:,1:]
    T,N = rewards.shape

    print("N: {}, T: {}".format(N, T))

    t = range(T)
    r = np.zeros((T,N))

    fig = plt.figure()

    for _t in t:
        for n in range(N):
            r[_t,n] = rewards[0:_t,n].sum(axis=0)

    if do_count:
        s = '1' + str(1 + N)
    else:
        s = '11'

    ax1 = fig.add_subplot(int(s + '1'))
    p = plt.plot(t, r)
    plt.legend(p, [ "reward #{}".format(n) for n in range(N) ], loc=2)

    if do_count:
        for n in range(N):
            ax = fig.add_subplot(int(s + str(n)))
            plt.hist(rewards[:,n], bins=2)

    if show_title:
        fig.suptitle(ddir)
    plt.savefig(os.path.join(ddir, 'reward.pdf'), dpi=300, bbox_inches='tight', pad_inches=0.15)
    if not quiet:
        plt.show()

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "cTqh")
    except getopt.GetoptError, err:
        print(str(err))
        usage()
        sys.exit(-1)

    if len(args) < 1:
        usage()
        sys.exit(-1)

    do_count = False
    show_title = False
    quiet = False

    for o, a in opts:
        if o == '-c':
            do_count = True
        elif o == '-T':
            show_title = True
        elif o == '-q':
            quiet = True
        elif o == '-h':
            usage()
            sys.exit(0)
        else:
            assert False, "unhandled option"

    for arg in args:
        reward(arg, do_count, quiet, show_title)

if __name__ == '__main__':
    main()
