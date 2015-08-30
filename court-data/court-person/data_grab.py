# coding=utf8
'''
Created on 2015年8月22日
获取个人法院失信人员的个人案件编号 一个法院案件编号可能对应多个实际失信人
将该案件编号和失信人员姓名保存到数据库
从数据库提前读取记录到队列，提供case_id,频繁关闭db连接,bad
@author: lex
'''
from __init__ import *
from bs4 import BeautifulSoup
import requests
import sqlite3  
import os,json, string
import thread,time,logging

def select_rec_by_id(case_id):
    sql = '''
    select case_id from person_court_info
    where case_id='%s'
    ''' % (case_id)
    print sql
    con = sqlite3.connect('person.db')
    if con is None:
        raise 'db conn is none' 
    cur = con.cursor()
    cur.execute(sql)
    count = len(cur.fetchall())
    cur.close()
    con.close()
    return count

def select_recs_new():
    sql='''
    select case_id from person_court_info
    where duty is null limit 20
    '''
    con = sqlite3.connect('person.db')
    if con is None:
        raise 'db conn is none' 
    cur = con.cursor()
    cur.execute(sql)
    l = cur.fetchall()
    cur.close()
    con.close()
    return l


def execute_sql(sql):
    con = sqlite3.connect('person.db')
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    cur.close()
    con.close()
    
def insert_sql(case_id, name):
    if case_id is None or name is None:
        raise 'case_id or name cannot be None'
    sql = '''
    insert into person_court_info(case_id,iname)
    values('%s','%s')
    ''' % (case_id, name)
    log.debug(sql)
    execute_sql(sql)
    
def update_person_info(params):
    if params is None or params.get('case_id') is None:
        #logger print params
        return
    sql = '''
    update person_court_info set iname="%s",sexy='%s',age=%d,cardNum='%s',
    courtName='%s',areaName='%s',gistId='%s',regDate='%s',
    caseCode='%s',gistUnit='%s',duty='%s',performance='%s',
    performedPart='%s',unperformPart='%s',disruptTypeName='%s',
    publishDate='%s',partyTypeName='%s' where case_id='%s'
    ''' % (params.get('iname'),params.get('sexy'), params.get('age'), params.get('cardNum'),
         params.get('courtName'), params.get('areaName'), params.get('gistId'), params.get('regDate'),
         params.get('caseCode'), params.get('gistUnit'), params.get('duty'), params.get('performance'),
         params.get('performedPart'), params.get('unperformPart'), params.get('disruptTypeName'),
         params.get('publishDate'), params.get('partyTypeName'), params.get('case_id'))
    log.debug(sql)
    execute_sql(sql)
    
def parser_html(html):
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find('table', id='Resultlist')
    if table is not None:
        rows = table.find_all('tr')
        for row in rows:
            id_tr = row.find_all('td')
            
            if len(id_tr) > 0 :
                cur_td = id_tr[1]
                td_a = cur_td.find('a')
                if td_a is not None:
                    case_id = td_a['id']
                    name = td_a['title']
                    if select_rec_by_id(case_id) == 0:
                        insert_sql(case_id, name)
 
# 跳到指定页面去循环读取该页面的case_id 注意添加header信息
def goto_specify_page(cookies, page_no=1):
    # max_page = 104672 #104672 共1570071条
    data = {'currentPage':page_no}
    
    headers = {
                   'Accept-Encoding':'gzip, deflate',
                   'Accept-Language':'zh-CN,zh;q=0.8',
                   'Origin':'http://shixin.court.gov.cn',
                   'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.132 Safari/537.36',
                   'Referer':'http://shixin.court.gov.cn/personMore.do'
                   }    
    
    r = requests.post(person_court_list_url, data=data, headers=person_headers, cookies=cookies)
    #print r.status_code
    parser_html(r.text)

# 根据id查询个人法院失信信息 验证通过，注意通过首页拿到cookie
def get_person_court_info(id,cookies):
    if id is None:
        return
    person_url = person_detail_url + id
    log.debug(person_url)
    
    headers = {
               'Accept-Encoding':'gzip, deflate,sdch',
               'Accept-Language':'zh-CN,zh;q=0.8',
               'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.132 Safari/537.36',
               'X-Requested-With':'XMLHttpRequest',
               'Referer':'http://shixin.court.gov.cn/personMore.do'
               }
    
    r = requests.get(person_url, headers=headers, cookies=cookies)
    if r.status_code == requests.codes.ok:
        text = r.text.encode('utf8')
        text = text.translate(string.maketrans('\n\r\t', '   '))
        content = json.loads(text)
        print content, content.get('duty'), type(content.get('duty'))
        content['case_id'] = id
        log.debug(content)
        update_person_info(content)

#query person court info using case_id from db
def qry_person_court_info_thd():
    person_referer_page = 'http://shixin.court.gov.cn/personMore.do'
    r = requests.get(person_referer_page, headers=person_headers)
    cookies = r.cookies
    while True:
        l=select_recs_new()
        log.debug(l)
        if len(l) < 1:
            time.sleep(3)
        else:
            for line in l:
                case_id = line[0]
                get_person_court_info(case_id,cookies)


def qry_person_list_thd(max_page=40426):
    #var totalPage = 40426;
    person_referer_page = 'http://shixin.court.gov.cn/personMore.do'
    r = requests.get(person_referer_page, headers=person_headers)
    cookies = r.cookies
    cur_page = 1
    while cur_page < max_page:
        goto_specify_page(cookies,cur_page)
        
        cur_page = cur_page + 1

if __name__ == '__main__':
    thread.start_new_thread(qry_person_list_thd,40426)
    
    thread.start_new_thread(qry_person_court_info_thd)