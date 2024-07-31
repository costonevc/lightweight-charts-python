# Description: This file contains the code to test the lightweight_charts package.

# file_path = "/Users/jiarui/Desktop/Summer2024/ohlcv.csv"

"""  Events

 Search """

# from lightweight_charts import Chart
# import pandas as pd

# def on_search(chart, string):
#     print(f'Search Text: "{string}" | Chart/SubChart ID: "{chart.id}"')
    
    
# if __name__ == '__main__':
#     chart = Chart()
#     df = pd.read_csv('ohlcv.csv')
#     chart.set(df)
    
#     # Subscribe the function above to search event
#     chart.events.search += on_search  
    
#     chart.show(block=True)

""" Topbar Button
 """
# from lightweight_charts import Chart

# def on_button_press(chart):
#     new_button_value = 'On' if chart.topbar['my_button'].value == 'Off' else 'Off'
#     chart.topbar['my_button'].set(new_button_value)
#     print(f'Turned something {new_button_value.lower()}.')
    
    
# if __name__ == '__main__':
#     chart = Chart()
#     chart.topbar.button('my_button', 'Off', func=on_button_press)
#     chart.show(block=True)

""" Topbar Switcher """
# from lightweight_charts import Chart

# def on_timeframe_selection(chart):
#     print(f'Getting data with a {chart.topbar["my_switcher"].value} timeframe.')
    
    
# if __name__ == '__main__':
#     chart = Chart()
#     chart.topbar.switcher(
#         name='my_switcher',
#         options=('1min', '5min', '30min'),
#         default='5min',
#         func=on_timeframe_selection)
#     chart.show(block=True)

""" Topbar Async block """
# import asyncio
# from datetime import datetime
# from lightweight_charts import Chart


# async def update_clock(chart):
#     while chart.is_alive:
#         await asyncio.sleep(1-(datetime.now().microsecond/1_000_000))
#         chart.topbar['clock'].set(datetime.now().strftime('%H:%M:%S'))


# async def main():
#     chart = Chart()
#     chart.topbar.textbox('clock')
#     await asyncio.gather(chart.show_async(), update_clock(chart))


# if __name__ == '__main__':
#     asyncio.run(main())

""" Click """

# from lightweight_charts import Chart
# import pandas as pd

# def on_click(chart, time, price):
#     print(f'Click time: "{time}" | Click price: "{price}"')
    
    
# if __name__ == '__main__':
#     chart = Chart()
#     df = pd.read_csv('ohlcv.csv')
#     chart.set(df)
    
#     # Subscribe the function above to search event
#     chart.events.click += on_click
    
#     chart.show(block=True)

""" hotkey """

# from lightweight_charts import Chart

# def place_buy_order(key):
#     print(f'Buy {key} shares.')


# def place_sell_order(key):
#     print(f'Sell all shares, because I pressed {key}.')


# if __name__ == '__main__':
#     chart = Chart()
#     chart.hotkey('shift', (1, 2, 3), place_buy_order)
#     chart.hotkey('shift', 'X', place_sell_order)
#     chart.show(block=True)

""" demo test1 """

# from lightweight_charts import Chart
# import pandas as pd

# last_click_time = None
# last_click_price = None

# def on_click(chart, time, price):
#     global last_click_time, last_click_price
#     last_click_time = time
#     last_click_price = price
#     print(f'Click time: "{time}" | Click price: "{price}"')
    
# def place_buy_order(key):
#     if last_click_time is not None and last_click_price is not None:
#         print(f'Buy {key} shares at price {last_click_price} on {last_click_time}.')
#     else:
#         print("No click location stored. Click on the chart first.")


# if __name__ == '__main__':
#     chart = Chart()
#     df = pd.read_csv('ohlcv.csv')
#     chart.set(df)
    
#     # Subscribe the function to click event
#     chart.events.click += on_click
    
