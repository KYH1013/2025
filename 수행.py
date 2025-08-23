import streamlit as st
import birthdata
from datetime import datetime

st.set_page_config(page_title="생일 정보 확인", layout="centered")
st.title("🎉 나의 생일 정보 확인 웹사이트")

# 카드 스타일 (CSS)
st.markdown("""
    <style>
    .card {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .card h3 {
        margin: 0 0 10px 0;
        font-size: 20px;
        color: #333333;
    }
    .card p {
        margin: 0;
        font-size: 16px;
        color: #555555;
    }
    </style>
""", unsafe_allow_html=True)

dob = st.date_input("생년월일을 선택하세요", datetime(2000, 1, 1))

if dob:
    month = dob.month
    day = dob.day
    year = dob.year

    st.subheader(f"🎂 {dob.strftime('%Y년 %m월 %d일')} 정보")

    # 탄생화
    month_day_key = f"{month:02d}-{day:02d}"
    flower = birthdata.BIRTH_FLOWERS_BY_DAY.get(month_day_key)
    if flower:
        st.markdown(f"""
        <div class="card">
            <h3>🌸 탄생화</h3>
            <p>{flower['name']} - {flower['meaning']}</p>
        </div>
        """, unsafe_allow_html=True)

    # 탄생석
    stone = birthdata.BIRTH_STONES.get(month)
    if stone:
        st.markdown(f"""
        <div class="card">
            <h3>💎 탄생석</h3>
            <p>{stone['name']} - {stone['meaning']}</p>
        </div>
        """, unsafe_allow_html=True)

    # 별자리
    sign, sign_emoji = birthdata.get_zodiac(month, day)
    st.markdown(f"""
    <div class="card">
        <h3>✨ 별자리</h3>
        <p>{sign} {sign_emoji}</p>
    </div>
    """, unsafe_allow_html=True)

    # 띠
    chinese_zodiac = birthdata.get_chinese_zodiac(year)
    st.markdown(f"""
    <div class="card">
        <h3>🐲 띠</h3>
        <p>{chinese_zodiac}</p>
    </div>
    """, unsafe_allow_html=True)

    # 기념일
    holidays = birthdata.HOLIDAYS_BY_DAY.get(month_day_key, [])
    if holidays:
        st.markdown(f"""
        <div class="card">
            <h3>🎉 기념일</h3>
            <p>{', '.join(holidays)}</p>
        </div>
        """, unsafe_allow_html=True)
