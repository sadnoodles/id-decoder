# -*- coding: utf-8 -*-

import time,  datetime
import json


SEX_DICT = {1:u'男', 0:u'女'}
N = (7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2)
ERROR_FIX_DICT = {0: '1', 1: '0', 2: 'X', 3: '9', 4: '8', 
                5: '7', 6: '6', 7: '5', 8: '4', 9: '3',10: '2'}
# k = '0 1 2 3 4 5 6 7 8 9 10'.split(' ')
# v = '1 0 X 9 8 7 6 5 4 3 2'.split(' ')
# for i in range(11):
    # errorfix_dict.__setitem__(int(k[i]), v[i])

def check_sum(id_number):
    return ERROR_FIX_DICT[sum( map( lambda x, y:x*int(y), N, id_number[:17])) % 11]
    
def isreal(id_number):
    """判断是否是真的身份证号"""
    return check_sum (id_number)== id_number[-1]
    
area_dict = json.load(open('area_dict.json','r'))

def upgrade(id):
    "15 length -> 18 length"
    if len(id) != 15:
        raise TypeError, u"请输入15位身份证号码"
    id=id[:6]+'19'+id[6:]
    id+=check_sum(id)
    return id
    
def decode_id(id_number):
    """分析身份证编号"""
    if len(id_number) != 18 and len(id_number) != 15:
        raise TypeError, u"请输入15/18位身份证号码"
    #地址
    if len(id_number)==15:
        id_number=upgrade(id_number)
        # print "Upgrade:",id_number
    address = area_dict.get(id_number[:6])
    if not address:
        raise ValueError,"No such area code."
    #生日
    birth_date = (int(id_number[6:10]),          #年
                  int(id_number[10:12]),         #月
                  int(id_number[12:14]))         #日
    birthday = u'%s年%s月%s日' % birth_date
    #年龄
    curr_time = time.localtime()[:3]
    date1 = datetime.date(curr_time[0], curr_time[1], curr_time[2])
    try:
        date2 = datetime.date(birth_date[0], birth_date[1], birth_date[2])
    except TypeError:
        print u"日期不存在！"
        return ()
    delta = date1-date2
    age = delta.days/365
    #性别
    sex = SEX_DICT[(int(id_number[-2]))%2]
    #校验真伪
    real = isreal(id_number)
    return address, birthday, age, sex, real

    
if __name__ == "__main__":
    print upgrade('533400751130363')
    for i in decode_id('533400197511303637'):
        print i,
    print 