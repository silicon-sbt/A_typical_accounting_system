import functools
from typing import Callable, TypeVar, Any
import time
from utils import print_msg


R =TypeVar('R')


    

def log(desc:str,level:str='info') :#desc，是写你来干啥的,这儿就是，获取列表    
    def decorator(fn:Callable[...,R])-> Callable[..., R]:
        @functools.wraps(fn)
        def wrapper(*args,**kwargs):
            print_msg(f'{desc}开始',level)
            result =fn(*args,**kwargs)
            print_msg(f'{desc}结束',level)
            return result
        return wrapper
    return decorator
def retry(times:int=3):
    def trytime(fn:Callable[...,R]) ->Callable[..., R]:
        @functools.wraps(fn)
        def true_run(*args,**kwargs):
            for i in range(times):
                try:
                    result = fn(*args,**kwargs)
                    return result
                except Exception as e:
                    if i != times - 1:
                        print_msg(f'出现报错，报错原因：{e}，进行第{i+1}','Warning')
                    if i == times - 1:
                        print_msg(f'重试彻底失败，最后原因：{e}', 'error')
                        raise 
        return true_run  
    return trytime
