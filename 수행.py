import streamlit as st
import time
from datetime import datetime
import birthdata

st.set_page_config(page_title="Birthdate Insights", page_icon="🌸", layout="centered")

st.title("🎂 Birthdate Insights")
st.write("생년월일을 입력하면 탄생화, 탄생석, 별자리, 띠, 세계 기념일 정보를 알려줍니다.")

# --- 사용자 입력 ---
birth_date = st.date_input("생년월일을 선택하세요", value=None)

if birth_date:
    with st.spinner("🔮 당신의 생일을 분석하는 중... 잠시만 기다려주세요..."):
        time.sleep(2)

    month = birth_date.month
    day = birth_date.day
    year = birth_date.year

    # ---------------------------
    # 헬퍼
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

    ZODIAC_EMOJI = {
        "물병자리 (Aquarius)": "♒️ 💧", "물고기자리 (Pisces)": "♓️ 🐟",
        "양자리 (Aries)": "♈️ 🐑", "황소자리 (Taurus)": "♉️ 🐂",
        "쌍둥이자리 (Gemini)": "♊️ 👯", "게자리 (Cancer)": "♋️ 🦀",
        "사자자리 (Leo)": "♌️ 🦁", "처녀자리 (Virgo)": "♍️ 🌾",
        "천칭자리 (Libra)": "♎️ ⚖️", "전갈자리 (Scorpio)": "♏️ 🦂",
        "사수자리 (Sagittarius)": "♐️ 🏹", "염소자리 (Capricorn)": "♑️ 🐐",
    }

    def get_zodiac_animal(year: int):
        return birthdata.ZODIAC_ANIMALS[year % 12]

    ZODIAC_ANIMAL_EMOJI = {
        "쥐": "🐀", "소": "🐂", "호랑이": "🐅", "토끼": "🐇", "용": "🐉",
        "뱀": "🐍", "말": "🐎", "양": "🐑", "원숭이": "🐒", "닭": "🐓",
        "개": "🐕", "돼지": "🐖",
    }

    def get_world_days(month: int, day: int):
        key = f"{month:02d}-{day:02d}"
        return birthdata.WORLD_DAYS.get(key, [])

    # ---------------------------
    # 출력 영역 (카드형)
    # ---------------------------
    st.success("✨ 당신의 생일 정보가 준비되었습니다!")

    # 탄생화 카드
    flower = get_birth_flower(month, day)
    if flower:
        st.markdown(f"""
        <div style="background-color:#ffe4e1; padding:15px; border-radius:10px;">
            <h3>🌸 {month}월 {day}일의 탄생화</h3>
            <p><b>{flower['name']}</b> — {flower['meaning']}</p>
        </div>
        """, unsafe_allow_html=True)

    # 탄생석 카드
    stone = get_birthstone(month)
    if stone:
        st.markdown(f"""
        <div style="background-color:#e0ffff; padding:15px; border-radius:10px;">
            <h3>💎 {month}월의 탄생석</h3>
            <p><b>{stone['name']}</b> — {stone['meaning']}</p>
        </div>
        """, unsafe_allow_html=True)

    # 별자리 카드
    zodiac = get_zodiac_sign(month, day)
    emoji = ZODIAC_EMOJI.get(zodiac, "")
    st.markdown(f"""
    <div style="background-color:#f0e68c; padding:15px; border-radius:10px;">
        <h3>✨ 당신의 별자리</h3>
        <p>{zodiac} {emoji}</p>
    </div>
    """, unsafe_allow_html=True)

    # 띠 카드
    animal = get_zodiac_animal(year)
    animal_emoji = ZODIAC_ANIMAL_EMOJI.get(animal, "")
    st.markdown(f"""
    <div style="background-color:#d8bfd8; padding:15px; border-radius:10px;">
        <h3>🐲 나는 무슨 띠?</h3>
        <p>{animal}띠 {animal_emoji}</p>
    </div>
    """, unsafe_allow_html=True)

    # 세계 기념일 카드
    days = get_world_days(month, day)
    if days:
        day_list = "<br>".join([f"- {d}" for d in days])
        st.markdown(f"""
        <div style="background-color:#f5f5dc; padding:15px; border-radius:10px;">
            <h3>🌍 {month}월 {day}일의 세계 기념일</h3>
            <p>{day_list}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="background-color:#f5f5dc; padding:15px; border-radius:10px;">
            <h3>🌍 {month}월 {day}일의 세계 기념일</h3>
            <p>이 날짜에 등록된 세계 기념일이 없습니다.</p>
        </div>
        """, unsafe_allow_html=True)
