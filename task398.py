import requests as req
from time import time
t = time()
class searchTree():
    '''Search Tree contains solutions nodes and functions to add node and read some node properties'''
    def __init__(self, m):
        self.nodes = []
        self.nextGen = []
        self.b_n = None
        self.m = m
    def get_rws(self,idx):
        res = []
        for i,r in enumerate(self.m):
            res.append(r[idx[i]:])
        return res
    def addNewNode(self, p, npc: int, rws: list):
        self.nodes.append(node(p,npc,rws))
        if p is not None:
            if len(p.children) == 0:
                p.children.append(self.nodes[-1])
            else:
                found = False
                for i,child in enumerate(p.children):
                    if self.nodes[-1].npc < child.npc:
                        p.children = p.children[:i]+ [self.nodes[-1]] +[child]+ p.children[i+1:]
                        found = True
                        break
                if not found:
                    p.children.append(self.nodes[-1])
    def newBN(self,n):
        self.b_n = node(n.parent,n.npc,n.rws)
    def delete(self, node):
        del self.nodes[self.nodes.index(node)]
        
class node():
    '''class node contains properties of curent point the program at
    parent - parent node for this one
    npc - node path cost
    rws - current position in the sorted matrix
    children - children nodes'''
    def __init__(self, p, npc: int, rws: list):
        self.parent = p
        self.npc = npc
        self.rws = rws
        self.children = []
#getting matrices
twenty_url = 'https://gist.githubusercontent.com/cosmologicon/4f6473b4e781f20d4bdef799132a3b4b/raw/d518a7515618f70d25c2bc6c58430f732f6e06ce/matrix-sum-20.txt'
twenty_mat_s = req.get(url=twenty_url).text
nintyseven_url = 'https://gist.githubusercontent.com/cosmologicon/641583595e2c76d7c119912f7afafbfe/raw/6f9ebcb354c3aa58fb19c6f4208d0eced310b62a/matrix-sum-97.txt'
nintyseven_mat_s = req.get(url=nintyseven_url).text

def req_to_list(s):
    '''splits request string into the matrix'''
    res = []
    for i in s.split('\n'):
        r = []
        for j in i.split(' '):
            r.append(int(j))
        res.append(r)
    return res

def is_sol(t,n):
    '''function to check if current node is solution'''
    sol = True
    cols = []
    for r in t.get_rws(n.rws):
        cols.append(r[0][1])
    for r in t.get_rws(n.rws):    
        if cols.count(r[0][1]) > 1:
            sol = False
    return sol

def matrix_iterate(m):
    '''this function sorts every row in matrix,
     creates searchTree, cretes temp searchTree to find first solution
     and returns result as new sorted matrix, where first element in each row is a solution'''
    res = []
    m_s = []
    for r in m:
        tmp = [(x,j) for j,x in enumerate(r)]
        m_s.append(sorted(tmp, key = lambda k:k[0])) #sorted matrix is 2d list of tuples 
        #each tuple is element which contains value of element and column in which it was before sorting
    #initializing the tree
    t = searchTree(m_s)
    #root node
    t.addNewNode(None, 0, [0]*len(m_s))
    tmpTree = searchTree(m_s)
    tmpTree.addNewNode(None, 0,[0]*len(m_s))
    t.newBN(genFirstBN(tmpTree,tmpTree.nodes[0]))
    if not is_sol(t,t.nodes[0]):
        m_s = treeRoute(t,[t.nodes[0]])
    del tmpTree
    for r in m_s:
        res.append(r[0])
    return res

def genFirstBN(t,c_n):
    '''generates first best solution node, which helps to slightly reduce number of iterations,
    returns object type node'''
    t.newBN(c_n)
    cols = []
    same_cols = 0
    if is_sol(t,t.b_n):
        return t.b_n

    for r in t.get_rws(t.b_n.rws):
        cols.append(r[0][1])
    for r in t.get_rws(t.b_n.rws):    
        if cols.count(r[0][1]) > 1:
            same_cols += 1

    for i,c in enumerate(cols):
        if cols.count(c) > 1:
            new_rws = t.b_n.rws.copy()
            new_rws[i] = new_rws[i]+1
            t.addNewNode(c_n, c_n.npc + t.get_rws(c_n.rws)[i][1][0]-t.get_rws(c_n.rws)[i][0][0], new_rws)
            break         
    return genFirstBN(t,t.nodes[-1])

