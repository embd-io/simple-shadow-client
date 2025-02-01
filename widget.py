import sys

from PySide6 import QtWidgets
from ui_form import Ui_Form
from PySide6.QtWidgets import QApplication, QFileDialog

class Widget(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.cert_file_path = ""
        self.key_file_path = ""
        
        self.button_browse_cert.clicked.connect(self.browse_cert_file)
        self.button_browse_key.clicked.connect(self.browse_key_file)
        self.button_connect.clicked.connect(self.connect_to_broker)
        self.button_send.clicked.connect(self.send_shadow_document)
        self.button_refresh.clicked.connect(self.refresh_shadow_document)

    def browse_cert_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Select Certificate File", "", "Certificate Files (*.crt);;All Files (*)")
        if filename:
            self.cert_file_path = filename
            self.lineEdit_cert.setText(filename)
            print(f"Selected Certificate: {filename}")

    def browse_key_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Select Key File", "", "Key Files (*.key);;All Files (*)")
        if filename:
            self.key_file_path = filename
            self.lineEdit_key.setText(filename)
            print(f"Selected Key: {filename}")

    def connect_to_broker(self):
        device_name = self.lineEdit_device.text()
        print(f"Connecting to broker with device name: {device_name}, cert: {self.cert_file_path}, key: {self.key_file_path}")
        # Add MQTT connection logic here

    def send_shadow_document(self):
        shadow_document = self.textEdit_editable.toPlainText()
        print(f"Sending shadow document: {shadow_document}")
        # Add MQTT publish logic here

    def refresh_shadow_document(self):
        print("Refreshing shadow document...")
        # Simulate retrieving updated shadow document
        reported_shadow = '{"reported": {"status": "updated"}}'
        self.textEdit_readonly.setPlainText(reported_shadow)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    sys.exit(app.exec())
