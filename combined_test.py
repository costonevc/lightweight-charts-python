from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPlainTextEdit, QHBoxLayout, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import QTimer
import sys
import asyncio
import qasync
from combined_window import PolygonQChart
from ib_insync import *

class MainWindow(QMainWindow):
    def __init__(self, api_key):
        super().__init__()
        self.resize(1000, 800) 
        self.setWindowTitle("Polygon Chart with Interactive Features")
        
        # Create a central widget
        widget = QWidget(self)
        self.setCentralWidget(widget)
        main_layout = QVBoxLayout(widget)

        # Create a horizontal layout for the chart and positions table
        top_layout = QHBoxLayout()
        # Create the chart
        self.chart = PolygonQChart(api_key=api_key, widget=widget, width=750, height=600, live=True)
        top_layout.addWidget(self.chart.get_webview(), 3)

        # Create the positions table
        self.positions_table = QTableWidget()
        self.setup_positions_table()
        top_layout.addWidget(self.positions_table, 1)

        main_layout.addLayout(top_layout, 3)

        # Create a log widget
        self.log_widget = QPlainTextEdit()
        self.log_widget.setReadOnly(True)
        main_layout.addWidget(self.log_widget, 1)

        self.chart.init_bridge(self)

        # Schedule the chart to be shown
        QTimer.singleShot(100, self.show_chart)
        QTimer.singleShot(100, self.init_ib_connection)

    # Setup the positions table
    def setup_positions_table(self):
        self.positions_table.setColumnCount(2)  # Two columns: Symbol and Quantity
        self.positions_table.setHorizontalHeaderLabels(['Symbol', 'Quantity'])
        self.positions_table.setEditTriggers(QTableWidget.NoEditTriggers)  # Make table read-only
        self.positions_table.setSelectionBehavior(QTableWidget.SelectRows)  # Enable row selection
        self.positions_table.clicked.connect(self.on_table_click)  # Connect click event

    # Event handler for table click
    def on_table_click(self, index):
        asyncio.ensure_future(self.async_on_table_click(index))

    # Async event handler for table click, location the symbol on the chart and show the data
    async def async_on_table_click(self, index):
        row = index.row()
        symbol = self.positions_table.item(row, 0).text()
        await self.chart.on_search(self.chart, symbol)

    # Initialize the IB connection
    def init_ib_connection(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self.chart.connect_ib())

    # Show the chart and start updating positions
    def show_chart(self):
        self.chart.show()
        self.update_positions() 

    def log_message(self, message):
        self.log_widget.appendPlainText(message)
    
    # Update the positions table
    def update_positions(self):
        self.positions_table.setRowCount(0)  # Clear existing data
        positions = self.chart.ib.positions(account='DU8014278')  # Get all positions from IB
        for pos in positions:
            row_position = self.positions_table.rowCount()
            self.positions_table.insertRow(row_position)
            self.positions_table.setItem(row_position, 0, QTableWidgetItem(pos.contract.symbol)) # Update the symbol
            self.positions_table.setItem(row_position, 1, QTableWidgetItem(str(pos.position)))  # Update the quantity
        QTimer.singleShot(5000, self.update_positions)  # Schedule next update

    # Close event handler
    def closeEvent(self, event):
        try:
            print("Cleaning up resources...")
            # Save the drawings
            self.chart.toolbox.export_drawings("drawings.json")
            # Disconnect from IB
            if self.chart.ib.isConnected():
                self.chart.ib.disconnect()
        except Exception as e:
            print(f"Error during cleanup: {e}")
        finally:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.stop()
            event.accept()


async def main(api_key):
    main_window = MainWindow(api_key=api_key)
    main_window.show()
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)

    loop.create_task(main(api_key="4EMv8sLwboYtrmq15pFTZdNO2aRv8yUF"))

    loop.run_forever()

    loop.close()