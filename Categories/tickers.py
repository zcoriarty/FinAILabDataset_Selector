from matplotlib import ticker
from yahooquery import Screener
import pandas as pd
from get_all_tickers import get_tickers as gt

import yahoo_fin.stock_info as si


class Tickers:

	

	def equities():
			ticker_list = si.tickers_sp500()

			return ticker_list

	def crypto():
		s = Screener()
		data = s.get_screeners('all_cryptocurrencies_us', count=250)

		data_df = pd.DataFrame(data['all_cryptocurrencies_us']['quotes'])
		# # data is in the quotes key
		# data['all_cryptocurrencies_us']['quotes']
		return data_df['symbol'].tolist()

	tickers_dict = {"Equities": equities,
                    # "Fixed Income": fixed_income,
                    # "FX": fx,
                    # "Commodities": commodities,
                    "Crypto": crypto,
                    # "Stock Fundamentals": fundamentals,
                    # "Macroeconomics Data": macro_datq,
                    # "News and Sentiments": news_sentiment,
                    # "Alt Data": alt_data
                    }
