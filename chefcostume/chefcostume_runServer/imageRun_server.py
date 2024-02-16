#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os,sys
import shutil
import time
import sys
# reload(sys)
# sys.setdefaultencoding("utf-8")
import xml.dom.minidom
import time,copy
import cv2,os,shutil
import numpy as np
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
# fontC = ImageFont.truetype("./Font/platech.ttf", 14, 0)
from PIL import Image
import platform


import argparse
import os,json
import shutil
import time


import cv2
import torch
import torch.backends.cudnn as cudnn
from numpy import random

import numpy

from models.experimental import attempt_load
from utils.datasets import LoadStreams, LoadImages
from utils.general import (
    check_img_size, non_max_suppression, apply_classifier, scale_coords,
    xyxy2xywh, plot_one_box, strip_optimizer, set_logging)
from utils.torch_utils import select_device, load_classifier, time_synchronized


base_dir=os.path.dirname(__file__)
sys.path.append(base_dir)  #临时修改环境变量
#可以读取带中文路径的图
def cv_imread(file_path,type=1):
    cv_img=cv2.imdecode(np.fromfile(file_path,dtype=np.uint8),-1)
    if(type==0):
        cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    return cv_img
# 生成xml

def create_lpr_json(pstr_confidence_rect_list,xml_path):
    dic_xml = {}

    dic_xml['result'] = []
    # for pstr, color_str, confidence, one_rect in pstr_confidence_rect_list:
    for pstr, confidence, one_rect in pstr_confidence_rect_list:
        x_min = max(0, int(one_rect[0]))
        y_min = max(0, int(one_rect[1]))
        w = int(one_rect[2])
        h = int(one_rect[3])
        one_dict={}

        if pstr==0:
            one_dict["value"] = 'chef_cap'
        elif pstr==1:
            one_dict["value"] = 'head'
        elif pstr==2:
            one_dict["value"] = 'chef_uniform'
        elif pstr==3:
            one_dict["value"] = 'clothes'
        elif pstr==4:
            one_dict["value"] = 'apron'

        one_dict["confidence"] = confidence
        one_dict["pointX"] = x_min
        one_dict["pointY"] = y_min
        one_dict["width"] = int(w)
        one_dict["height"] = int(h)
        dic_xml['result'].append(one_dict)
    dic_xml['result_num']= len(dic_xml["result"])
    dic_xml['analysisStatus']='success'
    dic_xml['endFlag'] = 1
    fw = open(xml_path, 'w', encoding='utf-8')  # 打开一个名字为‘user_info.json’的空文件
    import json
    json.dump(dic_xml, fw, ensure_ascii=False, indent=4)  # 字典转成json,字典转换成字符串,不需要写文件，自己帮你将转成的json字符串写入到‘user_info.json’的文件中

def inference(self,image,flag_recog):

    res_set = []

    return res_set

def detect(path,imgsz, half, model, device):

    # 将绝对的图片地址转换为图片文件夹的地址
    sysstr = platform.system()
    if (sysstr == "Windows"):
        source = path.split('\\')[0] + '\\' + path.split('\\')[1] + '\\' + path.split('\\')[2] + '\\' + path.split('\\')[3]
    else:

        # 将绝对的图片地址转换为图片文件夹的地址
        source = '/' + path.split('/')[1] + '/' + path.split('/')[2] + '/' + path.split('/')[3]

    # #给参数赋值
    # weights, view_img, save_txt, imgsz =   'adexqu.pt', False, False, 640
    #
    #
    # # Initialize
    # set_logging()
    # device = select_device('0')
    # half = device.type != 'cpu'  # half precision only supported on CUDA
    #
    # # Load model
    # model = attempt_load(weights, map_location=device)  # load FP32 model
    # imgsz = check_img_size(imgsz, s=model.stride.max())  # check img_size
    # if half:
    #     model.half()  # to FP16



    # Set Dataloader
    dataset = LoadImages(source, img_size=imgsz)
    print(dataset)

    # Get names and colors
    names = model.module.names if hasattr(model, 'module') else model.names
    colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(len(names))]

    # Run inference
    img = torch.zeros((1, 3, imgsz, imgsz), device=device)  # init img
    _ = model(img.half() if half else img) if device.type != 'cpu' else None  # run once

    for path, img, im0s, vid_cap in dataset:
        img = torch.from_numpy(img).to(device)
        img = img.half() if half else img.float()  # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        # Inference
        pred = model(img, augment=False)[0]

        # Apply NMS
        pred = non_max_suppression(pred, 0.45 ,0.45 ,None ,False)

    

        for i, det in enumerate(pred):  # detections per image
            p, s, im0 = path, '', im0s

            if det is not None and len(det):
                # Rescale boxes from img_size to im0 size

                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

                # Print results
                for c in det[:, -1].unique():
                    n = (det[:, -1] == c).sum()  # detections per class
                    s += '%g %ss, ' % (n, names[int(c)])  # add to string

        return det

def get_img_color_byClassier(card_img):


    color=None
    ratio =None

    return color,ratio

def create_mkdir(path):
    path=path.strip()  # 去除首位空格
    path=path.rstrip("/")    # 去除尾部 \ 符号
    isExists = os.path.exists(path) # 判断路径是否存在

    if not isExists:
        print(path+'创建成功')
        os.makedirs(path) # 创建目录操作函数
        return True
    else:
        return False
    return True

