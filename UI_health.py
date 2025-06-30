import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtCore import Qt, QPoint
from UI_calendar import save_event
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QTextCharFormat, QBrush, QColor, QFont
from UI_calendar import DateEventsDialog
from datetime import datetime
import json

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
#体测窗口
class TestWindow(QtWidgets.QMainWindow):
    def __init__(self,controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(600, 700)  # 增大窗口尺寸
        
        # 主容器和布局
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        layout = QtWidgets.QVBoxLayout(central_widget)
        
        # 设置白色背景
        central_widget.setStyleSheet("""
            QWidget {
                background: white;
                border-radius: 15px;
            }
        """)

        # 使用网格布局组织输入项
        grid = QtWidgets.QGridLayout()
        
        # 性别选择
        self.gender_group = QtWidgets.QButtonGroup(self)
        self.male_radio = QtWidgets.QRadioButton("男")
        self.female_radio = QtWidgets.QRadioButton("女")
        self.gender_group.addButton(self.male_radio)
        self.gender_group.addButton(self.female_radio)
        
        # 创建所有输入项
        fields = [
            ("性别", [self.male_radio, self.female_radio]),
            ("身高 (cm)", QtWidgets.QLineEdit()),
            ("体重 (kg)", QtWidgets.QLineEdit()),
            ("肺活量 (ml)", QtWidgets.QLineEdit()),
            ("引体向上 (个)", QtWidgets.QLineEdit()),
            ("50米跑 (秒)", QtWidgets.QLineEdit()),
            ("1000米跑 (分:秒)", QtWidgets.QLineEdit()),
            ("坐位体前屈 (cm)", QtWidgets.QLineEdit()),
            ("左眼视力", QtWidgets.QLineEdit()),
            ("右眼视力", QtWidgets.QLineEdit())
        ]
        
        # 统一设置输入框样式
        input_style = """
            QLineEdit, QRadioButton {
                background: #F5F5F5;
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
                border: 1px solid #DDD;
            }
            QRadioButton::indicator {
                width: 20px;
                height: 20px;
            }
        """

        # 添加组件到网格布局
        row = 0
        for label_text, widget in fields:
            label = QtWidgets.QLabel(label_text)
            label.setStyleSheet("font-weight: bold;")
            
            if isinstance(widget, list):  # 性别单选按钮
                hbox = QtWidgets.QHBoxLayout()
                hbox.addWidget(widget[0])
                hbox.addWidget(widget[1])
                hbox.addStretch()
                grid.addWidget(label, row, 0)
                grid.addLayout(hbox, row, 1)
            else:
                widget.setStyleSheet(input_style)
                grid.addWidget(label, row, 0)
                grid.addWidget(widget, row, 1)
            
            row += 1

        # 保存输入对象引用
        self.height_input = fields[1][1]
        self.weight_input = fields[2][1]
        self.lung_input = fields[3][1]
        self.pullup_input = fields[4][1]
        self.sprint_input = fields[5][1]
        self.longrun_input = fields[6][1]
        self.sitreach_input = fields[7][1]
        self.eye_left_input = fields[8][1]
        self.eye_right_input = fields[9][1]

        # 按钮区域
        btn_layout = QtWidgets.QHBoxLayout()
        self.save_btn = QtWidgets.QPushButton("保存数据")
        self.save_btn.clicked.connect(self.save_data)
        self.back_btn = QtWidgets.QPushButton("返回")
        self.back_btn.clicked.connect(self.controller.Test_to_Health)
        
        # 按钮样式
        btn_style = """
            QPushButton {
                min-width: 120px;
                padding: 10px;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton#save {
                background: #4CAF50;
                color: white;
            }
            QPushButton#back {
                background: #607D8B;
                color: white;
            }
        """
        self.save_btn.setObjectName("save")
        self.back_btn.setObjectName("back")
        self.save_btn.setStyleSheet(btn_style)
        self.back_btn.setStyleSheet(btn_style)
        
        btn_layout.addWidget(self.back_btn)
        btn_layout.addWidget(self.save_btn)
        
        # 组合布局
        layout.addLayout(grid)
        layout.addLayout(btn_layout)
        
        # 数据存储
        self.data_file = "health_data.csv"
        self.load_data()

    def load_data(self):
        """加载存储的数据"""
        try:
                with open(self.data_file, "r") as f:
                    data = f.read().split(',')
                if len(data) == 10:
                    gender = data[0]
                    self.male_radio.setChecked(gender == "男")
                    self.female_radio.setChecked(gender == "女")
                    self.height_input.setText(data[1])
                    self.weight_input.setText(data[2])
                    self.lung_input.setText(data[3])
                    self.pullup_input.setText(data[4])
                    self.sprint_input.setText(data[5])
                    self.longrun_input.setText(data[6])
                    self.sitreach_input.setText(data[7])
                    self.eye_left_input.setText(data[8])
                    self.eye_right_input.setText(data[9])
        except FileNotFoundError:
            pass

    def validate_inputs(self):
        """验证所有输入有效性"""
        try:
            float(self.height_input.text())
            float(self.weight_input.text())
            int(self.lung_input.text())
            int(self.pullup_input.text())
            float(self.sprint_input.text())
            self.parse_time(self.longrun_input.text())
            float(self.sitreach_input.text())
            float(self.eye_left_input.text())
            float(self.eye_right_input.text())
            return True
        except ValueError:
            return False

    def parse_time(self, time_str):
        """解析分:秒格式时间为秒数"""
        if ':' in time_str:
            minutes, seconds = map(float, time_str.split(':'))
            return minutes * 60 + seconds
        return float(time_str)

    def save_data(self):
        """保存数据到CS文件"""
        
        gender = "男" if self.male_radio.isChecked() else "女"
        data = [
            gender,
            self.height_input.text(),
            self.weight_input.text(),
            self.lung_input.text(),
            self.pullup_input.text(),
            self.sprint_input.text(),
            self.longrun_input.text(),
            self.sitreach_input.text(),
            self.eye_left_input.text(),
            self.eye_right_input.text()
        ]
        
        with open(self.data_file, "w") as f:
            f.write(",".join(data))
        
        QtWidgets.QMessageBox.information(self, "保存成功", "所有数据已保存！")

    

    # 保持窗口拖动功能
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and hasattr(self, 'drag_pos'):
            self.move(event.globalPos() - self.drag_pos)
            event.accept()
#人体示意图窗口
class AdviceWindow(QtWidgets.QMainWindow):
    def __init__(self, controller,parent=None):
        super().__init__(parent=parent)
        self.controller = controller
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(600, 1000)  # 与主窗口保持一致
        self.move(700,50)

        # 设置中心组件
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        
        # 垂直布局
        layout = QtWidgets.QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        h_layout = QtWidgets.QHBoxLayout()
        h_layout.addStretch()
        # 添加图片标签
        self.image_label = QtWidgets.QLabel()
        # 加载图片（请替换实际路径）
        pixmap = QtGui.QPixmap("test.png")  
        if not pixmap.isNull():
            scaled_width = 400
            scaled_pixmap = pixmap.scaledToWidth(scaled_width, Qt.SmoothTransformation)
            self.image_label.setPixmap(scaled_pixmap)
            eye_content=read_content("health/eye.txt")
            shoulder_content=read_content("health/shoulder.txt")
            back_content=read_content("health/back.txt")
            chest_content=read_content("health/chest.txt")
            leg_content=read_content("health/leg.txt")
            arm_content=read_content("health/arm.txt")
            abdomen_content=read_content("health/abdomen.txt")
            
            btn1 = CustomButton(
                parent=self.image_label,
                text="眼睛",
                content=eye_content,
                f_name="advice/eye.txt",
                position=(200, 20),  # 距离右下角20px偏移
                style="background-color: rgba(173, 216, 230, 200);"  # 淡蓝色
            )

            btn2 = CustomButton(
                parent=self.image_label,
                text="肩部",
                content=shoulder_content,
                f_name="advice/shoulder.txt",
                position=(100, 130),  # 距离右下角20px偏移
                style="background-color: rgba(173, 216, 230, 200);"  # 淡蓝色
            )

            btn3 = CustomButton(
                parent=self.image_label,
                text="胸部",
                content=chest_content,
                f_name="advice/chest.txt",
                position=(150, 200),  # 距离右下角20px偏移
                style="background-color: rgba(173, 216, 230, 200);"  # 淡蓝色
            )

            btn4 = CustomButton(
                parent=self.image_label,
                text="背部",
                content=back_content,
                f_name="advice/back.txt",
                position=(250, 250),  # 距离右下角20px偏移
                style="background-color: rgba(173, 216, 230, 200);"  # 淡蓝色
            )

            btn5 = CustomButton(
                parent=self.image_label,
                text="腹部",
                content=abdomen_content,
                f_name="advice/abdomen.txt",
                position=(250, 325),  # 距离右下角20px偏移
                style="background-color: rgba(173, 216, 230, 200);"  # 淡蓝色
            )

            btn6 = CustomButton(
                parent=self.image_label,
                text="手臂",
                content=arm_content,
                f_name="advice/arm.txt",
                position=(75, 325),  # 距离右下角20px偏移
                style="background-color: rgba(173, 216, 230, 200);"  # 淡蓝色
            )

            btn7 = CustomButton(
                parent=self.image_label,
                text="腿部",
                content=leg_content,
                f_name="advice/leg.txt",
                position=(150, 600),  # 距离右下角20px偏移
                style="background-color: rgba(173, 216, 230, 200);"  # 淡蓝色
            )

        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setScaledContents(True)  # 图片自适应
        h_layout.addWidget(self.image_label)
        h_layout.addStretch()
        layout.addLayout(h_layout)
        # 添加返回按钮
        self.back_btn = QtWidgets.QPushButton("返回")
        self.back_btn.setFixedSize(100, 30)
        self.back_btn.clicked.connect(self.controller.Advice_to_Health)

        # 将组件添加到布局
        layout.addWidget(self.image_label)
        layout.addWidget(self.back_btn, alignment=Qt.AlignCenter)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.drag_pos)
            self.drag_pos = event.globalPos()        

    
