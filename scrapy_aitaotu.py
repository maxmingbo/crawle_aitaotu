# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 21:54:41 2017

@author: zmb
"""



import requests
import os
from bs4 import BeautifulSoup as btfs
import re
import time


#tag = 'jiamiannvhuang'

src_url = 'https://www.aitaotu.com'
hds = {
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'Cookie':'UM_distinctid=15f34e0d33c260-03f92cc26b0ce6-58133b15-fa000-15f34e0d33d227; CNZZDATA1255139604=842059008-1508419324-https%253A%252F%252Fcn.bing.com%252F%7C1508419324; Hm_lvt_3b19253d112290a9184293cf68a02346=1508420671,1508420687; Hm_lpvt_3b19253d112290a9184293cf68a02346=1508421552',
'Host':'www.aitaotu.com',
'Referer':'https://cn.bing.com/',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0'
       }
       

tag = 'rosi'
#tag = ''


url_1 = 'https://www.aitaotu.com/tag/%s.html'%tag
root_path = 'D:/360Downloads/%s/'%tag
       


def download_pic(pic_url, root_path, pic_name):
    try:
        #time.sleep(0.1)
        if not os.path.exists( root_path   ):
            os.mkdir( root_path )
            
        if not os.path.exists( root_path + pic_name):
            r = requests.get(pic_url,headers = hds)
            with open(root_path + pic_name,'wb') as f:
                f.write(r.content)
                f.close()
                print('    '+ pic_name +'  图片保存成功!')
        else:
            print('图片已经存在')
    except:
        pass
        #print('        图片保存')   
        
def get_picurl_download(sp_2,download_speed_str = ''):
    for sp_j in sp_2.find_all(src = re.compile('^https://img.aitaotu.cc')):
        if sp_j.has_key('src'):
            '''
            待下载图片链接
            '''
            url_3 = sp_j['src']
            print '    ',url_3
            
            pic_name = download_speed_str + url_3[-14:].replace('/','_')
            #print '    ',pic_name
            download_pic(url_3 , root_path, pic_name)
    return sp_j

        
def open_url2(url_2, to_print = '' ):

    try:
        r_2 = requests.get(url_2,headers = hds)
        r_2.raise_for_status
        #r_2.encoding = r.apparent_encoding
    
        #print r.status_code
        dem_2 = r_2.text
        sp_2 = btfs(dem_2,"html.parser")
        

        seach_next = ''
        
        print to_print,'1' #进度显示
        sp_j = get_picurl_download(sp_2,to_print+'1')

        seach_next = sp_j.parent.attrs['href'].split('_')[0]
                #print '       ',seach_next
        
        
        '''
        寻找下一页
        '''               
        nub = 1
        for next in sp_2.find_all(href = re.compile('^%s_'%seach_next)):
            nub = max(nub, int(next['href'].split('_')[-1].split('.')[0]))
            
        '''
        loop 
        '''
            
        for i in range(2,nub+1):
            to_next = src_url + seach_next + '_' + str(i) + '.html'
            #print to_next
            
            r_2 = requests.get(to_next,headers = hds)
            r_2.raise_for_status
            #r_2.encoding = r.apparent_encoding
        
            #print r.status_code
            dem_2 = r_2.text
            sp_2 = btfs(dem_2,"html.parser")
            
            print to_print,'___%d'%i     #进度显示
            get_picurl_download( sp_2,to_print +  str(i) )
            
        #time.sleep(0.5)
    except:
        print("第二层网页打开失败")
        
        
def loop_url1(sp,m ):
    n = 0
    for sp_url in sp.find_all( href = re.compile('/guonei/\d{5}.html')):

        if sp_url.has_key('class'):

            url_2 = src_url + sp_url['href']
            #print url_2
            time.sleep(0.5)
            
            n = n+1
            
            to_print = str(m) +'__'+str(n) +'__'
            #print str(m) +'__'+str(n)
            
            open_url2(url_2 ,to_print )
            
        
        
        
        
'''
主函数：
'''
m = 0
try:
    r = requests.get(url_1,headers = hds)
    r.raise_for_status
    #r.encoding = r.apparent_encoding
    #print r.status_code
    dem = r.text
    sp = btfs(dem,"html.parser").body
    #print(sp.prettify())

    loop_url1(sp,m)   
    
    all_loop =   sp.find_all('span')[2]
    set_url = set()
    
    for url_loop in  all_loop.find_all(href = re.compile('/tag/%s'%tag)):
        set_url.add(src_url + url_loop['href'])
    #print set_url

    for url in set_url:
        m = m + 1

        try:
            r = requests.get(url,headers = hds)
            r.raise_for_status

            dem = r.text
            sp = btfs(dem,"html.parser").body
            
            loop_url1(sp,m)
            
            
        except:
            print("第一层网页打开失败")
        

except:
    print("第一层网页打开失败")

    
    
    


    
