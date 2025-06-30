import sys
import random
import json
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import (
    QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsPathItem,
    QGraphicsTextItem, QGraphicsItemGroup, QLineEdit, QPushButton, QWidget, QVBoxLayout, QHBoxLayout
)
from PyQt5.QtCore import Qt, QPointF, QRectF
from PyQt5.QtGui import QColor, QPolygonF, QBrush, QPen, QPainterPath

class TaskPriority(QMainWindow):
    def __init__(self,controller):
        super().__init__()
        # 修改任务提醒标签为左上角位置，并添加关闭按钮
        self.controller = controller
        self.reminder_frame = QtWidgets.QFrame(self)
        self.reminder_frame.setGeometry(20, 400, 360, 160)
        self.reminder_frame.setStyleSheet("""
            QFrame {
                background-color: #fff3cd;
                color: #856404;
                border: 2px solid #ffeeba;
                border-radius: 10px;
            }
        """)

        self.reminder_layout = QtWidgets.QVBoxLayout(self.reminder_frame)
        self.reminder_label = QtWidgets.QLabel()
        self.reminder_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-family: 'Microsoft YaHei';
            }
        """)
        self.reminder_label.setWordWrap(True)
        self.reminder_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.reminder_label.setText("<b>✅ 暂无即将到期任务</b>")

        self.close_button = QtWidgets.QPushButton("X")
        self.close_button.setFixedSize(25, 25)
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #856404;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                color: red;
            }
        """)
        self.close_button.clicked.connect(self.reminder_frame.hide)

        top_bar = QtWidgets.QHBoxLayout()
        top_bar.addStretch()
        top_bar.addWidget(self.close_button)
        import json
        from datetime import datetime

        reminders = []
        try:
            with open("calendar_events.json", "r", encoding="utf-8") as f:
                tasks = json.load(f)
                now = datetime.now()
                for task in tasks:
                    try:
                        dt = datetime(task['year'], task['month'], task['day'], task['hour'], task['minute'])
                        delta = (dt - now).days
                        if 0 <= delta <= 7:
                            content = task.get("content", "未命名任务")
                            reminders.append(f"● {content}：还有 {delta} 天")
                    except:
                        continue
        except:
            reminders.append("任务提醒读取失败")

        if reminders:
            self.reminder_label.setText("<b>📌 即将到期任务：</b><br>" + "<br>".join(reminders[-3:]))
        else:
            self.reminder_label.setText("<b>✅ 暂无即将到期任务</b>")

        self.reminder_layout.addLayout(top_bar)
        self.reminder_layout.addWidget(self.reminder_label)
        
        self.setWindowTitle('任务优先级四象限')
        self.setGeometry(500, 150, 1000, 650)

        self.task_offsets = {
            'Q1': -150,
            'Q2': -150,
            'Q3': 50,
            'Q4': 50
        }

        self.initUI()
        self.reminder_frame.raise_()
        # 读取json任务并加载
        self.load_tasks_from_json()

    def closeEvent(self, event):
        """重写关闭事件 - 关闭当前窗口并打开新窗口"""
        # 接受关闭事件，允许窗口关闭
        event.accept()
        self.controller.show_calendar()
        
    def initUI(self):
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(-300, -275, 600, 550)

        self.view = QGraphicsView(self.scene, self)
        self.view.setRenderHint(QtGui.QPainter.Antialiasing)
        self.view.setRenderHint(QtGui.QPainter.SmoothPixmapTransform)
        self.view.centerOn(0, 0)

        self.draw_quadrants()

        self.task_input = QLineEdit(self)
        self.task_input.setPlaceholderText("请输入任务名称")
        self.add_button = QPushButton("添加任务", self)
        self.add_button.clicked.connect(self.handle_add_task)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.task_input)
        input_layout.addWidget(self.add_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.view)
        main_layout.addLayout(input_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def draw_quadrants(self):
        pen = QPen(Qt.black)

        self.scene.addLine(0, -250, 0, 200, pen)
        self.scene.addLine(-300, 0, 300, 0, pen)

        self.add_arrow(0, -260, direction='up')
        self.add_arrow(310, 0, direction='right')

        self.add_label(250, -25, '<b>紧急程度</b>', '#000000', size=14)
        self.add_label(-35, -260, '<b>重要程度</b>', '#000000', size=14)

        self.add_label(-200, -240, '<b style="font-size:16px;">重要紧急</b>', '#D32F2F')
        self.add_label(60, -240, '<b style="font-size:16px;">重要不紧急</b>', '#388E3C')
        self.add_label(-200, 20, '<b style="font-size:16px;">不重要不紧急</b>', '#1976D2')
        self.add_label(60, 20, '<b style="font-size:16px;">不重要紧急</b>', '#F9A825')

    def add_arrow(self, x, y, direction='up'):
        arrow_size = 10
        pen = QPen(Qt.black)
        brush = QBrush(Qt.black)

        if direction == 'up':
            points = QPolygonF([
                QPointF(x, y),
                QPointF(x - arrow_size / 2, y + arrow_size),
                QPointF(x + arrow_size / 2, y + arrow_size)
            ])
        elif direction == 'right':
            points = QPolygonF([
                QPointF(x, y),
                QPointF(x - arrow_size, y - arrow_size / 2),
                QPointF(x - arrow_size, y + arrow_size / 2)
            ])
        else:
            return

        self.scene.addPolygon(points, pen, brush)

    def add_label(self, x, y, text, color, size=14):
        text_item = QGraphicsTextItem()
        html = f"""
        <div style="
            color: {color};
            font-size: {size}px;
            text-align: center;
            font-family: 'PingFang SC', 'Microsoft YaHei', 'Helvetica Neue', Arial, sans-serif;
            font-weight: bold;">
            {text}
        </div>
        """
        text_item.setHtml(html)
        text_item.setTextWidth(150)
        text_item.setPos(x, y)
        self.scene.addItem(text_item)

    def add_task(self, x, y, text, color, quadrant):
        char_width = 12
        padding = 30
        width = min(max(len(text) * char_width + padding, 150), 300)
        height = 50
        radius = 12

        rect = QRectF(0, 0, width, height)
        path = QPainterPath()
        path.addRoundedRect(rect, radius, radius)

        background_colors = {
            'Q1': "#FFEBEE",
            'Q2': "#E8F5E9",
            'Q3': "#E3F2FD",
            'Q4': "#FFFDE7"
        }

        task_item = QGraphicsPathItem(path)
        task_item.setBrush(QBrush(QColor(background_colors.get(quadrant, "#FFFACD"))))
        task_item.setPen(QPen(QColor("#CDAD00"), 1))

        label = QGraphicsTextItem(text)
        label.setDefaultTextColor(Qt.black)
        label.setTextWidth(width - 20)
        label.setPos(10, 12)

        group = self.scene.createItemGroup([task_item, label])
        group.setPos(x, y)
        group.setFlag(QGraphicsItemGroup.ItemIsMovable)

    def handle_add_task(self):
        task_text = self.task_input.text().strip()
        if not task_text:
            return

        quadrant = random.choice(['Q1', 'Q2', 'Q3', 'Q4'])
        x_positions = {
            'Q1': -200,
            'Q2': 50,
            'Q3': -200,
            'Q4': 50
        }

        y = self.task_offsets[quadrant]
        x = x_positions[quadrant]

        self.add_task(x, y, task_text, Qt.lightGray, quadrant)
        self.task_offsets[quadrant] += 60
        self.task_input.clear()

    def load_tasks_from_json(self):
        try:
            with open("calendar_events.json", "r", encoding="utf-8") as f:
                tasks = json.load(f)
                for task in tasks:
                    content = task.get("content", "无标题任务")
                    quadrant = random.choice(['Q1', 'Q2', 'Q3', 'Q4'])
                    x_positions = {
                        'Q1': -200,
                        'Q2': 50,
                        'Q3': -200,
                        'Q4': 50
                    }
                    y = self.task_offsets[quadrant]
                    x = x_positions[quadrant]
                    self.add_task(x, y, content, Qt.lightGray, quadrant)
                    self.task_offsets[quadrant] += 60
        except Exception as e:
            print(f"读取 calendar_events.json 出错: {e}")    