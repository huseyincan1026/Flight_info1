import streamlit as st

import flight
import havalimani
import ana_menu
import grafik


# Sidebar menü
st.sidebar.title("Sayfalar")
page = st.sidebar.radio("Sayfa Seçimi", ('Ana Menü', "Uçuşlar", "Havalimanı", 'Grafik'))
   
# Seçilen sayfayı göster
if page == 'Ana Menü':
    ana_menu.run()
elif page == 'Uçuşlar':
    flight.run()
elif page == "Havalimanı":
    havalimani.run()
       
elif page == "Grafik":
    grafik.run()