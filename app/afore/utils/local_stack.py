from werkzeug.local import LocalStack,LocalProxy

class G:
    '''协程安全变量
    _uid_stack 每次访问的用户标识
    '''
    _uid_stack = LocalStack() # 用户标识
    @classmethod
    def _find_uid(cls):
        '''获取UID，如果没有值则为{}'''
        top = cls._uid_stack.top
        if top is None:
            top = {}
        return top

    @classmethod
    def get_uid(cls) -> dict:
        '''获取用户标识UID值'''
        return LocalProxy(cls._find_uid)._get_current_object()

    @classmethod
    def push_uid(cls,value):
        '''上传用户标识'''
        cls._uid_stack.push(value)

    @classmethod
    def freed_uid(cls):
        '''释放变量，保证uid不被脏读'''
        cls._uid_stack.__release_local__()
