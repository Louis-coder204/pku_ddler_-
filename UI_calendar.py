from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QTextCharFormat, QBrush, QColor, QFont

from datetime import datetime
import json

DATA_FILE = "calendar_events.json"

def save_event(year, month, day, hour, minute, category, content):
    new_event = {
        "year": year, "month": month, "day": day,
        "hour": hour, "minute": minute,
        "category": category, "content": content
    }
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            events = json.load(f)
    except FileNotFoundError:
        events = []
    events.append(new_event)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(events, f, ensure_ascii=False, indent=4)

def load_events():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

class AddEventDialog(QtWidgets.QDialog):
    def __init__(self, date, parent=None):
        super().__init__(parent)
        self.date = date
        self.setWindowTitle("添加日程")
        self.resize(300, 250)
        self.initUI()

    def initUI(self):
        layout = QtWidgets.QVBoxLayout()

        time_layout = QtWidgets.QHBoxLayout()
        self.hour_box = QtWidgets.QComboBox()
        self.hour_box.addItems([f"{i:02d}" for i in range(24)])
        self.minute_box = QtWidgets.QComboBox()
        self.minute_box.addItems([f"{i:02d}" for i in range(0, 60, 5)])
        time_layout.addWidget(QtWidgets.QLabel("时间："))
        time_layout.addWidget(self.hour_box)
        time_layout.addWidget(QtWidgets.QLabel("时"))
        time_layout.addWidget(self.minute_box)
        time_layout.addWidget(QtWidgets.QLabel("分"))
        layout.addLayout(time_layout)

        layout.addWidget(QtWidgets.QLabel("事件类别："))
        self.combo_category = QtWidgets.QComboBox()
        self.combo_category.addItems(["考试", "作业", "学工", "玩乐","锻炼"])
        layout.addWidget(self.combo_category)

        layout.addWidget(QtWidgets.QLabel("事件内容（不超过20字）："))
        self.text_content = QtWidgets.QTextEdit()
        self.text_content.setMaximumHeight(50)
        layout.addWidget(self.text_content)

        btn_save = QtWidgets.QPushButton("保存")
        btn_save.clicked.connect(self.save_event)
        layout.addWidget(btn_save)

        self.setLayout(layout)

    def save_event(self):
        hour = int(self.hour_box.currentText())
        minute = int(self.minute_box.currentText())
        category = self.combo_category.currentText()
        content = self.text_content.toPlainText().strip()[:20]
        if content:
            save_event(self.date.year(), self.date.month(), self.date.day(), hour, minute, category, content)
        self.accept()

class DateEventsDialog(QtWidgets.QDialog):
    def __init__(self, date, parent=None):
        super().__init__(parent)
        self.date = date
        self.setWindowTitle("日程安排")
        self.resize(400, 300)
        self.initUI()

    def initUI(self):
        layout = QtWidgets.QVBoxLayout()

        all_events = load_events()
        today_events = [
            e for e in all_events
            if e["year"] == self.date.year() and e["month"] == self.date.month() and e["day"] == self.date.day()
        ]
        today_events.sort(key=lambda e: (e["hour"], e["minute"]))

        for e in today_events[:3]:
            block = QtWidgets.QWidget()
            grid = QtWidgets.QGridLayout()

            time_str = f"{e['year']}年{e['month']:02d}月{e['day']:02d}日 {e['hour']:02d}:{e['minute']:02d}"
            time_label = QtWidgets.QLabel(f"{time_str} - {e['category']}")
            content_label = QtWidgets.QLabel(e['content'])

            time_label.setStyleSheet("font-weight: bold; font-size: 15px; color: #333;")
            content_label.setStyleSheet("font-family: 'SimSun'; font-size: 18px; color: #000;")
            content_label.setAlignment(Qt.AlignCenter)

            grid.addWidget(time_label, 0, 0)
            grid.addWidget(content_label, 1, 0)
            block.setLayout(grid)
            block.setStyleSheet("""
                background-color: white;
                border: 1px solid #cce5ff;
                border-radius: 15px;
                padding: 12px;
                margin-bottom: 12px;
            """)
            layout.addWidget(block)

        layout.addStretch()

        btn_add = QtWidgets.QPushButton("+")
        btn_add.setFixedWidth(30)
        btn_add.clicked.connect(self.open_add_event_dialog)
        add_layout = QtWidgets.QHBoxLayout()
        add_layout.addStretch()
        add_layout.addWidget(btn_add)
        layout.addLayout(add_layout)

        self.setLayout(layout)

    def open_add_event_dialog(self):
        dialog = AddEventDialog(self.date, self)
        if dialog.exec_():
            self.close()
            new_dialog = DateEventsDialog(self.date, self.parent())
            new_dialog.exec_()

