import os
import shutil
import multiprocessing
import queue
import signal
from dfa import *

SEARCH_WORKERS = max(1, min(10, os.cpu_count() or 1))

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
            self.pool = multiprocessing.Pool(processes=SEARCH_WORKERS, initializer=init_worker)

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
                return {'dfa': self.conjecture, 'f': self.f, 'not_f': self.not_f, 'count': self.count}
            self.conjecture.nextdfa(self.n, self.k)
        return self.count

    def update_conjecture(self):
        self.start_pool()
        flag_cursor = dfa(self.n)
        flag_cursor.flag = self.conjecture.flag.copy()
        search_n = self.n
        completed = queue.SimpleQueue()
        pending = {}
        finished = {}
        submitted = 0
        next_result = 0
        match_found = False

        def submit_next():
            nonlocal search_n, submitted
            if submitted:
                flag_cursor.nextflag(search_n, self.k)
                if not flag_cursor.flag:
                    search_n += 1
                    flag_cursor.nextflag(search_n, self.k)
            index = submitted
            input = {'flag': flag_cursor.flag.copy(), 'n': search_n, 'strings': self.strings}
            pending[index] = self.pool.apply_async(
                self.findDFA,
                (input,),
                callback=lambda _: completed.put(index),
                error_callback=lambda _: completed.put(index),
            )
            submitted += 1

        for _ in range(SEARCH_WORKERS):
            submit_next()

        while True:
            index = completed.get()
            result = pending.pop(index).get()
            finished[index] = result
            if isinstance(result, dict):
                match_found = True
            if not match_found:
                submit_next()

            while next_result in finished:
                result = finished.pop(next_result)
                if isinstance(result, dict):
                    self.count += result['count']
                    self.conjecture = result['dfa']
                    self.n = self.conjecture.n
                    self.f = result['f']
                    self.not_f = result['not_f']
                    self.shutdown()
                    self.count_final += 1
                    self.conjecture.render(self.count_final, self.f)
                    print("\r" + str(self.count) + " DFAs processed", end="", flush=True)
                    return
                self.count += result
                next_result += 1

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
