from PyQt5.QtWidgets import QWidget, QApplication, QTableWidgetItem, QTableWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtCore import QObject, pyqtSlot as Slot, QUrl, QTimer
# from lightweight_charts.widgets import QtChart
from lightweight_charts import abstract
from lightweight_charts.util import parse_event_message
import asyncio
import datetime as dt
import pandas as pd
import qasync
from qasync import asyncSlot
import sys
import re
import pytz
from forex_python.converter import CurrencyCodes
from ib_insync import *
import json

if QWebEngineView:
    class Bridge(QObject):
        def __init__(self, chart, mainwindow=None):
            super().__init__()
            self.win = chart.win
            self.mainwindow = mainwindow
            self.chart = chart

        @Slot(str)
        def callback(self, message):
            emit_callback(self.win, message)
            
        @Slot(str)
        def log_message(self, message):
            self.mainwindow.log_message(message)

        @Slot(result=str)
        def getCurrentSymbol(self):
            return self.chart.get_current_symbol()
        
        @Slot(result=str)
        def getCurrentQuantity(self):
            return self.chart.get_current_quantity()
        
        @Slot(float, str, int, bool, result=str)
        def handleHorizontalLineOrder(self, line_price, operation='', quantity=0, update=False):
            ticker = self.chart.topbar['symbol'].value
            current_price = self.chart._last_bar['close']
            security = self.chart.topbar['security'].value

            if not update:
                operation = self.chart.topbar['order'].value
                quantity = self.chart.topbar['quantity'].value
            
            if not quantity:
                print("No quantity entered")
                return
            if operation == 'Buy':
                if line_price < current_price:
                    order_type = 'Limit'
                else:
                    order_type = 'Stop'
            elif operation == 'Sell':
                if line_price > current_price:
                    order_type = 'Limit'
                else:
                    order_type = 'Stop'
            if security == 'Stock':
                contract = Stock(ticker, 'SMART', 'USD')

            elif security == 'Forex':
                contract = Forex(ticker)
            
            elif security == 'Index':
                contract = Index(ticker)

            elif security == 'Option':
                symbol_all = ticker
                match = re.match(r"([A-Z]+)(\d{6})([CP])(\d+)", symbol_all)
                if match:
                    symbol = match.group(1)
                    lastdate = match.group(2)
                    right = match.group(3)
                    strike = match.group(4)

                    lastdate_formatted = f"20{lastdate}"

                    strike_price = float(strike) / 1000  
                
                    contract = Option(symbol=ticker, exchange='SMART', currency='USD', lastTradeDateOrContractMonth=lastdate_formatted, right=right, strike=strike_price)

            if contract:
                if order_type == 'Limit':
                    print("Placing limit order")
                    limit_price = round(line_price, 2)
                    limit_order = LimitOrder(operation, quantity, limit_price, account=self.chart.account)
                    trade = self.chart.ib.placeOrder(contract, limit_order)   

                elif order_type == 'Stop':
                    print("Placing stop order")
                    stop_price = round(line_price, 2)
                    stop_order = StopOrder(operation, quantity, stop_price, account=self.chart.account)
                    trade = self.chart.ib.placeOrder(contract, stop_order)
                    
            if trade:
                order_id = trade.order.orderId
                perm_id = trade.order.permId
                client_id = trade.order.clientId
                print("Order ID:", order_id, "Perm ID:", perm_id, "Client ID:", client_id)
                data = {'orderId': order_id, 'permId': perm_id, 'clientId': client_id, 'operation': operation}
                return json.dumps(data)
            
        @Slot(int, int, int)
        def handleCancelOrder(self, order_id, perm_id, client_id):
            self.chart.ib.cancelOrder(Order(orderId=order_id, permId=perm_id, clientId=client_id))
            print(f"Order {order_id} cancelled")
        

def emit_callback(window, string):
    func, args = parse_event_message(window, string)
    asyncio.create_task(func(*args)) if asyncio.iscoroutinefunction(func) else func(*args)

class CustomWebEnginePage(QWebEnginePage):
    def javaScriptConsoleMessage(self, level, message, line, sourceID):
        print("JS Console:", message, "Line:", line, "Source:", sourceID)
        super().javaScriptConsoleMessage(level, message, line, sourceID) 