#     # Define hotkeys
#     chart.hotkey('shift', (1, 2, 3), place_buy_order)
    
#     chart.show(block=True)

""" create line """

# from lightweight_charts import Chart
# import pandas as pd

# def calculate_sma(df, period: int = 50):
#     return pd.DataFrame({
#         'time': df['date'],
#         f'SMA {period}': df['close'].rolling(window=period).mean()
#     }).dropna()

# if __name__ == '__main__':
#     chart = Chart()
#     line = chart.create_line(name='SMA 50')

#     df = pd.read_csv('ohlcv.csv')
#     sma_df = calculate_sma(df, period=50)

#     chart.set(df)
#     line.set(sma_df)
    
#     chart.show(block=True)

""" horizontal line """
# import sys
# sys.path.append('/Users/jiarui/Desktop/Summer 2024/lightweight/lightweight-charts-python')
# from lightweight_charts import Chart
# import pandas as pd

# chart = Chart()

# horizontal_lines = {}

# tolerance = 0.1

# def on_click(chart, time, price):
   
#     line = chart.horizontal_line(price)
  
#     horizontal_lines[line.id] = line
#     print(f"Added horizontal line at price: {price}")

# def on_double_click(chart, time, price):

#     for line_id, line in list(horizontal_lines.items()):
#         if abs(line.price - price) < tolerance: 
           
#             horizontal_lines[line_id].delete()
    
#             del horizontal_lines[line_id]
#             print(f"Removed horizontal line at price: {price}")
#             break

# if __name__ == '__main__':
#     df = pd.read_csv(file_path)
#     chart.set(df)

#     chart.events.click += on_click
    
#     chart.events.double_click += on_double_click

#     chart.show(block=True)

""" bug """
# from lightweight_charts import Chart
# import pandas as pd
# import time

# chart = Chart()
# horizontal_lines = {}
# tolerance = 1
# last_click_time = 0
# click_interval = 1  

# def on_click(chart, time_clicked, price):
#     global last_click_time
#     current_click_time = time.time()
#     print(f'Current time: {current_click_time} | Last click time: {last_click_time}')

#     if (current_click_time - last_click_time) < click_interval:
#         for line_id, line in list(horizontal_lines.items()):
#             if abs(line.price - price) < tolerance:
#                 line.delete()  
#                 del horizontal_lines[line_id]
#                 print(f"Removed horizontal line at price: {price}")
#                 break
#     else:
#         line = chart.horizontal_line(price)  
#         horizontal_lines[line.id] = line
#         print(f"Added horizontal line at price: {price}")

#     last_click_time = current_click_time

# if __name__ == '__main__':
#     df = pd.read_csv(file_path)
#     chart.set(df)
#     chart.events.click += on_click
#     chart.show(block=True)

# import time
# from collections import deque
# from lightweight_charts import Chart
# import pandas as pd

# chart = Chart()
# horizontal_lines = {}
# tolerance = 0.1
# last_clicks = deque(maxlen=2)  # 保存最近两次点击的时间戳
# click_interval = 0.5  # 双击的时间阈值，500毫秒

# def on_click(chart, time_clicked, price):
#     current_time = time.time()
#     last_clicks.append(current_time)
#     print(f'Current time: {current_time} | Last clicks: {last_clicks}')

#     if len(last_clicks) == 2 and (last_clicks[1] - last_clicks[0] < click_interval):
#         # 处理双击事件
#         for line_id, line in list(horizontal_lines.items()):
#             if abs(line.price - price) < tolerance:
#                 line.delete()  # 假设的删除方法
#                 del horizontal_lines[line_id]
#                 print(f"Removed horizontal line at price: {price}")
#                 break
#         last_clicks.clear()  # 清空队列
#     elif len(last_clicks) == 2:
#         # 单击事件处理逻辑
#         line = chart.horizontal_line(price)  # 假设的添加方法
#         horizontal_lines[line.id] = line
#         print(f"Added horizontal line at price: {price}")
#         last_clicks.popleft()  # 移除较早的时间戳，保留最新的

