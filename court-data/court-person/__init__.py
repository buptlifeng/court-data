#coding=utf8

import requests,Queue
import logging,os

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",filename=os.path.join(os.getcwd(),'log.txt'),level=logging.DEBUG)
log = logging.getLogger('court-perInfo')   #Logger对象

court_main_url='http://shixin.court.gov.cn/'

person_court_list_url='http://shixin.court.gov.cn/personMore.do'

#http://shixin.court.gov.cn/visit.do?functionId=6&partyId=2036826 2036826为person_court_list_url页面拿到的id
person_court_info_url='http://shixin.court.gov.cn/visit.do?functionId=6&partyId='

person_referer_page='http://shixin.court.gov.cn/personMore.do'

unit_referer_page='http://shixin.court.gov.cn/unitMore.do'

person_detail_url='http://shixin.court.gov.cn/detail?id='

person_headers={'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
         'Accept-Language':'zh-CN,zh;q=0.8',
         'Referer':person_referer_page
         }

unit_headers={'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
         'Accept-Language':'zh-CN,zh;q=0.8',
         'Referer':unit_referer_page
         }

cookies={}

con = None