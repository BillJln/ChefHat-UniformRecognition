#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
# from Crypto.PublicKey import RSA
import base64,rsa,json,time
from flask import Flask,jsonify,request
from flask_script import Manager
from PIL  import Image, ImageDraw, ImageFont, ImageFilter
import sys,os,shutil
import base64
import random
import uuid
import json
import numpy as np
import platform
import datetime,time
import logging,logging.handlers,io
import xml
import cv2
# reload(sys)
# sys.setdefaultencoding('utf-8')
from flask import make_response,send_file
from configparser import ConfigParser

CONFIGFILE = "ip.cfg"

config = ConfigParser()
# 读取配置文件
config.read(CONFIGFILE)


# http:/api.hx-ai.com:5000/V1/ocr/license_plate
# APP_ID = '33333332'
# API_KEY = 'kEmeVW243444406o47oMFfA'
# SECRET_KEY = 'OyhdkY34566646DSFGRHRGDSAqt3Gfa'


sysstr = platform.system()


basedir = os.path.abspath(os.path.dirname(__file__))
file_name =os.path.basename(__file__)

# app = Flask(__name__)
app = Flask(__name__, static_url_path='', static_folder='static')
manager = Manager(app)

def walkFolders(folder):
    folders_Name = []
    files_Name = []
    folders_Count = 0
    files_Count = 0
    isExists = os.path.exists(folder) # 判断路径是否存在

    if isExists == False:
        print(folder,'no exist')
        return files_Count, folders_Count, files_Name, folders_Name
    folders = os.listdir(folder)
    for item in folders:

        curname = os.path.join(folder,item)
        if (sysstr == "Windows"):
            us = item.decode('gbk').encode('utf-8')
        else:
            us =item
        if os.path.isdir(curname):

            folders_Name.append(us)
            folders_Count = folders_Count + 1
        elif os.path.isfile(curname):

            files_Name.append(us)
            files_Count = files_Count + 1
    return files_Count,folders_Count,files_Name,folders_Name
def mymkdir(path):
    path=path.strip()  # 去除首位空格
    path=path.rstrip("/")    # 去除尾部 \ 符号
    isExists = os.path.exists(path) # 判断路径是否存在

    if isExists == False:
        print(str(path)+'  create folder success')
        try:
            os.makedirs(path)  # 创建目录操作函数
        except:
            print("makedirs failure")
    else:
        print(str(path) + '  isExists')

    return True
def myromvefile(file_path):
    # 判断文件是否存在
    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        print("要删除的文件不存在！")
def mymovefile(srcfile,dstfile):
    if not os.path.isfile(srcfile):
        print("%s not exist!"%(srcfile))
    else:
        fpath,fname=os.path.split(dstfile)    #分离文件名和路径
        if os.path.exists(fpath) == False:
            os.makedirs(fpath)                #创建路径
        shutil.move(srcfile,dstfile)          #移动文件

        print("move %s -> %s"%( srcfile,dstfile))
def mycopyfile(srcfile,dstfile):
    if not os.path.isfile(srcfile):
        print("%s not exist!"%(srcfile))
    else:
        fpath,fname=os.path.split(dstfile)    #分离文件名和路径
        if os.path.exists(fpath) == False:
            os.makedirs(fpath)                #创建路径
        shutil.copyfile(srcfile,dstfile)      #复制文件
        print("copy %s -> %s"%( srcfile,dstfile))
def base64_url_decode(inp):
    # 通过url传输时去掉了=号，所以需要补上=号
    import base64
    return base64.urlsafe_b64decode(str(inp + '=' * (4 - len(inp) % 4)))
def base64_url_encode(inp):
    import base64
    return base64.urlsafe_b64encode(str(inp)).rstrip('=')
# 判断文件是否为有效（完整）的图片
# 输入参数为bytes，如网络请求返回的二进制数据
def IsValidImage4Bytes2(buf):
    bValid = True
    if buf[6:10] in (b'JFIF', b'Exif'):  # jpg图片
        if not buf.rstrip(b'\0\r\n').endswith(b'\xff\xd9'):
            bValid = False
    else:
        try:
            Image.open(io.BytesIO(buf)).verify()
        except:
            bValid = False

    return bValid
