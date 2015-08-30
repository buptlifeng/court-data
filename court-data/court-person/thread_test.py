#coding=UTF8

import time,thread

def thd_test(count = 1):
    try:
        if count > 5:
            thread.exit()
        print 'hello,',time.localtime()
        count = count + 1
    except:
        print 'error here'

if __name__ == '__main__':
    thread.start_new_thread(thd_test,())
