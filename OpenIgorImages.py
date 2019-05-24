import numpy as np
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.ptime as ptime
import pyqtgraph as pg
from libtiff import TIFF
import RPi.GPIO as GPIO
from datetime import datetime
import time
 
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN)#-show movie
GPIO.setup(20, GPIO.IN)#-frame time


imagecounter=0
movieRunning=0
imagelist=[]
global_clock=0
RepeatForver=0
def dummy():
    wait=1
def updateData():
        global imagecounter,movieRunning,imagelist,global_clock,RepeatForver
        
        if(movieRunning==0):                
                loadMovie=0
                while(loadMovie==0):
                    loadMovie=GPIO.input(21)                
                if((loadMovie)):#and(GPIO.input(20)==0)):  #RUN
                        try:
                            tif=TIFF.open('/share/movie.tif',mode='r')
                                #print "open"
                        except:
                            wait=1
                            print "error opening file"
                        else:                                  
                            imagelist = list(tif.iter_images())
                            loadMovie=0
                            movieRunning=1
                            img.setImage(imagelist[0],levels=(0,255))
                            meanGPIOsignal=0
                            for countRepeatForver in range(100):
                                meanGPIOsignal=meanGPIOsignal+GPIO.input(20)
                            RepeatForver=(meanGPIOsignal>50)
                            imagecounter=3-2*RepeatForver
                            while(GPIO.input(21)):
                                wait=1
        #if movie is tunning show next frame
        if(movieRunning):  
                waitGPIO=0
                nextmovie=0
                while((waitGPIO==0)and(nextmovie==0)  ):
                    waitGPIO=GPIO.input(20)
                    nextmovie=GPIO.input(21)
                if( imagecounter>=len(imagelist)):
                    if (RepeatForver):
                        imagecounter=0
                    else:
                        movieRunning=0           
                if (nextmovie):# time out  -next movie
                    movieRunning=0
                else:
                    while(GPIO.input(20)):
                        wait=1
                if(movieRunning):
                    img.setImage(imagelist[imagecounter],levels=(0,255))
                    imagecounter=(imagecounter+1)                    
                else:
                    imagecounter=0
                    
        QtCore.QTimer.singleShot(1, updateData)     

    

app = QtGui.QApplication([])
## Create window with GraphicsView widget
win = pg.GraphicsLayoutWidget()
win.resize(800,800) #pixel on display
win.move(0,0)
win.setWindowTitle('Stimulus')
win.show()
view = win.addViewBox()
img = pg.ImageItem(border='k')
view.addItem(img)
view.setRange(QtCore.QRectF(-120, -140, 220*2, 200*2+0))    
#win.showMaximized()
    


QtCore.QTimer.singleShot(1, updateData)
## Start Qt event loop unless running in interactive mode.
print(QtCore)
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