def get_images_N(image_folder,image_num):
    '''
    find image files in test data path
    :return: list of files found
    '''
    files = []
    filesname = []
    exts = ['.jpg', '.png', '.jpeg', '.JPG', '.BMP']
    for parent, dirnames, filenames in os.walk(image_folder):
        for filename in filenames:
            for ext in exts:
                if filename.endswith(ext):
                    files.append(os.path.join(parent, filename))
                    filesname.append(filename)
                    break

            if (len(files) >= image_num):
                print('Find {} images'.format(len(files)))
                break

    return files, filesname

g_model = None
if g_model == None:
    print("INIT lpr model")
    g_model = None

def run_on_Folder(monitor_folder_path):
    global g_model
    if g_model == None:
        print("INIT lpr model")
        g_model = None
    if create_mkdir(monitor_folder_path) == False:
        print("创建文件夹失败")

    proced_monitor_folder_path = monitor_folder_path + "_proced"
    create_mkdir(proced_monitor_folder_path)

    # 给参数赋值
    weights, view_img, save_txt, imgsz = 'chef.pt', False, False, 640

    # Initialize
    set_logging()
    device = select_device('0')
    half = device.type != 'cpu'  # half precision only supported on CUDA

    # Load model
    model = attempt_load(weights, map_location=device)  # load FP32 model
    imgsz = check_img_size(imgsz, s=model.stride.max())  # check img_size
    if half:
        model.half()  # to FP16

    while (1):

        files, filesname = get_images_N(monitor_folder_path, 1)

        if(len(files)==1):
            print(files[0])
            image_path=files[0]
            image_name=filesname[0]

            (image_name_no_end, extension) = os.path.splitext(image_name)
            try:
                grr = cv_imread(image_path)

                # run_flag = 1
                # if (grr is None):
                #     print('none')
                #     run_flag = 0
                #
                # if (run_flag == 1):
                #     shape_img = grr.shape
                #     if (len(shape_img) != 3):
                #         print('len(shape_img) != 3 ')
                #         run_flag = 0
                #     else:
                #         if (shape_img[2] != 3):
                #             print('shape_img[2] != 3')
                #             run_flag = 0

                xml_path = monitor_folder_path + '/' + image_name_no_end + '.json'


                pstr_confidence_rect_list = []
                # if (run_flag != 1):
                #     create_lpr_json( pstr_confidence_rect_list, xml_path)
                #     time.sleep(0.001)  # 休眠0.1秒
                #     return

                start = time.time()
                src_image = copy.deepcopy(grr)
                #厨师服饰检测的功能
                res_set = detect(image_path, imgsz, half, model, device)
                if res_set == None:
                    create_lpr_json(pstr_confidence_rect_list, xml_path)
                    time.sleep(0.001)  # 休眠0.1秒
                    # print('6789009')
                else:
                    # for pstr,confidence,rect in res_set:提取出每个框的数据
                    for one in res_set:

                        pstr = int(float(one[5]))
                        confidence = float(one[4])
                        rect = [int(float(one[0])), int(float(one[1])), int(abs(one[0] - one[2])),
                                int(abs(one[1] - one[3]))]

                        rect1 = [int(rect[0]+0.5*rect[2]), int(rect[1]+0.5*rect[3]), rect[2],rect[3]]

                        if confidence > 0.4:
                            x_min = max(0, int(float(rect[0])))
                            y_min = max(0, int(float(rect[1])))
                            x_max = int(rect[0] + rect[2])
                            y_max = int(rect[1] + rect[3])
                            new_little_lpr_image = src_image[y_min:y_max, x_min:x_max]
                            color_str, _ = get_img_color_byClassier(new_little_lpr_image)
                            pstr_confidence_rect_list.append((pstr, confidence, rect1))

                    create_lpr_json(pstr_confidence_rect_list, xml_path)
            except Exception:
                print("读取图片未成功。")


            # 移走已经处理的图像
            dst_path = proced_monitor_folder_path + '/' + filesname[0]
            shutil.move(files[0], dst_path)  # 复制文件
            print("move %s -> %s" % (files[0], dst_path))

        time.sleep(0.001)  # 休眠0.1秒

    return



#输入参数说明：
# 指定路径文件夹监控处理，
# 前台运行：python run_server.py x/x/x/xxxx_folder
# 后台运行：nohup python -u run_server.py x/x/x/xxxx_folder &
#nohup.out 查看运行日志

#输出说明：生成三个文件，以x/x/x/a.jpg为例；在所在目录中新建一个x_result文件夹存放：
# x/x/x/xxxx_folder_result/a.jpg.txt 记录文字字段的坐标
# x/x/x/xxxx_folder_result/a.jpg_111_detection.jpg  在原图上，把文字框出
# x/x/x/xxxx_folder_result/a.jpg_222_reCreate.jpg   重建空段图，根据识别结果+检测位置，还原该图像

# 将处理完的图像，移动到x/x/x/xxxx_folder_proced

if __name__ == '__main__':


    cmd_len = len(sys.argv)
    cmd_list = sys.argv
    print('参数列表:', str(cmd_list))


    if(cmd_len==2):

        monitor_folder_path = cmd_list[1]
        # 是否是目录
        if os.path.exists(monitor_folder_path)==False:
            print("文件目录不存在")
        else:
            print("开启厨师服饰检测服务......")
            run_on_Folder(monitor_folder_path)
    else:
        print('参数个数错误')


# python imageRun_server.py D:\AI_CV\test\img_chefcostumefloat
