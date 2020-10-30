# 学习笔记

### process
1. os.fork(): 返回0表示为子进程，返回非0（子进程id）表示该进程为父进程
2. multiprocessing 这个更贴近于python

* multiprocessing.Process
```
target: target是run()函数调用的可调用对象
group：一般不用
name：process的名称
args：target调用时的参数
kwargs： target调用时的键值对
daemon：父进程退出时，将尝试将daemonic的子进程终止；另外daemonic的子进程不能在fork子进程，否则可能出现孤立进程

当没有存活的非守护线程时，整个Python程序才会退出
```

th1 = multiprocessing.Process(target=f, args=(var1,), kwargs={k:v}, daemon=None)

* ch.join([timeout])：不能在子进程中join自己。 父进程等待子进程结束,timeout不为空时表示父进程等待一个时间然后继续做后面的事情去了，不在等待子进程退出了

* ch.terminate(): 强制子进程退出 发送sigterm信号

* ch.kill():发送sigkill信号 only unnix os

* ch.close():释放子进程的资源，在这个函数调用完成后，再调用其他函数很多将会抛出异常；如果子进程还没有join掉，那么close将会抛出异常

* is_alive(), daemon, pid

### 调试

1. 在父进程和子进程中加入一些打印
2. multiprocessing.active_children(), multiprocessing.cpu_count()
3. 可以使用面向对象的方式创建子进程，即继承Process类

### 进程通信
#### 队列Queue  注意：这里的队列是从multiprocessing中导入的Queue
进程安全的

```
Queue(maxsize=10)
```

和现实中的排队是类似的，

* qsize()：返回当前队列的大小
* empty()： 检查当前队列是否为空
* full()
* put(obj[, block[, timeout]])：将obj放入到队列中去。如果block且timeout为None，那么将一直等待直到能将obj插入到当前队列；如果timeout指定了，那么在这个时间后，将抛出
queue。Full的异常；如果block为False，无法插入则会立马抛出异常
* put_nowait(obj): put(obj, False)
* get([block[, timeout]]):remove且get到一个数据，从队列中。block和timeout与put类似
* get nowait： get（obj，False）
* close():关闭队列，即无法再进行put操作
* join_thread()：再close后面使用，等待数据全部放入到pipe中后，再取消阻塞

### Pipe 底层通信
```
conn1, conn2 = Pipe(); conn1是Connection实列
conn1.send(['a'])
conn2.recv()
```
管子的两端，一端发送，一端获取

* send 发送数据
* recv 获取数据

### 共享内存
默认是进程安全的

```
from multiprocessing import Process, Value, Array
```

* Value(typecode, *args, lock=True): typecode指定这个value的类型，
args是传递给typecode的参数，lock=True是进程安全，否则不是
```
value = Value('d', 0.0)
value.value = 1.1 # set value
value.value # get value
```

* Array(typecode_or_type, size_or_initializer, *, lock=True)：
typecode是返回array中的元素的类型，size是array的长度或者一维数组
```
a = Array('i', range(10)) #只能是一维数组
a[:] # get all value
a[i] # get index i's value
```

### 资源抢占
锁
* lock = multiprocessing.Lock()
* RLock可进行叠加，Lock不可以

```
lock.aquire()
lock.release

with lock:
    pass
```

### 进程池

控制并行运行的进程数量, 可以灵活的使用with控制进程池，可以使用map和imap

```
p = Pool(processes=cpu_count)
ret = p.apply_async(func, args=(func_args)) # 异步运行， apply（）是同步运行，但意义不大
ret.get([timeout]) # 获取func的结果，超时后会抛出异常
p.close(): 等待woker process完成并退出，新的任务将无法加入到pool中。
p.join(): 阻塞父进程，必须在close或terminate后面调用，等待woker退出；join之后不能再去取数据，否则会报异常

def run(i, l):
    return (i, l)


if __name__ == '__main__':
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    with pool:  # pool 可以使用with， 相当于使用了close
        for i in range(10):
            ret = pool.apply_async(run, args=(i, 1)) # AsyncResult对象
            print(ret.get()) # 如果run抛出异常，那么在这里将再次被抛出

```

