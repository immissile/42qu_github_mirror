


#import pprint
#pprint.pprint(list(chunks(range(75), 10)))
#
#[[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
# [10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
# [20, 21, 22, 23, 24, 25, 26, 27, 28, 29],
# [30, 31, 32, 33, 34, 35, 36, 37, 38, 39],
# [40, 41, 42, 43, 44, 45, 46, 47, 48, 49],
# [50, 51, 52, 53, 54, 55, 56, 57, 58, 59],
# [60, 61, 62, 63, 64, 65, 66, 67, 68, 69],
# [70, 71, 72, 73, 74]]

def chunkiter(l, n):
    """ Yielistd successive n-sized chunks from list.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]


def lineiter(l):
    result = []
    for i in l:
        result.extend(i)
    return result

if "__main__" == __name__:
    pass