class QtChart(abstract.AbstractChart):
    def __init__(self, widget=None, inner_width: float = 1.0, inner_height: float = 1.0,
                 scale_candles_only: bool = False, toolbox: bool = False):
        if QWebEngineView is None:
            raise ModuleNotFoundError('QWebEngineView was not found, and must be installed to use QtChart.')
        self.webview = QWebEngineView(widget)
        custom_page = CustomWebEnginePage(self.webview)
        self.webview.setPage(custom_page)

        super().__init__(abstract.Window(self.webview.page().runJavaScript, 'window.pythonObject.callback'),
                         inner_width, inner_height, scale_candles_only, toolbox)

        self.web_channel = QWebChannel()
        self.bridge = Bridge(self)
        self.web_channel.registerObject('bridge', self.bridge)
        self.webview.page().setWebChannel(self.web_channel)
        self.webview.loadFinished.connect(lambda: self.webview.page().runJavaScript('''
            let scriptElement = document.createElement("script")
            scriptElement.src = 'qrc:///qtwebchannel/qwebchannel.js'

            scriptElement.onload = function() {
                var bridge = new QWebChannel(qt.webChannelTransport, function(channel) {
                    var pythonObject = channel.objects.bridge
                    window.pythonObject = pythonObject
                })
            }

            document.head.appendChild(scriptElement)

        '''))
        self.webview.loadFinished.connect(lambda: QTimer.singleShot(200, self.win.on_js_load))
        self.webview.load(QUrl.fromLocalFile(abstract.INDEX))


    def get_webview(self): return self.webview