# if __name__ == '__main__':
#     df = pd.read_csv(file_path)
#     chart.set(df)

#     chart.events.click += on_click

#     chart.show(block=True)

""" horizontal line (success ver.)"""

# import pandas as pd
# import threading
# from lightweight_charts import Chart

# chart = Chart()
# horizontal_lines = {}
# tolerance = 0.5
# click_timer = None
# click_interval = 0.3  

# def handle_click(chart, time, price):
#     line = chart.horizontal_line(price)
#     horizontal_lines[line.id] = line
#     print(f"Added horizontal line at price: {price}")

# def on_click(chart, time, price):
#     global click_timer
#     if click_timer is not None:
#         click_timer.cancel() 

#     click_timer = threading.Timer(click_interval, handle_click, [chart, time, price])
#     click_timer.start()

# def on_double_click(chart, time, price):
#     global click_timer
#     if click_timer is not None:
#         click_timer.cancel()  

#     for line_id, line in list(horizontal_lines.items()):
#         if abs(line.price - price) < tolerance:
#             line.delete()
#             del horizontal_lines[line_id]
#             print(f"Removed horizontal line at price: {price}")
#             break

# if __name__ == '__main__':
#     df = pd.read_csv(file_path)
#     chart.set(df)

#     chart.events.click += on_click
#     chart.events.double_click += on_double_click

#     chart.show(block=True)

""" polygon """

# from lightweight_charts import Chart

# if __name__ == '__main__':
#     chart = Chart()
#     chart.polygon.api_key('q0TtwNDqD1yz2pnD96HDLOBTMSKVh2Zl')
#     chart.polygon.stock(
#         symbol='AAPL',
#         timeframe='10min',
#         start_date='2024-06-09'
#     )
#     chart.show(block=True)

""" polygon and horizontal line """

# import pandas as pd
# import threading
# from lightweight_charts import Chart

# chart = Chart()
# horizontal_lines = {}
# tolerance = 0.5
# click_timer = None
# click_interval = 0.3  

# def handle_click(chart, time, price):
#     line = chart.horizontal_line(price)
#     horizontal_lines[line.id] = line
#     print(f"Added horizontal line at price: {price}")

# def on_click(chart, time, price):
#     global click_timer
#     if click_timer is not None:
#         click_timer.cancel() 

#     click_timer = threading.Timer(click_interval, handle_click, [chart, time, price])
#     click_timer.start()

# def on_double_click(chart, time, price):
#     global click_timer
#     if click_timer is not None:
#         click_timer.cancel()  

#     for line_id, line in list(horizontal_lines.items()):
#         if abs(line.price - price) < tolerance:
#             line.delete()
#             del horizontal_lines[line_id]
#             print(f"Removed horizontal line at price: {price}")
#             break

# if __name__ == '__main__':
#     chart.polygon.api_key('q0TtwNDqD1yz2pnD96HDLOBTMSKVh2Zl')
#     chart.polygon.stock(
#         symbol='AAPL',
#         timeframe='10min',
#         start_date='2024-06-09'
#     )

#     chart.events.click += on_click
#     chart.events.double_click += on_double_click

#     chart.show(block=True)

""" pyqt5  """
# import pandas as pd
# from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

# from lightweight_charts.widgets import QtChart

# app = QApplication([])
# window = QMainWindow()
# layout = QVBoxLayout()
# widget = QWidget()
# widget.setLayout(layout)

# window.resize(800, 500)
# layout.setContentsMargins(0, 0, 0, 0)

# chart = QtChart(widget)

# df = pd.read_csv(file_path)
# chart.set(df)

# layout.addWidget(chart.get_webview())

# window.setCentralWidget(widget)
# window.show()

# app.exec_()

