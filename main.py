import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtCore import Qt, QPoint
from UI_main_1 import Ui_Dialog as MainUI
from UI_calendar import CalendarPage  # 使用自定义封装类
from UI_calendar import save_event
from UI_task import TaskPriority
from UI_health import TestWindow,AdviceWindow,HealthPage
DATA_FILE = "calendar_events.json"
class MainWindow(QtWidgets.QDialog):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.ui = MainUI()
        self.ui.setupUi(self)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.ui.pushButton.clicked.connect(self.controller.show_calendar)

        self.drag_pos = QPoint()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.drag_pos)
            self.drag_pos = event.globalPos()

class CalendarWindow(QtWidgets.QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMinimumSize(1000, 700)

        self.page = CalendarPage(self.controller)  # ✅ 传入 controller 以便导航
        self.setCentralWidget(self.page)

        self.drag_pos = QPoint()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.drag_pos)
            self.drag_pos = event.globalPos()

class HealthWindow(QtWidgets.QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMinimumSize(1000, 700)

        self.page = HealthPage(self.controller)  # ✅ 传入 controller 以便导航
        self.setCentralWidget(self.page)

        self.drag_pos = QPoint()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.drag_pos)
            self.drag_pos = event.globalPos()


class AppController:
    def __init__(self):
        self.main_win = MainWindow(self)
        self.calendar_win = CalendarWindow(self)
        self.Health_win = HealthWindow(self)
        self.Test_win = TestWindow(self)
        self.Advice_win=AdviceWindow(self)
        self.task_win=TaskPriority(self)

    def show_main(self):
        self.calendar_win.close()
        self.main_win.show()

    def show_calendar(self):
        self.main_win.close()
        self.calendar_win.show()

    #Health to calendar
    def to_calendar(self):
        self.Health_win.close()
        self.calendar_win.show()
    
    #calendar to health
    def show_health(self):
        self.calendar_win.close()
        self.Health_win.show()
    
    #health to test
    def show_test(self):
        self.Health_win.close()
        self.Test_win.show()
    
    def show_task(self):
        self.calendar_win.close()
        self.task_win.show()
    
    #health to adice
    def show_advice(self):
        self.Health_win.close()
        self.Advice_win.show()
    
    #Advice_to_Health
    def Advice_to_Health(self):
        self.Advice_win.close()
        self.Health_win.show()

    #test to Health
    def Test_to_Health(self):
        self.Test_win.close()
        self.Health_win.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setFont(QtGui.QFont("Microsoft YaHei", 10))

    controller = AppController()
    controller.show_main()

    sys.exit(app.exec_())
