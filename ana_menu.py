import streamlit as st


def run():
    
    giris = st.markdown(
        "<h4 style='color: red;'> Merhabalar bu sitedeki veriler enuygun.com web sitesi aracılığı ile elde edilmiştir. \
        Hangi sayfaya geçiş yapacağınızı yan menüden seçebilirsiniz!</h4>",
        unsafe_allow_html=True
    )
    
    st.image('https://www.arup.com/globalassets/images/services/planning/airport-planning/plane-at-an-airport-terminal-airport-planning-hero.jpg')