""" pyqt5 test """
# import sys
# from PyQt5.QtWidgets import QApplication, QMainWindow

# def main():
#     app = QApplication(sys.argv)
#     window = QMainWindow()
#     window.setWindowTitle("Simple Test")
#     window.show()
#     sys.exit(app.exec_())

# if __name__ == "__main__":
#     main()

# import sys
# from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
# from lightweight_charts.widgets import QtChart

# def main():
#     app = QApplication(sys.argv)
#     window = QMainWindow()
#     layout = QVBoxLayout()
#     widget = QWidget()
#     widget.setLayout(layout)

#     window.resize(800, 500)
#     layout.setContentsMargins(0, 0, 0, 0)

#     chart = QtChart(widget)
#     layout.addWidget(chart.get_webview())

#     window.setCentralWidget(widget)
#     window.setWindowTitle("Test with QtChart")
#     window.show()
#     sys.exit(app.exec_())

# if __name__ == "__main__":
#     main()

""" wxpython """
# import wx
# import pandas as pd

# from lightweight_charts.widgets import WxChart


# class MyFrame(wx.Frame):
#     def __init__(self):
#         super().__init__(None)
#         self.SetSize(1000, 500)

#         panel = wx.Panel(self)
#         sizer = wx.BoxSizer(wx.VERTICAL)
#         panel.SetSizer(sizer)

#         chart = WxChart(panel)

#         df = pd.read_csv('ohlcv.csv')
#         chart.set(df)

#         sizer.Add(chart.get_webview(), 1, wx.EXPAND | wx.ALL)
#         sizer.Layout()
#         self.Show()


# if __name__ == '__main__':
#     app = wx.App()
#     frame = MyFrame()
#     app.MainLoop()


""" combine horizontal line and pyqt5 """
# import pandas as pd
# from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
# import threading
# from lightweight_charts.widgets import QtChart

# app = QApplication([])
# window = QMainWindow()
# layout = QVBoxLayout()
# widget = QWidget()
# widget.setLayout(layout)

# window.resize(800, 500)
# layout.setContentsMargins(0, 0, 0, 0)

# chart = QtChart(widget)

# horizontal_lines = {}
# tolerance = 0.5
# click_timer = None
# click_interval = 0.3  


# def handle_click(chart, time, price):
#     line = chart.horizontal_line(price)
#     horizontal_lines[line.id] = line
#     print(f"Added horizontal line at price: {price}")

# def on_click(chart, time, price):
#     global click_timer
#     if click_timer is not None:
#         click_timer.cancel() 

#     click_timer = threading.Timer(click_interval, handle_click, [chart, time, price])
#     click_timer.start()

# def on_double_click(chart, time, price):
#     global click_timer
#     if click_timer is not None:
#         click_timer.cancel()  

#     for line_id, line in list(horizontal_lines.items()):
#         if abs(line.price - price) < tolerance:
#             line.delete()
#             del horizontal_lines[line_id]
#             print(f"Removed horizontal line at price: {price}")
#             break

# df = pd.read_csv(file_path)
# chart.set(df)
# chart.events.click += on_click
# chart.events.double_click += on_double_click

# layout.addWidget(chart.get_webview())

# window.setCentralWidget(widget)
# window.show()

# app.exec_()

""" log gui 
调整组件大小
用Qthread替换threading
"""
# import pandas as pd
# from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPlainTextEdit
# import threading
# from lightweight_charts.widgets import QtChart

# app = QApplication([])
# window = QMainWindow()
# layout = QVBoxLayout()
# widget = QWidget()
# widget.setLayout(layout)

# window.resize(800, 600) 
# layout.setContentsMargins(0, 0, 0, 0)

# chart = QtChart(widget)
# layout.addWidget(chart.get_webview(), 1)  

# horizontal_lines = {}
# tolerance = 0.5
# click_timer = None
# click_interval = 0.3  

