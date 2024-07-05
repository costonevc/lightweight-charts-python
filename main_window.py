""" pyqt5 csv file and horizontal line """
# import pandas as pd
# from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPlainTextEdit, QInputDialog
# from lightweight_charts.widgets import QtChart
# from click_handler_thread import ClickHandlerThread  
# import asyncio
# from lightweight_charts import Chart

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.resize(800, 600)
#         widget = QWidget()
#         layout = QVBoxLayout(widget)
#         self.setCentralWidget(widget)

#         self.chart = QtChart(widget)
#         layout.addWidget(self.chart.get_webview(), 3)

#         self.log_widget = QPlainTextEdit()
#         self.log_widget.setReadOnly(True)
#         layout.addWidget(self.log_widget, 1)


#         self.horizontal_lines = {}
#         self.tolerance = 0.5
#         self.click_thread = None
#         self.click_interval = 0.3
        
#         self.ticker = "AAPL" # Default ticker
#         file_path = "/Users/jiarui/Desktop/Summer2024/ohlcv.csv"
#         df = pd.read_csv(file_path)
#         self.chart.set(df)

#         self.chart.events.click += self.on_click
#         self.chart.events.double_click += self.on_double_click

#     def log_message(self, message):
#         print(message)
#         self.log_widget.appendPlainText(message)

#     def handle_click(self, chart, time, price):
#         # line = chart.horizontal_line(price)
#         # self.horizontal_lines[line.id] = line
#         # self.log_message(f"Added horizontal line at price: {price}")
#         quantity, ok = QInputDialog.getInt(window, "Purchase Quantity", "Enter the number of shares to buy:")
#         if ok and quantity > 0:
#             line = chart.horizontal_line(price)
#             self.horizontal_lines[line.id] = line
#             self.log_message(f"Added horizontal line at price: {price}")
#             self.log_message(f"Buy {quantity} of {self.ticker} at {price}")

#     def on_click(self, chart, time, price):
#         from click_handler_thread import ClickHandlerThread
#         if self.click_thread is not None:
#             self.click_thread.terminate()
#             self.click_thread.wait()

#         self.click_thread = ClickHandlerThread(chart, time, price, self.click_interval)
#         self.click_thread.clicked.connect(self.handle_click)
#         self.click_thread.start()

#     def on_double_click(self, chart, time, price):
#         if self.click_thread is not None:
#             self.click_thread.terminate()
#             self.click_thread.wait()

#         for line_id, line in list(self.horizontal_lines.items()):
#             if abs(line.price - price) < self.tolerance:
#                 line.delete()
#                 del self.horizontal_lines[line_id]
#                 self.log_message(f"Removed horizontal line at price: {price}")

# if __name__ == '__main__':
#     app = QApplication([])
#     window = MainWindow()
#     window.show()
#     app.exec_()

""" pyqt5 polygon and horizontal line """
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPlainTextEdit, QInputDialog
from PyQt5.QtCore import QThread, pyqtSignal
from lightweight_charts.widgets import QtChart
from click_handler_thread import ClickHandlerThread  

class DataFetcher(QThread):
    dataLoaded = pyqtSignal(bool)

    def __init__(self, chart, ticker, timeframe, start_date):
        super().__init__()
        self.chart = chart
        self.ticker = ticker
        self.timeframe = timeframe
        self.start_date = start_date

    def run(self):
        self.chart.polygon.api_key('q0TtwNDqD1yz2pnD96HDLOBTMSKVh2Zl')
        self.chart.polygon.stock(
            symbol=self.ticker,
            timeframe=self.timeframe,
            start_date=self.start_date
        )
        self.dataLoaded.emit(True)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(800, 500)
        widget = QWidget()
        layout = QVBoxLayout(widget)
        self.setCentralWidget(widget)

        self.chart = QtChart(widget)
        layout.addWidget(self.chart.get_webview(), 3)

        self.log_widget = QPlainTextEdit()
        self.log_widget.setReadOnly(True)
        layout.addWidget(self.log_widget, 1)

        self.horizontal_lines = {}
        self.tolerance = 0.5
        self.click_thread = None
        self.click_interval = 0.3
        self.ticker = "AAPL"

        self.init_chart()

        self.chart.events.click += self.on_click
        self.chart.events.double_click += self.on_double_click

    def init_chart(self):
        self.fetcher = DataFetcher(self.chart, self.ticker, '10min', '2024-06-09')
        self.fetcher.dataLoaded.connect(self.on_data_loaded)
        self.fetcher.start()

    def on_data_loaded(self, success):
        if success:
            self.log_message("Data loaded successfully.")
        else:
            self.log_message("Failed to load data.")

    def log_message(self, message):
        self.log_widget.appendPlainText(message)

    def handle_click(self, chart, time, price):
        quantity, ok = QInputDialog.getInt(self, "Purchase Quantity", "Enter the number of shares to buy:")
        if ok and quantity > 0:
            line = chart.horizontal_line(price)
            self.horizontal_lines[line.id] = line
            self.log_message(f"Added horizontal line at price: {price}")
            self.log_message(f"Buy {quantity} of {self.ticker} at {price}")

    def on_click(self, chart, time, price):
        if self.click_thread is not None:
            self.click_thread.terminate()
            self.click_thread.wait()

        self.click_thread = ClickHandlerThread(chart, time, price, self.click_interval)
        self.click_thread.clicked.connect(self.handle_click)
        self.click_thread.start()

    def on_double_click(self, chart, time, price):
        if self.click_thread is not None:
            self.click_thread.terminate()
            self.click_thread.wait()

        for line_id, line in list(self.horizontal_lines.items()):
            if abs(line.price - price) < self.tolerance:
                line.delete()
                del self.horizontal_lines[line_id]
                self.log_message(f"Removed horizontal line at price: {price}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())