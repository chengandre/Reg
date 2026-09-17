import os
import shutil
import multiprocessing
import signal
from dfa import *

SEARCH_BATCH_SIZE = max(2, min(10, os.cpu_count() or 1))

def init_worker():
    signal.signal(signal.SIGINT, signal.SIG_IGN)

class scientist:
    def __init__(self):
        self.n = 2
        self.k = 2
        self.conjecture = dfa(self.n)
        self.pool = None

        self.count = 1
        self.count_final = 1

        self.strings = []
        self.f = 0
        self.not_f = 0
        self.start()

    def __getstate__(self):
        self_dict = self.__dict__.copy()
        del self_dict['pool']
        return self_dict

    def start_pool(self):
        if self.pool is None:
            self.pool = multiprocessing.Pool(processes=SEARCH_BATCH_SIZE, initializer=init_worker)

    def shutdown(self):
        if self.pool is not None:
            self.pool.terminate()
            self.pool.join()
            self.pool = None

    def start(self):
        if os.path.exists("./current_session"):
            shutil.rmtree("./current_session", ignore_errors=True)
        os.mkdir("./current_session")
        file = open("./current_session/strings.txt", 'w')
        file.close()
        self.conjecture.render(self.count_final, self.f)
        print("\r" + str(self.count) + " DFAs processed", end="", flush=True)

    def findDFA(self, input):
        self.n = input['n']
        self.strings = input['strings']
        self.conjecture.reset(self.n, input['flag'])
        self.count = 0
        while self.conjecture.delta:
            self.count += 1
            if self.update_final_states(self.strings) and self.conjecture.is_minimal(self.f):
                return {'id': input['id'], 'dfa': self.conjecture, 'f': self.f, 'not_f': self.not_f, 'count': self.count}
            self.conjecture.nextdfa(self.n, self.k)
        return self.count

    def update_conjecture(self):
        self.start_pool()
        flag_cursor = dfa(self.n)
        flag_cursor.flag = self.conjecture.flag.copy()
        search_n = self.n
        while True:
            inputs = []
            inputs.append({'flag': flag_cursor.flag.copy(), 'n': search_n, 'id': 0, 'strings': self.strings})
            for i in range(1, SEARCH_BATCH_SIZE):
                flag_cursor.nextflag(search_n, self.k)
                if not flag_cursor.flag:
                    search_n += 1
                    flag_cursor.nextflag(search_n, self.k)
                inputs.append({'flag': flag_cursor.flag.copy(), 'n': search_n, 'id': i, 'strings': self.strings})

            res = self.pool.map(self.findDFA, inputs, chunksize=1)

            target_index = None
            for i in range(len(res)):
                if isinstance(res[i], dict):
                    self.count += res[i]['count']
                    if target_index is None or res[i]['id'] < res[target_index]['id']:
                        target_index = i
                else:
                    self.count += res[i]

            if target_index is not None:
                self.conjecture = res[target_index]['dfa']
                self.n = self.conjecture.n
                self.f = res[target_index]['f']
                self.not_f = res[target_index]['not_f']
                self.count_final += 1
                self.conjecture.render(self.count_final, self.f)
                print("\r" + str(self.count) + " DFAs processed", end="", flush=True)
                return

    def update_final_states(self, strings):
        self.f = 0
        self.not_f = 0
        for x in strings:
            state = 1 << self.conjecture.get_final_state(x[1])
            if x[0]:
                if state & self.not_f:
                    return False
                self.f |= state
            else:
                if state & self.f:
                    return False
                self.not_f |= state
        return True

    def add_final_state(self, state):
        self.f |= state

    def add_not_final_state(self, state):
        self.not_f |= state

    def add_accepted_string(self, state):
        if state & self.f:
            return
        elif state & self.not_f == 0:
            self.add_final_state(state)
            if self.conjecture.is_minimal(self.f):
                self.count += 1
                self.count_final += 1
                self.conjecture.render(self.count_final, self.f)
                return
        self.update_conjecture()
        return

    def add_rejected_string(self, state):
        if state & self.not_f:
            return
        elif state & self.f == 0:
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

        string_final_state = 1 << self.conjecture.get_final_state(string)
        if is_in:
            self.add_accepted_string(string_final_state)
        else:
            self.add_rejected_string(string_final_state)

    def known_string(self, string):
        if (0, string) in self.strings or (1, string) in self.strings:
            return True
        return False
