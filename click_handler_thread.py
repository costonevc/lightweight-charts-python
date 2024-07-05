from PyQt5.QtCore import QThread, pyqtSignal

class ClickHandlerThread(QThread):
    clicked = pyqtSignal(object, float, float)

    def __init__(self, chart, time, price, interval):
        super().__init__()
        self.chart = chart
        self.time = time
        self.price = price
        self.interval = interval

    def run(self):
        # Convert seconds to milliseconds: 1 second = 1000 milliseconds
        ms_interval = int(self.interval * 1000)  # Convert to integer milliseconds
        self.msleep(ms_interval)  # msleep takes milliseconds as an integer
        self.clicked.emit(self.chart, self.time, self.price)