def IsValidImage4Bytes(buf):
    bValid = True

    try:
        Image.open(io.BytesIO(buf)).verify()
    except:
        bValid = False

    return bValid


import socket
import re

def get_ip(*args):
    if platform.system() == 'Windows':
        # my_name = socket.getfqdn(socket.gethostbyname('localhost'))
        # my_addr = socket.gethostbyname(my_name)
        # ip = my_addr.split('\n')[0]
        # return ip
        return socket.gethostbyname(socket.gethostname())

    else:
        # my_addr = os.popen("ifconfig | grep -A 1 %s|tail -1| awk '{print $2}'" % args[0]).read()

        # my_addr = os.popen("ifconfig | grep -A 1 %s | grep 'inet addr:' | grep -v '127.0.0.1' | cut -d: -f2 | awk '{print $1}' | head -1" % args[0]).read()
        my_addr = os.popen("ifconfig | grep -A 1 %s | grep 'inet addr:' | grep -v 'config['numbers'].get('host')' | cut -d: -f2 | awk '{print $1}' | head -1" % args[0]).read()
        # ip_STR = re.search(r'(?<![\.\d])(?:25[0-5]\.|2[0-4]\d\.|[01]?\d\d?\.)'\
        #                         r'{3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)(?![\.\d])',my_addr).group()
        # out = os.popen("ifconfig | grep 'inet addr:' | grep -v '127.0.0.1' | cut -d: -f2 | awk '{print $1}' | head -1").read()


        ip_STR = my_addr.split('\n')[0]
        return ip_STR

flag_lpr="myLPR"
# flag_lpr="hyperLPR"
env_dist = os.environ # environ是在os.py中定义的一个dict environ = {}
# for key in env_dist:
#     print(key + ' : ' + env_dist[key])
rootSaveFile = "D:/AI_CV/test"
if 'rootSaveFile' in env_dist.keys():
    rootSaveFile = env_dist['rootSaveFile']
    print('env rootSaveFile:',rootSaveFile)
else:
    print('no load ENV rootSaveFile, use default:',rootSaveFile)


my_ip_str_ = get_ip('ens3')  # enp7s0
if 'serverHostIp' in env_dist.keys():
    my_ip_str_ = env_dist['serverHostIp']
    print('env serverHostIp:',my_ip_str_)
else:
    print('no load ENV serverHostIp, get_ip:',my_ip_str_)

my_portCode='5000'
if 'serverHostPort' in env_dist.keys():
    my_portCode = env_dist['serverHostPort']
    print('env serverHostPort:',my_portCode)
else:
    print('no load ENV serverHostPort, use default:',my_portCode)




if(sysstr =="Windows"):
    rootSaveFile ='D:/AI_CV/test'
else:
    rootSaveFile='/home/data'


BIYI_COMP_LOG_PATH = rootSaveFile+'/BIYI_COMP_LOG_PATH'
if 'BIYI_COMP_LOG_PATH' in env_dist.keys():
    BIYI_COMP_LOG_PATH=env_dist['BIYI_COMP_LOG_PATH']
    print('BIYI_COMP_LOG_PATH: ', BIYI_COMP_LOG_PATH)
else:
    print('no load ENV BIYI_COMP_LOG_PATH,USE DEFAULI',BIYI_COMP_LOG_PATH)
mymkdir(BIYI_COMP_LOG_PATH)


# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
# rf_handler = logging.handlers.TimedRotatingFileHandler('imageAPI_logger.log', when='midnight', interval=1, backupCount=30, atTime=datetime.time(0, 0, 0, 0))
# rf_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
# rf_handler.suffix="%Y%m%d-%H%M.log"
# logger.addHandler(rf_handler)

# 第一步，创建一个logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO) # Log等级总开关
# 第二步，创建一个handler，用于写入日志文件
rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
log_path = rootSaveFile + '/imageAPILogs/'
if(sysstr =="Windows"):
    log_path = rootSaveFile + '\\imageAPILogs\\'
