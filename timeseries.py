from PyQt5.QtGui import QWheelEvent
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.patches import Rectangle
from matplotlib.widgets import Slider
import re
import time
start_times = []
durations = []
labels = []
sum_number=0
Tick = 0
def push_start(data):
    global start_times
    max_length = 20

    # 将数据添加到列表末尾
    start_times.append(data)

    # 检查列表长度是否超过最大数量
    if len(start_times) > max_length:
        # 删除前面的元素，保留最后的 max_length 个元素
        start_times = start_times[-max_length:]

def push_dur(data):
    global durations
    max_length = 20

    # 将数据添加到列表末尾
    durations.append(data)

    # 检查列表长度是否超过最大数量
    if len(durations) > max_length:
        # 删除前面的元素，保留最后的 max_length 个元素
        durations = durations[-max_length:]

def push_label(data):
    global labels
    max_length = 20

    # 将数据添加到列表末尾
    labels.append(data)

    # 检查列表长度是否超过最大数量
    if len(labels) > max_length:
        # 删除前面的元素，保留最后的 max_length 个元素
        labels = labels[-max_length:]
class TimeSeriesChartWidget(FigureCanvas):
    def __init__(self, parent=None):
        self.figure = Figure()
        super().__init__(self.figure)
        self.setParent(parent)
        self.axes = self.figure.add_subplot(111,frame_on=False)
        self.axes.tick_params(labelcolor='b',top=True,bottom=False,left=False,right=False)
        self.axes.set_xlabel('Time')
        self.axes.set_ylabel('Value')
        self.time_range = 10  # 初始时间范围
        # 添加水平滚动条
        self.ax_slider = self.figure.add_axes([0.1, 0, 0.65, 0.1], facecolor='lightgoldenrodyellow')
        self.slider = Slider(self.ax_slider, 'X Range', 0, 1, valinit=0, valstep=0.1)
        self.slider.on_changed(self.update_plot)
        self.axes.set_xlim(0, 10)

    def plot_blocks(self, start_times, durations, labels):
        # self.axes.clear()
        maxx = 0
        for start_time, duration, label in zip(start_times, durations, labels):
            end_time = start_time + duration
            labelcolor = (0,0,0)
            if label[0] == 'u' :
                labelcolor = (0.5,0.2,0.6)
            elif label[0] == 'm':
                labelcolor = (0.6,0.9,0.2)
            elif label[0] == 'I':
                labelcolor = (0.4,0.2,0.9)
            elif label[0] == 'L':
                labelcolor = (0.9,0.2,0.6)
            rect = Rectangle((start_time, 0), duration, 0.2, facecolor=labelcolor, alpha=0.5)
            self.axes.add_patch(rect)
            self.axes.text(start_time + duration / 2, 0.1, label, ha='center', va='center')
            maxx = max(maxx,start_time+duration)
            print(start_time,end_time,label)
        self.axes.set_xlim(0, 10)
        self.axes.set_ylim(0, 0.2)
        self.draw()

    def wheelEvent(self, event: QWheelEvent):
        if event.angleDelta().y() > 0:
            self.axes.set_xlim(self.axes.get_xlim()[0] * 1.1, self.axes.get_xlim()[1] * 1.1)
        else:
            self.axes.set_xlim(self.axes.get_xlim()[0] * 0.9, self.axes.get_xlim()[1] * 0.9)
        self.draw()

    def update_plot(self, val):
        # 更新X轴范围
        x_min, x_max = self.axes.get_xlim()
        x_range = x_max - x_min
        new_x_min = self.slider.val * x_range
        new_x_max = max(new_x_min + x_range,x_max)
        self.axes.set_xlim(new_x_min, new_x_max)
        self.draw()

    def update_images(self,data):
        # print("timeseries.py "+str(data))
        global Tick
        if data[0] == 't':
            numbers = re.findall(r'\d+', data)
            numbers = [int(x) for x in numbers]
            res = 0
            # if numbers[0]-Tick < 0:
            #     res = numbers[0]-Tick +100
            Tick = numbers[0]
            # if len(start_times) > 0 :
            #     push_start((start_times[-1]+res)%100)
            # else:
            #     push_start(res)
            push_start(Tick)
            if len(start_times) >= 2:
                dur = start_times[-1] - start_times[-2]
                if dur < 0:
                    dur += 100
                push_dur(dur)
        elif data[0] == 'e':
            data = data[2:]
            endstr = data
        elif data[0] == 'b':
            data = data[2:]
            beginstr = data
            push_label(beginstr)
        global sum_number
        sum_number = sum_number+1
        if sum_number%200 == 0:
            self.axes.clear()
            self.plot_blocks(start_times,durations,labels)
            sum_number = 0