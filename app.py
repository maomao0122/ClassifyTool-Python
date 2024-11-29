import os.path
import shutil
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QPushButton, QFileDialog, QLabel, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 设置窗体标题
        self.setWindowTitle("图片分类工具 - by毛毛")

        self.resize(900, 600)

        self.src_path = None

        self.dst_path = None

        self.header_layout = QHBoxLayout()

        self.content_layout = QVBoxLayout()

        self.form_layout = QHBoxLayout()

        self.img_name_list = []

        self.idx = 0

        self.label = QLabel(self)

        self.edit = QLineEdit()

        self.ok_btn = QPushButton("确定")
        self.ok_btn.setShortcut(Qt.Key_Return)

        self.delete_btn = QPushButton("删除")

        # 创建窗体布局
        self.window_layout = QVBoxLayout()

        self.init_header()
        self.init_form()

        self.window_layout.addLayout(self.header_layout)

        self.window_layout.addStretch(1)

        self.window_layout.addLayout(self.content_layout)

        self.window_layout.addLayout(self.form_layout)

        self.window_layout.addStretch(1)

        self.setLayout(self.window_layout)

    def init_header(self):
        src_btn = QPushButton("待分类文件夹")
        src_btn.clicked.connect(self.click_src_event)
        self.header_layout.addWidget(src_btn)

        dst_btn = QPushButton("存放文件夹")
        dst_btn.clicked.connect(self.click_dst_event)
        self.header_layout.addWidget(dst_btn)

        start_btn = QPushButton("开始")
        start_btn.clicked.connect(self.click_start_event)
        self.header_layout.addWidget(start_btn)

        self.header_layout.addStretch()

    def init_form(self):
        self.edit.setPlaceholderText("输入图片中的汉字")
        self.edit.setVisible(False)
        self.form_layout.addWidget(self.edit)

        self.ok_btn.clicked.connect(self.click_ok_event)
        self.ok_btn.setVisible(False)
        self.form_layout.addWidget(self.ok_btn)

        self.delete_btn.clicked.connect(self.click_delete_event)
        self.delete_btn.setVisible(False)
        self.form_layout.addWidget(self.delete_btn)

    def click_src_event(self):
        self.src_path = QFileDialog.getExistingDirectory(self, "选取文件夹", "./")
        if self.src_path == "":
            return
        for item in os.scandir(self.src_path):
            self.img_name_list.append(item.name)

    def click_dst_event(self):
        self.dst_path = QFileDialog.getExistingDirectory(self, "选取文件夹", "./")

    def click_start_event(self):
        if self.src_path is None:
            QMessageBox.warning(
                self, "警告", "请选择待分类文件夹！", QMessageBox.Yes, QMessageBox.Yes)
            return

        if self.dst_path is None:
            QMessageBox.warning(
                self, "警告", "请选择存放文件夹！", QMessageBox.Yes, QMessageBox.Yes)
            return

        if len(self.img_name_list) == 0:
            QMessageBox.warning(
                self, "警告", "文件夹为空！", QMessageBox.Yes, QMessageBox.Yes)
            return

        img_name = self.img_name_list[self.idx]
        self.show_image(img_name)

        self.edit.setVisible(True)
        self.ok_btn.setVisible(True)
        self.delete_btn.setVisible(True)

    def click_ok_event(self):
        if self.edit.text() == "":
            QMessageBox.warning(
                self, "警告", "请输入图片中的汉字名称！", QMessageBox.Yes, QMessageBox.Yes)
            return
        img_name = self.img_name_list[self.idx]
        text = self.edit.text()
        dir_path = os.path.join(self.dst_path, text)
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)

        src_img = os.path.join(self.src_path, img_name)
        dst_img = os.path.join(dir_path, img_name)

        shutil.move(src_img, dst_img)

        self.edit.clear()

        self.next()

        self.edit.setFocus()

    def click_delete_event(self):
        img_name = self.img_name_list[self.idx]
        path = os.path.join(self.src_path, img_name)
        os.remove(path)

        self.next()

        self.edit.setFocus()

    def next(self):
        self.idx += 1
        if self.idx < len(self.img_name_list):
            img_name = self.img_name_list[self.idx]
            self.show_image(img_name)
        else:
            self.label.setVisible(False)
            self.edit.setVisible(False)
            self.ok_btn.setVisible(False)
            self.delete_btn.setVisible(False)
            QMessageBox.information(self, "提示", "图片分类全部完成！", QMessageBox.Yes, QMessageBox.Yes)

    def show_image(self, name):
        self.label.clear()
        path = os.path.join(self.src_path, name)
        pixmap = QPixmap(path)
        self.label.setPixmap(pixmap)
        self.label.setFixedSize(120, 120)
        self.label.setScaledContents(True)
        self.content_layout.addWidget(self.label, 0, Qt.AlignCenter)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
