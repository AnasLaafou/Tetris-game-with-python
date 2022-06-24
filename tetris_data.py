import sys
from helper import vec


blocs_ids0 = {"T"   : [vec(0, 0), vec(1, 0), vec(0, 1), vec(-1, 0)],
              "I"   : [vec(0, 0), vec(0, -2), vec(0, -1), vec(0, 1)],
              "L"   : [vec(0, 0), vec(0, -2), vec(0, -1), vec(1, 0)],
              "t_L" : [vec(0, 0), vec(0, -2), vec(0, -1), vec(-1, 0)],
              "Z"   : [vec(0, 0), vec(-1, -1), vec(0, -1), vec(1, 0)],
              "t_Z" : [vec(0, 0), vec(1, -1), vec(0, -1), vec(-1, 0)],
              "O"   : [vec(0, 0), vec(1, 0), vec(1, -1), vec(0, -1)]}
    
blocs_ids90 = {"T"   : [vec(0, 0), vec(0, -1), vec(0, 1), vec(-1, 0)],
               "I"   : [vec(0, 0), vec(2, 0), vec(1, 0), vec(-1, 0)],
               "L"   : [vec(0, 0), vec(2, 0), vec(1, 0), vec(0, 1)],
               "t_L" : [vec(0, 0), vec(2, 0), vec(1, 0), vec(0, -1)],
               "Z"   : [vec(0, 0), vec(1, -1), vec(1, 0), vec(0, 1)],
               "t_Z" : [vec(0, 0), vec(-1, -1), vec(-1, 0), vec(0, 1)],
               "O"   : [vec(0, 0), vec(1, 0), vec(1, -1), vec(0, -1)]}
    
blocs_ids180 = {"T"   : [vec(0, 0), vec(1, 0), vec(0, -1), vec(-1, 0)],
                "I"   : [vec(0, 0), vec(0, -2), vec(0, -1), vec(0, 1)],
                "L"   : [vec(0, 0), vec(0, 2), vec(0, 1), vec(-1, 0)],
                "t_L" : [vec(0, 0), vec(0, 2), vec(0, 1), vec(1, 0)],
                "Z"   : [vec(0, 0), vec(-1, -1), vec(0, -1), vec(1, 0)],
                "t_Z" : [vec(0, 0), vec(1, -1), vec(0, -1), vec(-1, 0)],
                "O"   : [vec(0, 0), vec(1, 0), vec(1, -1), vec(0, -1)]}
    
blocs_ids270 = {"T"   : [vec(0, 0), vec(1, 0), vec(0, 1), vec(0, -1)],
                "I"   : [vec(0, 0), vec(2, 0), vec(1, 0), vec(-1, 0)],
                "L"   : [vec(0, 0), vec(-2, 0), vec(0, -1), vec(-1, 0)],
                "t_L" : [vec(0, 0), vec(-2, 0), vec(0, 1), vec(-1, 0)],
                "Z"   : [vec(0, 0), vec(1, -1), vec(1, 0), vec(0, 1)],
                "t_Z" : [vec(0, 0), vec(-1, -1), vec(-1, 0), vec(0, 1)],
                "O"   : [vec(0, 0), vec(1, 0), vec(1, -1), vec(0, -1)]}

boards = []

class Bloc:

    def __init__(self, _id, ind, board):
        self.successfully_constructed = True
        if _id not in blocs_ids0.keys():
            print(f"invalid bloc id : {_id}", file=sys.stderr)
            self.successfully_constructed = False
        if self.successfully_constructed:
            self.id = _id
            self.ind = ind
            self.board = board
            inds = [vec(*ind) + v for v in blocs_ids0[self.id]]
            for _ind in inds:
                if not self.board.isvalid_index(_ind) or self.board.isoccuped(_ind):
                    print(f"bloc construction failed : invalid index {ind} to insert this bloc in the board", file=sys.stderr)
                    self.successfully_constructed = False        
                    break
            if self.successfully_constructed:
                self.inds = inds
                self.heading = 0
        

