# Import libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# from streamlit.script_request_queue import RerunData
import yahoo_fin.stock_info as si
import streamlit as st
from datetime import datetime, timedelta
import plotly.graph_objects as go
import pandas_datareader.data as web
from st_btn_select import st_btn_select


class Equities:


	def general(ticker):

		data1, graph, data2 = st.columns(3)
	
		with graph:
			
			
			start_date = st.date_input("Start date", datetime.today().date() - timedelta(days=30))
			end_date = st.date_input("End date", datetime.today().date())
			
			# added selectbox for data intervals
			intervalDict = {'IntervalButton':['Daily','Weekly','Monthly'],'IntervalCode':['1d','1wk','1mo']}
			intervals= pd.DataFrame(intervalDict)
			time_interval_button = st_btn_select((intervals['IntervalButton']))
			
			plot_type = "Candle"
			st.write(ticker, ":   ", round(si.get_live_price(ticker),2)) # display chosen ticker name
			if plot_type =='Line':
			#plotting 
				def PlotTab2(start_date, end_date, time_interval_button):
					# data used in tab2 for closing price
					Tab2_ClosingPrice = si.get_data(ticker,start_date=start_date,end_date=end_date,interval=(intervals.loc[intervals['IntervalButton']==time_interval_button,'IntervalCode'].iloc[0]))
					fig,ax = plt.subplots(figsize=(10,5))
					ax.plot(Tab2_ClosingPrice['close'], label='Closing Price', color='green')
					ax2=ax.twinx() #twinning the first ax
					ax2.bar(Tab2_ClosingPrice.index,Tab2_ClosingPrice['volume'], label='Volume mlns',color='mediumseagreen') #plotting bar chart
					ax2.set_ylim(0,((Tab2_ClosingPrice['volume'].max())*5)) # diminishing the scale of the bar char 
					ax2.set_yticks([])  #hiding y ticks of bar chart from the plot
					ax.yaxis.tick_right() #moving ticks to the right side
					my_xticks = ax.get_xticks() #store ticks in np array
					ax.set_xticks([my_xticks[0], np.median(my_xticks),my_xticks[-1]]) # only show 1st and median ticks in the plot
					######Legend labels for both axes shown together in one legend:########
					lines, labels = ax.get_legend_handles_labels()
					lines2, labels2 = ax2.get_legend_handles_labels()
					ax2.legend(lines + lines2, labels + labels2, loc=0)
					ax.set_frame_on(False)
					ax2.set_frame_on(False)

					return st.pyplot(fig)  
				PlotTab2(start_date=start_date,end_date=end_date, time_interval_button=time_interval_button)
			else: 
				#plotting candle chart using py plot
				Data_CandleSt = si.get_data(ticker,start_date=start_date,end_date=end_date,interval=(intervals.loc[intervals['IntervalButton']==time_interval_button,'IntervalCode'].iloc[0]))
				fig = go.Figure(data=[go.Candlestick(x=Data_CandleSt.index,
						open=Data_CandleSt['open'],
						high=Data_CandleSt['high'],
						low=Data_CandleSt['low'],
						close=Data_CandleSt['close'])])
				#fig = go.bar(Data_CandleSt, x=Data_CandleSt.index, y=Data_CandleSt['Volume']) volume to be added 
				fig.update_layout(autosize=False,
    							  width=500,
    							  height=500,
								  margin=dict(l=0, r=0, t=20, b=20), 
								  xaxis_rangeslider_visible=False)
				st.plotly_chart(fig, use_container_width=True)
				
			# added radio boxes to choose a graph type
			plot_type = st_btn_select(('Candle','Line(not working)'))

		with data1:
			#get valuation info
			st.title('Valuation Measures')
			st.dataframe(si.get_stats_valuation(ticker).assign(hack='').set_index('hack'))
			
			dataTab3 = si.get_stats(ticker)
			#dataTab3.columns = [''] * len(dataTab3.columns)

			st.title('Financial Highlights')
			st.subheader('Fiscal Year')
			st.dataframe(dataTab3.iloc[29:31].assign(hack='').set_index('hack'))

			st.subheader('Profitability')
			st.dataframe(dataTab3.iloc[31:33].assign(hack='').set_index('hack'))

			st.subheader('Management Effectiveness')
			st.dataframe(dataTab3.iloc[32:34].assign(hack='').set_index('hack'))

			# st.subheader('Income Statement')
			# st.dataframe(dataTab3.iloc[35:43].assign(hack='').set_index('hack'))

			# st.subheader('Balance Sheet')
			# st.dataframe(dataTab3.iloc[43:49].assign(hack='').set_index('hack'))

			# st.subheader('Cash Flow Statement')
			# st.dataframe(dataTab3.iloc[49:].assign(hack='').set_index('hack'))
		with data2:
			st.title('Trading Information')
			st.subheader('Stock Price History')
			st.dataframe(dataTab3.iloc[:7].assign(hack='').set_index('hack'))

			st.subheader('Share Statistics')
			st.dataframe(dataTab3.iloc[7:15].assign(hack='').set_index('hack'))

			st.subheader('Dividends & Splits')
			st.dataframe(dataTab3.iloc[10:29].assign(hack='').set_index('hack'))

	def financials(ticker):
		# FinancialReportType = st_btn_select(('Income Statement','Balance Sheet','Cash Flow')) #selectbox to select FS type
		PeriodDict = {'Report':['Annual','Quarterly'],'ReportCode':[True,False]}
		PeriodDF=pd.DataFrame(PeriodDict)
		# PeriodType = st.radio('Report:',PeriodDF['Report']) #radio to select report period

		col1, col2 = st.columns(2)

		with col1:
			st.title("Annually")
			st.subheader('Annual Income Statement for '+ ticker)
			incs = si.get_income_statement(ticker,yearly=(PeriodDF.loc[PeriodDF['Report']=="Annual",'ReportCode'].iloc[0]))
			st.dataframe(incs)
			st.subheader('Annual Balance Sheet Statement for '+ ticker)
			bsht = si.get_cash_flow(ticker,yearly=(PeriodDF.loc[PeriodDF['Report']=="Annual",'ReportCode'].iloc[0]))
			st.dataframe(bsht)
			st.subheader('Annual Cash Flow Statement for '+ ticker)
			cflow= si.get_balance_sheet(ticker,yearly=(PeriodDF.loc[PeriodDF['Report']=="Annual",'ReportCode'].iloc[0]))
			st.dataframe(cflow)
		with col2:
			st.title("Quarterly")
			st.subheader('Quarterly Income Statement for '+ ticker)
			incs = si.get_income_statement(ticker,yearly=(PeriodDF.loc[PeriodDF['Report']=="Quarterly",'ReportCode'].iloc[0]))
			st.dataframe(incs)
			st.subheader('Quarterly Balance Sheet Statement for '+ ticker)
			bsht = si.get_cash_flow(ticker,yearly=(PeriodDF.loc[PeriodDF['Report']=="Quarterly",'ReportCode'].iloc[0]))
			st.dataframe(bsht)
			st.subheader('Quarterly Cash Flow Statement for '+ ticker)
			cflow= si.get_balance_sheet(ticker,yearly=(PeriodDF.loc[PeriodDF['Report']=="Quarterly",'ReportCode'].iloc[0]))
			st.dataframe(cflow)
		# def ShowReport(FinancialReportType,PeriodType): #defining a function to display the data according to selected parameters
		# 	if FinancialReportType == 'Income Statement': 
		# 		st.subheader(PeriodType +' Income Statement for '+ ticker)
		# 		x = si.get_income_statement(ticker,yearly=(PeriodDF.loc[PeriodDF['Report']==PeriodType,'ReportCode'].iloc[0]))
		# 		#selecting data. For yearly true or false refering to the DF PeriodDF to select True or False depending on Annual or Quarterly selection in radiobox
		# 	elif FinancialReportType == 'Balance Sheet':
		# 		st.subheader(PeriodType + ' Balance Sheet Statement for '+ ticker)
		# 		x = si.get_cash_flow(ticker,yearly=(PeriodDF.loc[PeriodDF['Report']==PeriodType,'ReportCode'].iloc[0]))
		# 	elif FinancialReportType == 'Cash Flow':
		# 		st.subheader(PeriodType +' Cash Flow Statement for '+ ticker)
		# 		x= si.get_balance_sheet(ticker,yearly=(PeriodDF.loc[PeriodDF['Report']==PeriodType,'ReportCode'].iloc[0]))
		# 	return st.dataframe(x)
		# ShowReport(FinancialReportType=FinancialReportType, PeriodType=PeriodType)

	def analysis(ticker):
		col1, col2 = st.columns(2)
		with col1:
			st.title(ticker)
			st.dataframe(si.get_analysts_info(ticker)['Earnings Estimate'].assign(hack='').set_index('hack')) #again, assign hides index values from printing
			st.dataframe(si.get_analysts_info(ticker)['Revenue Estimate'].assign(hack='').set_index('hack'))
			st.dataframe(si.get_analysts_info(ticker)['Earnings History'].assign(hack='').set_index('hack'))
		with col2: 
			st.markdown('#')
			st.dataframe(si.get_analysts_info(ticker)['EPS Trend'].assign(hack='').set_index('hack'))
			st.dataframe(si.get_analysts_info(ticker)['EPS Revisions'].assign(hack='').set_index('hack'))
			st.dataframe(si.get_analysts_info(ticker)['Growth Estimates'].assign(hack='').set_index('hack'))