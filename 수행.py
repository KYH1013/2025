import streamlit as st
import time
from datetime import datetime
import birthdata  # 별도의 데이터 파일

st.set_page_config(page_title="Birthdate Insights", page_icon="🌸", layout="centered")

st.title("🎂 Birthdate Insights")
st.write("생년월일을 입력하면 탄생화, 탄생석, 별자리, 간단 사주, 세계 기념일 정보를 알려줍니다.")

# --- 사용자 입력 ---
birth_date = st.date_input("생년월일을 선택하세요", value=None)

if birth_date:
    with st.spinner("🔮 운명을 점치는 중... 잠시만 기다려주세요..."):
        time.sleep(2)  # 로딩 효과 (2초)

    # 날짜 분리
    month = birth_date.month
    day = birth_date.day
    year = birth_date.year

    # ---------------------------
    # Helper functions
    # ---------------------------
    def get_birth_flower(month: int, day: int):
        key = f"{month:02d}-{day:02d}"
        return birthdata.BIRTH_FLOWERS_BY_DAY.get(key, None)

    def get_birthstone(month: int):
        return birthdata.BIRTHSTONES.get(month, None)

    def get_zodiac_sign(month: int, day: int):
        for sign, (start, end) in birthdata.ZODIAC_SIGNS.items():
            if (month, day) >= start and (month, day) <= end:
                return sign
        return "염소자리 (Capricorn)"  # 12/22~1/19 범위 처리

    def get_simple_saju(year: int):
        gan = birthdata.HEAVENLY_STEMS[year % 10]
        ji = birthdata.EARTHLY_BRANCHES[year % 12]
        zodiac = birthdata.ZODIAC_ANIMALS[year % 12]
        return f"{gan}{ji}년 ({zodiac}띠)"

    def get_world_days(month: int, day: int):
        key = f"{month:02d}-{day:02d}"
        return birthdata.WORLD_DAYS.get(key, [])

    # ---------------------------
    # 출력 영역
    # ---------------------------
    st.success("✨ 당신의 생일 정보가 준비되었습니다!")

    st.subheader("🌸 탄생화")
    flower = get_birth_flower(month, day)
    if flower:
        st.write(f"
