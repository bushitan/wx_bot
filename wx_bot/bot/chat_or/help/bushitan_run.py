#coding=utf8
import itchat, time
from itchat.content import *
import qiniu
import subprocess ,ssl,urllib,json
# @itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
# def text_reply(msg):
#     itchat.send('%s: %s' % (msg['Type'], msg['Text']), msg['FromUserName'])
import os
BASE_DIR = os.getcwd()
IMG_FILE  = os.path.join(BASE_DIR, "img/")

@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    if msg['FromUserName'] == msg['ToUserName']:
        if os.path.exists(IMG_FILE) is False:
            os.mkdir(IMG_FILE)
        img_src = IMG_FILE + msg['FileName']
        # print img_src
        msg['Text'](img_src)

        qiniu_path = ""
        img_path,img_type = img_resize(img_src)
        # img_path = msg['FileName']
        img_upload(qiniu_path,img_type,img_path)
        print 'success', msg['FromUserName'],img_src
        itchat.send('%s' % ("success"), msg['FromUserName'])
    # return '@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName'])

# @itchat.msg_register(FRIENDS)
# def add_friend(msg):
#     itchat.add_friend(**msg['Text']) # 该操作会自动将新好友的消息录入，不需要重载通讯录
#     itchat.send_msg('Nice to meet you!', msg['RecommendInfo']['UserName'])

# @itchat.msg_register(TEXT, isGroupChat=True)
# def text_reply(msg):
#     if msg['isAt']:
#         itchat.send(u'@%s\u2005I received: %s' % (msg['ActualNickName'], msg['Content']), msg['FromUserName'])


def Identity(img_url):
        _cmd = u"magick identify %s" %(img_url)
        out_str = subprocess.check_output(_cmd, shell=True)
        arr = out_str.split('\r\n')
        frame = arr[0].split(' ')
        _space =  float(frame[7][:-2])
        if frame[7][-2:] == 'MB':
            _space = _space*1024

        #计算Geometry是否变化，
        _temp = frame[3]
        # print _temp
        _is_same_geometry = True
        for i in range(0,len(arr)-1):
            _temp_frame = arr[i].split(' ')
            # print _temp_frame
            if _temp == _temp_frame[3]:
                _is_same_geometry = False

        return {
            "frame_num":len(arr),
            "width": float(frame[2].split('x')[0]),
            "height":float(frame[2].split('x')[1]),
            "type":frame[1],
            "color_code":frame[5],
            "space":int(_space),
            "color":frame[6][:-1],
            "ratio":float(frame[2].split('x')[1])/float(frame[2].split('x')[0]), #高/宽比，
            "is_same_geometry":_is_same_geometry
        }
#img_local_path 不带后缀
# 不用转格式了，该咋咋的
def img_resize(img_local_path):
    # print img_local_path
    # magick = Magick()
    # info =  Identity(img_local_path)
    _img_type = img_local_path.split(".")[-1].lower()
    # print "type:",_img_type
    # return  img_local_path,_img_type
    # #若是gif，压缩  ,暂不执行，压缩出问题~~
    if _img_type == "gif" :
        # img_new_path = img_local_path
        # _cmd = u"magick convert -resize 180x240 %s %s" %(img_local_path,img_new_path)
        _cmd = u"magick %s %s" %(img_local_path,img_local_path)
        subprocess.check_output(_cmd, shell=True,stderr=subprocess.STDOUT)
    # else:
    #     #根据magick 还原图片实际格式
    #     img_new_path = img_local_path.split(".")[0] + "." + _img_type
    #     _cmd = u"magick convert %s %s" %(img_local_path,img_new_path)
    #     subprocess.check_output(_cmd, shell=True,stderr=subprocess.STDOUT)
    return  img_local_path,_img_type

USER_ID = "2" # “系统”用户id
USER_CATEGORY = "6" # “系统” 今日斗图目录
URL_HOST =  "https://www.12xiong.top/"
URL_GET_SESSION  = URL_HOST + "user/session/"
URL_TOKEN  = URL_HOST + "upload/token/"
# URL  = "http://192.168.199.203:8000/upload/token/"
def img_upload(qiniu_path,img_type,img_path):
    #获取token
    # key = qiniu_path + img_name + "." + img_type
    # print qiniu_path,img_type,img_path
    #获取session
    params = {
        'uid': USER_ID,
    }
    params = urllib.urlencode(params)
    context = ssl._create_unverified_context() #跳过SSL认证~~
    ret = urllib.urlopen("%s?%s"%(URL_GET_SESSION, params),context = context)
    ret_read =  ret.read().decode("utf-8-sig")
    # print ret_read
    ret_json = json.loads( ret_read)
    _session = ret_json["session"]
    # print _session

    #获取token
    params = {
        'session': _session,
        'type':img_type,
        "category_id":USER_CATEGORY,
    }
    # print params
    params = urllib.urlencode(params)
    context = ssl._create_unverified_context() #跳过SSL认证~~
    ret = urllib.urlopen("%s?%s"%(URL_TOKEN, params),context = context)
    ret_read =  ret.read().decode("utf-8-sig")
    # print ret_read
    ret_json = json.loads( ret_read)

    # print ret_json["msg"]
    #上传图片
    if ret_json["status"] == "true":
        token =  ret_json["token"]
        key = ret_json["key"]
        ret, info = qiniu.put_file(token,key, img_path)
        # print ret
        if ret["status"] == "true":
            return True
    return False

itchat.auto_login()
itchat.run()

# if __name__ == "__main__":
#     msg = {"FileName":"170305-001248.gif"}
#     qiniu_path = ""
#     img_type = img_resize(msg['FileName'])
#     img_path = msg['FileName']
#     img_upload(qiniu_path,img_type,img_path)
#     params = {
#         'uid': "1",
#     }
#     params = urllib.urlencode(params)
#     context = ssl._create_unverified_context() #跳过SSL认证~~
#     ret = urllib.urlopen("%s?%s"%(URL_GET_SESSION, params),context = context)
#     ret_read =  ret.read().decode("utf-8-sig")
#     # print ret_read
#     ret_json = json.loads( ret_read)
#     _session = ret_json["session"]
#     print _session