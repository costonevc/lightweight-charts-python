from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPlainTextEdit
from PyQt5.QtCore import QTimer
import sys
import asyncio
import qasync
from combined_window import PolygonQChart

class MainWindow(QMainWindow):
    def __init__(self, api_key):
        super().__init__()
        self.resize(800, 600) 
        self.setWindowTitle("Polygon Chart with Interactive Features")
        
        widget = QWidget(self)
        self.setCentralWidget(widget)
        layout = QVBoxLayout(widget)

        self.chart = PolygonQChart(api_key=api_key, widget=widget, width=800, height=550, live=True)
        layout.addWidget(self.chart.get_webview(), 3)

        self.log_widget = QPlainTextEdit()
        self.log_widget.setReadOnly(True)
        layout.addWidget(self.log_widget, 1)

        self.chart.init_bridge(self)

        QTimer.singleShot(100, self.show_chart)

    def show_chart(self):
        self.chart.show()

    def log_message(self, message):
        self.log_widget.appendPlainText(message)


async def main(api_key):
    app = QApplication(sys.argv)
    qloop = qasync.QEventLoop(app)
    asyncio.set_event_loop(qloop)
    
    main_window = MainWindow(api_key=api_key)
    main_window.show()
    
    with qloop:
        await qloop.run_forever()

if __name__ == '__main__':
    try:
        asyncio.run(main(api_key="4EMv8sLwboYtrmq15pFTZdNO2aRv8yUF"))
    except KeyboardInterrupt:
        print("Application closed by user")