class PolygonQChart(QtChart):
    def __init__(self, api_key: str, widget: QWidget = None, live: bool = False, num_bars: int = 200,
                 end_date: str = 'now', limit: int = 5000,
                 timeframe_options: tuple = ('1min', '5min', '30min', 'D', 'W'),
                #  security_options: tuple = ('Stock', 'Option', 'Index', 'Forex', 'Crypto'),
                order_options: tuple = ('Buy', 'Sell'),
                 toolbox: bool = True, width: int = 800, height: int = 600,
                 inner_width: float = 1.0, inner_height: float = 1.0, scale_candles_only: bool = False):
        super().__init__(widget, inner_width, inner_height, scale_candles_only, toolbox)
        
        print("Initializing PolygonQChart")
        self.api_key = api_key
        self.num_bars = num_bars
        self.end_date = end_date
        self.limit = limit
        self.live = live

        self.ib = IB()
        self.account = 'DU8014278'

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
        # self.topbar.switcher('security', security_options, func=self._on_security_selection)
        self.topbar.textbox('security')

        self.topbar.textbox('quantity', '1', func=self._on_quantity_textbox)

        self.topbar.switcher('order', order_options)
        self.topbar.button('market', 'Place Market Order', func=self._on_market_order)

        self.toolbox.import_drawings("drawings.json")

        # Run initial script
        # self.run_script(f'''
        # {self.id}.search.window.style.display = "flex"
        # {self.id}.search.box.focus()
        # ''')
        # abstract.Window._return_q = PolygonQChart.WV.return_queue
        print("PolygonQChart initialization complete")
    
    async def connect_ib(self):
        util.patchAsyncio()
        try:
            await self.ib.connectAsync('127.0.0.1', 7497, clientId=10)
            print("IB Connection established")
        except Exception as e:
            print(f"Failed to connect IB: {str(e)}")

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

    def init_bridge(self, mainwindow):
        self.bridge = Bridge(self, mainwindow)
        self.web_channel.registerObject('bridge', self.bridge)

    async def _polygon(self, symbol):
        print(f"Fetching data for {symbol}")
        self.spinner(True)
        self.set(pd.DataFrame(), True)
        self.crosshair(vert_visible=False, horz_visible=False)
        mult, span = self._convert_timeframe(self.topbar['timeframe'].value)
        delta = dt.timedelta(**{span + 's': int(mult)})
        short_delta = (delta < dt.timedelta(days=7))
        start_date = dt.datetime.now() if self.end_date == 'now' else dt.datetime.strptime(self.end_date, '%Y-%m-%d')
        start_date = self.get_adjusted_date() if self.end_date == 'now' else start_date
        remaining_bars = self.num_bars
        while remaining_bars > 0:
            start_date -= delta
            if start_date.weekday() > 4 and short_delta:  # Monday to Friday (0 to 4)
                continue
            remaining_bars -= 1
        epoch = dt.datetime.fromtimestamp(0).date() if self.end_date == 'now' else dt.datetime.fromtimestamp(0)
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
    
    async def on_search(self, chart, searched_string):
        print(f"Search triggered for {searched_string}")
        chart.toolbox.save_drawings_under(chart.topbar['symbol'])
        chart.topbar['security'].set(self.identify_financial_instrument(searched_string))
        cleaned_string = re.sub(r'[\^\-]', '', searched_string)
        chart.topbar['symbol'].set(cleaned_string if await self._polygon(cleaned_string) else '')
        self.precision(5 if chart.topbar['security'].value == 'Forex' else 2)
        chart.toolbox.load_drawings(chart.topbar['symbol'].value)

    async def _on_timeframe_selection(self, chart):
        print("Timeframe selection changed")
        await self._polygon(chart.topbar['symbol'].value) if chart.topbar['symbol'].value else None


    async def _on_quantity_textbox(self, chart):
        print("Quantity textbox changed")
        quantity = chart.topbar['quantity'].value
        if quantity:
            print(f"Quantity: {quantity}")

    async def _on_market_order(self, chart):
        print("Market order button clicked")
        quantity = chart.topbar['quantity'].value
        operation = chart.topbar['order'].value
        if not chart.topbar['symbol'].value:
            print("No symbol selected")
            return
        if not quantity:
            print("No quantity entered")
            return
        if chart.topbar['security'].value == 'Stock':
            contract = Stock(chart.topbar['symbol'].value, 'SMART', 'USD')
            
        elif chart.topbar['security'].value == 'Option':
            symbol_all = chart.topbar['symbol'].value
            match = re.match(r"([A-Z]+)(\d{6})([PC])(\d+)", symbol_all)
            if match:
                symbol = match.group(1)
                lastdate = match.group(2)
                right = match.group(3)
                strike = match.group(4)

                lastdate_formatted = f"20{lastdate}"

                strike_price = float(strike) / 1000  
            
            contract = Option(symbol=symbol, exchange='SMART', currency='USD', lastTradeDateOrContractMonth=lastdate_formatted, right=right, strike=strike_price)
        
        elif chart.topbar['security'].value == 'Forex':
            contract = Forex(chart.topbar['symbol'].value)
        
        elif chart.topbar['security'].value == 'Index':
            contract = Index(chart.topbar['symbol'].value)

        if contract:
            market_order = MarketOrder(operation, quantity, account = self.account)
            market_trade = self.ib.placeOrder(contract, market_order)


    def _convert_timeframe(self, timeframe):
        spans = {
            'min': 'minute',
            'H': 'hour',
            'D': 'day',
            'W': 'week',
            'M': 'month',
            'sec': 'second'
        }
        try:
            multiplier = re.findall(r'\d+', timeframe)[0]
        except IndexError:
            return 1, spans[timeframe]
        timespan = spans[timeframe.replace(multiplier, '')]
        return multiplier, timespan
    
    def convert_to_est(self, utc_datetime):
        utc_zone = pytz.timezone('UTC')
        est_zone = pytz.timezone('America/New_York')
        utc_datetime = utc_zone.localize(utc_datetime)
        est_datetime = utc_datetime.astimezone(est_zone)
        return est_datetime
    
    def get_adjusted_date(self):
        current_utc = dt.datetime.utcnow()
        current_est = self.convert_to_est(current_utc)

        if current_est.time() < dt.datetime.strptime("09:00", "%H:%M").time():
            return current_est.date() - dt.timedelta(days=1)
        elif current_est.time() >= dt.datetime.strptime("16:00", "%H:%M").time():
            return current_est.date()
        return current_est.date()
    
    def identify_financial_instrument(self, input_string):
        # Check for Index
        if input_string.startswith('^'):
            return 'Index'
        
        # Check for Crypto
        if '-' in input_string:
            parts = input_string.split('-')
            if len(parts) == 2:
                return 'Crypto'
        
        # Check for Option using regex
        if re.match(r'[A-Z]+(\d{6}[CP]\d+)$', input_string):
            return 'Option'
        
        # Check for Forex

        currency_codes = CurrencyCodes()

        def is_valid_currency(currency):
            try:
                return currency_codes.get_currency_name(currency) is not None
            except:
                return False
        try:
            # Attempt to parse and get the rate to validate if it's a real currency pair
            if len(input_string) == 6 and is_valid_currency(input_string[:3]) and is_valid_currency(input_string[3:]):
                return 'Forex'
        except:
            pass
        
        # Default to Stock
        return 'Stock'
        

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