import streamlit as st
from src.vars import INCOME_STMT_KPI, BALANCE_SHEET_KPI, COMPUTED_KPI, ORDERED_KPIS
import pandas as pd
import plotly.graph_objects as go
import random

MONTE_CARLO_ITERATIONS = 15

GROWTH_RATE_MEAN_DEFAULT = 0.02
GROWTH_RATE_STD_DEFAULT = 0.05
GROWTH_RATE_LOWER_DEFAULT = -0.07
GROWTH_RATE_UPPER_DEFAULT = 0.1


def load_page():
    # KPIs
    if not "my_portfolio" in st.session_state:
        st.warning("no stocks loaded! Please go to 'create portfolio' to load stocks")
        st.stop()
    stocks = st.session_state.my_portfolio.stocks
    if len(stocks) == 0:
        st.warning("no stocks loaded! Please go to 'create portfolio' to load stocks")
    is_kpis = [x.value for x in INCOME_STMT_KPI]
    bs_kpis = [x.value for x in BALANCE_SHEET_KPI]
    for s in stocks:
        st.header(stocks[s].stock_name + " (" + stocks[s].ticker.get_info()["industry"] + ")")
        st.text(" ")
        st.markdown(stocks[s].ticker.get_info()["longBusinessSummary"])
        st.text(" ")
        st.divider()
        incomestmt = stocks[s].ticker.incomestmt
        valid_rows = set(incomestmt.index) & {x for x in is_kpis}
        incomestmt = incomestmt.loc[list(valid_rows)]
        balance_sheet = stocks[s].ticker.balance_sheet
        valid_rows = set(balance_sheet.index) & {x for x in bs_kpis}
        balance_sheet = balance_sheet.loc[list(valid_rows)]
        columns = sorted(list(set(incomestmt.columns) & set(balance_sheet.columns)))
        data = pd.concat([incomestmt[columns], balance_sheet[columns]])
        # Adding ratios
        try:
            data.loc[COMPUTED_KPI.LEVERAGE.value] = (
                data.loc[INCOME_STMT_KPI.EBITDA.value]
                / data.loc[BALANCE_SHEET_KPI.TOTAL_DEPT.value]
            )
            data.loc[COMPUTED_KPI.ENTERPRISE_MULTIPLE.value] = (
                data.loc[BALANCE_SHEET_KPI.TOTAL_CAPITALIZATION.value]
                / data.loc[INCOME_STMT_KPI.EBITDA.value]
            )
            data.loc[COMPUTED_KPI.EBITDA_MARGIN.value] = (
                data.loc[INCOME_STMT_KPI.EBITDA.value]
                / data.loc[INCOME_STMT_KPI.REVENUE.value]
            ) * 100
            data.loc[COMPUTED_KPI.REVENUE_GROWTH.value] = (
                data.loc[INCOME_STMT_KPI.REVENUE.value].pct_change() * 100
            )
            data.loc[COMPUTED_KPI.EBITDA_GROWTH.value] = (
                data.loc[INCOME_STMT_KPI.EBITDA.value].pct_change() * 100
            )
        except KeyError as e:
            print(f"waning: some rows are missing")
        not_empty_cols = [not all((data[x].isnull()) | (data[x] == 0)) for x in data.columns]
        data = data.loc[[x.value for x in ORDERED_KPIS if x.value in data.index], not_empty_cols]
        st.dataframe(data)

    st.divider()
    st.subheader("Revenue growth")
    radio_button_revenue_growth = st.radio(
        "Choose growth rate distribution", ("Normal", "Uniform")
    )

    gr_mean = GROWTH_RATE_MEAN_DEFAULT
    gr_std = GROWTH_RATE_STD_DEFAULT
    gr_lower = GROWTH_RATE_LOWER_DEFAULT
    gr_upper = GROWTH_RATE_UPPER_DEFAULT
    if radio_button_revenue_growth == "Normal":
        gr_mean = st.number_input("Mean revenue growth rate (in %)", value=gr_mean)
        gr_std = st.number_input("Revenue growth rate std. dev. (in %)", value=gr_std)
    elif radio_button_revenue_growth == "Uniform":
        gr_lower = st.number_input("Lower end growth rate (in %)", value=gr_lower)
        gr_upper = st.number_input("Upper end growth rate (in %)", value=gr_upper)

    # Add Sniff test tab
    if st.button("Run Simulation"):
        fig = go.Figure()
        for _ in range(MONTE_CARLO_ITERATIONS):
            if radio_button_revenue_growth == "Normal":
                grs = [random.gauss(gr_mean, gr_std) for x in range(100)]
            else:
                grs = [random.uniform(gr_lower, gr_upper) for x in range(100)]
            rev = data.loc[INCOME_STMT_KPI.REVENUE.value][-1]
            revs = []
            for gr in grs:
                rev *= 1 + gr
                revs.append(rev)
            fig.add_trace(
                go.Scatter(
                    y=revs,
                    mode="lines",
                )
            )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig)
