import itertools
import graphviz
import os

def sort_tuple(tup):
    return (tup[0], tup[1]) if tup[0] < tup[1] else (tup[1],tup[0])

class dfa:
    def __init__(self, n):
        self.k = 2 
        self.flag = [0] + [i*self.k-1 for i in range(1,n)]
        self.delta = []
        self.nextdfa(n, self.k)
            
    def nextflag(self, n, k):
        if self.flag == []:
            self.flag = [0] + [i*k-1 for i in range(1,n)]
            return
        elif self.flag[-1] == n - 2:
            self.flag.clear()
            return
        j = 1
        for i in range(n-1, 1, -1):
            if self.flag[i-1] != self.flag[i] - 1:
                j = i
                break
        self.flag[j] -= 1
        for i in range(j+1, n):
            self.flag[i] = k*i - 1

    def nextdfa(self, n, k):
        j = 0
        l = 1
        if self.delta != []:
            i = n - 1
            for j in range(k*n-1, -1, -1):
                if i != 0 and self.flag[i] == j:
                    i -= 1
                elif self.delta[j] < i:
                    break
            if j == 0 and (self.flag[1] == 1 or self.delta[0] == 1):
                self.delta.clear()
                return 
            else:
                self.delta[j] += 1
                j += 1
                l = i+1
        else:
            for i in range(k*n):
                self.delta += [0]
            for i in range(n):
                self.delta[self.flag[i]] = i
        for i in range(j, k*n):
            if l < n and i == self.flag[l]:
                l += 1
            else:
                self.delta[i] = 0
        
    def render(self, count_final, f):
        graph = graphviz.Digraph()
        graph.attr(rankdir='LR')
        graph.attr(splines='true')
        
        graph.node(" ", style="invisible",width="0", height="0")
        for i in range(len(self.flag)):
            if i in f:
                graph.node(str(i), shape="doublecircle")
            else:
                graph.node(str(i), shape="circle")
                
        graph.edge(' ', '0', dir="both", arrowtail="dot")
        for i in range(len(self.delta)):
            graph.edge(str(int(i/2)), str(self.delta[i]), label=str(i%2), dir="forward")
            
        graph.render("./current_session/out" + str(count_final-1), format='png')
        os.remove("./current_session/out" + str(count_final-1))
    
    def is_minimal(self, f):
        marked = {}
        for x in itertools.combinations(range(len(self.flag)), 2):
            marked[x] = [0]
        
        not_f = [x for x in range(len(self.flag)) if x not in f]
        for x in itertools.product(f, not_f):
            marked[sort_tuple(x)] = [1]
            
        found = False
        for x in list(itertools.combinations(f, 2)) + list(itertools.combinations(not_f, 2)):
            for i in range(self.k):
                next_pair = [self.delta[self.k*x[0]+i], self.delta[self.k*x[1]+i]]
                next_pair.sort()
                next_pair = tuple(next_pair)
                if next_pair not in marked or marked[next_pair][0] == 0:
                    continue
                    
                found = True
                to_mark = [x]
                while len(to_mark) != 0:
                    if to_mark[0] in marked:
                        target = marked[to_mark[0]]
                        target[0] = 1
                        for x in target[1:]:
                            if marked[x][0] == 0:
                                to_mark += [x]
                    to_mark = to_mark[1:]
            if not found:
                for i in range(self.k):
                    next_pair = [self.delta[self.k*x[0]+i], self.delta[self.k*x[1]+i]]
                    next_pair.sort()
                    next_pair = tuple(next_pair)
                    if next_pair[0] != next_pair[1]:
                        marked[next_pair] += [x]
            found = False
        for x in marked.values():
            if x[0] == 0:
                return False
        return True
    
    def get_final_state(self, string):
        current_state = 0
        for i in range(len(string)):
            current_state = self.delta[self.k*current_state + int(string[i])]
        return current_state
    
    
    
    
            
          
