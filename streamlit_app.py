import streamlit as st
import pandas as pd

st.title('The efficacy of molnupiravir as a first-line drug for short-term management of effusive form feline infectious peritonitis: a case series')

df = pd.read_csv("https://raw.githubusercontent.com/chphuttipan/data/main/mu_fip_project2.csv")

st.write(
    "Hello!, This is the web app to express a data visualization about this project"
)


