import sys
import serial
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit
from PyQt5.QtCore import QThread, pyqtSignal


class SerialReaderThread(QThread):
    data_received = pyqtSignal(str)

    def __init__(self, port='/dev/ttyUSB0', baud_rate=9600):
        super().__init__()
        self.port = port
        self.baud_rate = baud_rate
        self.serial_port = None

    def run(self):
        try:
            self.serial_port = serial.Serial(self.port, self.baud_rate)
            self.serial_port.open()
            self.serial_port.flushInput()
            self.serial_port.flushOutput()

            while True:
                if self.serial_port.inWaiting() > 0:
                    data = self.serial_port.readline().decode().strip()
                    self.data_received.emit(data)
        except serial.SerialException as e:
            print(f"Failed to open serial port: {e}")


class SerialMonitorWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.serial_thread = None
        self.text_edit = QTextEdit()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Serial Monitor")
        self.setCentralWidget(self.text_edit)

        # 打开串口
        self.open_serial_port()

    def open_serial_port(self):
        port_name = "/dev/ttyUSB0"  # 串口名称，根据实际情况修改
        baud_rate = 9600  # 波特率，根据实际情况修改

        self.serial_thread = SerialReaderThread(port_name, baud_rate)
        self.serial_thread.data_received.connect(self.handle_data_received)
        self.serial_thread.start()

    def handle_data_received(self, data):
        self.text_edit.append(data)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SerialMonitorWindow()
    window.show()
    sys.exit(app.exec_())
