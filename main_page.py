import streamlit as st
import side_bar as comp
import stTools as tools
import default_page
import portfolio_page
import model_page
import sniff_page

st.set_page_config(
    page_title="FinRisk",
    page_icon="🦈",
    layout="wide"
)

tools.remove_white_space()

st.title("SFS Risk Management Modeling")

comp.load_sidebar()
if "load_default_page" not in st.session_state:
    st.session_state["load_default_page"] = True

if "load_portfolio_check" not in st.session_state:
    st.session_state["load_portfolio_check"] = False

if "run_simulation_check" not in st.session_state:
    st.session_state["run_simulation_check"] = False

if "load_sniff_page" not in st.session_state:
    st.session_state["load_sniff_page"] = False


if st.session_state["load_default_page"]:
    default_page.load_page()

elif not st.session_state.run_simulation_check and st.session_state.load_portfolio_check:
    portfolio_page.load_page()

elif st.session_state.run_simulation_check:
    model_page.load_page()

elif st.session_state["load_sniff_page"]:
    sniff_page.load_page()