mymkdir(log_path)
log_name = log_path + rq + '.log'
logfile = log_path +'imageAPI_logger.log'
rf_handler = logging.handlers.TimedRotatingFileHandler(logfile, when='midnight', interval=1, backupCount=30, atTime=datetime.time(0, 0, 0, 0))

# 第三步，定义handler的输出格式
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
rf_handler.setFormatter(formatter)
# rf_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
rf_handler.suffix="%Y%m%d-%H%M.log"
logger.addHandler(rf_handler)




foldercount = 0
foldername = []


test_flag =0




img_folder_manholecover = rootSaveFile+'/img_manholecover'
img_folder_grain = rootSaveFile+'/img_grain'
img_folder_fireandsmoke = rootSaveFile+'/img_fireandsmoke'
img_folder_stand = rootSaveFile+'/img_stand'
img_folder_adexqu = rootSaveFile+'/img_adexqu'
img_folder_pothole = rootSaveFile+'/img_pothole'
img_folder_fishing = rootSaveFile+'/img_fishing'
img_folder_watercover = rootSaveFile+'/img_watercover'
img_folder_riverfloat = rootSaveFile+'/img_riverfloat'
img_folder_chefcostume = rootSaveFile+'/img_chefcostumefloat'
# img_folder_lprColor = rootSaveFile+'/img_lprColor'



message_flow_input_folder =rootSaveFile + '/message_folder'
message_flow_output_folder =rootSaveFile + '/message_folder_output'



models_root ='/root/models'
if(sysstr == "Windows"):
    models_root = r'D:\AI_CV\chefcostume\chefcostume_runServer\models'



def getAndCheckInputImageData(request,maxImageMnum=3):

    statusCode_str= 'success'
    message ='成功'
    imgdata = None
    inp_dict = None
    try:
        data = request.get_data()
        if data is None or data == b'{}' or data == b'':
            statusCode_str= 'postData_empty'
            message = '服务必填参数缺失'
            return  statusCode_str, message,imgdata,inp_dict


        if (sysstr == "Windows"):
            inp_dict = json.loads(data)  # 根据字符串书写格式，将字符串自动转换成 字典类型
        else:
            inp_dict = json.loads(data.decode('utf-8'))

        if "imageBase64" not in inp_dict.keys():
            statusCode_str = 'no_field_imageBase64'
            message = '服务必填参数缺失:imageBase64'
        # elif "access_token" not in inp_dict.keys():
        #     statusCode_str = 'no_field_access_token'

        if statusCode_str != 'success':
            return statusCode_str, message,imgdata,inp_dict


        # #从鉴权数据表张中，查询验证access_token是否存在
        # access_token_v = inp_dict['access_token']
        #
        # #访问鉴权验证接口


        img_imageBase64 = inp_dict['imageBase64']

        if (img_imageBase64 is None or len(img_imageBase64) == 0):
            statusCode_str = 'imageBase64_empty'
            message = '服务必填参数缺失:imageBase64'
            return statusCode_str, message,imgdata,inp_dict

        elif len(img_imageBase64) < 1024*1:

            statusCode_str = 'imageBase64<1K'
            message = '请求参数范围错误：图像小于1K'
            return statusCode_str, message,imgdata,inp_dict

        elif len(img_imageBase64) > 1024*1024*maxImageMnum:

            statusCode_str= 'imageBase64_greaterThan2M'
            message = '请求参数范围错误:图像大于2M'
            return  statusCode_str, message,imgdata,inp_dict


    except Exception:
        statusCode_str = 'postData_formError'
        message = '请求参数格式错误'
        return  statusCode_str, message,imgdata,inp_dict



    # 如果使用加载数据的形式，普通的base64编码就可以。如果通过url的形式，则需要使用base64_url_decode

    try:
        # imgdata = base64_url_decode(img_imageBase64)
        imgdata = base64.b64decode(img_imageBase64)



        # 判断字符串是否为图像
        statusCode = IsValidImage4Bytes(imgdata)
        if (statusCode == False):
            statusCode_str = 'imageBase64_formError'
            message = '请求参数范围错误：图像格式错误'
            return  statusCode_str, message,imgdata,inp_dict



    except Exception:
        statusCode_str= 'imageBase64_formError'
        message = '请求参数范围错误：图像格式错误'
        return statusCode_str, message,imgdata,inp_dict

    return  statusCode_str, message,imgdata,inp_dict



