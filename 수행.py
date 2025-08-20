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
    with st.expander("🌸 탄생화 & 💎 탄생석"):
        flower = birthdata.BIRTH_FLOWERS.get(month)
        if flower:
            st.markdown(f"**🌸 탄생화:** {flower['name']} - {flower['meaning']}")
        stone = birthdata.BIRTH_STONES.get(month)
        if stone:
            st.markdown(f"**💎 탄생석:** {stone['name']} - {stone['meaning']}")

    with st.expander("✨ 별자리"):
        sign, sign_emoji = birthdata.get_zodiac(month, day)
        st.markdown(f"**{sign_emoji} 별자리:** {sign}")

    with st.expander("🐲 띠"):
        chinese_zodiac = birthdata.get_chinese_zodiac(year)
        st.markdown(f"**띠:** {chinese_zodiac}")

    with st.expander("🎉 기념일"):
        month_day_key = f"{month:02d}-{day:02d}"
        holidays = birthdata.HOLIDAYS_BY_DAY.get(month_day_key, [])
        if holidays:
            st.markdown(f"{', '.join(holidays)}")
        else:
            st.markdown("없음")
