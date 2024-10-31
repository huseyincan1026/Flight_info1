from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
import streamlit as st
import havalimani as h

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def run():
    st.header('Uçak Uçuş Bilgileri')
    
    # Havalimani Secimi 
    secim = str(st.selectbox("Bir havalimanı seçin:", h.air.airport))
    secilen_air = h.air[h.air['airport'] == secim]['airport'].values[0]
    secilen_code = h.air[h.air['airport'] == secim]['code'].values[0]
    # Tarih seçimi
    selected_date = st.date_input("Tarih Seçin", value=pd.Timestamp('today'))
    formatted_date = selected_date.strftime("%d-%m-%Y").replace('-', '.')
    
    
    # URL oluşturma
    url = f'https://www.enuygun.com/ucak-bileti/arama/{secilen_air}-ecn-ercan-intl-havalimani-{secilen_code}-ecn/?gidis={formatted_date}&yetiskin=1&sinif=ekonomi&save=1&geotrip=international&trip=international&ref=ft-homepage'
    
    # Tarayıcı ayarlarını belirleyin
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Tarayıcıyı görünmez modda çalıştırır
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')




    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    
    try:
        # Öğenin yüklenmesini bekle
        flight_items = WebDriverWait(driver, 12).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.flight-item__wrapper'))
        )
    
        # Verileri toplama
        flight_firmas = []
        flight_kalkis = []
        flight_varis = []
        flight_sure = []
        flight_fiyat = []
    
        for item in flight_items:
            flight_firmas.append(item.text.split('\n')[0])
            flight_kalkis.append(item.text.split('\n')[4])
            flight_varis.append(item.text.split('\n')[6])
            flight_sure.append(item.text.split('\n')[7])   
            flight_fiyat.append(item.text.split('\n')[8])
    
        # DataFrame oluşturma
        df = pd.DataFrame({
            'Firma': flight_firmas,
            'Kalkış': flight_kalkis,
            'Varış': flight_varis,
            'Süre': flight_sure,
            'Fiyat': flight_fiyat
        })
       
        def highlight_first_row(val):
            color = 'background-color: green'
            return [color if val.name == 0 and col == 'Fiyat' else '' for col in val.index]
    
        # Stili uygulayıp Streamlit'te göster
        styled_df = df.style.apply(highlight_first_row, axis=1)
        st.dataframe(styled_df)
    
    
    except TimeoutException:
        st.markdown(
        "<h4 style='color: red;'>Üzgünüz, bu tarih için uçuş yok ya da tüm uçuşlar dolu!</h4>",
        unsafe_allow_html=True
    )
    finally:
        driver.quit()