def twoImgSave_getResult(readResultFunc,img_folder,xml_folder,log_id,imgdata1,imgdata2):


    iscreate = mymkdir(img_folder)
    # if iscreate == True:
    #     id_table = []
    iscreate = mymkdir(xml_folder)
    # if iscreate == True:
    #     id_table = []


    img_name = log_id
    img_path1 = img_folder+ "/" + img_name + "__1__.jpg"
    file1 = open(img_path1, 'wb')
    file1.write(imgdata1)
    file1.close()

    img_path2 = img_folder+ "/" + img_name + "__2__.jpg"
    file2 = open(img_path2, 'wb')
    file2.write(imgdata2)
    file2.close()

    dic_xml = {}


    txt_file_path = xml_folder + "/" + img_name + "__1__.out"


    statusCode_xml = 0
    oldtime = datetime.datetime.now()
    # dic_xml['recog_result'] = ""
    dic_xml['result'] = {}
    while (1):
        newtime = datetime.datetime.now()
        if os.path.isfile(txt_file_path):
            # 读取xml

            time.sleep(0.01)
            dic_xml = readResultFunc(txt_file_path)
            if dic_xml == None:
                continue


            # IIS服务器修改文件提示权限不足的解决办法
            # https:/blog.csdn.net/u014180504/article/details/46350341
            # # #将读取文件移走
            xml_folder_proced = xml_folder + '_proced'
            mymkdir(xml_folder_proced)

            dst_file_path = xml_folder_proced + "/" + img_name + "__1__.out"


            mymovefile(txt_file_path, dst_file_path)
            # mycopyfile(txt_file_path, dst_file_path)
            # myromvefile(txt_file_path)


            statusCode_xml = 1
            break

        # 如果超时也break
        if ((newtime - oldtime).seconds > 40):
            break
        time.sleep(0.1)

    if (statusCode_xml == 0):
        dic_xml['statusCode'] = 'overtime'

    dic_xml['log_id'] =log_id
    diff_time=(newtime - oldtime)
    run_time = diff_time.seconds + diff_time.microseconds / 1000000
    print(u'用时：%s秒' % run_time)
    dic_xml['timeSecond'] = run_time

    return dic_xml

def imgsave_getResult(readResultFunc,img_folder,xml_folder,log_id,imgdata):


    iscreate = mymkdir(img_folder)
    # if iscreate == True:
    #     id_table = []
    iscreate = mymkdir(xml_folder)
    # if iscreate == True:
    #     id_table = []


    img_name = log_id
    img_path = img_folder+ "/" + img_name + ".jpg"
    file = open(img_path, 'wb')
    file.write(imgdata)
    file.close()
    dic_xml = {}
    # txt_file_path = xml_folder + "/" + img_name + '.out'
    txt_file_path = xml_folder + "/" + img_name + '.json'

    print("log_id: " + log_id)
    print("img_path: " + img_path)
    print("txt_file_path: " +txt_file_path)



    statusCode_xml = 0
    oldtime = datetime.datetime.now()
    # dic_xml['recog_result'] = ""
    dic_xml['result'] = {}
    while (1):
        newtime = datetime.datetime.now()
        # 如果超时也break
        if ((newtime - oldtime).seconds > 40):
            break


        if os.path.isfile(txt_file_path):
            # 读取xml

            time.sleep(0.01)
            dic_xml = readResultFunc(txt_file_path)
            if dic_xml == None:
                continue




            # IIS服务器修改文件提示权限不足的解决办法
            # https:/blog.csdn.net/u014180504/article/details/46350341
            # # #将读取文件移走
            xml_folder_proced = xml_folder + '_proced'
            mymkdir(xml_folder_proced)


            dst_file_path = xml_folder_proced + "/" + img_name + ".out"

            mymovefile(txt_file_path, dst_file_path)
            # mycopyfile(txt_file_path, dst_file_path)
            # myromvefile(txt_file_path)


            statusCode_xml = 1
            break


        time.sleep(0.01)


    if (statusCode_xml == 0):
        dic_xml['statusCode'] = 'overtime'
        dic_xml['message'] = '超时'

    dic_xml['log_id'] =log_id
    diff_time=(newtime - oldtime)
    run_time = diff_time.seconds + diff_time.microseconds / 1000000
    print(u'用时：%s秒' % run_time)
    dic_xml['timeSecond'] = run_time

    # print(dic_xml)

    return dic_xml

