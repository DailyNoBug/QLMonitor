import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout
# from Serialbotton import SerialPortWidget
import Serialbotton
from timeseries import TimeSeriesChartWidget
from timeseries import start_times,durations,labels

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.chart_widget = TimeSeriesChartWidget()
        # self.reader_thread = SerialReaderThread(Serialbotton.selected_port)
        # self.reader_thread.dataReceived.connect(self.handleDataReceive)
        # self.reader_thread.start()
        global start_times,durations,labels
        self.chart_widget.plot_blocks(start_times, durations, labels)

        self.serial_botton_widget = Serialbotton.SerialPortWidget()

        self.reader_thread = self.serial_botton_widget.serial_thread
        self.reader_thread.dataReceived.connect(self.chart_widget.update_images)
        self.reader_thread.start()

        time_layout = QVBoxLayout()
        below_layout = QHBoxLayout()
        time_layout.addWidget(self.chart_widget,1)  #添加时间轴界面
        below_layout.addWidget(self.serial_botton_widget)
        time_layout.addLayout(below_layout,2)  #将下方的水平布局管理器加入

        central_widget = QWidget()
        central_widget.setLayout(time_layout)
        self.setCentralWidget(central_widget)
    def handleDataReceive(self,data):
        print(f'Data receive: {data}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    global window
    window = MainWindow()
    window.setWindowTitle("QLMonitor")
    window.show()
    sys.exit(app.exec_())
