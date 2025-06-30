# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(600, 420)
        Dialog.setStyleSheet("background-color: #F0F2F5;")

        # 外部垂直居中布局容器
        self.central_layout = QtWidgets.QVBoxLayout(Dialog)
        self.central_layout.setContentsMargins(0, 0, 0, 0)
        self.central_layout.setSpacing(0)
        self.central_layout.setAlignment(QtCore.Qt.AlignCenter)

        # 卡片容器 Frame
        self.card = QtWidgets.QFrame(Dialog)
        self.card.setFixedSize(480, 300)
        self.card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 20px;
                border: 1px solid #E0E0E0;
                box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
            }
        """)
        self.card.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.card.setFrameShadow(QtWidgets.QFrame.Raised)

        # 卡片内布局
        self.card_layout = QtWidgets.QVBoxLayout(self.card)
        self.card_layout.setAlignment(QtCore.Qt.AlignCenter)

        # 主标题
        self.label = QtWidgets.QLabel(self.card)
        self.label.setText("PKU DDLer")
        self.label.setStyleSheet("""
            QLabel {
                font: 700 36pt 'Segoe UI';
                color: #2C3E50;
            }
        """)
        self.card_layout.addWidget(self.label)

        # 副标题
        self.label_2 = QtWidgets.QLabel(self.card)
        self.label_2.setText("                  期末全队")
        self.label_2.setStyleSheet("""
            QLabel {
                font: 14pt 'Microsoft YaHei';
                color: #7F8C8D;
            }
        """)
        self.card_layout.addWidget(self.label_2)

        # 间距
        self.card_layout.addSpacing(30)

        # 开始按钮
        self.pushButton = QtWidgets.QPushButton(self.card)
        self.pushButton.setText("开始")
        self.pushButton.setFixedSize(150, 50)
        self.pushButton.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #6DD5FA, stop:1 #2980B9
                );
                color: white;
                border: none;
                border-radius: 25px;
                font: bold 14pt 'Microsoft YaHei';
            }
            QPushButton:hover {
                background-color: #3498DB;
            }
            QPushButton:pressed {
                background-color: #2980B9;
            }
        """)
        self.card_layout.addWidget(self.pushButton, alignment=QtCore.Qt.AlignCenter)

        self.central_layout.addWidget(self.card)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "PKU DDLer"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
