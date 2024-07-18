from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QGraphicsScene, QGraphicsPixmapItem, QProgressBar
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer
import time
import detection
from openFile import *

class MyClass(QMainWindow):
    def __init__(self):
        super().__init__()

        # Ui_Dialog sınıfından nesne oluşturma (örnek olarak burada adını "ui" olarak varsayalım)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.getImage)
        self.ui.pushButton_2.clicked.connect(self.detectionPath)
        self.ui.pushButton_3.clicked.connect(self.clearPath)

        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(QtCore.QRect(220, 685, 561, 31))
        self.pbar.setStyleSheet("background-color: rgb(81, 81, 81);")

        self.ui.pushButton_2.setEnabled(False)

        # Pencerenin boyutunu sabit yapın
        self.setFixedSize(1515, 770)  # İstediğiniz sabit boyutu ayarlayabilirsiniz

        
    def clearPath(self):
        self.ui.graphicsView.setScene(None)
        self.ui.graphicsView_2.setScene(None)
        self.updateProgressBar(0)

    def getImagePath(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', 'c:', "Image files (*.jpg *.gif)")
        return fname[0]

    def getImage(self):
        self.imagePath = self.getImagePath()
        if self.imagePath:
            scene = QtWidgets.QGraphicsScene(self)
            pixmap = QPixmap(self.imagePath)
        
            # Resmi istediğiniz genişlik ve yükseklikte ayarlayın
            new_width = 701  # Yeni genişlik
            new_height = 571  # Yeni yükseklik
            pixmap = pixmap.scaled(new_width, new_height)

            item = QtWidgets.QGraphicsPixmapItem(pixmap)
            scene.addItem(item)
            self.ui.graphicsView.setScene(scene)
            self.ui.graphicsView.setStyleSheet("border: none;")
            self.ui.pushButton_2.setEnabled(True)
  
    def detectionImage(self):
        self.updateProgressBar(0)
        
        detection.run(source=self.imagePath, exist_ok=True)
        for i in range(101):
            time.sleep(0.05)
            self.updateProgressBar(i)
        
    def detectionPath(self):
        self.image_Path = self.detectionImage()
        newPath = self.imagePath.replace("data/images", "runs/exp")
        if self.imagePath:
            scene = QtWidgets.QGraphicsScene(self)
            pixmap = QPixmap(newPath)

            # Resmi istediğiniz genişlik ve yükseklikte ayarlayın
            new_width = 701  # Yeni genişlik
            new_height = 571  # Yeni yükseklik
            pixmap = pixmap.scaled(new_width, new_height)

            item = QtWidgets.QGraphicsPixmapItem(pixmap)
            scene.addItem(item)
            self.ui.graphicsView_2.setScene(scene)
            self.ui.graphicsView_2.setStyleSheet("border: none;")

    def updateProgressBar(self, value):
        self.pbar.setValue(value)
# Bu kod parçası bir Qt uygulamasının ana döngüsünü başlatmak için kullanılır
app = QtWidgets.QApplication([])
dialog = MyClass()
dialog.show()
app.exec_()