# log_widget = QPlainTextEdit()
# log_widget.setReadOnly(True)
# layout.addWidget(log_widget, 1)  

# def log_message(message):
#     print(message)
#     log_widget.appendPlainText(message)

# def handle_click(chart, time, price):
#     line = chart.horizontal_line(price)
#     horizontal_lines[line.id] = line
#     log_message(f"Added horizontal line at price: {price}")

# def on_click(chart, time, price):
#     global click_timer
#     if click_timer is not None:
#         click_timer.cancel()
#     click_timer = threading.Timer(click_interval, handle_click, [chart, time, price])
#     click_timer.start()

# def on_double_click(chart, time, price):
#     global click_timer
#     if click_timer is not None:
#         click_timer.cancel()
#     for line_id, line in list(horizontal_lines.items()):
#         if abs(line.price - price) < tolerance:
#             line.delete()
#             del horizontal_lines[line_id]
#             log_message(f"Removed horizontal line at price: {price}")

# df = pd.read_csv(file_path)
# chart.set(df)
# chart.events.click += on_click
# chart.events.double_click += on_double_click

# window.setCentralWidget(widget)
# window.show()

# app.exec_()

""" combine pyqt5 and polygon (wrong)"""
# import pandas as pd
# from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

# from lightweight_charts.widgets import QtChart

# app = QApplication([])
# window = QMainWindow()
# layout = QVBoxLayout()
# widget = QWidget()
# widget.setLayout(layout)

# window.resize(800, 500)
# layout.setContentsMargins(0, 0, 0, 0)

# chart = QtChart(widget)

# # chart.polygon.api_key('q0TtwNDqD1yz2pnD96HDLOBTMSKVh2Zl')

# # chart.polygon.async_stock(
# #     symbol='AAPL',
# #     timeframe='10min',
# #     start_date='2024-06-09'
# # )



# layout.addWidget(chart.get_webview())

# window.setCentralWidget(widget)
# window.show()

# app.exec_()

""" combine pyqt5 and polygon (success?)"""
# import asyncio
# from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
# from lightweight_charts.widgets import QtChart
# from lightweight_charts import Chart

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Stock Chart")
#         self.resize(800, 500)

#         layout = QVBoxLayout()
#         widget = QWidget()
#         widget.setLayout(layout)

#         self.qt_chart = QtChart(widget)
#         self.qt_chart.polygon.api_key('q0TtwNDqD1yz2pnD96HDLOBTMSKVh2Zl')

#         layout.addWidget(self.qt_chart.get_webview())
#         layout.setContentsMargins(0, 0, 0, 0)

#         self.setCentralWidget(widget)

#     async def load_data(self):
#         # Create a standalone Chart object to fetch data
#         chart = Chart()
#         chart.polygon.api_key('q0TtwNDqD1yz2pnD96HDLOBTMSKVh2Zl')
        
#         # Use the stock method to fetch data
#         chart.polygon.stock(
#             symbol='AAPL',
#             timeframe='10min',
#             start_date='2024-06-09'
#         )

#         # Wait for the data to be loaded
#         await chart.show_async()

#         # Get the data from the chart and set it to the QtChart
#         data = chart.data
#         self.qt_chart.set(data)

# async def main():
#     app = QApplication([])
#     window = MainWindow()
#     window.show()

#     await window.load_data()

#     # Run the Qt event loop in a separate thread
#     loop = asyncio.get_event_loop()
#     await loop.run_in_executor(None, app.exec_)

# if __name__ == '__main__':
#     asyncio.run(main())

""" combine pyqt5 and polygon (success)"""
# import sys
# from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPlainTextEdit
# from PyQt5.QtCore import QThread, pyqtSignal
# from lightweight_charts.widgets import QtChart

# class DataFetcher(QThread):
#     dataLoaded = pyqtSignal(bool)

#     def __init__(self, chart, ticker, timeframe, start_date):
#         super().__init__()
#         self.chart = chart
#         self.ticker = ticker
#         self.timeframe = timeframe
#         self.start_date = start_date

