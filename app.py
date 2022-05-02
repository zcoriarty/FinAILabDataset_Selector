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

# other files
from tickers import Tickers as tk
from equities import Equities
from home import Home

# padding = 0
# st.markdown(f""" <style>
#     .reportview-container .main .block-container{{
#         padding-top: {padding}rem;
#         padding-right: {padding}rem;
#         padding-left: {padding}rem;
#         padding-bottom: {padding}rem;
#     }} </style> """, unsafe_allow_html=True)

# periods to select
periodDict = {'DurationText':['1M','3M','6M','YTD','1Y','2Y','5Y','MAX'], 'DurationN':[30,90,120,335,365,730,1825,18250]}
periods= pd.DataFrame(periodDict)

# defining first tab1: Summary ############################################

# start and end date of the plot data 
today = datetime.today().date()
#########display pct and usd change next to the price####################
# Current= (si.get_data('AAPL', start_date=today, end_date=today))['close']
# openprice= (si.get_data('AAPL', start_date=today, end_date=today))['open']

st.set_page_config(layout="wide")

def PageBeginning():

    
    st.title(ticker) # display chosen ticker name
        
    st.header(round(si.get_live_price(ticker),2)) # display price

    ############ captions for date time####################
    st.caption('S&P500 Real Time Price. Currency in USD.')
    dt_string = datetime.now().strftime("%d/%m/%Y %H:%M")
    st.caption("as of " + dt_string + " CET")
    #######################################################
    return



######################################################################################################################################
######################################################################################################################################
######################################################################################################################################
def tab6():
    N_Simualtions = st.selectbox('Number of simulations',[200,500,1000])
    T_Horizon = st.selectbox('Time horizon',[30,60,90])

    st.subheader('MonteCarlo simulation of a stock price for '+ ticker )
    class MonteCarlo(object):
        
        def __init__(self, ticker, data_source, start_date, end_date, time_horizon, n_simulation, seed):
            
            # Initiate class variables
            self.ticker = ticker  # Stock ticker
            self.data_source = data_source  # Source of data, e.g. 'yahoo'
            self.start_date = datetime.strptime(start_date, '%Y-%m-%d')  # Text, YYYY-MM-DD
            self.end_date = datetime.strptime(end_date, '%Y-%m-%d')  # Text, YYYY-MM-DD
            self.time_horizon = time_horizon  # Days
            self.n_simulation = n_simulation  # Number of simulations
            self.seed = seed  # Random seed
            self.simulation_df = pd.DataFrame()  # Table of results
            
            # Extract stock data
            self.stock_price = web.DataReader(ticker, data_source, self.start_date, self.end_date)
            
            # Calculate financial metrics
            # Daily return (of close price)
            self.daily_return = self.stock_price['Close'].pct_change()
            # Volatility (of close price)
            self.daily_volatility = np.std(self.daily_return)
            
        def run_simulation(self):
            
            # Run the simulation
            np.random.seed(self.seed)
            self.simulation_df = pd.DataFrame()  # Reset
            
            for i in range(self.n_simulation):

                # The list to store the next stock price
                next_price = []

                # Create the next stock price
                last_price = self.stock_price['Close'][-1]

                for j in range(self.time_horizon):
                    
                    # Generate the random percentage change around the mean (0) and std (daily_volatility)
                    future_return = np.random.normal(0, self.daily_volatility)

                    # Generate the random future price
                    future_price = last_price * (1 + future_return)

                    # Save the price and go next
                    next_price.append(future_price)
                    last_price = future_price

                # Store the result of the simulation
                self.simulation_df[i] = next_price

        def plot_simulation_price(self):
            
            # Plot the simulation stock price in the future
            fig, ax = plt.subplots()
            fig.set_size_inches(15, 10, forward=True)

            plt.plot(self.simulation_df)
            plt.title('Monte Carlo simulation for ' + self.ticker + \
                    ' stock price in next ' + str(self.time_horizon) + ' days')
            plt.xlabel('Day')
            plt.ylabel('Price')

            plt.axhline(y=self.stock_price['Close'][-1], color='red')
            plt.legend(['Current stock price is: ' + str(np.round(self.stock_price['Close'][-1], 2))])
            ax.get_legend().legendHandles[0].set_color('red')

            st.pyplot(fig)
    # Initiate
    today = datetime.today().date().strftime('%Y-%m-%d')
    mc_sim = MonteCarlo(ticker=ticker, data_source='yahoo',
                    start_date='2021-01-01', end_date=today,
                    time_horizon=T_Horizon, n_simulation=N_Simualtions, seed=123)
    # Run simulation
    mc_sim.run_simulation()
    # Plot the results
    mc_sim.plot_simulation_price()
    
#Creating a sidebar menu
def run(): #function to run the entire dashboard at once
    
    

    features = pd.read_csv('feature_tracker_table.csv')
    category_list = features.columns

    # Add selection box
    global ticker, category, source #move the ticker variable to global var names.

    category = st.sidebar.selectbox("Select a Category", category_list, index=0)
    ticker = st.sidebar.selectbox("Select a Ticker", tk.tickers_dict[category](), index=3)
        
    # Add a radio box
    # select_tab = st.sidebar.radio("Select tab", ['Home', 'Equity Market', 'Financials','Analysis','Monte Carlo Simulation'])
    # # defining an update button:
    # run_button = st.sidebar.button('Update Data')
    
    # if run_button:
    #     st.experimental_rerun()

     # Show the selected tab
    if category == 'Home':
        Home.page(ticker, periods, today)
    elif category == 'Equities':  
        general, financials, analysis = st.sidebar.button("General"), st.sidebar.button("Financials"), st.sidebar.button("Analysis")      
        if financials:
            Equities.financials(ticker)
        elif analysis:
            Equities.analysis(ticker)
        elif general:
            Equities.general(ticker)
        else:
            Equities.general(ticker)

    elif category == 'Monte Carlo Simulation':
        tab6()

    
run()