import streamlit as st
import time
from datetime import datetime
import birthdata

st.set_page_config(page_title="🎉 Birthday Insights", page_icon="🎂", layout="wide")

st.title("🎂 Birthday Insights")
st.markdown(
    "생년월일을 선택하면 당신의 **탄생화, 탄생석, 별자리, 띠, 세계 기념일**을 알려드립니다!"
)

# --- 입력 ---
birth_date = st.date_input("생년월일을 선택하세요", value=None)

if birth_date:
    with st.spinner("🔮 잠시만요, 생일을 분석하는 중입니다..."):
        time.sleep(2)

    month, day, year = birth_date.month, birth_date.day, birth_date.year

    # --- 헬퍼 ---
    def get_birth_flower(month, day):
        key = f"{month:02d}-{day:02d}"
        return birthdata.BIRTH_FLOWERS_BY_DAY.get(key, None)

    def get_birthstone(month):
        return birthdata.BIRTHSTONES.get(month, None)

    def get_zodiac_sign(month, day):
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

    def get_zodiac_animal(year):
        return birthdata.ZODIAC_ANIMALS[year % 12]

    ZODIAC_ANIMAL_EMOJI = {
        "쥐": "🐀", "소": "🐂", "호랑이": "🐅", "토끼": "🐇", "용": "🐉",
        "뱀": "🐍", "말": "🐎", "양": "🐑", "원숭이": "🐒", "닭": "🐓",
        "개": "🐕", "돼지": "🐖",
    }

    def get_world_days(month, day):
        key = f"{month:02d}-{day:02d}"
        return birthdata.WORLD_DAYS.get(key, [])

    st.success("✨ 분석 완료! 당신의 생일 정보입니다.")

    # --- 2열 레이아웃 ---
    col1, col2 = st.columns(2)

    # 탄생화 & 탄생석
    with col1:
        st.markdown("### 🌸 탄생화")
        flower = get_birth_flower(month, day)
        if flower:
            st.markdown(f"""
            <div style="padding:15px; border-radius:10px; border:1px solid #ccc;">
                <h4>{month}월 {day}일의 탄생화</h4>
                <p><b>{flower['name']}</b> — {flower['meaning']}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("해당 날짜의 탄생화 정보가 없습니다.")

        st.markdown("### 💎 탄생석")
        stone = get_birthstone(month)
        if stone:
            st.markdown(f"""
            <div style="padding:15px; border-radius:10px; border:1px solid #ccc;">
                <h4>{month}월의 탄생석</h4>
                <p><b>{stone['name']}</b> — {stone['meaning']}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("해당 월의 탄생석 정보가 없습니다.")

    # 별자리 & 띠
    with col2:
        st.markdown("### ✨ 별자리")
        zodiac = get_zodiac_sign(month, day)
        emoji = ZODIAC_EMOJI.get(zodiac, "")
        st.markdown(f"""
        <div style="padding:15px; border-radius:10px; border:1px solid #ccc;">
            <h4>{zodiac} {emoji}</h4>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 🐲 나는 무슨 띠?")
        animal = get_zodiac_animal(year)
        animal_emoji = ZODIAC_ANIMAL_EMOJI.get(animal, "")
        st.markdown(f"""
        <div style="padding:15px; border-radius:10px; border:1px solid #ccc;">
            <h4>{animal}띠 {animal_emoji}</h4>
        </div>
        """, unsafe_allow_html=True)

    # 세계 기념일
    st.markdown("### 🌍 세계 기념일")
    days = get_world_days(month, day)
    if days:
        st.markdown("<div style='display:flex; flex-wrap:wrap;'>", unsafe_allow_html=True)
        for d in days:
            st.markdown(f"""
            <div style="margin:5px; padding:10px; border-radius:8px; border:1px solid #ccc;">
                {d}
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("이 날짜에 등록된 세계 기념일이 없습니다.")
