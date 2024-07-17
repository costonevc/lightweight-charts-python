""" polygonqchart and mainwindow combined """
# import sys
# from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPlainTextEdit, QInputDialog
# from PyQt5.QtCore import QThread, pyqtSignal
# from combined_window import PolygonQChart
# from click_handler_thread import ClickHandlerThread  
# import asyncio
# import qasync

# async def main():
#     app = QApplication.instance() or QApplication(sys.argv)
#     qloop = qasync.QEventLoop(app)
#     asyncio.set_event_loop(qloop)

#     chart = PolygonQChart(
#         api_key="q0TtwNDqD1yz2pnD96HDLOBTMSKVh2Zl",
#         width=1000,
#         height=800,
#         live=False
#     )

#     chart.show()

#     # Keep the event loop running
#     while True:
#         await asyncio.sleep(0.1)

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.resize(1000,800)
#         widget = QWidget()
#         layout = QVBoxLayout(widget)
#         self.setCentralWidget(widget)

#         self.chart = PolygonQChart(widget)
#         layout.addWidget(self.chart.get_webview(), 3)

#         self.log_widget = QPlainTextEdit()
#         self.log_widget.setReadOnly(True)
#         layout.addWidget(self.log_widget, 1)

#         self.horizontal_lines = {}
#         self.tolerance = 0.5
#         self.click_thread = None
#         self.click_interval = 0.3

#         self.init_chart()

#         self.chart.events.click += self.on_click
#         self.chart.events.double_click += self.on_double_click

#     def init_chart(self):
#         try:
#             qasync.run(main())
#         except KeyboardInterrupt:
#             print("Application closed by user")

#     def log_message(self, message):
#         self.log_widget.appendPlainText(message)

#     def handle_click(self, chart, time, price):
#         quantity, ok = QInputDialog.getInt(self, "Purchase Quantity", "Enter the number of shares to buy:")
#         if ok and quantity > 0:
#             line = chart.horizontal_line(price)
#             self.horizontal_lines[line.id] = line
#             self.log_message(f"Added horizontal line at price: {price}")
#             self.log_message(f"Buy {quantity} of {self.ticker} at {price}")

#     def on_click(self, chart, time, price):
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
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec_())

""" polygonqchart and mainwindow combined and horizontal line"""
# from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPlainTextEdit, QInputDialog
# from PyQt5.QtCore import QTimer
# import sys
# import asyncio
# import qasync
# from combined_window import PolygonQChart
# from click_handler_thread import ClickHandlerThread
# from functools import partial

# class MainWindow(QMainWindow):
#     def __init__(self, api_key):
#         super().__init__()
#         self.resize(800, 600) 
#         self.setWindowTitle("Polygon Chart with Interactive Features")
        
#         widget = QWidget(self)
#         self.setCentralWidget(widget)
#         layout = QVBoxLayout(widget)

#         self.chart = PolygonQChart(api_key=api_key, widget=widget, width=800, height=550)
#         layout.addWidget(self.chart.get_webview(), 3)

#         self.log_widget = QPlainTextEdit()
#         self.log_widget.setReadOnly(True)
#         layout.addWidget(self.log_widget, 1)

#         self.horizontal_lines = {}
#         self.tolerance = 0.1
#         self.click_thread = None
#         self.click_interval = 0.3

#         self.chart.events.click += self.on_click
#         self.chart.events.double_click += self.on_double_click

#         QTimer.singleShot(100, self.show_chart)


#     def show_chart(self):
#         self.chart.show()

#     def log_message(self, message):
#         self.log_widget.appendPlainText(message)
    
#     def on_horizontal_line_move(self, window, chart, new_line):
#         self.log_message(f'Horizontal line moved to: {new_line.price}')

#     def handle_click(self, chart, time, price):
#         quantity, ok = QInputDialog.getInt(self, "Purchase Quantity", "Enter the number of shares to buy:", 1)
#         if ok and quantity > 0:
#             bound_on_horizontal_line_move = partial(self.on_horizontal_line_move, self)
#             line = chart.horizontal_line(price, func=bound_on_horizontal_line_move)
#             ticker = self.chart.get_current_symbol()
#             self.horizontal_lines[line.id] = line
#             self.log_message(f"Added horizontal line at price: {price}")
#             self.log_message(f"Buy {quantity} of {ticker} at {price}")

#     def on_click(self, chart, time, price):
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


# async def main(api_key):
#     app = QApplication(sys.argv)
#     qloop = qasync.QEventLoop(app)
#     asyncio.set_event_loop(qloop)
    
#     main_window = MainWindow(api_key=api_key)
#     main_window.show()
    
#     with qloop:
#         await qloop.run_forever()

# if __name__ == '__main__':
#     try:
#         asyncio.run(main(api_key="q0TtwNDqD1yz2pnD96HDLOBTMSKVh2Zl"))
#     except KeyboardInterrupt:
#         print("Application closed by user")

""" replace on_click with toolbox?"""
# from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPlainTextEdit, QInputDialog
# from PyQt5.QtCore import QTimer
# import sys
# import asyncio
# import qasync
# from combined_window import PolygonQChart
# from click_handler_thread import ClickHandlerThread
# from functools import partial

# class MainWindow(QMainWindow):
#     def __init__(self, api_key):
#         super().__init__()
#         self.resize(800, 600) 
#         self.setWindowTitle("Polygon Chart with Interactive Features")
        
#         widget = QWidget(self)
#         self.setCentralWidget(widget)
#         layout = QVBoxLayout(widget)

#         self.chart = PolygonQChart(api_key=api_key, widget=widget, width=800, height=550)
#         layout.addWidget(self.chart.get_webview(), 3)

#         self.log_widget = QPlainTextEdit()
#         self.log_widget.setReadOnly(True)
#         layout.addWidget(self.log_widget, 1)

