# items.py
#    This file contains modules and class definitions to make items for
#    an ordinary bin packing problem.
#    Author: Kristina Spencer
#    Date: March 31, 2016


def main():
    print('This python script contains modules to build bpp items.')
    print('  - makeitems(): makes items from an input file')
    print('  - makeobject(): turn a line in the input file into an item object')
    print('  - Item(): defines the object class Item')


def getiteminfo(items):
    from numpy import zeros
    weights = zeros((len(items), 1))
    heights = zeros((len(items), 1))
    for j in range(len(items)):
        weights[j, 0] = items[j].getweight()
        heights[j, 0] = items[j].getheight()
    info = [weights, heights]
    return info


def makeitems(file):
    # This module is designed to turn a text file into item objects.
    items = []
    j = 0
    infile = open(file, "r")
    for line in infile:
        if not line.strip():
            continue
        else:
            items.append(makeobject(line, j))
            j += 1
    bigc, maxh = items[0].getweight(), items[0].getheight()
    del items[0]
    infile.close()
    return bigc, maxh, items


def makeobject(string, j):
    # string is a tab-separated line: itemweight itemheight
    # returns a corresponding item object
    ci, hi = string.split("\t")
    index = j
    return Item(index, ci, hi)


class Item:
    def __init__(self, index, weight, height):
        self.index = index
        self.weight = int(weight)
        self.height = int(height)

    def getindex(self):
        return self.index

    def getweight(self):
        return self.weight

    def getheight(self):
        return self.height


if __name__ == '__main__':
    main()
