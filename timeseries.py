from PyQt5.QtGui import QWheelEvent
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.patches import Rectangle
from matplotlib.widgets import Slider

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
        self.axes.clear()
        for start_time, duration, label in zip(start_times, durations, labels):
            end_time = start_time + duration
            hashsum = hash(label)
            labelcolor =(float(hashsum%11)/11.0,float(hashsum%45)/45,float(hashsum%14)/14.0)
            rect = Rectangle((start_time, 0), duration, 0.2, facecolor=labelcolor, alpha=0.5)
            self.axes.add_patch(rect)
            self.axes.text(start_time + duration / 2, 0.1, label, ha='center', va='center')

        self.axes.set_xlim(0, max(start_times + durations) + 1)
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
