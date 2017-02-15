# -*- coding: utf-8 -*-

from django.conf.urls import url
from bot.views import *
urlpatterns = [

   #
   url(r'^bot/index/$', BotIndex.as_view()),
   url(r'^bot/user/login/$', UserLogin.as_view()),
   url(r'^bot/qr/status/$', QRStatus.as_view()),

   url(r'^bot/receive_callback/$', ReceiveCallback.as_view()),

   url(r'^bot/reply/$', Reply.as_view()),


   # url(r'^magick/join/$', UserLogin.as_view()),

]