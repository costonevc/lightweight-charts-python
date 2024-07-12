from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtCore import QObject, pyqtSlot as Slot, QUrl, QTimer
from lightweight_charts.widgets import QtChart
from lightweight_charts import abstract
from lightweight_charts.util import parse_event_message
import asyncio
import datetime as dt
import pandas as pd
import qasync
import sys
import re

class PolygonQChart(QtChart):
    def __init__(self, api_key: str, widget: QWidget = None, live: bool = False, num_bars: int = 200,
                 end_date: str = 'now', limit: int = 5000,
                 timeframe_options: tuple = ('1min', '5min', '30min', 'D', 'W'),
                 security_options: tuple = ('Stock', 'Option', 'Index', 'Forex', 'Crypto'),
                 toolbox: bool = True, width: int = 800, height: int = 600,
                 inner_width: float = 1.0, inner_height: float = 1.0, scale_candles_only: bool = False):
        super().__init__(widget, inner_width, inner_height, scale_candles_only, toolbox)
        
        print("Initializing PolygonQChart")
        self.api_key = api_key
        self.num_bars = num_bars
        self.end_date = end_date
        self.limit = limit
        self.live = live

        # Set up the QWebEngineView
        self.webview.setFixedSize(width, height)
        
        # Set up Polygon-specific configurations
        self.win.style(
            active_background_color='rgba(91, 98, 246, 0.8)',
            muted_background_color='rgba(91, 98, 246, 0.5)'
        )
        self.polygon.api_key(api_key)
        self.events.search += self.on_search
        self.legend(True)
        self.grid(False, False)
        self.crosshair(vert_visible=False, horz_visible=False)
        self.topbar.textbox('symbol')
        self.topbar.switcher('timeframe', timeframe_options, func=self._on_timeframe_selection)
        self.topbar.switcher('security', security_options, func=self._on_security_selection)

        self.topbar.textbox('quantity', '1', func=self._on_quantity_textbox)
        
        # Run initial script
        # self.run_script(f'''
        # {self.id}.search.window.style.display = "flex"
        # {self.id}.search.box.focus()
        # ''')
        
        print("PolygonQChart initialization complete")

    def show(self):
        print("Show method called")
        self.webview.show()
        QTimer.singleShot(1000, self.load_initial_data)

    def load_initial_data(self):
        print("Chart ready for user input")
        # Load some default data or symbol
        # asyncio.ensure_future(self._polygon('AAPL'))
        self.run_script(f'''
        {self.id}.search.window.style.display = "flex"
        {self.id}.search.box.focus()
        ''')
    
    def get_current_symbol(self):
        return self.topbar['symbol'].value
    
    def get_current_quantity(self):
        return self.topbar['quantity'].value

    # same method
    async def _polygon(self, symbol):
        print(f"Fetching data for {symbol}")
        self.spinner(True)
        self.set(pd.DataFrame(), True)
        self.crosshair(vert_visible=False, horz_visible=False)
        mult, span = self._convert_timeframe(self.topbar['timeframe'].value)
        delta = dt.timedelta(**{span + 's': int(mult)})
        short_delta = (delta < dt.timedelta(days=7))
        start_date = dt.datetime.now() if self.end_date == 'now' else dt.datetime.strptime(self.end_date, '%Y-%m-%d')
        remaining_bars = self.num_bars
        while remaining_bars > 0:
            start_date -= delta
            if start_date.weekday() > 4 and short_delta:  # Monday to Friday (0 to 4)
                continue
            remaining_bars -= 1
        epoch = dt.datetime.fromtimestamp(0)
        start_date = epoch if start_date < epoch else start_date
        success = await getattr(self.polygon, 'async_'+self.topbar['security'].value.lower())(
            symbol,
            timeframe=self.topbar['timeframe'].value,
            start_date=start_date.strftime('%Y-%m-%d'),
            end_date=self.end_date,
            limit=self.limit,
            live=self.live
        )
        self.spinner(False)
        self.crosshair() if success else None
        print(f"Data fetched for {symbol}: {'Success' if success else 'Failed'}")
        return success
    
    # same method
    async def on_search(self, chart, searched_string):
        print(f"Search triggered for {searched_string}")
        chart.topbar['symbol'].set(searched_string if await self._polygon(searched_string) else '')

    # same method
    async def _on_timeframe_selection(self, chart):
        print("Timeframe selection changed")
        await self._polygon(chart.topbar['symbol'].value) if chart.topbar['symbol'].value else None

    # same method
    async def _on_security_selection(self, chart):
        print("Security selection changed")
        self.precision(5 if chart.topbar['security'].value == 'Forex' else 2)

    async def _on_quantity_textbox(self, chart):
        print("Quantity textbox changed")
        quantity = chart.topbar['quantity'].value
        if quantity:
            print(f"Quantity: {quantity}")

    def _convert_timeframe(self, timeframe):
        spans = {
            'min': 'minute',
            'H': 'hour',
            'D': 'day',
            'W': 'week',
            'M': 'month',
        }
        try:
            multiplier = re.findall(r'\d+', timeframe)[0]
        except IndexError:
            return 1, spans[timeframe]
        timespan = spans[timeframe.replace(multiplier, '')]
        return multiplier, timespan

async def main():
    app = QApplication.instance() or QApplication(sys.argv)
    qloop = qasync.QEventLoop(app)
    asyncio.set_event_loop(qloop)

    chart = PolygonQChart(
        api_key="q0TtwNDqD1yz2pnD96HDLOBTMSKVh2Zl",
        width=1000,
        height=800,
        live=False
    )

    chart.show()

    # Keep the event loop running
    while True:
        await asyncio.sleep(0.1)

if __name__ == '__main__':
    try:
        qasync.run(main())
    except KeyboardInterrupt:
        print("Application closed by user")