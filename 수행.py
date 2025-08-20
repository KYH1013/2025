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

    # 탄생화
    flower = birthdata.BIRTH_FLOWERS_BY_DAY.get(month)
    if flower:
        st.write(f"🌸 **탄생화:** {flower['name']} - {flower['meaning']}")

    # 탄생석
    stone = birthdata.BIRTH_STONES.get(month)
    if stone:
        st.write(f"💎 **탄생석:** {stone['name']} - {stone['meaning']}")

    # 별자리
    sign, sign_emoji = birthdata.get_zodiac(month, day)
    st.write(f"✨ **별자리:** {sign} {sign_emoji}")


    # 띠
    chinese_zodiac = birthdata.get_chinese_zodiac(year)
    st.write(f"🐲 **띠:** {chinese_zodiac}")

    # 월별 기념일
    month_day_key = f"{month:02d}-{day:02d}"
    holidays = birthdata.HOLIDAYS_BY_DAY.get(month_day_key, [])
    if holidays:
        st.write(f"🎉 **기념일:** {', '.join(holidays)}")
