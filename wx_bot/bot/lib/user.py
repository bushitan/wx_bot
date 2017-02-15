#coding:utf-8
import requests
import re

class User(object):
	def __init__(self):
		pass
	BASE_URL = 'https://login.weixin.qq.com'
	USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
	#获取uuid
	def Get_QRuuid(self):
		url = '%s/jslogin' % self.BASE_URL
		params = {
			'appid' : 'wx782c26e4c19acffb',
			'fun'   : 'new', }
		headers = { 'User-Agent' : self.USER_AGENT }
		s = requests.Session()
		r = s.get(url, params=params, headers=headers)
		regx = r'window.QRLogin.code = (\d+); window.QRLogin.uuid = "(\S+?)";'
		data = re.search(regx, r.text)
		if data and data.group(1) == '200':
			uuid = data.group(2)
			return uuid

	#二维码链接
	def Get_QRurl(self,uuid = None):
		return  '%s/qrcode/%s' % (self.BASE_URL, uuid)

	USER_INFO = [{
		"uid":"1",
		"user_name":"11",
		"password":"11",
		"is_login":False,
		"is_scan":0,  # 0 未扫描  ，1 已扫描 ，2 超时
		"uuid":"ab",
		"auto_reply":{"1":"123","2":"wqe"},
		"talk_data":"",
	}]

	#增加用户信息
	def AddUser(self,uid = None,*args, **kwargs):
		user = self.GetUser(uid = uid)
		if user :
			return False
		user = {
			"uid":uid,
			"is_scan":0,
		}
		for key in kwargs:
			user[key] = kwargs[key]
		self.USER_INFO .append(user)

	#设置用户信息
	def SetUser(self,uid = None,*args, **kwargs):
		user = self.GetUser(uid = uid)
		for key in kwargs:
			user[key] = kwargs[key]

	#获取用户信息
	def GetUser(self,uid = None , uuid = None):
		for user in self.USER_INFO:
			if str(user["uid"]) == str(uid) :
				return user
			if  user["uuid"] == uuid: #启动时候添加回复
				return user
		return False

	#按条件查询用户是否存在
	def Check(self,**kwargs):
		count = len(kwargs)
		if count == 0 :
			return False
		for user in self.USER_INFO:
			index = 0
			for key in kwargs:
				if user[key] == kwargs[key]:
					index = index + 1
				if index == count:
					return user
		return False


if __name__ == "__main__":
	u = User()
	# u.SetUser(uid = 1,uuid = 23)
	print u.Check(user_name ="11",password="11" )