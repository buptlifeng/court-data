#coding=utf8
'''
Created on 2015年8月22日
获取个人法院失信人员的个人案件编号 一个法院案件编号可能对应多个实际失信人
将该案件编号和失信人员姓名保存到数据库
TODO 将cookie保存为全局变量，注意适时更新
TODO 首先保存所有的id,查询数据库，根据id去查询详细信息
TODO 乱七八糟的代码，先把功能实现，后期进行修改
@author: lex
'''
from __init__ import requests,person_headers,person_court_list_url,person_court_info_url,person_detail_url
from bs4 import BeautifulSoup
import sqlite3

def select_rec_by_id(case_id):
    sql='''
    select id from person_court_info
    where id='%s'
    '''%(case_id)
    print sql
    con = sqlite3.connect('person.db')
    cur = con.cursor()
    cur.execute(sql)
    count = len(cur.fetchall())
    print count
    cur.close()
    con.close()
    return count

def insert_init_rec(sql):
    con = sqlite3.connect('person.db')
    con.execute(sql)
    con.commit()
    con.close()

def init_req():
    r=requests.get(person_court_list_url,headers=person_headers)
    print r.text
    return r.text
    
def parser_html(html):
    f = open('person.html','r')
    content=f.read()
    soup=BeautifulSoup(content,'lxml')
    table = soup.find('table',id='Resultlist')
    if table is not None:
        rows = table.find_all('tr')
        for row in rows:
            id_tr = row.find_all('td')
            
            if len(id_tr) > 0 :
                cur_td = id_tr[1]
                td_a = cur_td.find('a')
                if td_a is not None:
                    case_id = td_a['id']
                    name=td_a['title']
                    if select_rec_by_id(case_id) == 0:
                        insert_sql(case_id, name)

def insert_sql(case_id,name):
    if case_id is None or name is None:
        raise 'case_id or name cannot be None'
    sql='''
    insert into person_court_info(id_index,name)
    values('%s','%s')
    '''%(case_id,name)
    print sql
    insert_init_rec(sql)
 
#跳到指定页面去循环读取该页面的case_id 注意添加header信息
def goto_next_page(page_no=0):
    #max_page = 104672
    data={'currentPage':page_no}
    r = requests.post(person_court_list_url,data=data,headers=person_headers)
    return r.text

#根据id查询个人法院失信信息 验证通过，注意通过首页拿到cookie
def get_person_court_info(id):
    if id is None:
        return
    person_url = person_detail_url+id
    
    url='http://shixin.court.gov.cn/personMore.do'
    r = requests.get(url,headers=person_headers)
    cookies=r.cookies
    
    headers = {
               'Accept-Encoding':'gzip, deflate,sdch',
               'Accept-Language':'zh-CN,zh;q=0.8',
               'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.132 Safari/537.36',
               'X-Requested-With':'XMLHttpRequest',
               'Referer':'http://shixin.court.gov.cn/personMore.do'
               }
    
    
    
    return requests.get(person_url,headers=headers,cookies = cookies).text

if __name__=='__main__':
    #init_req()
    #parser_html('')
    
    r=get_person_court_info('1818535')
    print r
    
