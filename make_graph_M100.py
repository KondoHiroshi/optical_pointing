"""
For Canon EOS M100 Camera
Ryohei Harada
2018/10/26
"""
import cv2
import numpy as np
import matplotlib.pyplot as plt
import subprocess
import sys
import os
import numpy
import pylab

#---parameters---
npix_x = 2400   #The number of pixcels
npix_y = 1600

sensor_x = 22.3   #sensor size [mm]
#sensor_y = 14.9   #sensor size [mm]

f = 500.  #shoten kyori  mm, Borg
#-------------------

fl = sorted(subprocess.getoutput('find raw/ -name "*.JPG"').split('\n'))
pix_x = []
pix_y = []
for fl1 in fl:
    img = cv2.imread(fl1,cv2.IMREAD_GRAYSCALE)
    ret, nimg = cv2.threshold(img, 10, 255, cv2.THRESH_BINARY)
    det_img, contours, hierarchy = cv2.findContours(nimg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    stars = []
    areas = []
    for cnt in contours:
        M = cv2.moments(cnt)    
        if M['m00'] != 0:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            stars.append(np.array([[cx,cy]], dtype='int32'))
        else:
            stars.append(np.array([cnt[0][0]], dtype='int32'))
        areas.append(cv2.contourArea(cnt))
    areasarr = np.array(areas)    
    idx = areasarr.argmax()
    plt.imshow(cv2.imread(fl1), vmin=0, vmax=256)
    plt.plot(stars[idx][0][0], stars[idx][0][1], marker='+')
    plt.show()
    plt.savefig('fig/'+os.path.splitext(os.path.basename(fl1))[0]+'.mark.JPG')
    plt.close()
    pix_x.append(stars[idx][0][0])
    pix_y.append(stars[idx][0][1])
    
pix = np.array([pix_x, pix_y]).T    
numpy.savetxt('pix.txt', pix, fmt="%i",delimiter=",", header='pix_x, pix_y')

#argvs = sys.argv
#txt = numpy.loadtxt('%s' % argvs[1])
pix = numpy.loadtxt('pix.txt', delimiter=",", dtype='int32')
dpix_x = (pix[:,0] - npix_x//2)
dpix_y = (pix[:,1] - npix_y//2)*-1

theta_x = 2 * numpy.degrees(numpy.arctan(sensor_x / (2*f)))   #Angle of view [degree]
#theta_y = 2 * numpy.degrees(numpy.arctan(sensor_y / (2*f)))   #Angle of view [degree]

pix_x_to_arcsec = (theta_x / npix_x) * 3600.
#pix_y_to_arcsec = (theta_y / npix_y) * 3600.
print(pix_x_to_arcsec)
#---pixcel --> arcsec
d_x = dpix_x * theta_x   #[arcsec]
d_y = dpix_y * theta_x   #[arcsec]

d_x_sigma = np.std(d_x)
d_y_sigma = np.std(d_y)

d_x_rms = numpy.sqrt(numpy.sum(d_x**2)/len(d_x))
d_y_rms = numpy.sqrt(numpy.sum(d_x**2)/len(d_x))

d_rms = numpy.sqrt(d_x_rms**2+d_y_rms**2)
d_sigma = numpy.sqrt(d_x_sigma**2+d_y_sigma**2)

print('d_rms = %0.2f'%d_rms)
print('d_sigma = %0.2f'%d_sigma)

#---load Az, El---
#AzEl = numpy.loadtxt('AzEl_list.txt')
Az = [125., 57., 218.]   #test data
El = [73., 43., 65.]

def scatter_plot(x, y, xlabel, ylabel):
    plt.figure()
    plt.scatter(x, y, s=5)
    if xlabel[0] == 'd_x' and ylabel[0] == 'd_y':
        plt.title('%s_vs_%s\nrms = %0.2f'%(xlabel[0], ylabel[0], d_rms))
    else:
        plt.title('%s_vs_%s'%(xlabel[0], ylabel[0]))
    plt.xlabel('%s [%s]'%xlabel)
    plt.ylabel('%s [%s]'%ylabel)
    plt.grid()
    plt.savefig('%s_vs_%s.png'%(xlabel[0], ylabel[0]))

scatter_plot(Az, El, ('Az','degree'), ('El','degree'))
scatter_plot(Az, d_x, ('Az','degree'), ('d_x','arcsec'))
scatter_plot(Az, d_y, ('Az','degree'), ('d_y','arcsec'))
scatter_plot(El, d_x, ('El','degree'), ('d_x','arcsec'))
scatter_plot(El, d_y, ('El','degree'), ('d_y','arcsec'))
scatter_plot(d_x, d_y, ('d_x','arcsec'), ('d_y','arcsec'))