def readJson(txt_file_path):
    with open(txt_file_path, encoding='utf-8') as file_open:
        # res = file_open.read()  # 读文件
        # mew_dict_xml =json.loads(res)  # 把json串变成python的数据类型：字典
        try:
            mew_dict_xml = json.load(file_open)  # ??????,存在报错
        except Exception:
            print('json.load_noCompleteContent')
            return None
    if "endFlag" in mew_dict_xml.keys():

        mew_dict_xml['statusCode'] = mew_dict_xml['analysisStatus']
        mew_dict_xml['message'] = mew_dict_xml['analysisStatus']
        return mew_dict_xml
    else:
        return None


def opencvImWrite_getResult(resultFlagStr,readResultFunc,img_folder,xml_folder,log_id,opencvimage):


    iscreate = mymkdir(img_folder)
    # if iscreate == True:
    #     id_table = []
    iscreate = mymkdir(xml_folder)
    # if iscreate == True:
    #     id_table = []


    img_name = log_id
    img_path = img_folder+ "/" + img_name + ".jpg"
    cv2.imwrite(img_path,opencvimage)


    time.sleep(0.1)

    dic_xml = {}
    txt_file_path=""
    if(resultFlagStr=="txt"):
        txt_file_path = xml_folder + "/" + img_name + ".jpg.txt"
    elif(resultFlagStr=="xml"):
        txt_file_path = xml_folder + "/" + img_name + ".xml"
    else:
        txt_file_path = xml_folder + "/" + img_name + ".jpg.txt"

    statusCode_xml = 0
    oldtime = datetime.datetime.now()
    # dic_xml['recog_result'] = ""
    dic_xml['result'] = {}
    while (1):
        newtime = datetime.datetime.now()
        # 如果超时也break
        if ((newtime - oldtime).seconds > 40):
            break
        if os.path.isfile(txt_file_path):
            # 读取xml


            dic_xml = readResultFunc(txt_file_path)
            if dic_xml == None:
                continue



            # IIS服务器修改文件提示权限不足的解决办法
            # https:/blog.csdn.net/u014180504/article/details/46350341
            # # #将读取文件移走
            xml_folder_proced = xml_folder + '_proced'
            mymkdir(xml_folder_proced)

            dst_file_path=""
            if (resultFlagStr == "txt"):
                dst_file_path = xml_folder_proced + "/" + img_name + ".jpg.txt"
            elif (resultFlagStr == "xml"):
                dst_file_path = xml_folder_proced + "/" + img_name + ".xml"
            else:
                dst_file_path = xml_folder_proced + "/" + img_name + ".jpg.txt"
            mymovefile(txt_file_path, dst_file_path)
            # mycopyfile(txt_file_path, dst_file_path)
            # myromvefile(txt_file_path)


            statusCode_xml = 1
            break



        time.sleep(0.1)

    if (statusCode_xml == 0):
        dic_xml['statusCode'] = 'overtime'

    dic_xml['log_id'] =log_id
    diff_time=(newtime - oldtime)
    run_time = diff_time.seconds + diff_time.microseconds / 1000000
    print(u'用时：%s秒' % run_time)
    dic_xml['timeSecond'] = run_time

    return dic_xml