#         self.horizontal_lines = {}
#         # self.tolerance = 0.1
#         # self.click_thread = None
#         # self.click_interval = 0.3

#         # self.chart.events.click += self.on_click
#         # self.chart.events.double_click += self.on_double_click

#         QTimer.singleShot(100, self.show_chart)


#     def show_chart(self):
#         self.chart.show()

#     def log_message(self, message):
#         self.log_widget.appendPlainText(message)
    
#     # def on_horizontal_line_move(self, window, chart, new_line):
#     #     self.log_message(f'Horizontal line moved to: {new_line.price}')

#     # def handle_click(self, chart, time, price):
#     #     quantity, ok = QInputDialog.getInt(self, "Purchase Quantity", "Enter the number of shares to buy:", 1)
#     #     if ok and quantity > 0:
#     #         bound_on_horizontal_line_move = partial(self.on_horizontal_line_move, self)
#     #         line = chart.horizontal_line(price, func=bound_on_horizontal_line_move)
#     #         ticker = self.chart.get_current_symbol()
#     #         self.horizontal_lines[line.id] = line
#     #         self.log_message(f"Added horizontal line at price: {price}")
#     #         self.log_message(f"Buy {quantity} of {ticker} at {price}")

#     # def on_click(self, chart, time, price):
#     #     if self.click_thread is not None:
#     #         self.click_thread.terminate()
#     #         self.click_thread.wait()

#     #     self.click_thread = ClickHandlerThread(chart, time, price, self.click_interval)
#     #     self.click_thread.clicked.connect(self.handle_click)
#     #     self.click_thread.start()

#     # def on_double_click(self, chart, time, price):
#     #     if self.click_thread is not None:
#     #         self.click_thread.terminate()
#     #         self.click_thread.wait()

#     #     for line_id, line in list(self.horizontal_lines.items()):
#     #         if abs(line.price - price) < self.tolerance:
#     #             line.delete()
#     #             del self.horizontal_lines[line_id]
#     #             self.log_message(f"Removed horizontal line at price: {price}")


# async def main(api_key):
#     app = QApplication(sys.argv)
#     qloop = qasync.QEventLoop(app)
#     asyncio.set_event_loop(qloop)
    
#     main_window = MainWindow(api_key=api_key)
#     main_window.show()
    
#     with qloop:
#         await qloop.run_forever()

# if __name__ == '__main__':
#     try:
#         asyncio.run(main(api_key="q0TtwNDqD1yz2pnD96HDLOBTMSKVh2Zl"))
#     except KeyboardInterrupt:
#         print("Application closed by user")

""" replace qinputdialog with textbox """
# from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPlainTextEdit
# from PyQt5.QtCore import QTimer
# import sys
# import asyncio
# import qasync
# from combined_window import PolygonQChart
# from click_handler_thread import ClickHandlerThread
# from functools import partial

# class MainWindow(QMainWindow):
#     def __init__(self, api_key):
#         super().__init__()
#         self.resize(800, 600) 
#         self.setWindowTitle("Polygon Chart with Interactive Features")
        
#         widget = QWidget(self)
#         self.setCentralWidget(widget)
#         layout = QVBoxLayout(widget)

#         self.chart = PolygonQChart(api_key=api_key, widget=widget, width=800, height=550)
#         layout.addWidget(self.chart.get_webview(), 3)

#         self.log_widget = QPlainTextEdit()
#         self.log_widget.setReadOnly(True)
#         layout.addWidget(self.log_widget, 1)

#         self.horizontal_lines = {}
#         self.tolerance = 0.1
#         self.click_thread = None
#         self.click_interval = 0.3

#         self.chart.events.click += self.on_click
#         # self.chart.events.double_click += self.on_double_click

#         QTimer.singleShot(100, self.show_chart)


#     def show_chart(self):
#         self.chart.show()

#     def log_message(self, message):
#         self.log_widget.appendPlainText(message)
    
#     def on_horizontal_line_move(self, window, chart, new_line):
#         self.log_message(f'Horizontal line moved to: {new_line.price}')

#     def handle_click(self, chart, time, price):
#         quantity = int(self.chart.get_current_quantity())
#         if quantity > 0:
#             bound_on_horizontal_line_move = partial(self.on_horizontal_line_move, self)
#             line = chart.horizontal_line(price, func=bound_on_horizontal_line_move)
#             ticker = self.chart.get_current_symbol()
#             self.horizontal_lines[line.id] = line
#             self.log_message(f"Added horizontal line at price: {price}")
#             self.log_message(f"Buy {quantity} of {ticker} at {price}")

#     def on_click(self, chart, time, price):
#         if self.click_thread is not None:
#             self.click_thread.terminate()
#             self.click_thread.wait()

#         self.click_thread = ClickHandlerThread(chart, time, price, self.click_interval)
#         self.click_thread.clicked.connect(self.handle_click)
#         self.click_thread.start()

# async def main(api_key):
#     app = QApplication(sys.argv)
#     qloop = qasync.QEventLoop(app)
#     asyncio.set_event_loop(qloop)
    
#     main_window = MainWindow(api_key=api_key)
#     main_window.show()
    
#     with qloop:
#         await qloop.run_forever()

# if __name__ == '__main__':
#     try:
#         asyncio.run(main(api_key="q0TtwNDqD1yz2pnD96HDLOBTMSKVh2Zl"))
#     except KeyboardInterrupt:
#         print("Application closed by user")

""" toolbox success ver. """
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPlainTextEdit, QInputDialog
from PyQt5.QtCore import QTimer
import sys
import asyncio
import qasync
from combined_window import PolygonQChart
# from click_handler_thread import ClickHandlerThread
from functools import partial

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