def npc_calc(nrws, orws):
    '''calculates path cost from previous node to curent node
    cost is how much sum of elements will differ from the smallest possible sum
    which is sum of minimum value in each row'''
    res = 0
    for i in range(len(nrws)):
        res+=nrws[i][0][0]-orws[i][0][0]
    return res
def treeRoute(t,c_n_l):
    '''Calculates best solution to the problem.
    The concept is based on that the best solution possible is when
    it is sum of minimum values in each row. Since it is not always the case,
    this function tries to find the node with less possible path cost.
    It iterates through matrix with sorted rows and finds solution (each node represents iteration).
    If current solution is better than the best solution,
    the best solution changes to the current one. If next child has larger path cost than the best solution, this child won't be created.
    Every created child of all nodes of this iteration are being appended to the next generation list.
    Generation is list of nodes which function iterates through at the moment. 
    Function ends when next generation list is empty which means that not a single child were created for each node in the current generation,
    which means that there is no point in looking further and create new generations since none of them will contain solution better than
    current best one.
    This function also contains little tricks which slightly reduce the number of iterations'''
    while True:
        t.nextGen = []
        sol_lst = []
        for c_n in c_n_l:
            cols = []
            for r in t.get_rws(c_n.rws):
                cols.append(r[0][1])
            cols_rep = {}
            for i,r in enumerate(t.get_rws(c_n.rws)):    
                if cols.count(r[0][1]) > 1:
                    if r[0][1] in cols_rep:
                        cols_rep[r[0][1]].append(i)
                    else:
                        cols_rep[r[0][1]] = [i]
            cols_rep_comb = {}           
            for k in cols_rep:
                for i in cols_rep[k]:
                    if k in cols_rep_comb:
                        cols_rep_comb[k].append([x for x in cols_rep[k] if x != i])
                    else:
                        cols_rep_comb[k] = [[x for x in cols_rep[k] if x != i]]
            comb = []
            for c,k in enumerate(cols_rep_comb):
                for j,i in enumerate(cols_rep_comb[k]):
                    if c == 0:
                        comb.append(i)
                    else:
                        if j == 0:
                            for l in range(len(comb)):
                                comb[l]+=i
                        else:
                            for l in range(len(comb)):
                                comb.append(comb[l][:-1]+i)
            for c in comb:
                new_rws = c_n.rws.copy()
                for i in c:
                    if new_rws[i]+1 == len(t.m):
                        new_rws[i] = 0
                    else:
                        new_rws[i] = new_rws[i]+1
                if ((c_n.npc + npc_calc(t.get_rws(new_rws),t.get_rws(c_n.rws)))< t.b_n.npc):
                    t.addNewNode(c_n, c_n.npc + npc_calc(t.get_rws(new_rws),t.get_rws(c_n.rws)), new_rws)      
            if len(c_n.children) == 0:
                c_n_l.remove(c_n)
                break
            for child in c_n.children:
                t.nextGen.append(child)
                if is_sol(t,child):
                    sol_lst.append(child)
            if len(sol_lst) == 1:
                t.newBN(sol_lst[0])
            elif len(sol_lst) > 1:
                temp = sol_lst[0]
                for n in sol_lst[1:]:
                    if temp.npc > n.npc:
                        temp = n
                t.newBN(temp)
        c_n_l = t.nextGen.copy()
        if len(t.nextGen) == 0:
            return t.get_rws(t.b_n.rws)
        t.nodes = t.nextGen

def min_trades(n,m):
    tr = []
    for i in m:
        for j in range(len(i)-1):
            tr.append(i[j+1][0]-i[j][0])
    tr = sorted(tr)
    if n > 0:
        return sum(tr[:n])
    else: return 0


nintyseven_mat = req_to_list(nintyseven_mat_s)
twenty_mat = req_to_list(twenty_mat_s)
res_m = matrix_iterate(twenty_mat)
# res_m = matrix_iterate(nintyseven_mat)
# res_m = matrix_iterate([[123456789,752880530,826085747,576968456,721429729],[173957326,1031077599,407299684,67656429,96549194],
# [1048156299,663035648,604085049,1017819398,325233271],[942914780,664359365,770319362,52838563,720059384],[472459921,662187582,163882767,987977812,394465693]])
print(res_m)
sum = 0
for i in res_m:
    sum+=i[0]
print(sum)
