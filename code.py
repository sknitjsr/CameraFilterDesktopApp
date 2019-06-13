# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Camera.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import cv2
import numpy as np
import putMask
import  putCap
class RecordVideo(QtCore.QObject):
    image_data = QtCore.pyqtSignal(np.ndarray)

    def __init__(self, camera_port=0, parent=None):
        super().__init__(parent)
        self.camera = cv2.VideoCapture(camera_port)

        self.timer = QtCore.QBasicTimer()

    def start_recording(self):
        self.timer.start(0, self)

    def timerEvent(self, event):
        if (event.timerId() != self.timer.timerId()):
            return

        read, data = self.camera.read()
        if read:
            self.image_data.emit(data)


class FaceDetectionWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.classifier = cv2.CascadeClassifier('data.xml')
        self.image = QtGui.QImage()
        self._red = (0, 0, 255)
        self._width = 2
        self._min_size = (30, 30)

    def detect_faces(self, image: np.ndarray):
        # haarclassifiers work better in black and white
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray_image = cv2.equalizeHist(gray_image)

        faces = self.classifier.detectMultiScale(gray_image,
                                                 scaleFactor=1.3,
                                                 minNeighbors=4,
                                                 flags=cv2.CASCADE_SCALE_IMAGE,
                                                 minSize=self._min_size)

        return faces

    def image_data_slot(self, image_data):
        faces = self.detect_faces(image_data)
        for (x, y, w, h) in faces:
            cv2.rectangle(image_data,
                          (x, y),
                          (x+w, y+h),
                          self._red,
                          self._width)

        self.image = self.get_qimage(image_data)
        if self.image.size() != self.size():
            self.setFixedSize(self.image.size())

        self.update()

    def image_mask_slot(self, image_data ):
            s_img = cv2.imread("mask_1.png", -1)
        # while True :
            faces = self.detect_faces(image_data)

            for (x, y, w, h) in faces:

                faces = self.detect_faces(image_data)
                image_data =  putMask.put_mask(faces , s_img , image_data , x , y ,w , h)

                self.image = self.get_qimage(image_data)

                if self.image.size() != self.size():
                        self.setFixedSize(self.image.size())
                self.update()

    def image_cap_slot1(self, image_data ):
            c_img = cv2.imread("cap_11.png", -1)
        # while True :
            faces = self.detect_faces(image_data)

            for (x, y, w, h) in faces:

                faces = self.detect_faces(image_data)
                image_data =  putCap.put_cap(faces , c_img , image_data , x , y ,w , h)

                self.image = self.get_qimage(image_data)

                if self.image.size() != self.size():
                        self.setFixedSize(self.image.size())
                self.update()


    def get_qimage(self, image: np.ndarray):
        height, width, colors = image.shape
        bytesPerLine = 3 * width
        QImage = QtGui.QImage

        image = QImage(image.data,
                       width,
                       height,
                       bytesPerLine,
                       QImage.Format_RGB888)

        image = image.rgbSwapped()
        return image

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawImage(0, 0, self.image)
        self.image = QtGui.QImage()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(260, 530, 521, 17))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(270, 10, 371, 81))
        self.label_2.setStyleSheet("font: 57 italic 35pt \"Ubuntu\";")
        self.label_2.setObjectName("label_2")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(119, 139, 961, 321))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)

        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 490, 181, 25))
        self.pushButton.setStyleSheet("\n"
"font: 14pt \"Ubuntu\";")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(480, 490, 241, 25))
        self.pushButton_2.setMaximumSize(QtCore.QSize(241, 16777215))
        self.pushButton_2.setStyleSheet("font: 14pt \"Ubuntu\";")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(230, 490, 181, 25))
        self.pushButton_3.setStyleSheet("font: 14pt \"Ubuntu\";")
        self.pushButton_3.setObjectName("pushButton_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        self.menuApp = QtWidgets.QMenu(self.menubar)
        self.menuApp.setObjectName("menuApp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuApp.menuAction())
        self.face_detection_widget = FaceDetectionWidget()

        # TODO: set video port
        self.record_video = RecordVideo(0)


        image_data_slot = self.face_detection_widget.image_data_slot
        image_cap_slot1 = self.face_detection_widget.image_cap_slot1
        image_mask_slot = self.face_detection_widget.image_mask_slot


        #for cap(uncooment this and comment others)
        # self.record_video.image_data.connect(image_cap_slot1)
        #for mask(uncomment this and comment other 2
        # self.record_video.image_data.connect(image_mask_slot)
        #for face detection
        self.record_video.image_data.connect(image_data_slot)
        self.verticalLayout.addWidget(self.face_detection_widget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "@developed by: Shipra and Sahil"))
        self.label_2.setText(_translate("MainWindow", "CameraApp"))
        self.pushButton.setText(_translate("MainWindow", "Face Detection"))
        self.pushButton_2.setText(_translate("MainWindow", "Apply Mask Filter"))
        self.pushButton_3.setText(_translate("MainWindow", "Apply Cap Filter"))
        self.menuApp.setTitle(_translate("MainWindow", "App"))
        self.pushButton.clicked.connect(self.record_video.start_recording)



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

