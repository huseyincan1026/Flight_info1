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
options.add_argument('--headless')  # Tarayıcıyı görünmez modda çalıştırır
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

def run():  
    st.header('10 Gun Raporu')
    
    # Havalimanı seçimi
    secim = str(st.selectbox("Bir havalimanı seçin:", h.air['airport']))
    secilen_air = h.air[h.air['airport'] == secim]['airport'].values[0]
    secilen_code = h.air[h.air['airport'] == secim]['code'].values[0]

    # Tarih seçimi
    selected_date = st.date_input("Tarih Seçin", value=pd.Timestamp('today'))

    fiyatlar = []  # Fiyatları saklamak için boş bir liste oluştur
    gunler = []
    # 10 gün boyunca fiyatları al
    for i in range(5):
        tarih = selected_date + timedelta(days=i)  # Her gün için tarihi hesapla
        formatted_date = tarih.strftime("%d-%m-%Y").replace('-', '.')  # Tarihi formatla

        # URL oluşturma
        url = f'https://www.enuygun.com/ucak-bileti/arama/{secilen_air}-ecn-ercan-intl-havalimani-{secilen_code}-ecn/?gidis={formatted_date}&yetiskin=1&sinif=ekonomi&save=1&geotrip=international&trip=international&ref=ft-homepage'
        
        # Tarayıcıyı başlat
        driver = webdriver.Chrome(options = options)
        driver.get(url)

        try:
            # Fiyat bilgilerini almak için bekleyin
            flight_items = WebDriverWait(driver, 13).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.flight-item__wrapper'))
            )

            # İlk fiyatı al
            flight_fiyat = flight_items[0].text.split('\n')[8].split(' ')[0]  # İlk uçuşun fiyatı
            fiyatlar.append(float(flight_fiyat.replace('.','').replace(',','.')))
            gunler.append(formatted_date)
            
        except TimeoutException:
            fiyatlar.append(None)  # Eğer fiyat alınamazsa None ekle
        finally:
            driver.quit()  # Tarayıcıyı kapat
    
    # DataFrame Olusurma        
    g_f = pd.DataFrame({'Date' : gunler,
                        'Price' :fiyatlar})
    
    # Olusturulan DF icerisindeki price degerlerini sayisal hale donustur
    g_f['Price'] = pd.to_numeric(g_f['Price'])
    
    # En dusuk fiyatin oldugu id bulalim
    min_price_index = g_f['Price'].idxmin()
    min_price = g_f['Price'].min()
    min_price_date = g_f.loc[g_f['Price'].idxmin(), 'Date']
    
    #  date verilerimizi datetime'a donusturelim
    g_f['Date'] = g_f['Date'].astype(str)
    g_f['Date'] = pd.to_datetime(g_f['Date']).dt.strftime("%d-%m-%Y")
    
    styled_df = g_f
    styled_df['Date']= pd.to_datetime(styled_df['Date']).dt.strftime("%d-%m-%Y")
    
    # Satir Stilini uygulama fonk olusturalim
    def highlight(row):
       return ['background-color: green' if row.name == min_price_index else '' for _ in row]

    styled_df = styled_df.style.apply(highlight, axis=1)

    
    st.dataframe(styled_df) # dataframe'in ciktisini alalim
  
    # Cizgi grafigi olustturalim
    st.line_chart(styled_df, x = 'Date', y= 'Price')      
    
    # en uygun biletin hangi gun oldugunu ve fiyatini yazdiralim
    st.markdown(f"<p style='color: black; font-size: 14px; font-weight: bold;'> En uygun bilet {min_price_date} tarihli {min_price} TL fiyatlı bilettir. Bilet ayrıntılarını görüntülemek isterseniz menüden Uçuşlar sayfasına geçiş yapabilirsiniz. 😊</p>", unsafe_allow_html=True)

# Streamlit uygulamanızı çalıştırmak için bu fonksiyonu çağırın
if __name__ == "__main__":
    run()