from bs4 import BeautifulSoup
import requests


class Stock:

    def __init__(self, stock):
        self.stock = stock
        self.soup = None
        self.stock_name = None
        self.stock_details = None
        self.stock_more_info = None
        self.stock_fundamental = None
        self.stock_technical = None
        self._get_parsed_html()
        self._get_stock_name()

    def get_stock_details(self):
        name = self.stock_name
        last_price = self._get_text_by_id('lblStockLatestLastPrice')
        open_price = self._get_text_by_id('lblStockLatestOpen')
        low_price = self._get_text_by_id('lblStockLatestLow')
        high_price = self._get_text_by_id('lblStockLatestHigh')
        ave_price = self._get_text_by_id('lblStockLatestAverage')

        details = f"{name}\n" \
                  f"Price: {last_price}\n" \
                  f"Open Price: {open_price}\n" \
                  f"Low Price: {low_price}\n" \
                  f"High Price: {high_price}\n" \
                  f"Average Price: {ave_price}\n"
        self.stock_details = details
        return self.stock_details

    def get_more_info(self):
        volume = self._get_text_by_id('lblStockLatestVolume')
        value = self._get_text_by_id('lblStockLatestValue')
        market_cap = self._get_text_by_id('lblStockLatestMarketCap')
        prev_close = self._get_text_by_id('lblStockLatestClose')
        net_foreign = self._get_text_by_id('lblStockLatestNetForeign')

        more_info = f"{self.stock_name}\n" \
                    "MORE INFO:\n" \
                    f"Volume: {volume}\n" \
                    f"Value: {value}\n" \
                    f"Market Cap: {market_cap}\n" \
                    f"Previous Closing Price: {prev_close}\n" \
                    f"Net foreign buying: {net_foreign}"
        self.stock_more_info = more_info
        return self.stock_more_info

    def get_fundamental(self):
        fundamental = self.soup.find('div', id='FundamentalAnalysisContent')
        fundamental_info = fundamental.find_all('td')
        high_52_week = fundamental_info[1].get_text()
        eps = fundamental_info[3].get_text()
        price_to_book = fundamental_info[5].get_text()
        low_52_week = fundamental_info[7].get_text()
        price_earning = fundamental_info[9].get_text()
        return_on_equity = fundamental_info[11].get_text()
        fair_value = fundamental_info[13].get_text()
        div_per_share = fundamental_info[15].get_text()

        details = f"{self.stock_name}\n" \
                  "FUNDAMENTAL\n" \
                  f"52-week High: {high_52_week}\n" \
                  f"52-week Low: {low_52_week}\n" \
                  f"Earnings Per Share: {eps}\n" \
                  f"Price to Book Value (P/BV): {price_to_book}\n" \
                  f"Price-Earnings Ratio (P/E): {price_earning}\n" \
                  f"Return on Equity (ROE): {return_on_equity}\n" \
                  f"Fair Value: {fair_value}\n" \
                  f"Dividends Per Share (DPS): {div_per_share}"
        self.stock_fundamental = details
        return self.stock_fundamental

    def get_technical(self):
        technical = self.soup.find('div', id='TechnicalAnalysisContent')
        technical_info = technical.find_all('td')
        supports = technical_info[1].get_text() + ", " + \
            technical_info[7].get_text()
        resistances = technical_info[3].get_text() + ", " + \
            technical_info[9].get_text()
        short_term = technical_info[5].get_text()
        medium_term = technical_info[11].get_text()

        details = f"{self.stock_name}\n" \
                  "TECHNICAL\n" \
                  f"Support: {supports}\n" \
                  f"Resistance: {resistances}\n" \
                  f"Short-term Trend: {short_term}\n" \
                  f"Medium-term Trend: {medium_term}"
        self.stock_technical = details
        return self.stock_technical

    def _get_parsed_html(self):
        page = requests.get(f"https://www.investagrams.com/Stock/{self.stock}")
        self.soup = BeautifulSoup(page.content, 'html.parser')

    def _get_stock_name(self):
        h4 = self.soup.find('h4', class_="mb-0")
        self.stock_name = h4.find('small').get_text()

    def _get_text_by_id(self, id):
        return self.soup.find(id=id).get_text()