#     def run(self):
#         # Simulate an API call delay
#         # self.sleep(2)

#         self.chart.polygon.api_key('q0TtwNDqD1yz2pnD96HDLOBTMSKVh2Zl')
#         self.chart.polygon.stock(
#             symbol='AAPL',
#             timeframe='10min',
#             start_date='2024-06-09'
#         )
#         self.dataLoaded.emit(True)

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.resize(800, 500)
#         widget = QWidget()
#         layout = QVBoxLayout(widget)
#         self.setCentralWidget(widget)

#         self.chart = QtChart(widget)
#         layout.addWidget(self.chart.get_webview(), 3)

#         self.log_widget = QPlainTextEdit()
#         self.log_widget.setReadOnly(True)
#         layout.addWidget(self.log_widget, 1)

#         self.init_chart()

#     def init_chart(self):
#         self.fetcher = DataFetcher(self.chart, 'AAPL', '10min', '2024-06-09')
#         self.fetcher.dataLoaded.connect(self.on_data_loaded)
#         self.fetcher.start()

#     def on_data_loaded(self, success):
#         if success:
#             self.log_message("Data loaded successfully.")
#         else:
#             self.log_message("Failed to load data.")

#     def log_message(self, message):
#         self.log_widget.appendPlainText(message)

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec_())


""" polygon chart """
# from lightweight_charts import PolygonChart

# if __name__ == '__main__':
#     chart = PolygonChart(
#         api_key='q0TtwNDqD1yz2pnD96HDLOBTMSKVh2Zl',
#         num_bars=200,
#         limit=5000,
#         live=False
#     )
#     chart.show(block=True)

""" horizontal line move """
# import pandas as pd
# from lightweight_charts import Chart


# def get_bar_data(symbol, timeframe):
#     if symbol not in ('AAPL', 'GOOGL', 'TSLA'):
#         print(f'No data for "{symbol}"')
#         return pd.DataFrame()
#     return pd.read_csv(f'examples/6_callbacks/bar_data/{symbol}_{timeframe}.csv')


# def on_search(chart, searched_string):  # Called when the user searches.
#     new_data = get_bar_data(searched_string, chart.topbar['timeframe'].value)
#     if new_data.empty:
#         return
#     chart.topbar['symbol'].set(searched_string)
#     chart.set(new_data)


# def on_timeframe_selection(chart):  # Called when the user changes the timeframe.
#     new_data = get_bar_data(chart.topbar['symbol'].value, chart.topbar['timeframe'].value)
#     if new_data.empty:
#         return
#     chart.set(new_data, True)


# def on_horizontal_line_move(chart, line):
#     print(f'Horizontal line moved to: {line.price}')


# if __name__ == '__main__':
#     chart = Chart(toolbox=True)
#     chart.legend(True)

#     chart.events.search += on_search

#     chart.topbar.textbox('symbol', 'TSLA')
#     chart.topbar.switcher('timeframe', ('1min', '5min', '30min'), default='5min',
#                           func=on_timeframe_selection)

#     df = get_bar_data('TSLA', '5min')
#     chart.set(df)

#     chart.horizontal_line(200, func=on_horizontal_line_move)

#     chart.show(block=True)

""" save drawings  """
# import pandas as pd
# from lightweight_charts import Chart


# def get_bar_data(symbol, timeframe):
#     if symbol not in ('AAPL', 'GOOGL', 'TSLA'):
#         print(f'No data for "{symbol}"')
#         return pd.DataFrame()
#     return pd.read_csv(f'examples/6_callbacks/bar_data/{symbol}_{timeframe}.csv')


# def on_search(chart, searched_string):
#     new_data = get_bar_data(searched_string, chart.topbar['timeframe'].value)
#     if new_data.empty:
#         return
#     chart.topbar['symbol'].set(searched_string)
#     chart.set(new_data)
    
