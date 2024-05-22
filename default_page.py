import streamlit as st
import stTools as tools


def load_page():
    st.markdown(
        """
            Welcome to the SFS FinRisk Modeling Simulator! Dive into this app to seamlessly evaluate and simulate your
            portfolio's risk. Risk management, akin to protective gear in sports, safeguards your investments against
            market uncertainties. Treat your investment journey as a strategic game; mastering the rules and anticipating challenges gives you a competitive edge. 
            Value at Risk (VaR) and Conditional Value at Risk (CVaR) act  as your financial GPS, guiding you through risk navigation and ensuring a resilient investment strategy
            
  
            """
    )

    st.subheader(f"Market Preview")

    col_stock1, col_stock_2, col_stock_3 = st.columns(3)

    with col_stock1:
        tools.create_candle_stick_plot(stock_ticker_name="^DJI",
                                       stock_name="Dow Jones Industrial")

    with col_stock_2:
        tools.create_candle_stick_plot(stock_ticker_name="^IXIC",
                                       stock_name="Nasdaq Composite")

    with col_stock_3:
        tools.create_candle_stick_plot(stock_ticker_name="^GSPC",
                                       stock_name="S&P 500")

    # make 3 columns for sectors
    col_sector1, col_sector2, col_sector3 = st.columns(3)

    with col_sector1:
        st.subheader(f"Technology")
        stock_list = ["AAPL", "MSFT", "AMZN", "GOOG", "META", "TSLA", "NVDA", "NFLX"]
        stock_name = ["Apple", "Microsoft", "Amazon", "Google", "Meta", "Tesla", "Nvidia", "Netflix"]

        df_stocks = tools.create_stocks_dataframe(stock_list, stock_name)
        tools.create_dateframe_view(df_stocks)

    with col_sector2:
        st.subheader(f"Banking")
        stock_list = ['JPM', 'BAC', 'WFC', 'GS', 'MS', 'C', 'USB', 'PNC']
        stock_name = ['JPMorgan', 'BoA', 'Wells Fargo', 'Goldman Sachs', 'Morgan Stanley',
                       'Citigroup', 'U.S. Bancorp', 'PNC']
        df_stocks = tools.create_stocks_dataframe(stock_list, stock_name)
        tools.create_dateframe_view(df_stocks)

    with col_sector3:
        st.subheader(f"Meme Stocks")
        stock_list = ["GME", "AMC", "BB", "NOK", "RIVN", "SPCE", "F", "T"]
        stock_name = ["GameStop", "AMC Entertainment", "BlackBerry", "Nokia", "Rivian",
                      "Virgin Galactic", "Ford", "AT&T"]

        df_stocks = tools.create_stocks_dataframe(stock_list, stock_name)
        tools.create_dateframe_view(df_stocks)
