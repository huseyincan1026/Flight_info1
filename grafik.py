from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
import havalimani as h

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

def run():  
    st.header('10 Günlük ✈️ Raporu')
    
    # Havalimanı seçimi
    secim = str(st.selectbox("Bir havalimanı seçin:", h.air['airport']))
    secilen_air = h.air[h.air['airport'] == secim]['airport'].values[0]
    secilen_code = h.air[h.air['airport'] == secim]['code'].values[0]

    # Tarih seçimi
    selected_date = st.date_input("Tarih Seçin", value=pd.Timestamp('today'))

    fiyatlar = []
    gunler = []
    
    # 10 gün boyunca fiyatları al
    for i in range(10):
        tarih = selected_date + timedelta(days=i)
        formatted_date = tarih.strftime("%d.%m.%Y")

        # URL oluşturma
        url = f'https://www.enuygun.com/ucak-bileti/arama/{secilen_air}-ecn-ercan-intl-havalimani-{secilen_code}-ecn/?gidis={formatted_date}&yetiskin=1&sinif=ekonomi&save=1&geotrip=international&trip=international&ref=ft-homepage'
        
        driver = webdriver.Chrome(options = options)
        driver.get(url)

        try:
            flight_items = WebDriverWait(driver, 13).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.flight-item__wrapper'))
            )
            flight_fiyat = flight_items[0].text.split('\n')[8].split(' ')[0]
            fiyatlar.append(float(flight_fiyat.replace('.','').replace(',','.')))
            gunler.append(formatted_date)
            
        except TimeoutException:
            fiyatlar.append(None)
        finally:
            driver.quit()
    
    # DataFrame Oluşturma        
    g_f = pd.DataFrame({'Date': gunler, 'Price': fiyatlar})
    g_f['Price'] = pd.to_numeric(g_f['Price'])

    # Boş fiyat verisi olmadığından emin ol
    if g_f['Price'].notna().any():
        min_price_index = g_f['Price'].idxmin()
        min_price = g_f['Price'].min()
        min_price_date = g_f.loc[min_price_index, 'Date']
    else:
        min_price_index = None
        min_price = "Veri yok"
        min_price_date = "Veri yok"

    # Tarihleri datetime formatına çevir ve sıralama işlemini uygula
    g_f['Date'] = pd.to_datetime(g_f['Date'], format="%d.%m.%Y")
    g_f = g_f.sort_values('Date')
    g_f['Date'] = g_f['Date'].dt.strftime("%d.%m.%Y")
    
    # Minimum fiyat satırını renklendirme
    def highlight(row):
        return ['background-color: green' if row.name == min_price_index else '' for _ in row]

    if min_price_index is not None:
        styled_df = g_f.style.apply(highlight, axis=1)
        st.dataframe(styled_df)
    else:
        st.dataframe(g_f)
    
    # Çizgi grafiği
    st.line_chart(g_f.set_index('Date')['Price'])
    
    # En uygun bilet bilgisi
    st.markdown(
        f"<p style='color: black; font-size: 14px; font-weight: bold;'>En uygun bilet {min_price_date} tarihli {min_price} TL fiyatlı bilettir.</p>",
        unsafe_allow_html=True
    )

# Streamlit uygulamanızı çalıştırmak için
if __name__ == "__main__":
    run()
