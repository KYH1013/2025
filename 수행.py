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

    # 카드형 정보
    with st.container():
        st.markdown(
            f"""
            <div style="background-color:white; padding:20px; border-radius:10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);">
                <!-- 탄생석 -->
                <h3>💎 탄생석</h3>
                <p>{birthdata.BIRTH_STONES.get(month, {{'name':'정보 없음','meaning':''}})['name']} - {birthdata.BIRTH_STONES.get(month, {{'name':'정보 없음','meaning':''}})['meaning']}</p>
                <hr>
                <!-- 별자리 -->
                <h3>✨ 별자리</h3>
                <p>{birthdata.get_zodiac(month, day)[0]} {birthdata.get_zodiac(month, day)[1]}</p>
                <hr>
                <!-- 띠 -->
                <h3>🐲 띠</h3>
                <p>{birthdata.get_chinese_zodiac(year)}</p>
                <hr>
                <!-- 월별 기념일 -->
                <h3>🎉 기념일</h3>
                <p>{', '.join(birthdata.HOLIDAYS_BY_DAY.get(f"{month:02d}-{day:02d}", [])) or '없음'}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
