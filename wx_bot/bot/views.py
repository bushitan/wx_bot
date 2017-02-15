#coding:utf-8
from django.views.decorators.csrf import csrf_exempt
import httplib, urllib,urllib2
from django.http import HttpResponse, Http404
from bot.models import *
from django.views.generic import View, TemplateView, ListView, DetailView
import logging
import os
import sys
import wx_bot.settings as SETTING
# logger
logger = logging.getLogger(__name__)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

import subprocess
import re
import json
from django.db import transaction #事务

from bot.lib.user import User
userLib = User()

BOT_RUN_FILE_PATH = SETTING.BASE_DIR + r'\bot\chat\bot_run.py'

print BOT_RUN_FILE_PATH
class BotIndex(ListView):
    template_name = 'bot_index.html'
    qr_url = ""
    # init_file_name = 5
    def get(self, request, *args, **kwargs):

        _uid = request.GET.get("uid", "")
        print _uid
        user = userLib.GetUser(uid = _uid) #获取用户信息
        print user

        if user : #已登录
            uuid = userLib.Get_QRuuid() #获取uuid
            self.uuid = uuid
            user["uuid"] = uuid #用户同步uuid
            userLib.SetUser(uid = user["uid"], uuid=uuid) #获取二维码链接
            self.auto_reply = user["auto_reply"] #准备将回复模板传到前端
            self.qr_url = userLib.Get_QRurl( uuid =uuid) #获取二维码链接
            _cmd = u'python '+ BOT_RUN_FILE_PATH + "  " + uuid + "  " + SETTING.BASE_HOST #运行脚本
            print _cmd
            subprocess.Popen(_cmd, shell=True) #启动项目
        else:#未登录情况
            mydict = {"msg":u"用户未登录"}
            return HttpResponse(
                json.dumps(mydict),
                content_type="application/json"
            )
            # self.uuid = 123
            # self.auto_reply = None
            # pass
        return super(BotIndex, self).get(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context =super(BotIndex, self).get_context_data(**kwargs)
        context['qr_url'] = self.qr_url
        context['uuid'] = self.uuid
        context['auto_reply'] = self.auto_reply
        return context
    def get_queryset(self):
        pass
    def post(self, request, *args, **kwargs):
        pass

class UserLogin(ListView):
    template_name = 'bot_login_user.html'
    def get(self, request, *args, **kwargs):
        # uuid = request.GET.get("uuid", "")
        return super(UserLogin, self).get(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context =super(UserLogin, self).get_context_data(**kwargs)
        return context
    def get_queryset(self):
        pass
    def post(self, request, *args, **kwargs):
        print "OK",request
        _register = request.POST.get("register", "")
        _user_name = request.POST.get("user_name", "")
        _password = request.POST.get("password", "")
        _uid = "2"
        #用户注册
        if _register:
            userLib.AddUser(uid = _uid,user_name = _user_name,password = _password ,is_login=False, uuid = '',auto_reply = {"a":"mnm","b":"pop"},talk_data = '')
            mydict = {'is_login':'false', 'msg':u'注册成功'}
        else:
            user = userLib.Check( user_name = _user_name,password =  _password )
            if user:
                mydict = {'is_login':'true','msg':u'登陆成功',"uid":user["uid"] }
            else :
                mydict = {'is_login':'false','msg':u'登陆失败'}
        # print mydict,USER_INFO
        return HttpResponse(
            json.dumps(mydict),
            content_type="application/json"
        )
import time
#查询二维码是否扫描，若已经扫描，则登陆成功
# 0 未扫描  ，1 已扫描 ，2 超时
QR_WATER_SCAN = '0'
QR_IS_SCAN = '1'
QR_TIME_OUT = '2'
class QRStatus(ListView):
    #bot线程，更改is_scan状态
    def get(self, request, *args, **kwargs):

        _uuid = request.GET.get("uuid", "")
        _is_scan =  request.GET.get("is_scan", "")
        _user_name =  request.GET.get("user_name", "")

        user = userLib.GetUser( uuid = _uuid)
        print user,_uuid
        userLib.SetUser(uid = user["uid"],is_scan = _is_scan )
        # user["is_scan"] = _is_scan
        # print 123,uuid,is_login,user_name
        mydict = {"msg":"scan ok"}
        return HttpResponse(
            json.dumps(mydict),
            content_type="application/json"
        )

    #前端，查询is_scan状态
    def post(self, request, *args, **kwargs):
        _uuid = request.POST.get("uuid", "")
        user = userLib.GetUser( uuid = _uuid)
        #长连接轮训二维码扫描情况
        step = 0
        while step<50:
            # print "step:",step
            if user["is_scan"] == QR_IS_SCAN :
                mydict = {'qr_status':QR_IS_SCAN, 'msg':u'已扫描，登陆成功'}
                return HttpResponse(
                    json.dumps(mydict),
                    content_type="application/json"
                )
            if user["is_scan"] == QR_TIME_OUT:
                mydict = {'qr_status':QR_TIME_OUT, 'msg':u'二维码超时，请重新登录'}
                return HttpResponse(
                    json.dumps(mydict),
                    content_type="application/json"
                )
            step = step + 1
            time.sleep(0.1)

        mydict = {'qr_status':QR_WATER_SCAN, 'msg':u'二维码未扫描'}
        # print mydict
        return HttpResponse(
            json.dumps(mydict),
            content_type="application/json"
        )


class ReceiveCallback(ListView):
    def get(self, request, *args, **kwargs):
        uuid = request.GET.get("uuid", "")
        # is_login =  request.GET.get("is_login", "")
        # user_name =  request.GET.get("user_name", "")

        # print uuid
        #Todo uuid查询用户
        user = userLib.GetUser( uuid = uuid )

        # print "ReceiveCallback:", user["auto_reply"]
        mydict = {
            "auto_reply":user["auto_reply"]
        }
        return HttpResponse(
            json.dumps(mydict),
            content_type="application/json"
        )


class Reply(ListView):
    def get(self, request, *args, **kwargs):
        _uuid = request.GET.get("uuid", "")
        user = userLib.GetUser( uuid = _uuid)
        mydict = {"auto_reply":user["auto_reply"]}
        print mydict
        return HttpResponse(
            json.dumps(mydict),
            content_type="application/json"
        )

    def post(self, request, *args, **kwargs):
        _uuid = request.POST.get("uuid", "")
        user = userLib.GetUser( uuid = _uuid)
        _reply = request.POST.get("reply", "")
        # print _reply
        _reply_dict = json.loads(_reply)
        # print _reply_dict
        # print user
        userLib.SetUser(uid = user["uid"],auto_reply=_reply_dict)
        print userLib.GetUser( uuid = _uuid)
        # user["auto_reply"] = _reply_dict  #直接更改user_reply 的key
        mydict = {"msg":u"回复模板设置成功"}
        return HttpResponse(
            json.dumps(mydict),
            content_type="application/json"
        )

















