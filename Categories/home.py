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
class Home:

	

	def page(ticker, periods, today):

		#######################################################################################################
		#buttons to select desired period of data 
		buttons_tab1 = st_btn_select((periods['DurationText']))
		########################################################################################################

		#plots for each selected duration: 
		def PlotTab1(buttons_tab1): 
			x = today-timedelta(periods.loc[periods['DurationText']==buttons_tab1,'DurationN'].iloc[0].item()) #start date that varies with selected period
			closing_price= si.get_data(ticker, start_date=x, end_date=today) #data for the plots
			fig,ax = plt.subplots(figsize=(10,5))
			ax.plot(closing_price['close'], label='Closing Price',color='green')
			#plt.fill_between(closing_price.index, closing_price['close'],color='green') #fill the color under the line
			ax2=ax.twinx() #twinning bar chart plot
			ax2.bar(closing_price.index,closing_price['volume'], label='Volume mlns',color='mediumseagreen') #plotting bar chart
			ax2.set_ylim(0,((closing_price['volume'].max())*5)) # diminishing the scale of the bar char 
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
			#######################################################################
			st.pyplot(fig)
		PlotTab1(buttons_tab1=buttons_tab1) #call the function

		################defining columns and tables to show summary data in two columns########################
		col1, col2 = st.columns(2)
		QuoteTable = si.get_quote_table(ticker, dict_result=False)
		QuoteTable['value'] = QuoteTable['value'].astype(str)
		QuoteTable = QuoteTable.drop(15) #dropping one of the lines from the df to divide equally into 2 cols

		with col1: 
			st.dataframe(QuoteTable.iloc[:8,:].assign(hack='').set_index('hack')) #showing df and hiding index col
		with col2:
			st.dataframe(QuoteTable.iloc[8:,].assign(hack='').set_index('hack'))
