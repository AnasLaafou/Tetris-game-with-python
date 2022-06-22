def str_to_list(Q):
    L1 = []
    for i in range(1, len(Q)-1):
        if Q[i] == "[":
            j = i
        elif Q[i] == "]":
            t = Q[j:i+1]
            L1.append(t)
    for i in range(len(L1)):
        tt = L1[i][1:len(L1[i])-1].split(",")
        L1[i] = tt
    for i in range(len(L1)):
        for j in range(len(L1[0])):
            L1[i][j] = float(L1[i][j])
    return L1

def vec_to_list(vec):
    for i in range(len(vec)):
        vec[i] = vec[i][0]

def column(mat, i):
    Col = []
    if mat != []:
        if type(mat) in [list, tuple] and type(mat[0]) in [list, tuple]:
            Col = []
            for k in range(len(mat)):
                Col.append(mat[k][i])
    return Col