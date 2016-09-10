# constraints.py
#   This python script contains modules to check for constraint violations
#   during and after calculations.

from __future__ import print_function
import binpacking as bp
import items as itemmaker
import numpy as np
from glob import glob
from pandas import read_csv


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
    # Return True if violation exists
    if binweight > w:
        return True
    if binheight > h:
        return True
    return False


def xycheck(m, x, y):
    # This function verifies that the number of open bins in x and y agree
    n = len(y)
    itembins = np.sum(x, axis=1)
    for i in range(n):
        if (itembins[i] > 0 and y[i] == 1) is False:
            if (itembins[i] == 0 and y[i] == 0) is False:
                print('Solution', m, 'has an open bin error: bin', i)


def recheck(n, folder, filename, flag=None):
    # This module allows the user to recheck solutions for constraint
    # violations after calculations have been completed.
    #   - n is the number of items to be sorted
    #   - folder is the main folder where the input file is located
    #   - filename is the input file name
    #   - flag (optional) is the name of the folder where the solution
    #     matrices are stored
    data = folder + filename
    # Reformulate item objects and bin packing problem
    binc, binh, items = itemmaker.makeitems(data)
    bpp = bp.BPP(n, binc, binh, items)
    print('Max bin weight:', binc)
    print('Max bin height:', binh)
    # Go through each solution (x-y pair) to find violations
    xs, ys, solids = getxys(folder + flag, n)
    for m in range(len(xs)):
        concheck(solids[m], xs[m], bpp)
        xycheck(solids[m], xs[m], ys[m])


def getxys(folder, nitems):
    # This function allows the user to double-check for constraint violations
    # after calculations have been completed. It sorts through the x and y text
    # files and returns x and y matrices, which are collected in a list.
    xfiles, yfiles, solids = getsolutions(folder)
    xs = []
    ys = []
    for f in range(len(xfiles)):
        # Import text files into DataFrames
        x = read_csv(xfiles[f], sep=' ', header=None, names=range(nitems), skiprows=1)
        y = read_csv(yfiles[f], sep=' ', header=None, skiprows=1)
        # Translate DataFrames into matrices
        xmatrix = np.zeros((n, n))  # nxn matrix
        ymatrix = np.zeros((n, 1))  # nx1 matrix
        for i in range(n):
            ymatrix[i, 0] = y.get_value(i, 0, takeable=True)
            for j in range(n):
                xmatrix[i, j] = x.get_value(i, j, takeable=True)
        # Add to lists
        xs.append(xmatrix)
        ys.append(ymatrix)
    return xs, ys, solids


def getsolutions(folder):
    # This function automates the process of listing the solution text files.
    # It assumes the x-matrices and y-matrices have been stored separately in
    # txt format with the naming convention: solid_x.txt, solid_y.txt
    # Collect file names into list:
    xfiles = glob(folder + '*_x.txt')
    yfiles = glob(folder + '*_y.txt')
    # Retrieve calculation assigned solution id numbers:
    solids = []
    for f in range(len(xfiles)):
        idstr = xfiles[f][xfiles[f].find(folder) + len(folder):xfiles[f].find('_')]
        solids.append(int(idstr))
    # Sort lists by solution number from smallest to largest:
    xfiles = [x for (solid, x) in sorted(zip(solids, xfiles))]
    yfiles = [y for (solid, y) in sorted(zip(solids, yfiles))]
    solids.sort()
    return xfiles, yfiles, solids


if __name__ == '__main__':
    n = eval(input('How many items should be sorted? \n'))
    filename = input('Please enter the name of your input file: \n')
    folder = input('Please enter the name of the folder containing your input '
                   'file: \n')
    needflag = input('Are your solution files located in another folder from your '
                     'input file? [y/n] \n').lower()
    if needflag.startswith('y'):
        flag = input('Where are your solution files stored? \n')
        recheck(n, folder, filename, flag=flag)
    else:
        recheck(n, folder, filename)