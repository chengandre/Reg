import os
import shutil
from dfa import *

class scientist:
    def __init__(self):
        self.n = 2
        self.k = 2
        self.conjecture = dfa(self.n)
        
        self.count = 1
        self.count_final = 1
        
        self.strings = []
        self.f = []
        self.not_f = []
        self.start()
        
    def start(self):
        if os.path.exists("./current_session"):
            shutil.rmtree("./current_session", ignore_errors=True)
        os.mkdir("./current_session")
        file = open("./current_session/strings.txt", 'w')
        file.close()    
        self.conjecture.render(self.count_final, self.f)
        print("\r" + str(self.count) + " DFAs processed", end="", flush=True)
        
    def update_conjecture(self):
        while True:
            while self.conjecture.flag != []:
                self.conjecture.nextdfa(self.n, self.k)
                
                while self.conjecture.delta != []:
                    self.count += 1
                    if self.count % 100000 == 0:
                        print("\r" + str(self.count) + " DFAs processed", end="", flush=True)
                        
                    if self.update_final_states(self.strings) and self.conjecture.is_minimal(self.f):
                        self.count_final += 1
                        self.conjecture.render(self.count_final, self.f)
                        print("\r" + str(self.count) + " DFAs processed", end="", flush=True)
                        
                        return
                    self.conjecture.nextdfa(self.n, self.k)
                self.conjecture.nextflag(self.n, self.k)
            self.n += 1
            self.conjecture.nextflag(self.n, self.k)
            self.conjecture.nextdfa(self.n, self.k)
            
    def update_final_states(self, strings):
        self.f = []
        self.not_f = []
        for x in strings:
            if x[0]:
                self.add_final_state(self.conjecture.get_final_state(x[1]))
        self.f = list(set(tuple(self.f)))
        
        for x in strings:
            if x[0] == 0:
                state = self.conjecture.get_final_state(x[1])
                if state in self.f:
                    return False
                
                self.add_not_final_state(state)
                
        self.not_f = list(set(tuple(self.not_f)))
        return True
    
    def add_final_state(self, state):
        if state < self.n:
            self.f += [state]
    
    def add_not_final_state(self, state):
        if state < self.n:
            self.not_f += [state]  
    
    
    def add_accepted_string(self, state):
        if state in self.f:
            return
        elif state not in self.not_f:
            self.add_final_state(state)
            if self.conjecture.is_minimal(self.f):
                self.count += 1
                self.count_final += 1
                self.conjecture.render(self.count_final, self.f)
                return
        self.update_conjecture()
        return
    
    def add_rejected_string(self, state):
        if state in self.not_f:
            return
        elif state not in self.f:
            self.add_not_final_state(state)
            return
        self.update_conjecture()
        return
    
    def add_string(self, is_in, string):
        self.strings += [(is_in, string)]
        
        file = open("./current_session/strings.txt", 'a')
        if string == "":
            file.write(str(is_in) + " " + "eps" + "\n")
        else:
            file.write(str(is_in) + " " + string + "\n")
        file.close()
        
        string_final_state = self.conjecture.get_final_state(string)
        if is_in:
            self.add_accepted_string(string_final_state)
        else:
            self.add_rejected_string(string_final_state)
    
    def known_string(self, string):
        if (0, string) in self.strings or (1, string) in self.strings:
            return True
        return False