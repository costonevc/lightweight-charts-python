from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPlainTextEdit, QInputDialog, QLineEdit, QHBoxLayout, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import QTimer
import sys
import asyncio
import qasync
from combined_window import PolygonQChart
from functools import partial
from ib_insync import *

class MainWindow(QMainWindow):
    def __init__(self, api_key):
        super().__init__()
        self.resize(1000, 800) 
        self.setWindowTitle("Polygon Chart with Interactive Features")
        
        widget = QWidget(self)
        self.setCentralWidget(widget)
        main_layout = QVBoxLayout(widget)

        top_layout = QHBoxLayout()
        self.chart = PolygonQChart(api_key=api_key, widget=widget, width=750, height=600, live=True)
        top_layout.addWidget(self.chart.get_webview(), 3)

        self.positions_table = QTableWidget()
        self.setup_positions_table()
        top_layout.addWidget(self.positions_table, 1)

        main_layout.addLayout(top_layout, 3)

        self.log_widget = QPlainTextEdit()
        self.log_widget.setReadOnly(True)
        main_layout.addWidget(self.log_widget, 1)

        self.chart.init_bridge(self)

        QTimer.singleShot(100, self.show_chart)
        QTimer.singleShot(100, self.init_ib_connection)


    def setup_positions_table(self):
        self.positions_table.setColumnCount(2)  # Two columns: Symbol and Quantity
        self.positions_table.setHorizontalHeaderLabels(['Symbol', 'Quantity'])
        self.positions_table.setEditTriggers(QTableWidget.NoEditTriggers)  # Make table read-only
        self.positions_table.setSelectionBehavior(QTableWidget.SelectRows)  # Enable row selection
        self.positions_table.clicked.connect(self.on_table_click)  # Connect click event

    def on_table_click(self, index):
        asyncio.ensure_future(self.async_on_table_click(index))

    async def async_on_table_click(self, index):
        row = index.row()
        symbol = self.positions_table.item(row, 0).text()
        await self.chart.on_search(self.chart, symbol)

    def init_ib_connection(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self.chart.connect_ib())

    def show_chart(self):
        self.chart.show()
        self.update_positions() 


    def log_message(self, message):
        self.log_widget.appendPlainText(message)
    
    def update_positions(self):
        # This function needs to fetch data and update the table
        self.positions_table.setRowCount(0)  # Clear existing data
        positions = self.chart.ib.positions(account='DU8014278')  # Get all positions from IB
        for pos in positions:
            row_position = self.positions_table.rowCount()
            self.positions_table.insertRow(row_position)
            self.positions_table.setItem(row_position, 0, QTableWidgetItem(pos.contract.symbol))
            self.positions_table.setItem(row_position, 1, QTableWidgetItem(str(pos.position)))
        QTimer.singleShot(5000, self.update_positions)  # Schedule next update


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