def get_class_list(labeltxt):
    lines =[]
    with open(labeltxt, 'rt') as f:
        for line in f:
            lines.append(line.strip())
        return lines

def classier_OpencvDnnCaffeNet_predict(classier_OpencvDnnCaffeNet,classNames_OpencvDnnCaffeNet,frame_opencv,img_width,img_height,meanValue):

    # blob = dnn.blobFromImage(cv.imread('space_shuttle.jpg'), 1, (224, 224), (104, 117, 123), False)
    blob = cv2.dnn.blobFromImage(frame_opencv, 1 , (img_width,  img_height), meanValue, False)
    classier_OpencvDnnCaffeNet.setInput(blob)
    prob = classier_OpencvDnnCaffeNet.forward()
    # FEATURE = classier_OpencvDnnCaffeNet.forward("loss3_classifier_model")

    # timeit_forward(net)        #Uncomment to check performance
    print("Output:", prob.shape, prob.dtype)
    print("Best match", classNames_OpencvDnnCaffeNet[prob.argmax()])
    # 输出概率最大的前5个预测结果
    #建立索引与值的字典,这样计算量太大
    # list_prob =[]
    # for i,v in enumerate(prob[0]):
    #     list_prob.append((i,v))
    # sorted(list_prob, key=lambda pp: pp[1])  # sort by age
    k = 5
    import copy
    prob_tmp =copy.deepcopy(prob[0])
    temp = []
    Inf = 0
    for i in range(k):
        idex =prob_tmp.argmax()
        temp.append(idex)
        prob_tmp[idex] = Inf

    return [classNames_OpencvDnnCaffeNet[i] for i in temp],[prob[0][i] for i in temp]


@app.route('/')
def index():
    if request.method == "GET":
        return "get，Hello，AI！"
    else:
        return "post，Hello，AI！"


########################################################################################
#dcoos  车牌识别
########################################################################################
def getAndCheckInputImageData_dcoos(request,maxImageMnum=3):

    statusCode_str= 'success'
    imgdata = None
    inp_dict = None
    try:
        data = request.get_data()
        if data is None or data == b'{}' or data == b'':
            statusCode_str= 'postData_empty'
            return statusCode_str, imgdata, inp_dict


        if (sysstr == "Windows"):
            inp_dict = json.loads(data)  # 根据字符串书写格式，将字符串自动转换成 字典类型
        else:
            inp_dict = json.loads(data.decode('utf-8'))

        if "imageBase64" not in inp_dict.keys():
            statusCode_str = 'no_field_imageBase64'
        elif "timestamp" not in inp_dict.keys():
            statusCode_str = 'no_field_timestamp'
        elif "seqid" not in inp_dict.keys():
            statusCode_str = 'no_field_seqid'


        if statusCode_str != 'success':
            return statusCode_str,None, inp_dict


        # #从鉴权数据表张中，查询验证access_token是否存在
        # access_token_v = inp_dict['access_token']
        #
        # #访问鉴权验证接口


        img_imageBase64 = inp_dict['imageBase64']

        if (img_imageBase64 is None or len(img_imageBase64) == 0):
            statusCode_str = 'imageBase64_empty'
            return statusCode_str, imgdata,inp_dict

        elif len(img_imageBase64) < 1024*1:

            statusCode_str = 'imageBase64<1K'
            return statusCode_str, imgdata, inp_dict

        elif len(img_imageBase64) > 1024*1024*maxImageMnum:
            statusCode_str= 'imageBase64_greaterThan2M'
            return statusCode_str, imgdata, inp_dict


    except Exception:
        statusCode_str = 'postData_formError'
        return statusCode_str, imgdata,inp_dict



    # 如果使用加载数据的形式，普通的base64编码就可以。如果通过url的形式，则需要使用base64_url_decode

    try:
        # imgdata = base64_url_decode(img_imageBase64)
        imgdata = base64.b64decode(img_imageBase64)

        # 判断字符串是否为图像
        statusCode = IsValidImage4Bytes(imgdata)
        if (statusCode == False):
            statusCode_str = 'imageBase64_formError'
            return statusCode_str, imgdata,inp_dict



    except Exception:
        statusCode_str= 'imageBase64_formError'
        return statusCode_str, imgdata,inp_dict

    return statusCode_str, imgdata,inp_dict


