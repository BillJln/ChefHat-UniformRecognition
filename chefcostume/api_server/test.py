import base64

img_path = "D:/AI_CV/test/img_riverfloat_proced/20220906114102_baab5cbe-2d95-11ed-84b0-44af289019f0.jpg"

with open(img_path,"rb") as f:#转为二进制格式
    base64_data = base64.b64encode(f.read())#使用base64进行加密
    print("base64: " + str(base64_data))