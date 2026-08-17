import threading
import time

class BackgroundTasks():
    # HOW TO USE
    # 
    # def foo(a, b):
    #     print("->", a+b)
    #
    # bg = BackgroundTasks()
    #
    # xs = [1,2,3,4,5,6,7,8,9,10]
    # for x in xs:
    #     bg.create(foo, (x,0))
    #
    # bg.start()
    def __init__(self, task_ptr=None, task_args=(), wait_time=5, max_threads=5):
        self.threads = []
        self.wait_time = wait_time
        self.thread_function_ptr = task_ptr
        self.thread_args = task_args
        self.max_threads = max_threads

    def create(self, function_ptr=None, args=()):
        t = threading.Thread(target=self.thread_function_ptr if not function_ptr else function_ptr, args=self.thread_args if not args else args)
        self.threads.append(t)

    def thread_pool(self):
        for i in range(0, len(self.threads), self.max_threads):
            chunk = self.threads[i : i + self.max_threads]
            print(f"BackgroundTasks::thread_pool::chunk {len(chunk)}")
            for c in chunk:
                c.start()
            time.sleep(self.wait_time)

    def start(self):
        t = threading.Thread(target=self.thread_pool, args=() )
        t.start()

    def wait(self):
        for i in range(0, len(self.threads), self.max_threads):
            chunk = self.threads[i : i + self.max_threads]
            for t in chunk:
                while t.ident is None:
                    time.sleep(self.wait_time)
                    print("BackgroundTasks::wait", len(chunk), t.ident, t.is_alive(), t)
                t.join()
