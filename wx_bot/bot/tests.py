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


import xml.sax
import xml.sax.handler
msg = u'''
<msg>
	<emoji fromusername = "bushitan" tousername = "bushitan" type="1" idbuffer="media:0_0" md5="96290a82ef6fd6388baea885cee38df1" len = "93371" productid="" androidmd5="96290a82ef6fd6388baea885cee38df1" androidlen="93371" s60v3md5 = "96290a82ef6fd6388baea885cee38df1" s60v3len="93371" s60v5md5 = "96290a82ef6fd6388baea885cee38df1" s60v5len="93371" cdnurl = "http://emoji.qpic.cn/wx_emoji/4iaDDq8CCF7ILQEvmicu7Ht8ax7T5PiaX5iaS243vXdsUibwjjpv0y0Ziacg/" designerid = "" thumburl = "" encrypturl = "http://emoji.qpic.cn/wx_emoji/4iaDDq8CCF7ILQEvmicu7Ht8ax7T5PiaX5iaqjsW6wcWg5EAmdcvbJPXdQ/" aeskey= "d482c7d637ae3dd43dfe5b38923294f3" width= "400" height= "400" >
	</emoji>
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