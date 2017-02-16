# -*- coding: utf-8 -*-
import new_itchat as itchat , time
from new_itchat.content import *
import new_itchat.config as config
from filter import Filter
import glob
import random
import requests
import json

#群消息
# @itchat.msg_register(TEXT, isFriendChat=True, isGroupChat=True, isMpChat=True)
# def general_reply(msg):
#     return 'I received a %s' % msg['Type']

#私聊
AUTO_REPLY = {}

BASE_HOST =  'http://192.168.200.27:8000/'
# rece = {"1":123321}
    # print msg['MsgType'],msg['AppMsgType'],msg['FromUserName'],msg['ToUserName'],msg['Url'],msg['FileName'],msg['Content']
    # itchat.send('%s: %s' % (msg['Type'], msg['Text']), msg['FromUserName'])
    # itchat.send('%s: %s' % (msg['Type'], msg['Url']), msg['FromUserName'])
    # itchat.send('%s: %s' % (msg['Type'], msg['Content']), msg['FromUserName'])
    # itchat.send('@img@%s' % '170210-105741.gif',msg['FromUserName'])
    # itchat.send('@img@%s' % '170210-105741.gif',msg['FromUserName'])
    # itchat.send('%s: %s' % (msg['Type'], msg['Text']), msg['FromUserName'])

@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    print msg['MsgType']
    print msg['Content']
    # msg['Text'](msg['FileName'])
    # url = {'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil')
    # msg = msg['FileName']
    # # print msg
    # print  url,msg


    # _gif_all =  glob.glob(r"E:\CarcerWorld\code\Python\git\image_str\image_server\wx_app\lib\robote/*.gif")
    # print _gif_all[0]
    # msg['Text'](msg['FileName'])
    # _ran_index = int(random.random()*(len(_gif_all)-1))
    # return '@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), _gif_all[_ran_index])

    # return '@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName'])
# itchat.send('@%s@%s' % (url,_gif_all[0]), msg['FromUserName'])

    # print msg['MsgType']
    # print msg['Content']
    # print msg['MsgType'],msg['AppMsgType'],msg['FromUserName'],msg['ToUserName'],msg['Url'],msg['FileName'],msg['Content']
    # itchat.send('@%s@%s' % (url,msg), msg['FromUserName'])
    # itchat.send('%s' % ( msg['Content'] ), msg['FromUserName'])
    # return '@%s@%s' % (url,msg)

@itchat.msg_register(FRIENDS)
def add_friend(msg):
    # print msg
    itchat.add_friend(**msg['Text']) # 该操作会自动将新好友的消息录入，不需要重载通讯录
    # itchat.send_msg('Nice to meet you!', msg['RecommendInfo']['UserName'])
    itchat.send_msg(u'公众号信息分享给我，所有图片自动转表情', msg['RecommendInfo']['UserName'])
    itchat.send_msg(u'存储空间不够了？搜索“表情袋”，斗图再多也能存!', msg['RecommendInfo']['UserName'])

@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    pass
    # print msg
    # if msg['isAt']:
    #     itchat.send(u'@%s\u2005I received: %s' % (msg['ActualNickName'], msg['Content']), msg['FromUserName'])

@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO], isGroupChat=True)
def download_files_group(msg):
    pass
    # print msg["Type"], msg["MsgType"] , msg['Url']
    # msg['Text'](msg['FileName'])
    # if msg['isAt']:
    #     msg['Text'](msg['FileName'])
    #     return '@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName'])




@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    print msg

    content = msg['Content']
    if msg['FromUserName'] == msg['ToUserName']:
        print content
        WORD_CLEAR = u"自助回复清除成功"
        WORD_ADD = u"自助回复增加成功"
        WORD_UPDATE = u"自助回复更新成功"
        if content == "QC": #清除
            AUTO_REPLY.clear()
            itchat.send('%s' % (WORD_CLEAR), msg['FromUserName'])
            return
        sub = content.split("Q")
        if len(sub) == 3:
            q = sub[1]
            a = sub[2]
            AUTO_REPLY[q] = a
            itchat.send('%s' % (WORD_ADD), msg['FromUserName'])
            return

    if  msg['Type'] == 'Text':
        if AUTO_REPLY.has_key(content):
            itchat.send('%s' % (AUTO_REPLY[content]), msg['FromUserName'])
            return

    if  msg['Type'] == 'Sharing':
        imgFilter = Filter()
        img_list = imgFilter.getContents(msg['Url'])
        i=0
        for img in img_list:
            print img_list,img,i
            i = i+1
            itchat.send('@img@%s' % str(i)+".gif" ,msg['FromUserName'])

