import sys
import cv2
import numpy as np
import matplotlib
from PySide6.QtCore import (Qt, QTimer)
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (QApplication, QLineEdit, QPushButton, QWidget,
                               QHBoxLayout, QSizePolicy, QComboBox, QLabel,
                               QMainWindow, QVBoxLayout, QGridLayout, QRadioButton)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.m_proc_img=None
        self.m_main_img=None
        self.q_img=None

        self.setWindowTitle("My Form")
        self.setGeometry(0, 0, 800, 500)
        self.label = QLabel()
        self.label.setFixedSize(640, 480)
        self.geo_label = QLabel("geometry type")
        self.filter_label = QLabel("Filter type")
        self.edit = QLineEdit("Write path")

        self.radiobutton_1 = QRadioButton("Image")
        self.radiobutton_2 = QRadioButton("Video")
        self.radiobutton_3 = QRadioButton("Webcam")
        self.radiobutton_1.setChecked(True)

        self.load_button = QPushButton("Load Image")
        self.binary_button = QPushButton("Binary Image")
        self.geometry_button = QPushButton("geometry Image")
        self.initpos_button = QPushButton("Initialize Pos")
        self.perspec_button = QPushButton("Perspective Image")
        self.edge_button = QPushButton("Edge Detection")

        self.my_combo_box = QComboBox()
        self.my_combo_box.addItem("flip")
        self.my_combo_box.addItem("translation")
        self.my_combo_box.addItem("rotation")

        self.filter_combo_box = QComboBox()
        self.filter_combo_box.addItem("Sobel_XY")
        self.filter_combo_box.addItem("Scharr_X")
        self.filter_combo_box.addItem("Scharr_Y")
        self.filter_combo_box.addItem("Laplacian")
        self.filter_combo_box.addItem("Canny")

        self.label_pos1 = QLabel("Pos1")
        self.label_pos2 = QLabel("Pos2")
        self.label_pos3 = QLabel("Pos3")
        self.label_pos4 = QLabel("Pos4")
        self.Ledit_x1 = QLineEdit()
        self.Ledit_y1 = QLineEdit()
        self.Ledit_x2 = QLineEdit()
        self.Ledit_y2 = QLineEdit()
        self.Ledit_x3 = QLineEdit()
        self.Ledit_y3 = QLineEdit()
        self.Ledit_x4 = QLineEdit()
        self.Ledit_y4 = QLineEdit()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.display_video_stream)

        self.mouse_count = 0
        self.MODE_VIDEO = False
        self.EDGE_TYPE = None
        self.previous_plot = None

        self.canvas = FigureCanvas(Figure(figsize=(0, 0.5)))
        self.axes = self.canvas.figure.subplots()

        self.axes.set_ylim([6000, 10900])

        n_data = 50
        self.xdata = list(range(n_data))
        self.axes.set_xticks(self.xdata, [])
        self.ydata = [0 for i in range(n_data)]

        layout = QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.canvas)

        layout1_1 = QHBoxLayout()
        layout1_1.addWidget(self.radiobutton_1)
        layout1_1.addWidget(self.radiobutton_2)
        layout1_1.addWidget(self.radiobutton_3)

        layout1 = QHBoxLayout()
        layout1.addWidget(self.edit)
        layout1.addLayout(layout1_1)
        layout1.addWidget(self.load_button)
        layout1.addWidget(self.binary_button)

        layout2 = QHBoxLayout()
        layout2.addWidget(self.geo_label, alignment=Qt.AlignmentFlag.AlignRight)
        layout2.addWidget(self.my_combo_box)
        layout2.addWidget(self.geometry_button)

        layout3_1 = QGridLayout()
        layout3_1.addWidget(self.label_pos1,0,0)
        layout3_1.addWidget(self.Ledit_x1,0,1)
        layout3_1.addWidget(self.Ledit_y1,0,2)
        layout3_1.addWidget(self.label_pos2,0,3)
        layout3_1.addWidget(self.Ledit_x2,0,4)
        layout3_1.addWidget(self.Ledit_y2,0,5)
        layout3_1.addWidget(self.label_pos3,1,0)
        layout3_1.addWidget(self.Ledit_x3,1,1)
        layout3_1.addWidget(self.Ledit_y3,1,2)
        layout3_1.addWidget(self.label_pos4,1,3)
        layout3_1.addWidget(self.Ledit_x4,1,4)
        layout3_1.addWidget(self.Ledit_y4,1,5)

        layout3_2 = QHBoxLayout()
        layout3_2.addWidget(self.initpos_button)
        layout3_2.addWidget(self.perspec_button)

        layout3 = QHBoxLayout()
        layout3.addLayout(layout3_1)
        layout3.addLayout(layout3_2)

        layout4 = QHBoxLayout()
        layout4.addWidget(self.filter_label, alignment=Qt.AlignmentFlag.AlignRight)
        layout4.addWidget(self.filter_combo_box)
        layout4.addWidget(self.edge_button)

        layout_vert = QVBoxLayout()
        layout_vert.addLayout(layout)
        layout_vert.addLayout(layout1)
        layout_vert.addLayout(layout2)
        layout_vert.addLayout(layout3)
        layout_vert.addLayout(layout4)

        widget = QWidget(self)
        widget.setLayout(layout_vert)

        self.setCentralWidget(widget)

        self.radiobutton_1.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.initpos_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.perspec_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.load_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.binary_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.edit.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        self.radiobutton_1.clicked.connect(lambda :self.load_button.setText("Load Image"))
        self.radiobutton_2.clicked.connect(lambda: self.load_button.setText("Load Video"))
        self.radiobutton_3.clicked.connect(lambda: self.load_button.setText("Load Webcam"))
        self.load_button.clicked.connect(self.load_img_func)
        self.binary_button.clicked.connect(self.load_binaryimages)
        self.geometry_button.clicked.connect(self.select_geometry)
        self.initpos_button.clicked.connect(self.initialize_pos)
        self.perspec_button.clicked.connect(self.perspective_image)
        self.edge_button.clicked.connect(self.method_edge_detection)

    # def load_img_func(self):
    #     self.m_main_img = cv2.imread(f"{self.edit.text()}", cv2.IMREAD_COLOR)
    #     self.m_main_img = cv2.resize(self.m_main_img, (640, 480), interpolation=cv2.INTER_CUBIC)
    #     self.m_proc_img = self.m_main_img.copy()
    #     self.update_image(self.m_proc_img)

    def mousePressEvent(self, event):
        if self.MODE_VIDEO:
            return
        #if self.m_proc_img==None: return
        x = event.position().x() - self.label.x()
        y = event.position().y() - self.label.y()
        x, y = int(x), int(y)
        if self.mouse_count == 0:
            self.Ledit_x1.setText(f"{x}")
            self.Ledit_y1.setText(f"{y}")
            cv2.circle(self.m_proc_img, (x, y), 5, (255, 0, 0), -1)

        elif self.mouse_count == 1:
            self.Ledit_x2.setText(f"{x}")
            self.Ledit_y2.setText(f"{y}")
            cv2.circle(self.m_proc_img, (x, y), 5, (0, 255, 0), -1)


        elif self.mouse_count == 2:
            self.Ledit_x3.setText(f"{x}")
            self.Ledit_y3.setText(f"{y}")
            cv2.circle(self.m_proc_img, (x, y), 5, (0, 0, 255), -1)

        elif self.mouse_count == 3:
            self.Ledit_x4.setText(f"{x}")
            self.Ledit_y4.setText(f"{y}")
            cv2.circle(self.m_proc_img, (x, y), 5, (255, 255, 0), -1)
        self.mouse_count += 1
        self.update_image(self.m_proc_img)


    def perspective_image(self):
        rows, cols = self.m_proc_img.shape[:2]
        x1 = int(self.Ledit_x1.text())
        y1 = int(self.Ledit_y1.text())
        x2 = int(self.Ledit_x2.text())
        y2 = int(self.Ledit_y2.text())
        x3 = int(self.Ledit_x3.text())
        y3 = int(self.Ledit_y3.text())
        x4 = int(self.Ledit_x4.text())
        y4 = int(self.Ledit_y4.text())

        pts1 = np.float32([[x1, y1], [x2, y2], [x3, y3], [x4, y4]])
        pts2 = np.float32([[0, 0], [cols-1, 0], [cols-1, rows-1], [0, rows-1]])
        Mat1 = cv2.getPerspectiveTransform(pts1, pts2)
        self.m_proc_img = cv2.warpPerspective(self.m_proc_img, Mat1, (cols, rows))

        self.update_image(self.m_proc_img)


    def update_image(self, img):
        if len(img.shape) < 3:
            h, w = img.shape
            ch = 1
            img_format = QImage.Format_Grayscale8

        else:
            h, w, ch = img.shape
            img_format = QImage.Format_RGB888
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        img = QImage(img.data, w, h, ch * w, img_format)
        scaled_img = img.scaled(640, 480, Qt.KeepAspectRatio)

        self.label.setPixmap(QPixmap.fromImage(scaled_img))

    def update_plot(self, img):

        temp = img > 250
        sum_value = temp.sum()

        self.ydata = self.ydata[1:] + [sum_value]

        if self.previous_plot is None:
            self.previous_plot = self.axes.plot(self.xdata, self.ydata, 'r')[0]
        else:
            self.previous_plot.set_ydata(self.ydata)

        self.canvas.draw()

    def initialize_pos(self):
        for w in [self.Ledit_x1, self.Ledit_y1, self.Ledit_x2, self.Ledit_y2,
                  self.Ledit_x3, self.Ledit_y3, self.Ledit_x4, self.Ledit_y4]:
            w.clear()
        # 상태 초기화
        self.mouse_count = 0
        self.load_img_func()

    def method_edge_detection(self):
        if self.m_proc_img is not None:
            if len(self.m_proc_img.shape) >= 3:
                self.m_proc_img = cv2.cvtColor(self.m_proc_img, cv2.COLOR_BGR2GRAY)

            if self.filter_combo_box.currentText() == 'None':
                if self.MODE_VIDEO is True:
                    self.EDGE_TYPE = None
                return
            elif self.filter_combo_box.currentText() == 'Sobel_XY':
                edge_img = cv2.Sobel(self.m_proc_img, cv2.CV_8U, 1, 1, ksize=3)
            elif self.filter_combo_box.currentText() == 'Laplacian':
                edge_img = cv2.Laplacian(self.m_proc_img, cv2.CV_8U, ksize=3)
            elif self.filter_combo_box.currentText() == 'Canny':
                if self.MODE_VIDEO is True:
                    self.EDGE_TYPE = 'Canny'
                    return
                edge_img = cv2.Canny(self.m_proc_img, 150, 300)
            self.update_image(edge_img)

    def convert_QImage(self, img):
        self.m_proc_img=img
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, ch = img.shape
        q_img = QImage(img.data, w, h, ch * w, QImage.Format_RGB888)
        q_img = q_img.scaled(640, 480, Qt.KeepAspectRatio)
        self.label.setPixmap(QPixmap.fromImage(q_img))
        self.q_img=q_img

    def select_geometry(self):
        #flip
        if self.my_combo_box.currentIndex() == 0:
            img = cv2.flip(self.m_proc_img, 1)
        #reflect
        elif self.my_combo_box.currentIndex() == 1:
            rows, cols = self.m_proc_img.shape[:2]
            Mat = np.float32([[1, 0, 50],
                              [0, 1, 20]])
            img = cv2.warpAffine(self.m_proc_img, Mat, (cols, rows), borderMode=cv2.BORDER_REFLECT)
        #replicate
        elif self.my_combo_box.currentIndex() == 2:
            rows, cols = self.m_proc_img.shape[:2]
            Mat1 = cv2.getRotationMatrix2D((0, 0), 60, 1.0)
            img = cv2.warpAffine(self.m_proc_img, Mat1, (cols, rows), borderMode=cv2.BORDER_REPLICATE)
        #convert to Qimage
        self.convert_QImage(img)

    def load_binaryimages(self):
        img = cv2.cvtColor(self.m_proc_img, cv2.COLOR_BGR2GRAY)
        _, dst = cv2.threshold(img, 160, 255, cv2.THRESH_BINARY)
        self.m_proc_img = dst
        h, w = dst.shape
        dst = QImage(dst.data, w, h, QImage.Format_Grayscale8)
        scaled_img = dst.scaled(640, 480, Qt.KeepAspectRatio)
        self.label.setPixmap(QPixmap.fromImage(scaled_img))
        self.q_img=scaled_img

    def load_img_func(self):

        if self.radiobutton_1.isChecked() is True:
            try:
                self.MODE_VIDEO = False
                self.m_main_img = cv2.imread(f"{self.edit.text()}", cv2.IMREAD_COLOR)


                self.m_main_img = cv2.resize(self.m_main_img, (640, 480), interpolation=cv2.INTER_CUBIC)
                self.m_proc_img = self.m_main_img.copy()
                self.update_image(self.m_proc_img)
                print("update image")
            except :
                print(f'Error Image path : "{self.edit.text()}"')
        elif self.radiobutton_2.isChecked() is True:
            try:
                self.MODE_VIDEO = True
                self.setup_camera(f"{self.edit.text()}")
            except:
                print(f'Error Load Video : {self.edit.text()}')
        elif self.radiobutton_3.isChecked() is True:
            try:
                self.MODE_VIDEO = True
                self.setup_camera(0)
            except:
                print(f'Error Load Webcam')
    def setup_camera(self, vid):
        self.capture = cv2.VideoCapture(vid)
        if not self.capture.isOpened():
            print("Camera open failed")
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.label.size().width())
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.label.size().height())

        self.timer.start(30)

    def display_video_stream(self):
        retval, self.m_proc_img = self.capture.read()
        if not retval:
            return

        if self.EDGE_TYPE == 'Canny':
            self.m_proc_img = cv2.Canny(self.m_proc_img, 150, 300)
            self.update_plot(self.m_proc_img)
        elif self.EDGE_TYPE == 'Laplacian':
            self.m_proc_img = cv2.Laplacian(self.m_proc_img, cv2.CV_8U, ksize=3)
            self.update_plot(self.m_proc_img)

        self.update_image(self.m_proc_img)

        if self.MODE_VIDEO is False:
            self.timer.stop()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Window()
    form.show()
    sys.exit(app.exec())
