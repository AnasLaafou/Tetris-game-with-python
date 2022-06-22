import sys
import _matrix
import tools
import linear_sys

class Matrix():

	def __init__(self, Data, shape = None):
		self.data_converted_to_matrix = False
		if Data is None:
			self.body = None
			self.shape = None
			return
		self.shape = None
		if not shape:
			List = []
			a = True
			if type(Data) == list:
				if type(Data[0]) == list:
					List.append(Data[0])
					for i in range(1, len(Data)):
						if type(Data[i]) == list and len(Data[i]) == len(Data[0]):
							List.append(Data[i])
						else:
							a = False
			if a:
				self.body = List
			else:
				self.body = None
		else:
			n, m = shape
			L2 = []
			try :
				L = list(Data)
			except :
				self.body = None, type(Data)
			else:
				for i in range(n):
					Ll = []
					for j in range(m):
						Ll.append(L[(m*i)+j])
					L2.append(Ll)
				self.body = L2
		if self.body == None:
			print("Data = ", Data, " could not be converted to a Matrix object", sep = "'", file = sys.stderr)
		elif type(self.body) == tuple:
			print("Data = ", Data, " of type ", self.body[1], " could not be converted to a Matrix object", sep = "", file = sys.stderr)
		else :
			self.data_converted_to_matrix = True
			self.shape = (len(self.body), len(self.body[0]))

	def getattrs(self):
		return list(self.__dict__.keys())

	def addattr(self, name, value):
		self.__dict__[name] = value

	def item(self, i, j):
		try : it = self.body[i][j]
		except : it = None
		finally : return it

	def __str__(self):
		return str(self.body)

	def __neg__(self):
		return self.__mul__(-1)

	def __add__(self, other):
		if isinstance(other, Matrix):
			return Matrix(_matrix.sum(self.body, other.body))

	def __sub__(self, other):
		if isinstance(other, Matrix):
			nother = other.__neg__()
			return Matrix(_matrix.sum(self.body, nother.body))

	def __matmul__(self, other):
		if isinstance(other, Matrix):
			return Matrix(_matrix.mul(self.body, other.body))

	def __mul__(self, scalar):
		if isinstance(scalar, (int, float)):
			O = _matrix.null(len(self.body), len(self.body[0]))
			for i in range(len(self.body)):
				for j in range(len(self.body[0])):
					O[i][j] = self.body[i][j] * scalar
			return Matrix(O)

	def __pow__(self, n):
		if isinstance(n, int):
			return Matrix(_matrix.pow(self.body, n))
	
	def __eq__(self, other):
		if isinstance(other, Matrix):
			return self.body == other.body

	def index(self, item):
		if self.__contains__(item):
			ind = self.inds
			delattr(self, "inds")
			return ind
		print(f"{item} not found in this matrix")

	def __contains__(self, item):
		for lis in self.body:
			if item in lis:
				ind0, ind1 = self.body.index(lis), lis.index(item)
				self.addattr("inds", (ind0, ind1))
				return True
		return False

	def concatenate(self, other):
		if isinstance(other, Matrix):
			return Matrix(_matrix.concatenate(self.body, other.body))

	def disconcat(self, start_column):
		if start_column in range(self.shape[1]):
			return Matrix(_matrix.disconcatenate(self.body, start_column))

	def to_upper_triangular(self):
		u_tri = _matrix.to_upper_triangular(self.body)
		return Matrix(u_tri)

	def isSquare(self):
		return self.shape[0] == self.shape[1]

	def transpose(self):
		self.body = _matrix.transpose(self.body)

	def det(self):
		return _matrix.determinant(self.body)

	def rank(self):
		return _matrix.rank(self.body)

	def trace(self):
		return _matrix.trace(self.body)

	def __invert__(self):
		d = self.det()
		if d == None: 
			return
		elif d != 0:
			n = self.shape[0]
			Bc = []
			for i in range(n):
				e = [[delta(i, j)] for j in range(n)]
				Bc.append(Matrix(e))
			mat = []
			for k in range(n):
				M = Matrix(self.body)
				vec = linear_sys.solve_sys_lin(M, Bc[k])
				tools.vec_to_list(vec)
				mat.append(vec)
			_matrix.transpose(mat)
			return Matrix(mat)

def delta(i, j):
    if i == j:
        return 1
    else:
        return 0

def Diag(*args):
    M = [[0 for j in range(len(args))] for i in range(len(args))]
    for k in range(len(args)):
        M[k][k] = args[k]
    return Matrix(M)