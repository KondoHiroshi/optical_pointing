from __future__ import print_function
import os
import logging
import subprocess
import sys
import time
import socket
import gphoto2 as gp
from PIL import Image
from io import BytesIO
import numpy

time1 = time.ctime()
time2 = time.strptime(time1)
time3 = time.strftime('%Y%m%d_H.%M.%S', time2)

savedir_pre = '/home/telescope/optical_pointing_image/'
HOST = '192.168.100.55'
PORT = 50000

def capture(savedir, imagename):
    f = open("%s%s"%(savedir, imagename), "w")
    f.write("test")
    f.close()

    logging.basicConfig(
        format = "%(levelname)s: %(name)s: %(massage)s", level=logging.WARNING)
    gp.check_result(gp.use_python_logging())
    camera = gp.check_result(gp.gp_camera_new())
    gp.check_result(gp.gp_camera_init(camera))
    print("Capturing Image")
    file_path = gp.check_result(gp.gp_camera_capture(
        camera, gp.GP_CAPTURE_IMAGE))
    print("Camera file path: {0}/{1}".format(file_path.folder, file_path.name))
    target = os.path.join(savedir, imagename)
    print("Copying image to",target)
    camera_file = gp.check_result(gp.gp_camera_file_get(
        camera, file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL))
    gp.check_result(gp.gp_file_save(camera_file, target))
    # subprocess.call(["xdg-open", target])
    gp.check_result(gp.gp_camera_exit(camera))




s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

time1 = time.ctime()
time2 = time.strptime(time1)
time3 = time.strftime('%Y%m%d_H.%M.%S', time2)
savedir = savedir_pre + time3
os.mkdir(savedir)
os.chdir(savedir)
print("server is listening for connections")

while True:
    conn, addr = s.accept()
    print("connected")

    time1 = time.ctime()
    time2 = time.strptime(time1)
    time3 = time.strftime('%Y%m%d_H.%M.%S', time2)
    imagename = time3 + ".jpg"
    ret = capture(savedir, imagename)

    img = open(imagename,"rb").read()
    s.send(img)

"""

##pc2
import socket
from PIL import Image
import numpy
from io import BytesIO

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.connect(("localhost", 50009))
data_sum = b''
while True:
    data = soc.recv(5000) #1024バイトづつ分割して受信する
    data_sum = data_sum + data #受信した分だけ足していく
    print("0")
    if len(data) < 5000 : #どのようにデータを全て受信したかどうか判断すればよいか分からない
        break

bytesimg = BytesIO(data_sum)
img = Image.open(bytesimg)
img.save("test2.jpg","JPEG")


###raspi

import socket
from PIL import Image
import numpy
imagename = "DSC00658.JPG"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("localhost", 50009))    # 指定したホスト(IP)とポートをソケットに設定
s.listen(1)                  # 1つの接続要求を待つ
soc, addr = s.accept()          # 要求が来るまでブロック
print("Conneted by"+str(addr))  #サーバ側の合図

img = open("DSC00658.JPG","rb").read()
soc.send(img)              # ソケットにデータを送信
"""
