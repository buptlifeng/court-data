#coding=utf8
'''
Created on 2015-8-23

@author: lex
'''

import sqlite3

def db_conn():
    conn = sqlite3.Connection("person.db")  # person_court
    return conn

def db_init():
    conn = db_conn()
    conn.execute('create table person_info(id integer primary key autoincrement,name text,gender' + 
     'text,age integer default 0)')
    conn.commit()
    conn.execute('insert into person_info values(1,"lifeng","male",25)')
    conn.commit()
    db_conn_close(conn)

def db_select():
    print 'hello1'
    conn = db_conn()
    cur = conn.cursor()
    print 'hello2'
    cur.execute('SELECT * FROM person_info')
    print 'hello3'
    print cur.fetchall()
    db_conn_close(conn)

def db_conn_close(conn):
    if conn is not None:
        conn.close()

def db_qry_none_result(sql):
    if sql is not None:
        conn = db_conn()
        conn.execute(sql)
        db_conn_close(conn)

def db_qry_result(sql):
    if sql is not None:
        conn = db_conn()
        conn.execute(sql)
        db_conn_close(conn)
 
def update_person_court(sql):
    if sql is not None:
        conn = db_conn()
        conn.execute(sql)
        conn.commit()
        db_conn_close(conn)

def insert_person_court(sql):
    conn=db_conn()
    conn.execute(sql)
    db_conn_close(conn)
           
def select_person_court(sql):
    if sql is not None:
        conn = db_conn()
        conn.execute(sql)
        # cur=conn.cursor()
        # cur.
        db_conn_close(conn) 
        
def init_person_court(sql):
    conn = db_conn()
    create_tb = '''
create table person_court_info(
    id integer primary key autoincrement,
    case_id text comment '案件索引编号',
    iname text comment '被执行人姓名/名称',
    sexy text comment '性别',
    age TINYINT comment '年龄',
    cardNum text comment '身份证号码/组织机构代码',
    courtName text comment '执行法院',
    areaName text comment '省份',
    gistId text comment '执行依据文号',
    regDate text comment '立案时间',
    caseCode text comment '案号',
    gistUnit text comment '作出执行依据单位',
    duty text comment '生效法律文书确定的义务',
    performance text comment '被执行人的履行情况',
    performedPart text comment '已经履行部分',
    unperformPart text comment '未履行部分',
    disruptTypeName text comment '失信被执行人行为具体情形',
    publishDate text comment '发布时间',
    partyTypeName integer comment '关注次数',
    remark text comment '备注'
    );
    '''
    conn.execute(create_tb)
    conn.commit()
    db_conn_close(conn)
        
if __name__ == '__main__':
    
    
    
    init_person_court('')
    
    '''
    conn = db_conn()
    cur = conn.cursor()
    cur.execute('SELECT * FROM person_info')
    print cur.fetchall()
    db_conn_close(conn)
    '''
