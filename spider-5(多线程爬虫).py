import threading
import requests
import os
from lxml import etree
from queue import Queue
import random
import time

class ThreadSpider(threading.Thread):
	"""docstring for ThreadSpider"""
	def __init__(self, func, status):
		super(ThreadSpider, self).__init__()
		self.func = func
		self.status = status

	def run(self):
		print(self.status)
		self.func()

class MainSpider(object):
	"""docstring for MainSpider"""
	def __init__(self):
		self.header = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36"}
		self.pageUrl_Queue = Queue()
		self.dict_Queue = Queue()
	
	def tree_requests(self,url):	
		r = requests.get(url=url,headers=self.header)
		tree = etree.HTML(r.text)
		return tree

	def get_Home_Total_Page(self):
		url = "http://www.fanjian.net/"
		total_page = self.tree_requests(url).xpath('//div[@class="pager"]/span[@class="fc-gray"]/text()[1]')[0].strip("共 页，跳至")
		return int(total_page)

	def create_Page_Url(self):
		print(self.get_Home_Total_Page())
		for i in range(100):
			print("正在向1号队列中存放第 %d 个url---------"%i)
			self.pageUrl_Queue.put("http://www.fanjian.net/latest-" + "%d"%i)

	def crawl_page(self):
		while True:
			print("正在向1号队列中获取url---------")
			try:
				pageUrl = self.pageUrl_Queue.get(True,3)
			except Exception:
				print("1号队列已空----->>>>")
				break
			tree = self.tree_requests(pageUrl)
			title_list = tree.xpath('//li[@class="cont-item"]/h2/a/text()')
			img_list = tree.xpath('//li[@class="cont-item"]/div[@class="cont-list-main"]/p/img/@data-src')
			print("正在向2号队列中存放字典数据---------")
			self.dict_Queue.put(dict(zip(title_list,img_list)))
			if self.pageUrl_Queue.empty():
				break

	def download_img(self):
		if not os.path.exists("word"):
			os.mkdir("word")
		while True:
			try:
				print("正在向2号队列中获取字典数据********")
				title_img_dict = self.dict_Queue.get(True,5)
			except Exception:
				print("2号队列已空，正在结束线程----->>>>>>")
				break
			num = random.randint(0,10000)
			with open("./word/sss-%s.txt"%num,"a",encoding="utf8") as fp:
				for title, src in title_img_dict.items():
					string = title + ":  " + src + "\n"
					print("正在写入文件：sss-%s.txt"%num)
					fp.write(string)

def not_thread():
	sp = MainSpider()
	sp.create_Page_Url()
	sp.crawl_page()
	sp.download_img()

def have_thread():
	sp = MainSpider()
	thread_list = []
	thread_url = ThreadSpider(sp.create_Page_Url, "存放url的线程----")
	thread_list.append(thread_url)
	for i in range(8):
		thread_title = ThreadSpider(sp.crawl_page, "解析网页的线程----%d" % i)
		thread_picture = ThreadSpider(sp.download_img, "写入文件的线程----%d" % i)
		thread_list.append(thread_title)
		thread_list.append(thread_picture)
	
	for onethread in thread_list:
		onethread.start()
	
	for onethread in thread_list:
		onethread.join()

if __name__ == '__main__':
	start_time = time.time()
	have_thread()
	end_time = time.time()
	print("本次程序运行时间为：%.2f 秒"%(end_time - start_time))









