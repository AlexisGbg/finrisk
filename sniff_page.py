
import streamlit as st
from src.vars import INCOME_STMT_KPI, BALANCE_SHEET_KPI
import pandas as pd


def load_page():
    # KPIs 
    stocks = st.session_state.my_portfolio.stocks
    if len(stocks) == 0:
        st.warning("no stocks loaded! Please go to 'create portfolio' to load stocks")
    is_kpis = [x.value for x in INCOME_STMT_KPI]
    bs_kpis = [x.value for x in BALANCE_SHEET_KPI]
    for s in stocks:
        st.header(stocks[s].stock_name)
        incomestmt = stocks[s].ticker.incomestmt.loc[is_kpis]
        balance_sheet = stocks[s].ticker.balance_sheet.loc[bs_kpis]
        data = pd.concat([incomestmt, balance_sheet])
        st.dataframe(data)