class Ui_Calendar(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1000, 700)

        self.horizontalLayout = QtWidgets.QHBoxLayout(Dialog)

        self.sidebar = QtWidgets.QFrame(Dialog)
        self.sidebar.setMinimumWidth(200)
        self.sidebar.setMaximumWidth(220)
        self.sidebar.setStyleSheet("""
               QFrame {
                   background-color: #2C3E50;
                   border-top-left-radius: 20px;
                   border-bottom-left-radius: 20px;
               }
               QPushButton {
                   background-color: #34495E;
                   color: white;
                   font-size: 16px;
                   padding: 15px;
                   border-radius: 10px;
               }
               QPushButton:hover {
                   background-color: #3D5A73;
               }
           """)

        self.sidebarLayout = QtWidgets.QVBoxLayout(self.sidebar)
        self.sidebarLayout.setContentsMargins(20, 40, 20, 40)
        self.sidebarLayout.setSpacing(30)

        self.btn_calendar = QtWidgets.QPushButton("DDL日历")
        self.btn_tasks = QtWidgets.QPushButton("任务安排")
        self.btn_health = QtWidgets.QPushButton("健康系统")

        self.sidebarLayout.addStretch()
        self.sidebarLayout.addWidget(self.btn_calendar)
        self.sidebarLayout.addWidget(self.btn_tasks)
        self.sidebarLayout.addWidget(self.btn_health)
        self.sidebarLayout.addStretch()

        self.content = QtWidgets.QFrame(Dialog)
        self.content.setStyleSheet("background-color: white; border-top-right-radius: 20px; border-bottom-right-radius: 20px;")
        self.contentLayout = QtWidgets.QVBoxLayout(self.content)

        self.calendar = QtWidgets.QCalendarWidget(self.content)
        self.calendar.setGridVisible(True)
        self.calendar.setStyleSheet("""
               QCalendarWidget QTableView {
                   selection-background-color: #2980B9;
                   font-size: 14px;
               }
               QCalendarWidget QWidget#qt_calendar_navigationbar {
                   background-color: #3498DB;
               }
           """)
        self.contentLayout.addWidget(self.calendar)

        self.horizontalLayout.addWidget(self.sidebar)
        self.horizontalLayout.addWidget(self.content)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "日历界面"))

    def setup_calendar_styles(self):
        weekend_format = QTextCharFormat()
        weekend_format.setForeground(Qt.red)
        self.calendar.setWeekdayTextFormat(Qt.Saturday, weekend_format)
        self.calendar.setWeekdayTextFormat(Qt.Sunday, weekend_format)

        self.calendar.setStyleSheet("""
            QCalendarWidget QTableView {
                selection-background-color: transparent;
                outline: none;
            }
            QCalendarWidget QTableView::item {
                min-width: 40px;
                min-height: 40px;
                border-radius: 20px;
                margin: 4px;
                padding: 2px;
            }
            QCalendarWidget QTableView::item:hover {
                background-color: #E6F2FF;
                border: 1px solid #007BFF;
            }
        """)

        self.selected_format = QTextCharFormat()
        self.selected_format.setBackground(QBrush(QColor("#B3D7FF")))
        self.selected_format.setForeground(QBrush(Qt.white))
        self.selected_format.setFontWeight(QFont.Bold)

    def update_selected_date(self):
        selected_date = self.calendar.selectedDate()
        if hasattr(self, 'previous_selected_date'):
            self.calendar.setDateTextFormat(self.previous_selected_date, QTextCharFormat())
        self.calendar.setDateTextFormat(selected_date, self.selected_format)
        self.previous_selected_date = selected_date

    def show_date_dialog(self, date):
        dialog = DateEventsDialog(date)
        dialog.exec_()

