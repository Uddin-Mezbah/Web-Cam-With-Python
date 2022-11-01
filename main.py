
##############################
# My Camera Application      #
# MD MEZBAH UDDIN            #
# Nantong University(China)  #
# CSE                        #
#                            #
##############################

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap,QImage,QIcon
from PyQt5.QtCore import QTimer
import cv2
import datetime

class Window(QWidget):
    '''Main app window'''

    def __init__(self):
        super().__init__()

        #variable for app window
        self.window_width = 640
        self.window_height = 400

        #image variable
        self.img_width =  640
        self.img_height = 400

        #other variable
        self.dt = '0-0-0'
        self.record_flag = False

        #load icon
        self.camera_icon = QIcon(cap_icon_path)
        self.rec_icon = QIcon(rec_icon_path)
        self.stop_icon = QIcon(stop_icon_path)

        #to save video
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')

        #setup the window
        self.setWindowTitle('My Camera App')
        self.setGeometry(0, 0,self.window_width,self.window_height)
        self.setFixedSize(self.window_width,self.window_height)

        #setup timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)


        self.ui()

    def ui(self):
        '''contain all ui things'''
        # layout
        grid = QGridLayout()
        self.setLayout(grid)
        #image label
        self.image_label = QLabel(self)
        self.image_label.setGeometry(0,0,self.img_width,self.img_height)
        
        #capture button
        self.capture_btn = QPushButton(self)
        self.capture_btn.setIcon(self.camera_icon)
        self.capture_btn.setStyleSheet("border-radius: 30; border : 2px solid black;border-width: 3px")
        self.capture_btn.setFixedSize(60,60)
        self.capture_btn.clicked.connect(self.save_img)

        #record button
        self.rec_btn = QPushButton(self)
        # self.rec_btn.setIcon(self.rec_icon)
        self.rec_btn.setStyleSheet("border-radius: 30; border : 2px solid black;border-width: 3px")
        self.rec_btn.setFixedSize(60,60)
        self.rec_btn.clicked.connect(self.record)


        if not self.timer.isActive():
            self.cap = cv2.VideoCapture(0)
            self.timer.start(20)

        #add things to the layout
        grid.addWidget(self.capture_btn,0,0)
        grid.addWidget(self.image_label,0,1,2,3)
        grid.addWidget(self.rec_btn,1,0)
        

        self.show()

    def update(self):
        """update frams"""
        _, self.fram = self.cap.read()

        if self.record_flag == True:
            print("Recoding....")
            self.rec_btn.setIcon(self.stop_icon)
            self.fram = cv2.circle(self.fram,(20,70),5,(0,0,255),10)
        else:
            self.rec_btn.setIcon(self.rec_icon)

        frame = cv2.cvtColor(self.fram,cv2.COLOR_BGR2RGB)
        height,width,channel = frame.shape
        stop = channel*width

        q_frame = QImage(frame.data,width,height,stop,QImage.Format_RGB888)
        self.image_label.setPixmap(QPixmap.fromImage(q_frame))



    def save_img(self):
        '''save image from camera'''
        print("Saving image")
        self.get_time()
        cv2.imwrite(f"{self.dt}.jpg",self.fram)

    def record(self):
        '''record video'''
        print(self.record_flag)

        if self.record_flag == True:
            self.record_flag = False
            print("Stopping the recoord process")
        else:
            self.record_flag = True
            print("Starting to record.....")
            self.get_time()

            self.out = cv2.VideoWriter(f"{self.dt}.avi",self.fourcc,20.0,(self.img_width,self.img_height))

    def get_time(self):
        now = datetime.datetime.now()
        self.dt = now.strftime("%m-%d-%y,%H-%M-%S")
        print(self.dt)


#run

if __name__ == '__main__':
    cap_icon_path = 'asset/capture.png'
    rec_icon_path = 'asset/video-camera.png'
    stop_icon_path = 'asset/stop.png'

    app = QApplication(sys.argv)
    win = Window()
    sys.exit(app.exec_())

        





