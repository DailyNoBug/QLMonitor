import sys
import serial
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtCore import QThread, pyqtSignal
from Serialbotton import SerialPortWidget
import Serialbotton
from timeseries import TimeSeriesChartWidget
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.chart_widget = TimeSeriesChartWidget()
        # self.reader_thread = SerialReaderThread(Serialbotton.selected_port)
        # self.reader_thread.dataReceived.connect(self.handleDataReceive)
        # self.reader_thread.start()

        start_times = [0, 2, 4, 7]  # 每个块的开始时间
        durations = [2, 3, 1, 4]  # 每个块的持续时间
        labels = ['State 1', 'State 2', 'State 3', 'State 4']  # 每个块的标签
        self.chart_widget.plot_blocks(start_times, durations, labels)

        self.serial_botton_widget = SerialPortWidget()
        print(type(self.serial_botton_widget))

        time_layout = QVBoxLayout()
        below_layout = QHBoxLayout()
        time_layout.addWidget(self.chart_widget,2)  #添加时间轴界面
        below_layout.addWidget(self.serial_botton_widget)
        time_layout.addLayout(below_layout,1)  #将下方的水平布局管理器加入

        central_widget = QWidget()
        central_widget.setLayout(time_layout)
        self.setCentralWidget(central_widget)
    def handleDataReceive(self,data):
        print(f'Data receive: {data}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("QLMonitor")
    window.show()
    sys.exit(app.exec_())
