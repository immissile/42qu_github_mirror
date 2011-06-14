cdef extern from "math.h":
    double log10(double)
    double sqrt(double)

cpdef double hot(long ups, long downs, double date):
    """The hot formula"""
    s = ups - downs
    order = log10(max(abs(s), 1))
    if s > 0:
        sign = 1
    elif s < 0:
        sign = -1
    else:
        sign = 0
    seconds = date - 1293811200
    return round(order + sign * seconds / 45000, 7)

cpdef double controversy(long ups, long downs):
    """The controversy sort."""
    return float(ups + downs) / max(abs(ups - downs), 1)

cpdef double _confidence(int ups, int downs):
    """The confidence sort.
       http://www.evanmiller.org/how-not-to-sort-by-average-rating.html"""
    cdef float n = ups + downs

    if n == 0:
        return 0

    cdef float z = 1.281551565545 # 80% confidence
    cdef float p = float(ups) / n

    left = p + 1/(2*n)*z*z
    right = z*sqrt(p*(1-p)/n + z*z/(4*n*n))
    under = 1 + 1/n*z*z

    return (left - right) / under

cdef int up_range = 400
cdef int down_range = 100
cdef list _confidences = []
for ups in xrange(up_range):
    for downs in xrange(down_range):
        _confidences.append(_confidence(ups, downs))
def confidence(int ups, int downs):
    if ups + downs == 0:
        return 0
    elif ups < up_range and downs < down_range:
        return _confidences[downs + ups * down_range]
    else:
        return _confidence(ups, downs)
