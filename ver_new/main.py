from PyQt5 import QtCore, QtGui, QtWidgets
from json import loads
# from requests import get
from cv2 import VideoCapture, cvtColor, imwrite, COLOR_BGR2RGB, CAP_PROP_FPS, putText, rectangle, FONT_HERSHEY_SIMPLEX, LINE_AA, CAP_DSHOW, CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT
from os import mkdir, path, environ, makedirs
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from shutil import rmtree
import pandas as pd
import cv2

class PandasModel(QAbstractTableModel):
    def __init__(self, df = pd.DataFrame(), parent =  None):
        QAbstractTableModel.__init__(self, parent=None)
        self._df = df 
        self.setChanged = False

    def headerData(self, section, orientaion, role= Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return  QVariant()
        if orientaion == Qt.Horizontal:
            try:
                return self._df.columns.tolist()[section]
            except (IndexError, ):
                return  QVariant()
        elif orientaion == Qt.Vertical:
            try:
                return  self._df.index.tolist()[section]
            except (IndexError, ):
                return QVariant()
    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if (role == Qt.EditRole):
                return self._df.values[index.row()][index.column()]
            elif (role == Qt.DisplayRole):
                return self._df.values[index.row()][index.column()]
        return None

    def setData(self, index, value, role):
        row = self._df.index[index.row()]
        col = self._df.columns[index.column()]
        self._df.values[row][col] = value
        self.dataChanged.emit(index, index)
        return True

    def rowCount(self, parent=QModelIndex()): 
        return len(self._df.index)

    def columnCount(self, parent=QModelIndex()): 
        return len(self._df.columns)

    def sort(self, column, order):
        colname = self._df.columns.tolist()[column]
        self.layoutAboutToBeChanged.emit()
        self._df.sort_values(colname, ascending= order == Qt.AscendingOrder, inplace=True)
        self._df.reset_index(inplace=True, drop=True)
        self.layoutChanged.emit()
    
class Ui_add_image_2(object):   
    def getIDStudent(self):            
        global IDStudent
        IDStudent = self.text_input_id_add_image_2.toPlainText()
        self.names = IDStudent
        if ( IDStudent.isdigit() == True ):
            self.millisecs = 200
            self.lenImage = 0
            self.status_label_add_image_2.setText("Success")
            try:
                if (int(IDStudent) == 0):   
                    self.cap.release()                    
                print(makedirs("Data/{}".format(IDStudent)))
                self.status_label_add_image_2.setText("Create data student {} ".format(IDStudent))
  
            except:
                self.lenImage = -1
                try:
                    if path.exists("Data/{}".format(IDStudent)):
                        self.status_label_add_image_2.setText("Exist data student {}".format(IDStudent))
                    else:
                        makedirs("Data/{}".format(IDStudent))
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
        if ret:
            if  (self.lenImage != -1):
                self.millisecs = 200
                lenFaceDetect = 1
                if(lenFaceDetect == 1):
                    self.status_label_add_image_2.setText("{}%".format(self.lenImage))
                    self.lenImage = self.lenImage + 1
                    imwrite("Data/{}/{}.png".format(IDStudent, IDStudent),self.frame)
                    # imwrite("Data/{}.png".format(IDStudent, IDStudent),self.frame)
                    self.frame = putText(self.frame, "MNV: {}".format(self.names), (20,60), FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, LINE_AA)
                if(self.lenImage == 1):         ######### số lượng ảnh muốn lấy
                    self.lenImage = -1
                    self.millisecs = 10
                    self.video_add_image_2.setPixmap(QtGui.QPixmap("Finish.png"))
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

    def openFile(self, path=None):
        print("Opencsv " + str(self.model.setChanged))
        if  self.model.setChanged == True:
            print("is changed, saving?")
            quit_msg = "<b>The document was changed.<br>Do you want to save the changes?</ b>"
            reply = QMessageBox.question(self, 'Save Confirmation', 
                     quit_msg, QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                self.writeCSV_update()
            else:
                print("not saved, loading ...")
                return
        path, _ = QFileDialog.getOpenFileName(None)
        if path:
            return path
    
    def loadCSV(self):
        fileName = self.openFile()
        if fileName:
            print("Load CSV " +fileName + " loaded")
            f = open(fileName, 'r+b')
            with f:
                df = pd.read_csv(f, delimiter = ',',   keep_default_na = False, low_memory=False, header=None)
                f.close()
                self.model = PandasModel(df)
                self.lb.setModel(self.model)
                self.lb.resizeColumnsToContents()
                self.lb.selectRow(0)

    def showSelection(self, item):
        cellContent = item.data()
        ros = item.row()
        cos = item.column()
        sfd = self.model._df.values[ros,:]
        print(sfd[1])
        print("You clicked on {} {}".format(ros, cos))
        if str(cos) == "5":      
            print("gsasafdgsfadhsfhafghdfahgfdhgd2")
        sf = "You clicked on {}".format(cellContent)
        self.text_input_id_add_image_2.setText(sfd[1])
        statusimg = None
        if path.exists("Data/{}/{}.png".format(str(sfd[1]), str(sfd[1]))):
            statusimg = "Yes"
            self.status_label_add_image_2.setText("Exist data student {}".format(str(sfd[1])))
            cv2.imwrite("tam.png", cv2.resize(cv2.imread("Data/{}/{}.png".format(str(sfd[1]), str(sfd[1]))),(150, 150)))
        else:
            self.status_label_add_image_2.setText("Statu: None ")
            cv2.imwrite("tam.png", cv2.resize(cv2.imread('none4.png'),(150, 150)))
        noidung = "FullName : {}.\nTitkulcode: {}.\nClass: {}.\nStatus: {}.".format(sfd[3],sfd[1], sfd[4], statusimg)
        self.status_label_info.setText(noidung)
        pixmap = QPixmap("tam.png")
        self.status_label_image.setPixmap(pixmap)


    def findInTable(self):
        self.lb.clearSelection()
        text = self.lineFind.text()
        model = self.lb.model()
        for column in range(self.model.columnCount()):
            start = model.index(0, column)
            matches = model.match(start, Qt.DisplayRole, text, -1, Qt.MatchContains)
            if matches:
                for index in matches:
                    print(index.row(), index.column())
                    self.lb.selectionModel().select(index, QItemSelectionModel.Select)
                    
    def writeCSV(self):
        fileName, _ = QFileDialog.getSaveFileName(None, "Open File", self.filename,"CSV Files (*.csv)")
        if fileName:
            print("write csv "+fileName + " saved")
            f = open(fileName, 'w')
            newModel = self.model
            dataFrame = newModel._df.copy()
            dataFrame.to_csv(f, sep=',', index = False, header = False)
                   
    def writeCSV_update(self):
        if self.filename:
            f = open(self.filename, 'w')
            newModel = self.model
            dataFrame = newModel._df.copy()
            dataFrame.to_csv(f, sep=',', index = False, header = False)
            self.model.setChanged = False
            print("%s %s" % (self.filename, "saved"))

    def removeimage(self):
        self.IDStudentss = self.text_input_id_add_image_2.toPlainText()
        if self.IDStudentss != "":
            msg = QMessageBox()
            msg.setWindowTitle("Message Box")
            msg.setText("Bạn có chắc chắn muốn xóa hình này")
            
            msg.setIcon(QMessageBox.Question)
            msg.setStandardButtons(QMessageBox.Cancel|QMessageBox.Ok)
            msg.buttonClicked.connect(self.removepath)
            x = msg.exec_()
    def removepath(self, i):
        if str(i.text()) == "OK":
            try:
                rmtree("Data/" + str(self.IDStudentss))
            except Exception as e:
                msg = QMessageBox()
                msg.setWindowTitle("Error")
                msg.setText(str(e))
                x = msg.exec_()

    def setupUi(self, add_image_2):
        self.filename = ''
        # VideoCapture = 0;   HD camera
        # VideoCapture = 1;   logitechC920 
        self.cap = VideoCapture(1)
        self.cap.set(CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(CAP_PROP_FRAME_HEIGHT, 736)
        add_image_2.setObjectName("add_image_2")
        add_image_2.resize(640, 600)
        add_image_2.setMinimumSize(QtCore.QSize(1380, 800))
        add_image_2.setMaximumSize(QtCore.QSize(1380, 800))
        self.video_add_image_2 = QtWidgets.QLabel(add_image_2)
        self.video_add_image_2.setGeometry(QtCore.QRect(20, 50, 640, 480))
        self.video_add_image_2.setMinimumSize(QtCore.QSize(600, 440))
        self.video_add_image_2.setMaximumSize(QtCore.QSize(600, 440))
        self.video_add_image_2.setText("")
        self.video_add_image_2.setPixmap(QtGui.QPixmap("./UNKNOW.png"))
        self.video_add_image_2.setScaledContents(True)
        self.video_add_image_2.setObjectName("video_add_image_2")
        self.lb =  QtWidgets.QTableView(add_image_2)
        self.lb.setGeometry(650, 200 , 710, 575)
        self.lb.verticalHeader().setVisible(True)
        self.lb.setGridStyle(1)
        self.model = PandasModel()
        self.lb.setModel(self.model)
        self.lb.setEditTriggers(QAbstractItemView.DoubleClicked)
        self.lb.setSelectionBehavior(self.lb.SelectRows)
        self.lb.setSelectionMode(self.lb.SingleSelection)
        self.lb.setStyleSheet(stylesheet(self))
        self.lb.setAcceptDrops(True)
        self.lb.clicked.connect(self.showSelection)
        self.menu = QToolBar(add_image_2)
        self.menu.setGeometry(20, 0, 500, 50)
        self.menu.setFixedSize(QSize(600, 50))          # không cho resize
        self.openAct = QAction(QIcon('open4.png'), 'Open', triggered=self.loadCSV, shortcut = QKeySequence.Open)
        self.saveAct = QAction(QIcon('save4.png'), 'Save', triggered=self.writeCSV_update, shortcut = QKeySequence.Save)
        self.saveAs = QAction(QIcon('saveas4.png'), 'Save as', triggered=self.writeCSV, shortcut = QKeySequence.SaveAs)
        self.removeACt = QAction(QIcon('remove4.png'), 'Remove', triggered=self.removeimage, shortcut = QKeySequence.SaveAs)

        self.OAct = self.menu.addAction(self.openAct)
        self.SAct = self.menu.addAction(self.saveAct)
        self.SasAct = self.menu.addAction(self.saveAs)
        self.RemoveAct = self.menu.addAction(self.removeACt)

        self.lineFind = QLineEdit(add_image_2)
        self.lineFind.setGeometry(650, 10 , 480, 30)
        self.lineFind.setPlaceholderText("find")
        self.lineFind.setClearButtonEnabled(True)
        self.lineFind.returnPressed.connect(self.findInTable)

        self.text_input_id_add_image_2 = QtWidgets.QTextEdit(add_image_2)
        self.text_input_id_add_image_2.setGeometry(QtCore.QRect(50, 500, 250, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.text_input_id_add_image_2.setFont(font)
        self.text_input_id_add_image_2.setObjectName("text_input_id_add_image_2")
        self.ID_Label_add_image_2 = QtWidgets.QLabel(add_image_2)
        self.ID_Label_add_image_2.setGeometry(QtCore.QRect(20, 510, 50, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.ID_Label_add_image_2.setFont(font)
        self.ID_Label_add_image_2.setObjectName("ID_Label_add_image_2")
        self.on_button_add_image_2 = QtWidgets.QPushButton(add_image_2)
        self.on_button_add_image_2.setGeometry(QtCore.QRect(320, 500, 201, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.on_button_add_image_2.setFont(font)
        self.on_button_add_image_2.setObjectName("on_button_add_image_2")
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
        self.status_label_add_image_2.setGeometry(QtCore.QRect(100, 550, 350, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.status_label_add_image_2.setFont(font)
        self.status_label_add_image_2.setAlignment(QtCore.Qt.AlignCenter)
        self.status_label_add_image_2.setObjectName("status_label_add_image_2")

        self.status_label_info = QtWidgets.QLabel(add_image_2)
        self.status_label_info.setGeometry(QtCore.QRect(850, 45, 650, 100))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.status_label_info.setFont(font)
        self.status_label_info.setObjectName("status_label_info")

        self.status_label_image = QtWidgets.QLabel(add_image_2)
        self.status_label_image.setGeometry(QtCore.QRect(650, 45, 150, 150))
        # cv2.imwrite("tam.png", cv2.resize(cv2.imread('none4.png'),(150, 150)))
        pixmap = QPixmap("tam.png")
        self.status_label_image.setPixmap(pixmap)

        font = QtGui.QFont()
        font.setPointSize(12)
        self.retranslateUi(add_image_2)
        QtCore.QMetaObject.connectSlotsByName(add_image_2)

    def retranslateUi(self, add_image_2):
        _translate = QtCore.QCoreApplication.translate
        add_image_2.setWindowTitle(_translate("add_image_2", "Form"))
        self.ID_Label_add_image_2.setText(_translate("add_image_2", "ID:"))
        self.on_button_add_image_2.setText(_translate("add_image_2", "ON"))
        self.status_label_add_image_2.setText(_translate("add_image_2", "Status : None"))
        self.status_label_info.setText(_translate("add_image_2", "Status : None"))

def stylesheet(self):
        return """
    QMainWindow
        {
         background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                 stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
                                 stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
        }
        QMenuBar
        {
            background: transparent;
            border: 0px;
        }
        QTableView
        {
            background: qlineargradient(y1:0,  y2:1,
                        stop:0 #d3d7cf, stop:1 #ffffff);
            border: 1px solid #d3d7cf;
            border-radius: 0px;
            font-size: 8pt;
            selection-color: #ffffff
        }
        QTableView::item:hover
        {   
            color: #eeeeec;
            background: #c4a000;;           
        }
        
        
        QTableView::item:selected {
            color: #F4F4F4;
            background: qlineargradient(y1:0,  y2:1,
                        stop:0 #2a82da, stop:1 #1f3c5d);
        } 

        QTableView QTableCornerButton::section {
            background: transparent;
            border: 0px outset black;
        }
    QHeaderView
        {
         background: qlineargradient( y1: 0, y2: 1,
                                 stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
                                 stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
        color: #888a85;
        }

    QToolBar
        {
        background: transparent;
        border: 0px;
        }
    QStatusBar
        {
        background: transparent;
        border: 0px;
        color: #555753;
        font-size: 7pt;
        }

    """

if __name__ == "__main__":      
    app = QtWidgets.QApplication(sys.argv)
    add_image_2 = QtWidgets.QWidget()
    ui = Ui_add_image_2()
    ui.setupUi(add_image_2)
    add_image_2.show()
    sys.exit(app.exec_())

