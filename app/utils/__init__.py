import wrapt
from threading import Thread

@wrapt.decorator
def new_thread(wrapped, instance, args, kwargs):
    '''启动新的线程'''
    thread = Thread(target=wrapped,args=args,kwargs=kwargs)
    thread.start()


def mutate_dict(f,d:dict):
    for k, v in d.items():
        d[k] = f(v)
    


    