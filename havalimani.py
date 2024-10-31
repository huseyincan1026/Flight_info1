import streamlit as st
import pandas as pd

data = [['istanbul', 'ist', 'istanbul-havalimani'],
        ['istanbul', 'saw', 'istanbul-sabiha-gokcen-havalimani'],
        ['ankara', 'esb', 'esenboga-havalimani'],
        ['izmir', 'adb', 'adnan-menderes-havalimani']]

air = pd.DataFrame(data, columns = ['city', 'code', 'airport'])
def run():
    st.dataframe(air)