from __future__ import print_function
import os
import logging
import subprocess
import sys
import time
import socket
import gphoto2 as gp

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
print("server is listening for connections")

while True:
    conn, addr = s.accept()
    print("connected")
    #data = conn.recv(1024)
    #print("(server) data=", data)
    time1 = time.ctime()
    time2 = time.strptime(time1)
    time3 = time.strftime('%Y%m%d_H.%M.%S', time2)
    imagename = time3 + ".jpg"
    ret = capture(savedir, imagename)
    bytes = open("%s%s"%(savedir, imagename)).read()
    #bytes = open("/home/1p85m/evaluation/optical_pointing/test/fig/20181124_09.05.28/2018.11.24-09.05.48.jpg").read()
    #print("byte",len(bytes))
    #bytes += "¥n"
    #_file = open("/home/1p85m/evaluation/optical_pointing/test/fig/test3.jpg", "wg")
    #_file.write(bytes)
    #_file.close()
    #conn.send(str(len(bytes)))
    conn.send(bytes)
