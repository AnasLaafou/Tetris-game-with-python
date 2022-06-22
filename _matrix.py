import tools

def sum(M, N): # this function return the result of the sum of two matrices M and N
    dim_M, dim_N = (len(M), len(M[0])), (len(N), len(N[0]))
    if dim_M != dim_N:# cannot sum M and N
    	return
    n, m = dim_M
    P = []
    P = [[0 for j in range(m)] for i in range(n)]
    for i in range(n):
        for j in range(m):
            P[i][j] = M[i][j]+N[i][j]
    return P

def mul(M, N): # this function returns the result of the multiplication of the matrix M by the matrix N
	dim_M, dim_N = (len(M), len(M[0])), (len(N), len(N[0]))
	if dim_M[1] != dim_N[0]:# cannot multiply M by N
		return
	n, l = dim_M
	m = dim_N[1]
	P = []
	P = [[0 for j in range(m)] for i in range(n)]
	for i in range(n):
		for j in range(m):
			for k in range(l):
				P[i][j] += M[i][k]*N[k][j]
	return P

def transpose(A): #returns the transposed matrix of A
    if A == []:return A
    if not hasattr(A[0], "__len__"):return A #A is a line vector
    cols = []
    for i in range(len(A[0])):
        cols += tools.column(A, i)
    return cols

def transpose_sq(A): #returns the transposed matrix of A
    n, m = len(A), len(A[0])
    for i in range(n):
        for j in range(i, m):
            A[i][j], A[j][i] = A[j][i], A[i][j]

def rank(A): #calculates the rank of the square matrix A
    n, m = len(A), len(A[0])
    if n != m:
    	return
    if n == 0 or isNull(A):
        return 0
    else:
        B = Transform(A)
        A1 = extract(B)
        return 1 + rank(A1)


def isNull(A): #tests if a square matrix A is null
    n = len(A)
    for i in range(n):
        for j in range(n):
            if A[i][j] != 0:
                return False
    return True


def isNull_v2(A): #tests if a square matrix A is null
    n = len(A)
    O = [[0 for i in range(n)] for j in range(n)]
    return A == O


def isNull_v3(A): #tests if a matrix A is null
    n, m = len(A), len(A[0])
    O = [[0 for i in range(m)] for j in range(n)]
    return A == O


def extract(A):#extracts a submatrix from a square matrix A
    n = len(A)
    A1 = [[0 for i in range(n-1)] for j in range(n-1)]
    for i in range(n-1):
        for j in range(n-1):
            A1[i][j] = A[i+1][j+1]
    return A1

def extract_v2(A, i0, j0):#extracts a submatrix from a matrix A
    n = len(A)
    A1 = [[0 for i in range(n-1)] for j in range(n-1)]
    for i in range(n-1):
        for j in range(n-1):
            if i < i0 and j < j0 :
                A1[i][j] = A[i][j]
            elif j < j0:
                A1[i][j] = A[i+1][j]
            elif i < i0:
                A1[i][j] = A[i][j+1]
            else :
                A1[i][j] = A[i+1][j+1]
    return A1

def extract_v3(A): #extracts a submatrix from a matrix A
    n, m = len(A), len(A[0])
    A1 = [[0 for i in range(m-1)] for j in range(n-1)]
    for i in range(n-1):
        for j in range(m-1):
            A1[i][j] = A[i+1][j+1]
    return A1

def concatenate(M, N): #concatenates the matrix N with the matrix M
    if len(M) == len(N):
        L = []
        for i in range(len(M)):
            L1 = M[i] + N[i]
            L.append(L1)
        return L

def disconcatenate(M, j0): #splits matrix M from column index i0 into two matrices 
	M1, M2 = [], []
	for i in range(len(M)):
		L1, L2 = M[i][:j0], M[i][j0:]
		M1.append(L1)
		M2.append(L2)
	return M1, M2

def to_upper_triangular(A): #transforms a matrix A to upper triangular matrix
    n, m = len(A), len(A[0])
    O1 = [[0] for k in range(n-1)]
    if n == 1  or isNull_v3(A):
        return A
    else:
        B = Transform_v2(A)
        A1 = extract_v3(B)
        return [A[0]]+concatenate(O1, to_upper_triangular(A1))

def find_pivot(A): #finds gauss pivot in a square matrix A
    n = len(A)
    for i in range(n):
        for j in range(n):
            if A[i][j] != 0:
                return i, j

def find_pivot_v2(A): #finds gauss pivot in a matrix A
    n, m = len(A), len(A[0])
    for i in range(n):
        for j in range(m):
            if A[i][j] != 0:
                return i, j

def swap_lines(A, i, j): #swaps i and j lines
    A[i], A[j] = A[j], A[i]
    return A

def swap_columns(A, i, j): #swaps i and j columns
    n = len(A)
    C1, C2 = [], []
    for k in range(n):
        C1.append(A[k][i])
        C2.append(A[k][j])
        A[k][i], A[k][j] = A[k][j], A[k][i]
    return A

def Transform(A):# this function transforms a square matrix A into a matrix whose first column without the first term is null. """
    n = len(A)
    t = find_pivot(A)
    if t != (0, 0):
        swap_lines(A, 0, t[0])
        swap_columns(A, 0, t[1])
    for i in range(1, n):
        k = A[i][0] / A[0][0]
        for j in range(n):
            A[i][j] -= k*A[0][j]
    return A
    
def Transform_v2(A):# this function transforms matrix A into a matrix whose first column without the first term is null.
    n, m = len(A), len(A[0])
    t = find_pivot_v2(A)
    if t != (0, 0):
        swap_lines(A, 0, t[0])
        swap_columns(A, 0, t[1])
    for i in range(1, n):
        k = A[i][0] / A[0][0]
        for j in range(m):
            A[i][j] -= k*A[0][j]
    return A

def constructor_K(n, r):
    K = [[0 for i in range(n)] for j in range(n)]
    for i in range(r):
        k = n-r+i
        K[i][k] = 1
    return K

def null(n, m): #creates a null matrix
    return [[0 for i in range(m)] for j in range(n)]

def identity(n): #creates the identity matrix of size n
    I = null(n, n)
    for i, j in zip(range(n), range(n)):
        I[i][j] = 1
    return I

def pow(M, n): #calculates (M)**n
    if n >= 1:
        P = M
        for i in range(1, n):
            P = mul(P, M)
    elif n == 0:
        N = str(M)
        L = tools.str_to_list(N)
        if rank(L) == len(M):
            return identity(len(M))
        else:
            print(M, "is not invertible")
            return

def trace(A):
	n, m = len(A), len(A[0])
	if n != m:
		return 
	s = 0
	for i in range(n):
		s += A[i][i]
	return s

def determinant(A):
	n, m = len(A), len(A[0])
	if n != m:
		return 
	if n == 2:
		a, b, c, d = A[0][0], A[1][0], A[0][1], A[1][1]
		return (a*d)-(b*c)
	else:
		S = 0
		for j in range(n):
			S = A[0][j]*determinant(_matrix.extract_v2(A, 0, j))*((-1)**j) + S
		return S 