########################################################################################
#河道漂浮物检测
########################################################################################

@app.route('/demo/image/chefcostumedetection')
def demo_image_chefcostumedetection():
    return send_file("static/demo_image_chefcostume.html")



@app.route('/APIService/chefcostumedetectionService', methods=['GET','POST'])
def chefcostumeService():
    dic_xml = {}
    log_id =time.strftime("%Y%m%d%H%M%S", time.localtime())+ '_' + str(uuid.uuid1())
    cc = time.localtime(time.time())
    # log_id = str(cc.tm_year) + str(cc.tm_mon) + str(cc.tm_mday) + str(cc.tm_hour) + str(cc.tm_sec) + '_' + str(uuid.uuid1())
    ip_str= request.remote_addr
    host_string = request.host_url
    logger.info(ip_str + " "+ host_string+'/APIService/chefcostumedetectionService in:' + log_id)
    statusCode_str,msg, imgdata,inp_dict = getAndCheckInputImageData(request)
    if (statusCode_str != 'success'):

        dic_xml['statusCode'] = statusCode_str
        dic_xml['message'] =msg
        dic_xml['log_id'] = log_id
        json_str = json.dumps(dic_xml, ensure_ascii=False)
        # outstr = 'callback' + '(' + json_str + ')'
        rst = make_response(json_str)
        rst.headers['Access-Control-Allow-Origin'] = '*'
        rst.headers['Access-Control-Allow-Methods'] = 'POST'  # 响应POST
        rst.headers['Content-Type'] = 'application/json;charset=utf-8'  # 响应POST
        return rst

    logger.info(ip_str + " "+ host_string+'/APIService/chefcostumedetectionService process:' + log_id)
    companyId = "000"
    path_folder=BIYI_COMP_LOG_PATH+"/"+"chefcostumedetectionService"
    logger_name =  path_folder+ "/" + companyId +"-"+ str(cc.tm_year) + str(cc.tm_mon) + str(cc.tm_mday)+".log"
    mymkdir(path_folder)

    try:

        logger_name_new = logger_name
        if os.path.exists(logger_name_new):
            fsize = os.path.getsize(logger_name_new)
            if (fsize > 100*1024*1024):
                index = 1
                while (1):
                    logger_name_new = logger_name +"_"+ str(index)
                    if os.path.exists(logger_name_new):
                        fsize = os.path.getsize(logger_name_new)
                        if (fsize > 100*1024*1024):
                            index += 1
                        else:
                            break
                    else:
                        break

        log_dict = {
            "content":
                {
                    "time_iso8601": "2020-03-09T11:11:14+08:00",
                    "companyId": "000",
                    "company": "ctsi",
                    "projectNameCN": "001",
                    "projectName": "biyi",
                    "componentName": "biyi-hx-chefcostumedetectionService",
                    "componentMethodName": "biyi-hx-chefcostumedetectionService",
                    "componentType": "微服务组件",
                    "componentVer": "v1.0.0",
                    "componentLang": "python",
                    "userName": "admin"
                },
            "sign": "1111111111111"
        }
        log_dict["content"]["time_iso8601"]=time.strftime("%Y-%m-%dT%H:%M:%S+08:00", time.localtime())
        # rsa_one(logger_name_new, log_dict)


        dic_xml = imgsave_getResult(readJson,img_folder_chefcostume,img_folder_chefcostume,log_id,imgdata)

        print("dic_xml: ")
        print(dic_xml)


        if "playFlag" in inp_dict.keys():

            img_array = np.fromstring(imgdata, np.uint8)  # 转换np序列


            showimage = cv2.imdecode(img_array, cv2.COLOR_BGR2RGB)  # 转换Opencv格式

            # img_path = img_folder_riverfloat+"_proced/"+log_id+'.jpg'
            #
            # print(img_path)
            #
            # showimage = cv2.imread(img_path)

            # cv2.imshow("img", showimage)

            # cv2.waitKey(0)  # 等待按键

            point_color = (84, 46, 8)  # BGR
            thickness = 3
            lineType = 8

            for one in dic_xml['result']:
                # print('12345')
                # color_v =one['color']
                num_v = one['value']
                print("label:" + num_v)
                w_v = int(one['width'])
                h_v = int(one['height'])
                x_v = int(one['pointX'])
                y_v = int(one['pointY'])
                x2 = int(x_v + 0.5 * w_v)
                y2 = int(y_v + 0.5 * h_v)
                x1 = int(x_v - 0.5 * w_v)
                y1 = int(y_v - 0.5 * h_v)
                ptStart = (x1, y1)
                ptEnd = (x2, y2)

                if (num_v=="chef_cap"):
                    point_color = (219, 112, 147) #红色
                elif(num_v=="head"):
                    point_color = (100, 149, 237) #蓝色
                elif (num_v == "chef_uniform"):
                    point_color = (124, 252, 0)  # 绿色
                elif (num_v == "clothes"):
                    point_color = (255, 215, 255)  # 黄色
                else:
                    point_color = (203, 192, 255)  # 粉色

                cv2.rectangle(showimage, ptStart, ptEnd, point_color, thickness, lineType)

                cv2.imwrite(rootSaveFile + '/result/' + log_id + "_result" + ".jpg", showimage)

            # base64_str = np.array(cv2.imencode('.jpg', showimage)[1]).tostring()
            #
            # dic_xml["showimageBase64"] = base64.b64encode(base64_str).decode(encoding="utf-8")

            import base64
            img_path = rootSaveFile + '/result/' + log_id + "_result" + ".jpg"
            print(img_path)

            with open(img_path, "rb") as f:  # 转为二进制格式
                base64_str = base64.b64encode(f.read())  # 使用base64进行加密
                # print("base64: " + str(base64_str,'utf-8'))
                dic_xml["showimageBase64"] = str(base64_str, 'utf-8')

        return_str = json.dumps(dic_xml,ensure_ascii=False)

    except Exception:
        dic_xml['statusCode'] = 'recog_runError'
        dic_xml['message'] = 'recog_runError'
        dic_xml['log_id'] = log_id
        json_str = json.dumps(dic_xml,ensure_ascii=False)
        # outstr = 'callback' + '(' + json_str + ')'
        # outstr = 'callback' + '(' + json_str + ')'
        rst = make_response(json_str)
        rst.headers['Access-Control-Allow-Origin'] = '*'
        rst.headers['Access-Control-Allow-Methods'] = 'POST'  # 响应POST
        rst.headers['Content-Type'] = 'application/json;charset=utf-8'  # 响应POST
        return rst


    # outstr = 'callback' + '(' + return_str + ')'
    rst = make_response(return_str)
    rst.headers['Access-Control-Allow-Origin'] = '*'
    rst.headers['Access-Control-Allow-Methods'] = 'POST'  # 响应POST
    rst.headers['Content-Type'] = 'application/json;charset=utf-8'  # 响应POST
    return rst


########################################################################################
if __name__ == '__main__':

    app.run(host = config['numbers'].get('host1'))  #gunicorn -w 4 -b 0.0.0.0:5000 imageAPIServer:app   或者   nohup gunicorn -w 4 -b 0.0.0.0:5000 imageAPIServer:app &
    #windows无法使用gunicorn，改为waitress，waitress-serve --listen=0.0.0.0:5000 imageAPIServerForExample:app
    # app.run(host = '0.0.0.0')  #gunicorn -w 4 -b 0.0.0.0:5000 imageAPIServer:app   或者   nohup gunicorn -w 4 -b 0.0.0.0:5000 imageAPIServer:app &
    # #manager.run()  # python img_api_server.py runserver -h 0.0.0.0 -p 80#这样就开启了本机的80端口，别的机器可以远程访

    # http://127.0.0.1:5000/demo/image/chefcostumedetection