#     # Load the drawings saved under the symbol.
#     chart.toolbox.load_drawings(searched_string)


# def on_timeframe_selection(chart):
#     new_data = get_bar_data(chart.topbar['symbol'].value, chart.topbar['timeframe'].value)
#     if new_data.empty:
#         return
#     # The symbol has not changed, so we want to re-render the drawings.
#     chart.set(new_data, keep_drawings=True)


# if __name__ == '__main__':
#     chart = Chart(toolbox=True)
#     chart.legend(True)

#     chart.events.search += on_search
#     chart.topbar.textbox('symbol', 'TSLA')
#     chart.topbar.switcher(
#         'timeframe',
#         ('1min', '5min', '30min'),
#         default='5min',
#         func=on_timeframe_selection
#     )

#     df = get_bar_data('TSLA', '5min')

#     chart.set(df)

#     # Imports the drawings saved in the JSON file.
#     chart.toolbox.import_drawings('test/drawings.json')
    
#     # Loads the drawings under the default symbol.
#     chart.toolbox.load_drawings(chart.topbar['symbol'].value)  
    
#     # Saves drawings based on the symbol.
#     chart.toolbox.save_drawings_under(chart.topbar['symbol'])  

#     chart.show(block=True)
    
#     # Exports the drawings to the JSON file upon close.
#     chart.toolbox.export_drawings('test/drawings.json')  


# import pandas as pd
# import pytz

# def calculate_unix_timestamp(time_str):
#     # 定义时区
#     utc_zone = pytz.timezone('UTC')
#     eastern = pytz.timezone('America/New_York')
    
#     # 解析时间字符串为 UTC datetime
#     utc_datetime = pd.to_datetime(time_str).tz_localize(utc_zone)
    
#     # 转换时区到 New York
#     eastern_datetime = utc_datetime.tz_convert(eastern)
    
#     # 计算 Unix 时间戳 (自 1970-01-01 00:00:00 UTC)
#     unix_timestamp = (eastern_datetime - pd.Timestamp("1970-01-01", tz=utc_zone)).total_seconds()
    
#     return unix_timestamp

# # 示例使用
# time_str = "2024-07-29 15:26:51.703000+00:00"
# timestamp = calculate_unix_timestamp(time_str)
# print("Unix Timestamp:", timestamp)

# import pendulum

# dt = pendulum.parse('2012-09-05T23:26:11.123789')
# print(type(dt))

import pandas as pd
# def _df_datetime_format(self, df: pd.DataFrame, exclude_lowercase=None):
#         df = df.copy()
#         df.columns = self._format_labels(df, df.columns, df.index, exclude_lowercase)
#         self._set_interval(df)

#         if not pd.api.types.is_datetime64_any_dtype(df['time']):
#             df['time'] = pd.to_datetime(df['time'], unit='ms')
#         if df['time'].dt.tz is None:
#             df['time'] = df['time'].dt.tz_localize('UTC').dt.tz_convert('America/New_York')
#         else:
#             df['time'] = df['time'].dt.tz_convert('America/New_York')
#         df['time'] = (df['time'] - pd.Timestamp("1970-01-01", tz='America/New_York')) // pd.Timedelta(seconds=1) #少了一个小时
#         # df['time'] = df['time'].apply(lambda x: int(x.timestamp()))
#         # 使用 Pendulum 转换时间到 New York 时区
#         # df['time'] = df['time'].apply(lambda x: pendulum.instance(x.to_pydatetime(), tz='UTC').in_tz('America/New_York')) #这步是对的
#         # print(df['time'])

