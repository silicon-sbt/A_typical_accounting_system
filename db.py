import sqlite3
import hashlib
import time
import decorator
from utils import print_msg
from utils import bill


@decorator.log('建表')
@decorator.retry()
def initdb()->None:  ##作为首次使用建表用
    with sqlite3.connect("SQLite/记账.db") as conn:
        cursor = conn.cursor()
        
        # 执行建表 SQL
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                type TEXT NOT NULL,
                amount INTEGER NOT NULL,
                category TEXT,
                note TEXT,
                hash TEXT,
                time float,
                related_id INTEGER
            )
        ''')
        print_msg('建表成功','info')

@decorator.log('写入账单')
@decorator.retry()
def Save(bill:bill)->str: 
    """写入账单，如果之前有就账单就进行普通的记账和hash的计算，如果之间没有的话就进行创世区块的计算"""
    now_time = time.time()
    with sqlite3.connect("SQLite/记账.db")as conn:
        cursor = conn.cursor();
        cursor.execute("SELECT hash FROM records ORDER BY id DESC LIMIT 1")
        result = cursor.fetchone() 
        if result == None:
            print_msg('检测到账本为空，接下来执行创世区块操作')
            midle=f'{bill.times}||{bill.expense_type}||{bill.amount}||{bill.use_key}||{bill.category}||{bill.note}||{now_time}||{bill.related_id}'
            h =hashlib.sha256(midle.encode()).hexdigest()   
            cursor.execute('''
                INSERT INTO records (date, type, amount, category, note, hash, time,related_id)
                VALUES (?, ?, ?, ?, ?, ?, ?,?)
            ''', (bill.times, bill.expense_type, bill.amount, bill.category, bill.note, h, now_time,bill.related_id))
            conn.commit()
        elif result != None:
            print_msg('账本非空，进行正常流程')
            last_hash =result[0]    
            midle = f'{last_hash}||{bill.times}||{bill.expense_type}||{bill.amount}||{bill.use_key}||{bill.category}||{bill.note}||{now_time}||{bill.related_id}'
            h =hashlib.sha256(midle.encode()).hexdigest()  
            cursor.execute('''
                            INSERT INTO records (date, type, amount, category, note, hash, time,related_id)
                            VALUES (?, ?, ?, ?, ?, ?, ?,?)
                        ''', (bill.times, bill.expense_type, bill.amount, bill.category, bill.note, h, now_time,bill.related_id))  
            conn.commit()   
@decorator.log('读表/账单')
@decorator.retry()
def Read():
    pass #todo，还没动工





           
        





initdb()
