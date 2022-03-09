from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, QRect, Qt
from json import loads
# from requests import get
from cv2 import VideoCapture, cvtColor, imwrite, COLOR_BGR2RGB, CAP_PROP_FPS, putText, rectangle, FONT_HERSHEY_SIMPLEX, LINE_AA, CAP_DSHOW, CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT
# from face_recognition import face_locations
from os import mkdir, path, environ, makedirs
import sys


class Ui_add_image_2(object):   
    def getIDStudent(self):            
        global IDStudent
        IDStudent = self.text_input_id_add_image_2.toPlainText()
        self.names = IDStudent

        print(self.millisecs)
        if ( IDStudent.isdigit() == True ):
            self.millisecs = 200
            self.lenImage = 0
            self.status_label_add_image_2.setText("Success")
            try:
                if (int(IDStudent) == 0):   
                    self.cap.release()                    
                print(makedirs(".\\Data\\" + str(IDStudent)))
                self.status_label_add_image_2.setText("Create data student {} ".format(IDStudent))
  
            except:
                # self.millisecs = 10
                self.lenImage = -1
                try:
                    if path.exists(".\\Data\\" + str(IDStudent)):
                        self.status_label_add_image_2.setText("Exist data student {}".format(IDStudent))
                    else:
                        makedirs(".\\Data\\" + str(IDStudent))
                        print("dont's")
                    
                except:
                    self.status_label_add_image_2.setText("Error") 
        else:
            self.millisecs = 10
            if ( IDStudent.isspace() == True or not IDStudent):
                self.status_label_add_image_2.setText("ID Empty")
            else:
                self.status_label_add_image_2.setText("ID Contain Aplphabet")
        self.time_video_steam = QtCore.QTimer()
        self.time_video_steam.setTimerType(QtCore.Qt.PreciseTimer)
        self.time_video_steam.timeout.connect(self.steamVideo)
        self.time_video_steam.start(self.millisecs)
    def steamVideo(self):
        ret, self.frame = self.cap.read()
        # print( self.frame.shape)
        if ret:
            if  (self.lenImage != -1):
                self.millisecs = 200
                lenFaceDetect = 1
                if(lenFaceDetect == 1):
                    self.status_label_add_image_2.setText("{}%".format(self.lenImage))
                    self.lenImage = self.lenImage + 1
                    # imwrite(".\\Data\\" + str(IDStudent) + "\\Image{}.png".format(self.lenImage),self.frame)
                    imwrite(".\\Data\\" + str(IDStudent) + "\\{}.png".format(str(IDStudent)),self.frame)
                    self.frame = putText(self.frame, "MNV: {}".format(self.names), (20,60), FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, LINE_AA)
                if(self.lenImage == 1):       ######### số lượng ảnh muốn lấy
                    self.lenImage = -1
                    self.millisecs = 10
                    self.video_add_image_2.setPixmap(QtGui.QPixmap(".\\Finish.png"))
                    self.status_label_add_image_2.setText("Finish")
                    self.time_video_steam.start(self.millisecs)
            else:
                self.millisecs = 10
                self.frame = rectangle(self.frame, ( 256, 90), (1024, 630), (0, 255, 0), 4)
                self.frame = putText(self.frame, 'Waiting for .....', (20,60), FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, LINE_AA)
                self.names = ''
                self.time_video_steam.start(self.millisecs)
        self.frame = cvtColor(self.frame, COLOR_BGR2RGB)
        height, width, channel = self.frame.shape
        step = channel * width
        qImg = QtGui.QImage(self.frame.data, width, height, step, QtGui.QImage.Format_RGB888)
        self.video_add_image_2.setPixmap(QtGui.QPixmap.fromImage(qImg))
        
    def setupUi(self, add_image_2):
        self.cap = VideoCapture(1, CAP_DSHOW)
        self.cap.set(CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(CAP_PROP_FRAME_HEIGHT, 736)
        add_image_2.setObjectName("add_image_2")
        add_image_2.resize(640, 600)
        add_image_2.setMinimumSize(QtCore.QSize(640, 600))
        add_image_2.setMaximumSize(QtCore.QSize(640, 600))
        #add_image_2.setStyleSheet("background-color:#ff80c1")
        self.video_add_image_2 = QtWidgets.QLabel(add_image_2)
        self.video_add_image_2.setGeometry(QtCore.QRect(0, 0, 1280, 736))
        self.video_add_image_2.setMinimumSize(QtCore.QSize(640, 480))
        self.video_add_image_2.setMaximumSize(QtCore.QSize(640, 480))
        self.video_add_image_2.setText("")
        self.video_add_image_2.setPixmap(QtGui.QPixmap("./UNKNOW.png"))
        self.video_add_image_2.setScaledContents(True)
        self.video_add_image_2.setObjectName("video_add_image_2")
        self.text_input_id_add_image_2 = QtWidgets.QTextEdit(add_image_2)
        self.text_input_id_add_image_2.setGeometry(QtCore.QRect(80, 500, 281, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.text_input_id_add_image_2.setFont(font)
        self.text_input_id_add_image_2.setObjectName("text_input_id_add_image_2")
        #self.text_input_id_add_image_2.setStyleSheet("background-color:#f7f7f7; color:#40BEEE")
        self.ID_Label_add_image_2 = QtWidgets.QLabel(add_image_2)
        self.ID_Label_add_image_2.setGeometry(QtCore.QRect(40, 510, 41, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.ID_Label_add_image_2.setFont(font)
        self.ID_Label_add_image_2.setObjectName("ID_Label_add_image_2")
        #self.ID_Label_add_image_2.setStyleSheet("color: #40BEEE")     
        self.on_button_add_image_2 = QtWidgets.QPushButton(add_image_2)
        self.on_button_add_image_2.setGeometry(QtCore.QRect(400, 500, 201, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.on_button_add_image_2.setFont(font)
        self.on_button_add_image_2.setObjectName("on_button_add_image_2")
        #self.on_button_add_image_2.setStyleSheet("border-radius: 10px; background: #40BEEE;color: white")  
        
        self.fps = int(self.cap.get(CAP_PROP_FPS))
        self.millisecs = 100 #int(1000.0 / self.fps)
        self.time_video_steam = QtCore.QTimer()
        self.time_video_steam.setTimerType(QtCore.Qt.PreciseTimer)
        self.time_video_steam.timeout.connect(self.steamVideo)
        self.time_video_steam.start(self.millisecs )
        self.lenImage = -1
        """---------------------------------------------------------------"""
        self.on_button_add_image_2.clicked.connect(self.getIDStudent)
        """---------------------------------------------------------------"""
        
        self.status_label_add_image_2 = QtWidgets.QLabel(add_image_2)
        self.status_label_add_image_2.setGeometry(QtCore.QRect(50, 550, 531, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.status_label_add_image_2.setFont(font)
        self.status_label_add_image_2.setAlignment(QtCore.Qt.AlignCenter)
        self.status_label_add_image_2.setObjectName("status_label_add_image_2")
        font = QtGui.QFont()
        font.setPointSize(12)
        self.retranslateUi(add_image_2)
        QtCore.QMetaObject.connectSlotsByName(add_image_2)

    def retranslateUi(self, add_image_2):
        _translate = QtCore.QCoreApplication.translate
        add_image_2.setWindowTitle(_translate("add_image_2", "Form"))
        self.ID_Label_add_image_2.setText(_translate("add_image_2", "ID :"))
        self.on_button_add_image_2.setText(_translate("add_image_2", "ON"))
        self.status_label_add_image_2.setText(_translate("add_image_2", "Status : None"))

if __name__ == "__main__":      
    app = QtWidgets.QApplication(sys.argv)
    add_image_2 = QtWidgets.QWidget()
    ui = Ui_add_image_2()
    ui.setupUi(add_image_2)
    add_image_2.show()
    sys.exit(app.exec_())