class boardMatrix():

    def __init__(self, size=(12, 20), data=None):
        global boards
        if vec(*size) < vec(5, 5):
            print(f"invalid board size : {size}")
            return
        if data is None:
            data = [[0 for j in range(size[0])] for i in range(size[1])]
        self.data = data
        self.size = size
        self.spawn_ind = (int(self.size[0]//2)-(self.size[0]+1)%2, 2)
        boards += [self, ]
        self.blocs = []

    def show(self):
        for line in self.body:
            for case in line:
                print(case, end=" ")
            print()

    def isvalid_index(self, ind):
        return ind[0] in range(self.size[0]) and ind[1] in range(self.size[1])

    def isoccuped(self, ind):
        if self.isvalid_index(ind):
            return self.data[ind[1]][ind[0]] == 1
        
    def isborder(self, ind):
        if self.isvalid_index(ind):
            return ind[0] in (0, self.size[0]-1) and ind1 in (0, self.size[1]-1)

    def occuped_inds(self):
        o_inds = []
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if self.isoccuped((i, j)):
                    o_inds.append((i, j))
        return o_inds
        
    def next_ind(self, ind, direc, inds):
        if self.isvalid_index(ind):
            _next = vec(*ind) + vec(*direc)
            if self.isvalid_index(_next):
                if not self.isoccuped(_next) or _next in inds:
                    return _next
            return ind

    def next_inds(self, bloc, direc):
        if bloc not in self.blocs:
            return 
        inds = bloc.inds
        next_inds = []
        for ind in inds:
            _next = self.next_ind(ind, direc, inds)
            if _next == ind:
                next_inds = inds
                break
            next_inds.append(_next)
        return next_inds
        
    def insert_bloc(self, bloc_id):
        ind = self.spawn_ind
        b = Bloc(bloc_id, ind, self)
        if b.successfully_constructed:
            self.blocs.append(b)
            for _ind in b.inds:
                self.data[_ind[1]][_ind[0]] = 1
        return b
        
    def move(self, b, direc):
        if b not in self.blocs:
            return
        n_inds = self.next_inds(b, direc)
        for _ind in b.inds:
            self.data[_ind[1]][_ind[0]] = 0
        for n_ind in n_inds:
            self.data[n_ind[1]][n_ind[0]] = 1
        b.inds = n_inds
        b.ind = b.inds[0]

    def projection(self, b):
        if b not in self.blocs:
            return
        n_inds = self.next_inds(b, (0, 1))
        while b.inds != n_inds:
            self.move(b, (0, 1))
            n_inds = self.next_inds(b, (0, 1))
            
    def rotate(self, bloc):
        if bloc not in self.blocs:
            return
        for ind in bloc.inds:
            self.data[ind[1]][ind[0]] = 0
        bloc.heading = (bloc.heading + 90) % 360
        orient = eval(f"blocs_ids{bloc.heading}")
        ind = bloc.ind
        inds = [vec(*ind) + v for v in orient[bloc.id]]
        for ind in inds:
            if not self.isvalid_index(ind) or self.isoccuped(ind):
                inds = bloc.inds
                bloc.heading = (bloc.heading - 90) % 360
                break
        bloc.inds = inds
        for ind in bloc.inds:
            self.data[ind[1]][ind[0]] = 1

    def set_bloc_heading(self, bloc, heading):
        while bloc.heading != heading:
            self.rotate(bloc)

    def isfrozen(self):
        if self.blocs == []:
            return True
        copy = boardMatrix(size=self.size)
        bloc = self.blocs[-1]
        copybloc = copy.insert_bloc(bloc.id)
        direc = vec(*bloc.ind) - vec(*copybloc.ind)
        copy.set_bloc_heading(copybloc, bloc.heading)
        copy.move(copybloc, direc)
        for ind in self.occuped_inds():
            if not copy.isoccuped(ind):
                copy.data[ind[1]][ind[0]] = 1
        for b in copy.blocs:
            copy.move(b, (0, 1))
        return copy.data == self.data

    def clear(self):
        self.blocs = []
        self.data = [[0 for j in range(self.size[0])] for i in range(self.size[1])]
        
    def evolution(self):
        evo_counter = 0
        for i in range(len(self.data)):
            line = self.data[i]
            if self.data[i] == [1 for _ in range(len(line))]:
                self.data.remove(self.data[i])
                self.data.insert(0, [0 for _ in range(len(line))])
                evo_counter += 10
        return evo_counter
                
