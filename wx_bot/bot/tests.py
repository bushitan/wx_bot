# -*- coding: utf-8 -*-
from django.test import TestCase
import requests
# Create your tests here.
# BASE_HOST = 'http://192.168.200.27:8000/'
# # url =  BASE_HOST + "bot/reply/"
# url =  BASE_HOST + "bot/receive_callback/"
# params = { 'uuid':'gYN-IkhV_g=='}
# s = requests.Session()
# postQr = s.get(url, params=params)
# print postQr.text
'''
download_fn:
<new_itchat.core.Core object at 0x025D2F90>
<Response [200]>
https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxgetmsgimg
{'msgid': 4704996205557820628L, 'skey': u'@crypt_2c1738d0_b04b0057e72da5c9cead911a3f4dc159'}
{'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}

https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxgetmsgimg?msgid=2679422332675280357L&skey=@crypt_2c1738d0_cdbb804101a27456328c8aac55343236
'''

import xml.sax
import xml.sax.handler
msg = u'''
<msg>
	<emoji fromusername = "bushitan" tousername = "bushitan" type="1" idbuffer="media:0_0" md5="96290a82ef6fd6388baea885cee38df1" len = "93371" productid="" androidmd5="96290a82ef6fd6388baea885cee38df1" androidlen="93371" s60v3md5 = "96290a82ef6fd6388baea885cee38df1" s60v3len="93371" s60v5md5 = "96290a82ef6fd6388baea885cee38df1" s60v5len="93371" cdnurl = "http://emoji.qpic.cn/wx_emoji/4iaDDq8CCF7ILQEvmicu7Ht8ax7T5PiaX5iaS243vXdsUibwjjpv0y0Ziacg/" designerid = "" thumburl = "" encrypturl = "http://emoji.qpic.cn/wx_emoji/4iaDDq8CCF7ILQEvmicu7Ht8ax7T5PiaX5iaqjsW6wcWg5EAmdcvbJPXdQ/" aeskey= "d482c7d637ae3dd43dfe5b38923294f3" width= "400" height= "400" >
	</emoji>
</msg>
'''
msg = u'''
<?xml version="1.0"?>
<msg>
	<img aeskey="6c104ef90ed84fc09706217a1bbfd8a4" encryver="1" cdnthumbaeskey="6c104ef90ed84fc09706217a1bbfd8a4" cdnthumburl="305002010004493047020100020425c2bf0602033d14bb02040c813379020458ba91f20425617570696d675f396331613864323032323538303735315f313438383632323036353134350201000201000400" cdnthumblength="7983" cdnthumbheight="120" cdnthumbwidth="120" cdnmidheight="0" cdnmidwidth="0" cdnhdheight="0" cdnhdwidth="0" cdnmidimgurl="305002010004493047020100020425c2bf0602033d14bb02040c813379020458ba91f20425617570696d675f396331613864323032323538303735315f313438383632323036353134350201000201000400" length="25807" cdnbigimgurl="305002010004493047020100020425c2bf0602033d14bb02040c813379020458ba91f20425617570696d675f396331613864323032323538303735315f313438383632323036353134350201000201000400" hdlength="4508" md5="ebe7464720a2ac1ccc91c6ac0ec65669" />
</msg>
'''
input_xml_string = """
                   <root>
                        <item>
                            <data version="1.0" url="http://***" />
                            <data version="2.0" url="http://***" />
                         </item>
                         <other>
                             <data version="1.0" url="http://***" />
                             <data version="2.0" url="http://***" />
                          </other>
                     </root>
                     """
import xml.dom.minidom
doc = xml.dom.minidom.parseString(msg)
# print doc
for node in doc.getElementsByTagName("emoji"):
	if node.getAttribute("cdnurl") != "":
		print  node.getAttribute("cdnurl")
	# print (node, node.tagName, node.getAttribute("cdnurl"))

import ssl
import httplib, urllib,urllib2
url = "https://www.12xiong.top/img/add/url"
cdn_url = "http://emoji.qpic.cn/wx_emoji/68tn3AkhCqWflsbaVLkniayPHvLgKVtPUTCSIaxZFQ2Ovawy0xbCP7g/"
print cdn_url.split("/")[-1]
# params = {
#     'img_url': cdn_url,
# }
# params = urllib.urlencode(params)
# context = ssl._create_unverified_context() #跳过SSL认证~~
# ret = urllib.urlopen("%s?%s"%(url, params),context = context)
# print ret
# ret_read =  ret.read().decode("utf-8-sig")
# print ret_read
# ret_json = json.loads( ret_read)
# print ret_json
# itchat.send('%s' % ("上传成功"), msg['FromUserName'])