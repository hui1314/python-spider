# -*- coding: UTF-8 -*-
import re
import os
import random
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import threading

class DongM_Download():
	def __init__(self,mod='',name=''):
		self.url = 'http://www.ezdmw.com'
		self.head = self.get_headers()
		#self.proxies = {"http": "http://127.0.0.1:10809"}
		if(mod=='search'):
			self.search_name(name)
		elif(mod=='download'):
			self.DongM = name
			self.get_id()
		else:
			print('No mod, I\'m stupid')

	def get_headers(self):
	    user_agent_list =[
	    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
	    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
	    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
	    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
	    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
	    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
	    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
	    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
	    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
	    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
	    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
	    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
	    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
	    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
	    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
	    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
	    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
	    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
	    ]
	    UserAgent=random.choice(user_agent_list)
	    headers = {'User-Agent': UserAgent}
	    return headers

	def get_id(self):
		#搜索功能
		list0=[] #集数的NK标识
		number=0 #统计集数
		pattern = re.compile(r'/(\d+).html')#正则模式,匹配数字NK
		params = {"searchText":self.DongM}
		#fireq0 = requests.get(url=self.url+'/Home/Index/search.html',params=params,headers=self.head,proxies=self.proxies).text
		fireq0 = requests.get(url=self.url+'/Home/Index/search.html',params=params,headers=self.head).text
		bf = BeautifulSoup(fireq0,"html.parser")
		texts=bf.find_all('div',style="margin-left:18px;")[0].a['href']
		#获取视频API-ID功能
		fireq1=requests.get(url=self.url+texts,headers=self.head)
		html1=fireq1.text
		bf0 = BeautifulSoup(html1,"html.parser")
		texts=bf0.find_all('section',class_="anthology")
		if '其他1' in str(texts[0]) and '线路A' not in str(texts[0]):
			texts=texts[0].find_all('a',class_="circuit_switch1")
			number=int(texts[0].span['class'][0])
			for i in range(number):
				list0.append(pattern.findall(texts[i]['href'])[0])
				print(list0,'其他1线路')
		elif '线路A' in str(texts[0]) and '其他1' not in str(texts[0]):
			texts=texts[0].find_all('a')
			number=int(texts[0].span['class'][0])
			for i in range(number):
				list0.append(pattern.findall(texts[i]['href'])[0])
				print(list0,'线路A')
		else:
			print('解析线路出现问题')
		print('信息提取完成......\n准备下载...')
		self.Threading_model(list0)
	def down_from_url(self,url,dst="test.mp4"):
		response = requests.get(url, stream=True)
		dst=response.headers['Content-Disposition'][22:-1].encode('raw-unicode-escape').decode()
		file_size = int(response.headers['content-length'])
		if os.path.exists(dst):
			first_byte = os.path.getsize(dst)
			print(dst+'已存在')
		else:
			first_byte = 0
		if first_byte >= file_size:
			return file_size
		header = {"Range": f"bytes={first_byte}-{file_size}","user-agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
		pbar = tqdm(total=file_size, initial=first_byte, unit='B', unit_scale=True, desc=dst)
		req = requests.get(url, headers=header, stream=True)
		with open(dst, 'ab') as f:
			for chunk in req.iter_content(chunk_size=1024):
				if chunk:
					f.write(chunk)
					pbar.update(1024)
		pbar.close()
	def Threading_model(self,id_list):
		threading_list=[]
		for i in id_list:
			req0=requests.get(url='https://api.tzdjzu.com/index.php?nk={0}&barrage_switch='.format(i),headers=self.head).text
			bf1=BeautifulSoup(req0,"html.parser")
			video_url=bf1.find_all('video',id="video")[0].source['src']
			#多线程
			added_Thread=threading.Thread(target=self.down_from_url,args=(video_url,))
			threading_list.append(added_Thread)
		for i in threading_list:
			i.start()
		for i in threading_list:
			i.join()
	def search_name(self,DongM_Name):
		#搜索功能，不记得就搜索一下把，有关键字就行
		params = {"searchText":DongM_Name}
		#fireq0 = requests.get(url=self.url+'/Home/Index/search.html',params=params,headers=self.head,proxies=self.proxies).text
		fireq0 = requests.get(url=self.url+'/Home/Index/search.html',params=params,headers=self.head).text
		bf = BeautifulSoup(fireq0,"html.parser")
		texts=bf.find_all('div',style="margin-left:18px;")
		for i in texts:
			print(list(i.p.span.strings)[0],end="\n")

if __name__ == '__main__':
	#Mod='download' Mod='search'
	#download模式:明确知道动漫名字,直接下载
	#search模式 ：知道关键词搜索相关动漫名
	Mod='search'
	Search_DongM_Name='齐木'
	DongM_Download(Mod,Search_DongM_Name)

	