#部位按钮类
class CustomButton(QtWidgets.QPushButton):
    def __init__(self, parent, text, content, f_name,position, style=None):
       
        super().__init__(text, parent)
        
        # 基础样式
        base_style = """
        QPushButton {
            background-color: rgba(255, 255, 255, 200);
            border: 2px solid #2c3e50;
            border-radius: 15px;
            padding: 8px;
            min-width: 80px;
            font-weight: bold;
            color: #2c3e50;
        }
        QPushButton:hover {
            background-color: rgba(255, 255, 255, 230);
            border-color: #3498db;
        }
        """
        self.setStyleSheet(style or base_style)
        self.setCursor(Qt.PointingHandCursor)
        
        # 自动计算位置
        self.parent_widget = parent
        self.position = position
        self.adjustPosition()
        
        # 绑定点击事件
        self.clicked.connect(lambda: self.show_text_window(content,f_name))

    def adjustPosition(self):
        """根据父组件尺寸调整位置"""
        parent_size = self.parent_widget.size()
        self.move(
            self.position[0],
            self.position[1]
        )

    def show_text_window(self, content,f_name):
        """显示文字窗口"""
        self.window = CustomTextWindow(
            title="详细信息",
            content=content,
            f_name=f_name,
            parent=self
        )
        self.window.exec_()
