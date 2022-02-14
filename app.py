import streamlit as stm
from predict_pg import show_predict_pg
from explore_pg import show_explore_page

page = stm.sidebar.selectbox("Explore or Predict",("Predict","Explore"))

if page =="Predict":
    show_predict_pg()
else:
    show_explore_page()