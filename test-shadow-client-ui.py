"""
Copyright (c) 2023 embd-io
latyr.fall@embd-io.com

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import sys
import json
from time import sleep

from PySide6 import QtWidgets, QtGui
from ui_form import Ui_Form
from PySide6.QtWidgets import QApplication, QFileDialog

from shadow_client import ShadowClient
from awsiot import iotshadow

class Widget(QtWidgets.QWidget, Ui_Form):
    """"""
    
    def __init__(self):
        """"""
        super().__init__()
        self.setupUi(self)
        
        self.cert_file_path = ""
        self.key_file_path = ""
        self.root_file_path = ""
        self.device_name = ""
        self.endpoint = ""
        self.port = 0
        
        self.connected = False

        self.button_browse_cert.clicked.connect(self.browse_cert_file)
        self.button_browse_key.clicked.connect(self.browse_key_file)
        self.button_browse_root.clicked.connect(self.browse_root_file)
        self.button_connect.clicked.connect(self.connect_to_broker)
        self.button_send.clicked.connect(self.send_shadow_document)
        self.button_refresh.clicked.connect(self.refresh_shadow_document)

        self.shadow_client = ShadowClient()

        self.DEFAULT_CONFIG_FILE = "default-config.json"
        self.load_default_config(self.DEFAULT_CONFIG_FILE)

    def closeEvent(self, event):
        """"""
        try:
            if self.connected:
                self.shadow_client.disconnect(0)
                self.shadow_client.wait_for_disconnection()
        except Exception as e:
            print(f"Failed to disconnect: {e}")
        super().closeEvent(event)

    def load_default_config(self, filename):
        """"""
        try:
            config = json.load(open(filename, "r"))
            self.lineEdit_device.setText(config['clientId'])
            self.lineEdit_endpoint.setText(config['endpoint'])
            self.lineEdit_cert.setText(config['cert'])
            self.lineEdit_key.setText(config['key'])
            self.lineEdit_root.setText(config['ca'])
            self.lineEdit_port.setText(str(config['port']))
        except Exception as e:
            print(f"Failed to load default config: {e}")

    def browse_cert_file(self):
        """"""
        filename, _ = QFileDialog.getOpenFileName(self, "Select Certificate File", "", "Certificate Files (*.crt);;All Files (*)")
        if filename:
            self.cert_file_path = filename
            self.lineEdit_cert.setText(filename)
            print(f"Selected Certificate: {filename}")

    def browse_key_file(self):
        """"""
        filename, _ = QFileDialog.getOpenFileName(self, "Select Key File", "", "Key Files (*.key);;All Files (*)")
        if filename:
            self.key_file_path = filename
            self.lineEdit_key.setText(filename)
            print(f"Selected Key: {filename}")

    def browse_root_file(self):
        """"""
        filename, _ = QFileDialog.getOpenFileName(self, "Select Root CA File", "", "Key Files (*.pem);;All Files (*)")
        if filename:
            self.root_file_path = filename
            self.lineEdit_root.setText(filename)
            print(f"Selected Root CA: {filename}")

    def connect_to_broker(self):
        """"""
        try:
            self.cert_file_path = self.lineEdit_cert.text()
            self.key_file_path = self.lineEdit_key.text()
            self.root_file_path = self.lineEdit_root.text()
            self.device_name = self.lineEdit_device.text()
            self.endpoint = self.lineEdit_endpoint.text()
            self.port = int(self.lineEdit_port.text())
            print(f"Connecting to broker at {self.endpoint}:{self.port}...")
            self.shadow_client.connect(self.endpoint, self.port, self.cert_file_path, self.key_file_path, self.root_file_path, self.device_name)
            self.shadow_client.subscribe()
            self.connected = True
            self.button_connect.setPalette(QtGui.QPalette(QtGui.QColor("green")))
        except Exception as e:
            print(f"Failed to connect: {e}")

    def send_shadow_document(self):
        """"""
        shadow_text = self.textEdit_editable.toPlainText()
        print(f"Sending shadow document: {shadow_text}")
        try:
            shadow_obj = json.loads(shadow_text)
            self.textEdit_editable.setPlainText(json.dumps(shadow_obj, indent=2))
            if 'desired' in shadow_obj.keys():
                self.shadow_client.publish_update_shadow(shadow_obj['desired'])
        except Exception as e:
            print(f"Failed to send shadow document: {e}")


    def refresh_shadow_document(self):
        """"""
        print("Refreshing shadow document...")
        try:
            self.shadow_client.fetch_shadow_document()
            sleep(2)
            state: iotshadow.ShadowStateWithDelta = self.shadow_client.get_shadow_document()
            obj = {'delta': state.delta, 'reported': state.reported, 'desired': state.desired}
            self.textEdit_readonly.setPlainText(json.dumps(obj, indent=2))
        except Exception as e:
            print(f"Failed to refresh shadow document: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    sys.exit(app.exec())
