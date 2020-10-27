import random
import threading
import queue
import time


class Producer(threading.Thread):
    def __init__(self, q: queue.Queue,
                 conn: threading.Condition, name: str):
        super().__init__()
        self.q = q
        self.conn = conn
        self.name = name
        print(f'Producer {self.name} started')

    def run(self) -> None:
        while True:
            global lk
            with self.conn:
                if self.q.full():
                    with lk:
                        print(f'{self.name} queue if full, producer wait')

                    self.conn.wait()

                else:
                    v = random.randint(0, 10)
                    with lk:
                        print(f'{self.name} put value {str(v)}')

                    self.q.put(f'{self.name}: {str(v)}')
                    self.conn.notify()
                    time.sleep(1)


lk = threading.Lock()


class Consumer(threading.Thread):
    def __init__(self, q: queue.Queue,
                 conn: threading.Condition, name: str):
        super().__init__()
        self.q = q
        self.conn = conn
        self.name = name

    def run(self) -> None:
        while True:
            global lk
            with self.conn:
                if self.q.empty():
                    with lk:
                        print('queue is empty, consumer wait')

                    self.conn.wait()

                else:
                    v = str(self.q.get())
                    with lk:
                        print(f'{self.name} get value {v}')

                    time.sleep(1)


if __name__ == '__main__':
    # q = queue.Queue(8)
    # con = threading.Condition()
    #
    # p1 = Producer(q, con, 'p1')
    # p1.start()
    #
    # p2 = Producer(q, con, 'p2')
    # p2.start()
    #
    # c1 = Consumer(q, con, 'c1')
    # c1.start()

    p = queue.PriorityQueue(5)
    p.put((1, 'a'))
    p.put((-1, 'b'))
    print(p.get())