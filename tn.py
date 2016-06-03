#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
紧接着 tr.py。
tn.py 负责对 句子 
1，分词
2，标记拼音（假）
3，标记音素
'''

import sys,re


reload(sys)
sys.setdefaultencoding("utf-8")


def remove_short(ucc):
    rr = []
    for l in ucc:
        if len(l.strip()) > 15 :
            rr.append(l.strip())
    return rr

def remove_white(ucc):
    '''去掉有空格的行'''
    rr = []
    for l in ucc:
        flag = True
        for w in l:
            if w == u' ':
                flag = False
                break
        if flag:
            rr.append(l)
    return rr

def split_tab(ucc):
    '''tab分行'''
    rr = []
    for l in ucc:
        ll = l.split(u'　')
        for nl in ll:
            rr.append(nl)
    return rr;
    
    
def split_white(ucc):
    '''空格分行'''
    rr = []
    for l in ucc:
        ll = l.split(u' ')
        for nl in ll:
            rr.append(nl)
    return rr;
    
def split_with_juhao(ucc):
    '''句号换行'''
    rr = []
    for l in ucc:
        ll = l.split(u'。')
        for nl in ll:
            rr.append(nl+u'。')
    
    return rr

def replace_things(ucc):
    '''分号改成逗号'''
    rr = []
    for l in ucc:
        t = l.replace(u'；', u'，')
        t = t.replace(u'：', u'，')
        rr.append(t)
    return rr
    
def remove_kuahao(ucc):
    '''括号内的删除'''
    rr = []
    for l in ucc:
        t = re.sub(u'\uff08.*\uff09', u'', l)
        t = re.sub(u'\(.*\)', u'', t)
        t = re.sub(u'\[.*\]', u'', t)

        rr.append(t)
    
    return rr   

def split_long(ucc):
    '''太长的分'''
    rr = []
    for l in ucc:
        if len(l) > 40:
            ll = l.split(u'，')
            if len(ll) >=2:
                idx = len(ll)/2
                nl = ll[0]
                for i in xrange(1,idx):
                    nl = nl + u'，' + ll[i]
                rr.append(nl+u'。')
                nl = ll[idx]
                for i in xrange(idx+1, len(ll)):
                    nl = nl + u'，' + ll[i]
                rr.append(nl)
        else:
            rr.append(l)
    return rr

'''
关于编码
utf-8(类型 str)  ---decode(utf-8)----> 类型unicode  -----encode(utf-8)---->  utf-8(类型 str) 
空格的删除，字数的计算，都必须在 unicode 层面。
'''

def gen(fn, fno):
    with open(fn, 'r') as fp:
        cc = fp.readlines()
        
        ucc = [c.decode("utf-8") for c in cc]
        
        #unicode start
        
        ucc = remove_kuahao(ucc)
        ucc = split_tab(ucc)
        ucc = split_white(ucc)
        
        ucc = remove_kuahao(ucc)

        ucc = remove_short(ucc)
        ucc = remove_white(ucc)
        
        ucc = split_with_juhao(ucc)
        ucc = remove_short(ucc)
        
        ucc = replace_things(ucc)
        
        
        ucc = split_long(ucc)
        ucc = remove_short(ucc)
        ucc = split_long(ucc)
        ucc = remove_short(ucc)
        ucc = split_long(ucc)

        
        #unicode end
        cc = [c.encode("utf-8") for c in ucc]
        
        
        for l in cc:
            print l
        
        print 'Total=%d'%len(cc)
        
        with open(fno, 'w') as fpo:
            for l in cc:
                fpo.write(l+'\n')
            
        
    

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "usage: tr.sh fn prefix"
        sys.exit()
        
    print sys.argv[1], sys.argv[2]
        
    gen(sys.argv[1], sys.argv[2])