进程池map映射并发, 和普通的map函数很像
```
def run(i):
    return (i, 1)


if __name__ == '__main__':
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    with pool:
        ret = pool.imap(run, range(10)) #返回一个iterable对象
        for i in ret:
            print(i)
```


### 线程
* 阻塞和非阻塞： 发起方行为
* 同步和异步：接收方行为

* 并发：多人一个目的地
* 并行：多人多目的地

创建多线程，有以下两种方式：

1. threading.Tread(target=f)
2. 继承Tread并重写run函数

* start() ##
* run()  ##
* join()
* is_alive()
* getName()


### 线程锁：Lock Rlock ， 为了线程安全，需要进行加锁操作

* with lock： 自动加解锁 ## 这个是重点
* lock.acquire(), lock.release()
* wait(), notify() ：wait会将底层的Condition锁给释放，所以其他地方的notify可以获到锁并进行下去，
notify会通知wait继续往下进去，通过wait释放对应的锁
* setDaemon(True)之后，关掉终端，程序会自己运行不退出，同时主程序被干掉后，daemon
程序也会被干掉

**条件锁**： threading和process中的条件锁是一样的，都是用的threading中的
Condition。这个和生产者消费者相似

```
def func(c: multiprocessing.Condition, i):
    with c:
        print(i, 'func')
        c.wait()
        print(i, 'waited')


def func1(c: multiprocessing.Condition, i):
    with c:
        print(i, 'notify')
        c.notify()
        print(i, 'notified')
```

**信号量** ： 类似进程里面的进程池，可限定同时运行的数目
```
def func1(c: threading.BoundedSemaphore, i):
    c.acquire()
    print(f'run the thread {i}')
    time.sleep(1)
    c.release()


if __name__ == '__main__':
    c = threading.BoundedSemaphore(2)
    for i in range(20):
        t = threading.Thread(target=func1, args=(c, i,))
        t.start()
```

**定时器** 指定在几秒后运行.1秒后执行func2函数
```
    t = threading.Timer(1, func2)
    t.start()
```

#### 多线程队列
FIFO,  多线程用到的是queue库的队列，多进程用的是多进程自己的队列

1. 内置库queue的使用
```
q = queue.Queue(5)
q.put(1)
q.get()
q.qsize()
q.full()
q.empty()

q.task_done() # 对于使用了get方法，调用该方法，告诉别人队列中的这个项目已经完毕
  最后调用该方法，以提示join是否继续阻塞，让线程即席执行后续代码
q.join() # 阻塞,直到队列中的所有项目完成；每次调用task done将标记该对象已经完成
```

**beizhu** 利用queque的join特性可以实现程序的正常退出。 每个对象使用get，然后task
done， 在主程序中使用queue的join等待即可


消费者模型： 使用Thread来模拟，使用queque来进行商品的生产，使用Condition锁进行生产者和消费者的通知

2. 优先及队列
```
优先及队列
```
q = queue.PriorityQueue()
q.put((1, 'work')) #  1是优先及，数字越小越优先被取出;相同优先及则先入的先取出
q.get()
```

3. 堆栈队列。了解即可

### 线程池


```
from multiprocessing.dummy import Pool as ThreadPool
```

高级封装,3.2以后支持
```
from concurrentfutures import ThreadPoolExecutor
```

1. ThreadPool和线程池的用法几乎是一样的
```
urls = [
        'http://www.baidu.com',
        'http://www.python.org',
        'http://www.douban.com'
        ]
pool = ThreadPool(4)
ret = pool.map(requests.get, urls)

pool.close()
pool.join()

for i in ret:
    print(i.text)
```

2. ThreadPoolExecutor的用法，注意submit函数和map函数的区别

map将传递过来的参数分别给func函数，而submit将传递过来的参数直接给func函数
两者都返回函数执行后返回的值
```
with ThreadPoolExecutor(max_workers=3) as exe:
    ret = exe.map(requests.get, urls)
    for i in ret:
        print(i.url)
```

### GIL和性能瓶颈
GIL将多线程变为了伪线程，拿到GIL才可以执行CPU，遇到IO时，CPU将释放给别人用

1. **多线程在IO密集型的 才会有优势**