QR_WATER_SCAN = '0'
QR_IS_SCAN = '1'
QR_WATER_LOGIN = '2'
QR_TIME_OUT = '3'
QR_LOGIN = '4'
QR_EXIT = '5'


class QRCallback:
    def __call__(self ,uuid = None, status = None ):
        print "qr call back:",uuid,status
        is_scan = QR_WATER_SCAN
        if status == '201':
            is_scan = QR_IS_SCAN
        elif status == '200':
            is_scan = QR_LOGIN
        elif status != '408':
            is_scan = QR_TIME_OUT
        print str(uuid) + "user qr..."
        url =  BASE_HOST + "bot/qr/status/"
        params = { 'uuid':uuid ,'is_scan':is_scan}
        s = requests.Session()
        postQr = s.get(url, params=params)
        print "itchat post qr callback success:", postQr


#登陆成功，提示前台
class loginCallBack:
    def __call__(self , uuid = None,userName = None , nickName = None):
        print "login call back:",uuid,userName,nickName
        # print str(uuid) + "user login..."
        url =  BASE_HOST + "bot/qr/status/"
        params = { 'uuid':uuid ,'is_scan':QR_LOGIN,'user_name':userName}
        s = requests.Session()
        postQr = s.get(url, params=params)
        print "itchat post logincallback success:", postQr
        # Todo 登陆成功，同步 自动回复列表
#退出
class Exit():
    def __call__(self , uuid = None):
        print "exit call back:",uuid
        # print str(uuid) + "user login..."
        url =  BASE_HOST + "bot/qr/status/"
        params = { 'uuid':uuid ,'is_scan':QR_EXIT}
        s = requests.Session()
        postQr = s.get(url, params=params)
        print "itchat post logincallback success:", postQr


#上传数据至服务器，并下载将要执行的操作
class Receive():
    def __call__(self,uuid = None):
        # print 'rece',rece
        # url =  BASE_HOST + "bot/update_reply/"
        url =  BASE_HOST + "bot/receive_callback/"
        params = { 'uuid':uuid}
        s = requests.Session()
        postQr = s.get(url, params=params)
        # print "Receive:", postQr
        _dict = json.loads(postQr.text)

        #Todo 如果存在auto_reply，更新自动回复
        if _dict.has_key("auto_reply"):
            _reply_dict = _dict["auto_reply"]
            AUTO_REPLY.clear()
            for i in _reply_dict:
                AUTO_REPLY[i] = _reply_dict[i]
        # print "Receive:",AUTO_REPLY

        # params = { 'uuid':self.uuid,}
        # s = requests.Session()
        # postQr = s.get(url, params=params)
        # print postQr
        # print json.loads(postQr.text)
        # return json.loads(postQr.text)


alive = True
#测试专用线程
def testThread ( receiveCallback = None):
    while alive:
        receiveCallback()
        time.sleep(5)

import sys
if __name__ == '__main__':
    # uuid = "ab"
    # loginCall = loginCallBack(uuid)
    # loginCall()
    uuid = sys.argv[1]
    BASE_HOST = sys.argv[2]
    print BASE_HOST
    print 534543, uuid
    qr = QRCallback()
    loginCall = loginCallBack()
    receive =  Receive()
    exit = Exit()
    itchat.auto_login(uuid=uuid,qrCallback = qr,loginCallback = loginCall , receiveCallback = receive , exitCallback = exit ) #hack 做设置回调
    itchat.run()

    # uuid = '2'
    # BASE_HOST =  'http://192.168.200.27:8000/'
    # qr = QRCallback()
    # qr(uuid,BASE_HOST)

    # testThread( receiveCallback = receive)



    # itchat.auto_login(uuid=uuid)


