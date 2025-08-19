import streamlit as st
import time
from datetime import datetime
import birthdata  # 탄생화, 탄생석, 별자리, 띠, 세계 기념일 데이터

st.set_page_config(page_title="Birthdate Insights", page_icon="🌸", layout="centered")

st.title("🎂 Birthdate Insights")
st.write("생년월일을 입력하면 탄생화, 탄생석, 별자리, 띠, 세계 기념일 정보를 알려줍니다.")

# --- 사용자 입력 ---
birth_date = st.date_input("생년월일을 선택하세요", value=None)

if birth_date:
    with st.spinner("🔮 당신의 생일을 분석하는 중... 잠시만 기다려주세요..."):
        time.sleep(2)  # 로딩 효과 (2초)

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
        return "염소자리 (Capricorn)"

    # 별자리 이모지 맵
    ZODIAC_EMOJI = {
        "물병자리 (Aquarius)": "♒️ 💧",
        "물고기자리 (Pisces)": "♓️ 🐟",
        "양자리 (Aries)": "♈️ 🐑",
        "황소자리 (Taurus)": "♉️ 🐂",
        "쌍둥이자리 (Gemini)": "♊️ 👯",
        "게자리 (Cancer)": "♋️ 🦀",
        "사자자리 (Leo)": "♌️ 🦁",
        "처녀자리 (Virgo)": "♍️ 🌾",
        "천칭자리 (Libra)": "♎️ ⚖️",
        "전갈자리 (Scorpio)": "♏️ 🦂",
        "사수자리 (Sagittarius)": "♐️ 🏹",
        "염소자리 (Capricorn)": "♑️ 🐐",
    }

    def get_zodiac_animal(year: int):
        return birthdata.ZODIAC_ANIMALS[year % 12]

    # 띠 이모지 맵
    ZODIAC_ANIMAL_EMOJI = {
        "쥐": "🐀",
        "소": "🐂",
        "호랑이": "🐅",
        "토끼": "🐇",
        "용": "🐉",
        "뱀": "🐍",
        "말": "🐎",
        "양": "🐑",
        "원숭이": "🐒",
        "닭": "🐓",
        "개": "🐕",
        "돼지": "🐖",
    }

    def get_world_days(month: int, day: int):
        key = f"{month:02d}-{day:02d}"
        return birthdata.WORLD_DAYS.get(key, [])

    # ---------------------------
    # 출력 영역
    # ---------------------------
    st.success("✨ 당신의 생일 정보가 준비되었습니다!")

    # 탄생화
    st.subheader(f"🌸 {month}월 {day}일의 탄생화는?")
    flower = get_birth_flower(month, day)
    if flower:
        st.write(f"**{flower['name']}** — {flower['meaning']}")
    else:
        st.write("해당 날짜의 탄생화 정보가 없습니다.")

    # 탄생석
    st.subheader(f"💎 {month}월의 탄생석은?")
    stone = get_birthstone(month)
    if stone:
        st.write(f"**{stone['name']}** — {stone['meaning']}")
    else:
        st.write("해당 월의 탄생석 정보가 없습니다.")

    # 별자리
    st.subheader("✨ 당신의 별자리는?")
    zodiac = get_zodiac_sign(month, day)
    emoji = ZODIAC_EMOJI.get(zodiac, "")
    st.write(f"{zodiac} {emoji}")

    # 띠
    st.subheader("🐲 나는 무슨 띠?")
    animal = get_zodiac_animal(year)
    animal_emoji = ZODIAC_ANIMAL_EMOJI.get(animal, "")
    st.write(f"{animal}띠 {animal_emoji}")

    # 세계 기념일
    st.subheader(f"🌍 {month}월 {day}일의 세계 기념일은?")
    days = get_world_days(month, day)
    if days:
        for d in days:
            st.write(f"- {d}")
    else:
        st.write("이 날짜에 등록된 세계 기념일이 없습니다.")
