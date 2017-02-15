# -*- coding: utf-8 -*-
from django.test import TestCase
import requests
# Create your tests here.
BASE_HOST = 'http://192.168.200.27:8000/'
# url =  BASE_HOST + "bot/reply/"
url =  BASE_HOST + "bot/receive_callback/"
params = { 'uuid':'gYN-IkhV_g=='}
s = requests.Session()
postQr = s.get(url, params=params)
print postQr.text