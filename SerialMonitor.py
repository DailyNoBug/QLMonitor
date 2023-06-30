import sys
import serial
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QAction, QFileDialog


class SerialMonitorWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.serial_port = None
        self.text_edit = QTextEdit()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Serial Monitor")
        self.setCentralWidget(self.text_edit)

        # 创建菜单栏
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")

        # 创建保存日志的动作
        save_action = QAction("Save Log", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_log)
        file_menu.addAction(save_action)

        # 打开串口
        self.open_serial_port()

    def open_serial_port(self):
        port_name = "/dev/ttyUSB0"  # 串口名称，根据实际情况修改
        baud_rate = 9600  # 波特率，根据实际情况修改

        try:
            self.serial_port = serial.Serial(port_name, baud_rate)
            self.serial_port.open()
            self.serial_port.flushInput()
            self.serial_port.flushOutput()
        except serial.SerialException as e:
            print(f"Failed to open serial port: {e}")
            sys.exit()

        self.serial_port_ready()

    def serial_port_ready(self):
        while self.serial_port.isOpen():
            if self.serial_port.inWaiting() > 0:
                received_data = self.serial_port.readline().decode().strip()
                self.text_edit.append(received_data)

    def save_log(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Log", "", "Text Files (*.txt)")

        if file_path:
            with open(file_path, "w") as file:
                file.write(self.text_edit.toPlainText())
                print(f"Log saved to: {file_path}")


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = SerialMonitorWindow()
#     window.show()
#     sys.exit(app.exec_())
