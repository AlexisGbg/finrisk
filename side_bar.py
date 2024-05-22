import streamlit as st
import stTools as tools
import side_bar_components


def load_sidebar() -> None:
    # inject custom CSS to set the width of the sidebar
    tools.create_side_bar_width()

    st.sidebar.title("Control Panel")

    if "load_portfolio" not in st.session_state:
        st.session_state["load_portfolio"] = False

    if "run_simulation" not in st.session_state:
        st.session_state["run_simulation"] = False

    portfo_tab, model_tab, sniff_tab = st.sidebar.tabs(["📈 Create Portfolio",
                                             "🐂 Build Risk Model",
                                             "Sniff Test"])

    # add portfolio tab components
    portfo_tab.title("Portfolio Building")
    side_bar_components.load_sidebar_dropdown_stocks(portfo_tab)
    side_bar_components.load_sidebar_stocks(portfo_tab,
                                            st.session_state.no_investment)
    st.session_state["load_portfolio"] = portfo_tab.button("Load Portfolio",
                                                           key="side_bar_load_portfolio",
                                                           on_click=tools.click_button_port)

    portfo_tab.markdown("""
        You can construct a portfolio with up to 10 investments. For each investment, kindly furnish details including the stock name, number of shares, and purchase date. 
        You're welcome to adhere to default values or tailor them to your liking.
        To simplify, the purchase price will be determined based on the closing price on the purchase date.
    """)

    # add model tab
    model_tab.title("Risk Model Building")
    side_bar_components.load_sidebar_risk_model(model_tab)
    st.session_state["run_simulation"] = model_tab.button("Run Simulation",
                                                         key="main_page_run_simulation",
                                                         on_click=tools.click_button_sim)

    model_tab.markdown("""
        :green[VaR (Value at Risk)]: Think of VaR as a safety net, indicating the 
        maximum potential loss within a confidence level, e.g., a 95% chance of not losing 
        more than $X. It prepares you for worst-case scenarios, with alpha representing the 
        confidence level (e.g., 5% -> 95% confidence).

        :green[Conditional Value at Risk)]: CVaR goes beyond, revealing expected losses 
        beyond the worst-case scenario. It's like a backup plan for extreme situations, 
        with alpha denoting the confidence level (e.g., 5% -> 95% confidence).

        :red[Why Should You Care?]: In a video game analogy, VaR is your character's maximum damage 
        tolerance, while CVaR is your backup plan with health potions. Understanding these helps you make 
        smart moves and avoid losses.
    """)

    # Add Sniff test tab
    sniff_tab.button(
        "Load KPIs",
        key="sniff_page_load_revenue",
        on_click=tools.click_button_sniff)