#健康界面，同日历界面，保证还能够看到每日的日程，更改了左侧三个按钮内容
class Ui_Halendar(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1000, 700)

        self.horizontalLayout = QtWidgets.QHBoxLayout(Dialog)

        self.sidebar = QtWidgets.QFrame(Dialog)
        self.sidebar.setMinimumWidth(200)
        self.sidebar.setMaximumWidth(220)
        self.sidebar.setStyleSheet("""
               QFrame {
                   background-color: #2C3E50;
                   border-top-left-radius: 20px;
                   border-bottom-left-radius: 20px;
               }
               QPushButton {
                   background-color: #34495E;
                   color: white;
                   font-size: 16px;
                   padding: 15px;
                   border-radius: 10px;
               }
               QPushButton:hover {
                   background-color: #3D5A73;
               }
           """)

        self.sidebarLayout = QtWidgets.QVBoxLayout(self.sidebar)
        self.sidebarLayout.setContentsMargins(20, 40, 20, 40)
        self.sidebarLayout.setSpacing(30)

        self.btn_calendar = QtWidgets.QPushButton("体测系统")
        self.btn_tasks = QtWidgets.QPushButton("健康建议")
        self.btn_health = QtWidgets.QPushButton("返回")

        self.sidebarLayout.addStretch()
        self.sidebarLayout.addWidget(self.btn_calendar)
        self.sidebarLayout.addWidget(self.btn_tasks)
        self.sidebarLayout.addWidget(self.btn_health)
        self.sidebarLayout.addStretch()

        self.content = QtWidgets.QFrame(Dialog)
        self.content.setStyleSheet(
            "background-color: white; border-top-right-radius: 20px; border-bottom-right-radius: 20px;")
        self.contentLayout = QtWidgets.QVBoxLayout(self.content)

        self.calendar = QtWidgets.QCalendarWidget(self.content)
        self.calendar.setGridVisible(True)
        self.calendar.setStyleSheet("""
               QCalendarWidget QTableView {
                   selection-background-color: #2980B9;
                   font-size: 14px;
               }
               QCalendarWidget QWidget#qt_calendar_navigationbar {
                   background-color: #3498DB;
               }
           """)
        self.contentLayout.addWidget(self.calendar)

        self.horizontalLayout.addWidget(self.sidebar)
        self.horizontalLayout.addWidget(self.content)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "日历界面"))


