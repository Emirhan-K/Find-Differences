from PyQt5.QtWidgets import *
from start_ui import Ui_MainWindow
from results import Result_Page
import cv2
import imutils
import numpy as np 
from PyQt5.QtGui import QPixmap

class Start_Page(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.startPage = Ui_MainWindow()
        self.startPage.setupUi(self)
        self.result_page = Result_Page()
        self.img1 = None
        self.img2 = None
        self.startPage.btn_img1.clicked.connect(self.btnImg1)
        self.startPage.btn_img2.clicked.connect(self.btnImg2)
        self.startPage.btn_run.clicked.connect(self.btnRun)

    def btnImg1(self):
        self.img1, _ = QFileDialog.getOpenFileName(self, 'Resim Dosyası Seç', '', 'Resim Dosyaları (*.png *.jpg *.jpeg *.bmp *.gif);;Tüm Dosyalar (*.*)')
        self.startPage.btn_img2.setEnabled(True)
    
    def btnImg2(self):
        self.img2, _ = QFileDialog.getOpenFileName(self, 'Resim Dosyası Seç', '', 'Resim Dosyaları (*.png *.jpg *.jpeg *.bmp *.gif);;Tüm Dosyalar (*.*)')
        self.startPage.btn_run.setEnabled(True)

    
    def btnRun(self):
        img1 = cv2.imread(self.img1)
        img2 = cv2.imread(self.img2)
        
        img1 = cv2.resize(img1,(600,400))
        img2 = cv2.resize(img2,(600,400))
        
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        diff = cv2.absdiff(gray1, gray2)

        threshold = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        kernel = np.ones((5,5), np.uint8)
        dilate = cv2.dilate(threshold, kernel=kernel, iterations=2)

        contours = cv2.findContours(dilate.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)

        for contour in contours:
            if cv2.contourArea(contour=contour) > 100:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(img1, (x, y), (x+w, y+h), (0, 0, 255), 2)
                cv2.rectangle(img2, (x, y), (x+w, y+h), (0, 0, 255), 2)
        
        x = np.zeros((400,10,3),np.uint8)
        result_img = np.hstack((img1, x, img2))
        
        cv2.imwrite('result.jpg', result_img)

        similarity_score = cv2.matchTemplate(gray1, gray2, cv2.TM_CCOEFF_NORMED)[0][0]
        similarity_score = 'RESİMLERİN BENZERLİK ORANI: %' + str(np.round(similarity_score*100))

        self.result_page.resultPage.lbl_similarty_score.setText(similarity_score)
        self.result_page.resultPage.lbl_result.setPixmap(QPixmap('result.jpg').scaled(1210,400))
        self.result_page.show()
        self.close()

    
