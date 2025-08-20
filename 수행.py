import streamlit as st
import birthdata
from datetime import datetime

st.set_page_config(page_title="생일 정보 확인", layout="centered")
st.title("🎉 나의 생일 정보 확인 웹사이트")

dob = st.date_input("생년월일을 선택하세요", datetime(2000,1,1))

if dob:
    month = dob.month
    day = dob.day
    year = dob.year

    st.subheader(f"🎂 {dob.strftime('%Y년 %m월 %d일')} 정보")

    # 카드 컨테이너
    with st.container():
        st.markdown(
            f"""
            <div style="background-color:white; padding:20px; border-radius:10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);">
                <h3>🌸 탄생화</h3>
                <p>{birthdata.BIRTH_FLOWERS.get(month)['name']} - {birthdata.BIRTH_FLOWERS.get(month)['meaning']}</p>
                <hr>
                <h3>💎 탄생석</h3>
                <p>{birthdata.BIRTH_STONES.get(month)['name']} - {birthdata.BIRTH_STONES.get(month)['meaning']}</p>
                <hr>
                <h3>✨ 별자리</h3>
                <p>{birthdata.get_zodiac(month, day)[0]} {birthdata.get_zodiac(month, day)[1]}</p>
                <hr>
                <h3>🐲 띠</h3>
                <p>{birthdata.get_chinese_zodiac(year)}</p>
                <hr>
                <h3>🎉 기념일</h3>
                <p>{', '.join(birthdata.HOLIDAYS_BY_DAY.get(f"{month:02d}-{day:02d}", []))}</p>
            </div>
            """, unsafe_allow_html=True
        )