#部位详情窗口类
class CustomTextWindow(QtWidgets.QDialog):
    def __init__(self, title, content,f_name, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumSize(400, 300)
        self.f_name=f_name
        
        layout = QtWidgets.QVBoxLayout(self)
        
        # 文字显示区域（支持HTML）
        self.text_browser = QtWidgets.QTextBrowser()
        self.text_browser.setHtml(content)
        self.text_browser.setOpenExternalLinks(True)  # 允许打开外部链接
        
        # 关闭按钮
        close_btn = QtWidgets.QPushButton("关闭")
        close_btn.clicked.connect(self.close)
        close_btn.setFixedSize(150, 30)
        ex_btn = QtWidgets.QPushButton("一键添加计划")
        ex_btn.clicked.connect(self.add_advice)
        ex_btn.setFixedSize(150, 30)
        
        layout.addWidget(self.text_browser)
        layout.addWidget(ex_btn, alignment=Qt.AlignCenter)
        layout.addWidget(close_btn, alignment=Qt.AlignCenter)
    
    def add_advice(self):
        content=read_content(self.f_name)
        if(content!="无"):
            content=content.split()
            save_event(int(content[0]),int(content[1]),int(content[2]),int(content[3]),int(content[4]),content[5],content[6])
            QtWidgets.QMessageBox.information(self, "成功", "添加计划成功！")
        else:
            
            QtWidgets.QMessageBox.information(self, "失败！", "添加计划失败！")


        
#功能函数        
#读取详情文件
def read_content(name):
    try:
        with open(name, 'r',encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        with open(name, 'w',encoding='utf-8') as f:
            f.write('无')
        with open(name, 'r',encoding='utf-8') as f:
            return f.read()

