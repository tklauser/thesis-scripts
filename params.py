import os

def import_params(ddir, pfile='params.log'):
    if not os.path.isdir(ddir):
        print("{} is not a directory".format(ddir))
        return None

    p = os.path.join(ddir, pfile)
    if not os.path.isfile(p):
        print("parameter file {} not found".format(p))
        return None

    f = open(p, 'r')
    labels = f.readline().strip().split(',')
    values = f.readline().strip().split(',')
    f.close()

    if len(labels) == 0 or len(values) == 0:
        print("no parameters found in {}".format(p))
        return None

    if len(labels) != len(values):
        print("number of labels doesn't correspond to number of values in {}".format(p))
        return None

    # put parameters into a directory, accessable by parameter name
    return dict(zip(labels, values))
