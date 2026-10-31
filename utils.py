import time
from dataclasses import dataclass

def print_msg (msg:str,level:str = 'info',)->None:  #抽离出来，后期方便做持久化的文档处理
    now_time = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f'{now_time},[{level}]:{msg}')

@dataclass
class bill:
    times:str
    expense_type:str
    amount:float  #自动处理成int值，所以虽然传入的float，但传进来后实际是int值，避免浮点偏差
    use_key:str
    category: str = "默认分类"
    note: str = "无备注"
    related_id:int =None

    def __post_init__(self):
        self.amount = int(round(self.amount*100))
        