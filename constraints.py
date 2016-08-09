# constraints.py

from __future__ import print_function
import analyze
import binpacking as bp
import items as itemmaker
import numpy as np


def main():
    n = 500
    folder = '/Users/k9s/Documents/ObjectiveMethod/NSGA-II/Static/SBSBPP500/Experiment01/amaxweight/'
    data = folder + 'SBSBPP500_run1.txt'
    binc, binh, items = itemmaker.makeitems(data)
    bpp = bp.BPP(n, binc, binh, items)
    print('Max bin weight:', binc)
    print('Max bin height:', binh)
    xs, ys = analyze.getxys(folder, n)
    for m in range(len(xs)):
        xmatrix = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                xmatrix[i, j] = xs[m].get_value(i, j, takeable=True)
        concheck(m, xmatrix, bpp)


def concheck(m, x, bpp):
    # This module checks the loading pattern for overall feasibility.
    #  - m is the solution number
    #  - x is the decoded array
    items = bpp.getitems()
    n = len(items)      # n is the number of items to pack
    iteminfo = itemmaker.getiteminfo(items)
    # Constraint 1
    for j in range(n):
        xj = 0
        for i in range(n):
            xj += x[i, j]
        if xj != 1:
            print('Solution', m, 'has a physicality error: item', j)
    # Constraint: max bin weight
    binweights = np.dot(x, iteminfo[0])
    for i in range(n):
        if binweights[i] > bpp.getwbin():   # w is the max. bin weight
            print('Solution', m, ', bin', i, 'is over weight:', binweights[i])
    # Constraint: max bin height
    binheights = np.dot(x, iteminfo[1])
    for i in range(n):
        if binheights[i] > bpp.getub():     # h is the max bin height
            print('Solution', m, ' bin', i, 'is over height.')
    return x


def bincheck(bin, bpp):
    # This function checks to see if an individual bin violates
    # problem constraints.
    # bin should be a list of item indices
    # Note: item indices are j+1 where j is the order in the items list
    w = bpp.getwbin()   # w is the max. bin weight
    h = bpp.getub()     # h is the max. bin height
    items = bpp.getitems()
    binweight = 0
    binheight = 0
    for j in bin:
        binweight += items[j-1].getweight()
        binheight += items[j-1].getheight()
    if binweight > w:
        return True
    if binheight > h:
        return True
    return False


if __name__ == '__main__':
    main()