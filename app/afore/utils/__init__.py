import wrapt
from threading import Thread
from .sugers import AppT,RqsH
from .local_stack import G
import base64
import re
from afore.config import WORDS


@wrapt.decorator
def new_thread(wrapped, instance, args, kwargs):
    '''启动新的线程'''
    thread = Thread(target=wrapped,args=args,kwargs=kwargs)
    thread.start()

def mutate_dict(fn,kwargs:dict):
    '''修改字典参数'''
    for k, v in kwargs.items():
        kwargs[k] = fn(v)
    

def filter_word(w):
    '屏蔽敏感词语'
    with open(WORDS) as f:
        data = ""
        for i in f:
            data += base64.b64decode(i).decode().replace("\n","|")
            pattern = re.compile(data)
            if isinstance(w, str):
                w = pattern.sub(r'*',w)
            return w