#         # # 计算 UNIX 时间戳，以东部时间为基准
#         # df['time'] = df['time'].apply(lambda x: x.int_timestamp) #这样还是utc
#         # print('before', df['time'])
#         # df['time'] = df['time'].apply(lambda x: x.isoformat())
#         # df['time'] = df['time'].apply(lambda x: x.strftime('%Y-%m-%dT%H:%M:%S'))
#         # print(df['time'])
#         return df
import datetime
import pytz
# eastern = pytz.timezone('America/New_York')
# dt_naive = datetime.datetime(2024, 7, 30, 4, 0, 0)  # 创建一个不带时区信息的 datetime 对象
# dt_aware = eastern.localize(dt_naive)  # 将时区信息添加到 datetime 对象

# print(dt_aware)

# dt_aware = (dt_aware - pd.Timestamp("1970-01-01", tz='America/New_York')) // pd.Timedelta(seconds=1)
# print(dt_aware)

eastern = pytz.timezone('America/New_York')
dt_naive = datetime.datetime(2023, 6, 1, 4, 0, 0)  # 创建一个不带时区信息的 datetime 对象
dt_aware = eastern.localize(dt_naive)  # 将时区信息添加到 datetime 对象

print(dt_aware)

timestamp = (dt_aware - pd.Timestamp("1970-01-01", tz='America/New_York')) // pd.Timedelta(seconds=1)
print(timestamp)

if dt_aware.tzinfo.utcoffset(dt_aware).total_seconds() == -14400:  # EDT offset in seconds
    timestamp += 3600  # Add one hour in seconds

print("Adjusted UNIX timestamp:", timestamp)

def convert_timestamp_to_est(unix_timestamp):
    # Define the timezone for Eastern Time
    eastern = pytz.timezone('America/New_York')
    
    # Convert the UNIX timestamp to a datetime object in UTC
    utc_time = datetime.datetime.utcfromtimestamp(unix_timestamp)
    
    # Localize the UTC datetime object to UTC timezone (to make it timezone-aware)
    utc_time = pytz.utc.localize(utc_time)
    
    # Convert the timezone from UTC to Eastern Time
    eastern_time = utc_time.astimezone(eastern)
    
    return eastern_time

# Example usage

eastern_time = convert_timestamp_to_est(timestamp)
print(eastern_time)

data = {
    'time': [datetime.datetime(2023, 6, 1, 4, 0, 0),datetime.datetime(2023, 12, 1, 4, 0, 0)]
}
df = pd.DataFrame(data)
print(df['time'])
df['time'] = df['time'].dt.tz_localize('UTC').dt.tz_convert('America/New_York')

def adjust_time(row):
    # 获取时间戳
    ts = row['time']
    # 获取时区偏移
    offset_seconds = ts.tzinfo.utcoffset(ts).total_seconds()
    # 计算新的时间戳
    new_ts = (ts - pd.Timestamp("1970-01-01", tz='America/New_York')) // pd.Timedelta(seconds=1)
    # 如果是EDT (东部夏令时，偏移为-14400秒)
    if offset_seconds == -14400:
        new_ts += 3600
    return new_ts

# 应用调整
df['time'] = df.apply(adjust_time, axis=1)

# 打印结果
print(df)
# df['offset'] = df['time'].apply(lambda x: x.tzinfo.utcoffset(x).total_seconds())
# print(df)

# # 检查每个时间戳的时区偏移是否为EDT或EST
# df['timezone'] = df['offset'].apply(lambda x: 'EDT' if x == -14400 else 'EST')
# print(df)

# print(df['time'].dt.tz)
# offset_seconds = df['time'].dt.tz[0].utcoffset().total_seconds()
# print("Offset in seconds:", offset_seconds)
# if df['time'].dt.tz.utcoffset(df['time']).total_seconds() == -14400:  # EDT offset in seconds
#     df['time'] = (df['time'] - pd.Timestamp("1970-01-01", tz='America/New_York')) // pd.Timedelta(seconds=1) + 3600
# else:
#     df['time'] = (df['time'] - pd.Timestamp("1970-01-01", tz='America/New_York')) // pd.Timedelta(seconds=1)