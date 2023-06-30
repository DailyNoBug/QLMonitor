from PyQt5.QtWidgets import QWidget, QVBoxLayout, QComboBox, QTextEdit, QHBoxLayout
from PyQt5.QtCore import QThread, pyqtSignal
import re
import serial

selected_port = '/dev/ttyUSB0'

Tick = 0
endstr = ""
beginstr = ""

class SerialReaderThread(QThread):
    dataReceived = pyqtSignal(str)
    def __init__(self,port):
        super().__init__()
        self.port = port
        self.serial_port = None

    def run(self):
        self.serial_port = serial.Serial(self.port,baudrate=9600)
        while True:
            try:
                line = self.serial_port.readline().decode().strip()
                if line :
                    data = str(line)
                    self.dataReceived.emit(data)
            except serial.SerialException:
                break

    def stop(self):
        if self.serial_port and self.serial_port.is_open :
            self.serial_port.close()
class SerialPortWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()

        # 创建串口选择框
        self.combo_box = QComboBox()
        self.combo_box.currentIndexChanged.connect(self.serial_port_selected)
        layout.addWidget(self.combo_box)

        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)

        # 添加串口选项
        self.populate_serial_ports()
        self.setLayout(layout)
        self.setWindowTitle("Serial Port Widget")

    def populate_serial_ports(self):
        # 假设这里使用了PySerial库来获取可用的串口列表
        import serial.tools.list_ports

        ports = serial.tools.list_ports.comports()
        for port in ports:
            self.combo_box.addItem(port.device)

    def serial_port_selected(self, index):
        selected_port = self.combo_box.itemText(index)

        self.text_edit.clear()  # 清空文本框内容

        # 创建串口读取线程，并连接数据接收信号到槽函数
        self.serial_thread = SerialReaderThread(selected_port)
        self.serial_thread.dataReceived.connect(self.handle_data_received)
        self.serial_thread.start()

    def handle_data_received(self, data):
        self.text_edit.append(data)
        # print("Serialbotton"+data)