class CalendarPage(QtWidgets.QWidget):
    def __init__(self, controller=None, parent=None):
        super().__init__(parent)
        self.controller = controller  # 用于控制导航
        self.ui = Ui_Calendar()
        self.ui.setupUi(self)

        self.calendar = self.ui.calendar  # 简化引用

        # 设置日历样式和交互
        self.setup_calendar_styles()

        # 日期点击交互：展示事件详情
        self.calendar.clicked.connect(self.show_date_dialog)

        # 侧边栏按钮交互
        self.ui.btn_calendar.clicked.connect(lambda: print("已在 DDL 日历界面"))
        if self.controller:
            self.ui.btn_tasks.clicked.connect(self.controller.show_task)  # 示例：返回主界面
            self.ui.btn_health.clicked.connect(self.controller.show_health)

    def setup_calendar_styles(self):
        # 设置周末格式
        weekend_format = QTextCharFormat()
        weekend_format.setForeground(QBrush(QColor("#E74C3C")))  # 红色周末
        self.calendar.setWeekdayTextFormat(Qt.Saturday, weekend_format)
        self.calendar.setWeekdayTextFormat(Qt.Sunday, weekend_format)

        # 使用更完整的样式表，确保选中日期的文字可见
        self.calendar.setStyleSheet("""
            QCalendarWidget QTableView {
                alternate-background-color: #F5F5F5;
                selection-background-color: #B3D7FF;
                selection-color: #000000;  /* 确保选中日期的文字是黑色 */
                font-size: 14px;
                outline: none;
            }

            QCalendarWidget QWidget#qt_calendar_navigationbar {
                background-color: #3498DB;
                color: white;
            }

            QCalendarWidget QToolButton {
                color: white;
                background-color: transparent;
                font-size: 16px;
                font-weight: bold;
            }

            QCalendarWidget QToolButton:hover {
                background-color: #2980B9;
                border-radius: 5px;
            }

            QCalendarWidget QMenu {
                background-color: white;
            }

            /* 日期单元格样式 */
            QCalendarWidget QTableView::item:selected {
                background-color: #B3D7FF;
                color: #000000;  /* 选中时文字颜色 */
                border-radius: 15px;
            }

            QCalendarWidget QTableView::item:hover {
                background-color: #E6F2FF;
                border: 1px solid #007BFF;
                border-radius: 15px;
            }
        """)

    def show_date_dialog(self, date):
        dialog = DateEventsDialog(date, self)
        dialog.exec_()


# 健康界面，同日历界面，保证还能够看到每日的日程，更改了左侧三个按钮内容
class HealthPage(QtWidgets.QWidget):
    def __init__(self, controller=None, parent=None):
        super().__init__(parent)
        self.controller = controller  # 用于控制导航
        self.ui = Ui_Halendar()
        self.ui.setupUi(self)

        self.calendar = self.ui.calendar  # 简化引用

        # 设置日历样式和交互
        self.setup_calendar_styles()

        # 日期点击交互：展示事件详情
        self.calendar.clicked.connect(self.show_date_dialog)

        # 侧边栏按钮交互
        self.ui.btn_calendar.clicked.connect(self.controller.show_test)
        if self.controller:
            self.ui.btn_tasks.clicked.connect(self.controller.show_advice)
            self.ui.btn_health.clicked.connect(self.controller.to_calendar)

    def setup_calendar_styles(self):
        # 设置周末格式
        weekend_format = QTextCharFormat()
        weekend_format.setForeground(QBrush(QColor("#E74C3C")))  # 红色周末
        self.calendar.setWeekdayTextFormat(Qt.Saturday, weekend_format)
        self.calendar.setWeekdayTextFormat(Qt.Sunday, weekend_format)

        # 使用更完整的样式表，确保选中日期的文字可见
        self.calendar.setStyleSheet("""
            QCalendarWidget QTableView {
                alternate-background-color: #F5F5F5;
                selection-background-color: #B3D7FF;
                selection-color: #000000;  /* 确保选中日期的文字是黑色 */
                font-size: 14px;
                outline: none;
            }

            QCalendarWidget QWidget#qt_calendar_navigationbar {
                background-color: #3498DB;
                color: white;
            }

            QCalendarWidget QToolButton {
                color: white;
                background-color: transparent;
                font-size: 16px;
                font-weight: bold;
            }

            QCalendarWidget QToolButton:hover {
                background-color: #2980B9;
                border-radius: 5px;
            }

            QCalendarWidget QMenu {
                background-color: white;
            }

            /* 日期单元格样式 */
            QCalendarWidget QTableView::item:selected {
                background-color: #B3D7FF;
                color: #000000;  /* 选中时文字颜色 */
                border-radius: 15px;
            }

            QCalendarWidget QTableView::item:hover {
                background-color: #E6F2FF;
                border: 1px solid #007BFF;
                border-radius: 15px;
            }
        """)

    def show_date_dialog(self, date):
        dialog = DateEventsDialog(date, self)
        dialog.exec_()