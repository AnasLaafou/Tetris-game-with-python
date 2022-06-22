""" helper module """

class vec(tuple):

    def __new__(cls, x, y):
        return tuple.__new__(cls, (x, y))

    def __add__(self, other):
        return vec(self[0]+other[0], self[1]+other[1])

    def __sub__(self, other):
        return vec(self[0]-other[0], self[1]-other[1])

    def __rmul__(self, other):
        if isinstance(other, (int, float)):
        	return vec(other*self[0], other*self[1])
        elif isinstance(other, vec):
        	return vec(self[0]*other[0], self[1]*other[1])

    def __lt__(self, other):
        return self[0] < other[0] and self[1] < other[1]

    def __gt__(self, other):
        return self[0] > other[0] and self[1] > other[1]
