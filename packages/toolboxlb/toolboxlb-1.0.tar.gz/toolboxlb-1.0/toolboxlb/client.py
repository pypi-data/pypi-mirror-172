import time
import re
import platform
import uuid
import http.client
import json
import socket
from os import system as sys
import requests
class Client:
	def __init__(self):
		self.online = False
	def checkinet(self):
		print("Проверка вашего интернет соеденения(по средством отправки запроса на сервер google)")
		try:
			res = requests.get('https://google.com')
			print("интернет доступен")
			self.online = True
			print(res)
		except:
			print("интернет недоступен")
			
	def sleep(self, seccond):
		time.sleep(seccond)
	def clear(self):
		sys("clear || cls")
	def seccondo(self):
		self.sec = 0
		while True:
			self.sec = self.sec + 1
			print(f"          {self.sec}       ")
			time.sleep(1)
	def timer(self, secc):
		self.seccc = 0
		self.seccc = self.seccc + secc
		while True:
			print(f"     Осталось {self.seccc} секунд    ")
			time.sleep(1)
			self.seccc = self.seccc - 1
			if self.seccc < 0:
				try:
					try:
						break
					except:
						break
				except:
					pass
			else:
				pass
	def installmod(self, module):
		print("Это часть установки модуля")
		try:
			self.mod = sys(f"pip install {module}")
			print(f"Установка модуля {module} прошла успешно")
		except:
			print(f"Непредвиденная ошибка {self.mod}")
	def update_pip(self):
		print("Обновление pip")
	def get_ip(self):
		self.conn = http.client.HTTPConnection("ifconfig.me")
		self.conn.request("GET", "/ip")
		self.vip = self.conn.getresponse().read()
		print(f"{self.vip}")
	def get_mac(self):
		self.mac = ':'.join(re.findall('..', '%012x' % uuid.getnode())).upper()
		print(f"{self.mac}")
	def get_platform(self):
		self.jost = platform.uname()
		print(f"{self.jost}")
	def get_request(self, url):
		res = requests.get(url)
	def request(self, url):
		req = requests.get(url)
		neq = requests.delete(url)
		print(neq)
		peq = requests.head(url)
		print(peq)
		teq = requests.put(url)
		print(teq)
		quq = requests.options(url)
		print(quq)
		
	def requestm(self, url):
		print("Отправка get и post, и head запроса на любой сервер на ваш выбор в целях проверки онлайн ли сервер")
		self.get = requests.get(url)
		self.post = requests.post(url)
		self.head = requests.head(url)
		print(f"get and post and head request has send, response >>\n get>> {self.get}\n post>> {self.post}\n head>> {self.head}")
		
