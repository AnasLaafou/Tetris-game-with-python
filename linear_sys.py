from Matrices import *

def solve_eq_lin(a, b, c):
    return (c-b)/a

def solve_sys_lin(sysmat, resvec):
    n = sysmat.shape[0]
    newmat = sysmat.concatenate(resvec)
    u_tri = newmat.to_upper_triangular()
    tupmat = u_tri.disconcat(u_tri.shape[1]-1)
    u_tri, resvec = tupmat
    vec = []
    for i in range(n-1, -1, -1):
        L = u_tri.body[i]
        b = 0
        if vec != []:
            for j in range(len(vec)):
                b += vec[j][0]*L[n-1-j] 
        x = solve_eq_lin(L[i], b, resvec.body[i][0])
        vec.append([x])
    vec2 = []
    for k in range(len(vec)-1, -1, -1):
        vec2.append(vec[k])
    return vec2