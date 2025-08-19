import streamlit as st
import time
from datetime import datetime
import birthdata

st.set_page_config(page_title="🎉 Birthday Insights", page_icon="🎂", layout="wide")

st.title("🎂 Birthday Insights")
st.markdown(
    "생년월일을 선택하면 **탄생화, 탄생석, 별자리, 띠, 세계 기념일**을 재미있게 보여드립니다! 🌈"
)

birth_date = st.date_input("생년월일을 선택하세요", value=None)

if birth_date:
    with st.spinner("🔮 잠시만요, 생일 정보를 불러오는 중..."):
        time.sleep(1.5)

    month, day, year = birth_date.month, birth_date.day, birth_date.year

    # --- 데이터 조회 함수 ---
    def get_birth_flower(month, day):
        return birthdata.BIRTH_FLOWERS_BY_DAY.get(f"{month:02d}-{day:02d}", None)

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

    # 60간지 계산
    tian_gan = ['갑','을','병','정','무','기','경','신','임','계']
    di_zhi = ['자','축','인','묘','진','사','오','미','신','유','술','해']
    colors_by_tian_gan = {'갑':'푸른','을':'푸른','병':'붉은','정':'붉은',
                          '무':'황금','기':'황금','경':'흰','신':'흰','임':'검은','계':'검은'}
    animals_by_di_zhi = {'자':'쥐','축':'소','인':'호랑이','묘':'토끼','진':'용','사':'뱀',
                         '오':'말','미':'양','신':'원숭이','유':'닭','술':'개','해':'돼지'}
    emojis_by_animal = {'쥐':'🐀','소':'🐂','호랑이':'🐅','토끼':'🐇','용':'🐉','뱀':'🐍',
                        '말':'🐎','양':'🐑','원숭이':'🐒','닭':'🐓','개':'🐕','돼지':'🐖'}

    tg_index = (year-4)%10
    dz_index = (year-4)%12
    tg = tian_gan[tg_index]
    dz = di_zhi[dz_index]
    animal = animals_by_di_zhi[dz]
    animal_emoji = emojis_by_animal[animal]
    color_name = colors_by_tian_gan[tg]

    def get_world_days(month, day):
        return birthdata.WORLD_DAYS.get(f"{month:02d}-{day:02d}", [])

    st.success("✨ 분석 완료! 당신의 생일 정보입니다.")

    # ---------------- 카드 스타일 ----------------
    card_style = ("padding:20px; border-radius:15px; "
                  "border:1px solid #ddd; box-shadow:3px 3px 10px rgba(0,0,0,0.1); "
                  "margin-bottom:15px; min-height:120px; background-color:#fafafa;")

    # ---------------- 왼쪽, 오른쪽 컬럼 ----------------
    col1, col2 = st.columns(2)

    # ---------------- 탄생화 ----------------
    flower = get_birth_flower(month, day)
    with col1:
        if flower:
            st.markdown(f"""
            <div style="{card_style}">
                <h3>🌸 {month}월 {day}일 탄생화</h3>
                <p style="font-size:18px;"><b>{flower['name']}</b> — {flower['meaning']}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("해당 날짜의 탄생화 정보가 없습니다.")

    # ---------------- 탄생석 ----------------
        stone = get_birthstone(month)
        if stone:
            st.markdown(f"""
            <div style="{card_style}">
                <h3>💎 {month}월 탄생석</h3>
                <p style="font-size:18px;"><b>{stone['name']}</b> — {stone['meaning']}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("해당 월의 탄생석 정보가 없습니다.")

    # ---------------- 별자리 ----------------
    zodiac = get_zodiac_sign(month, day)
    zodiac_emoji = ZODIAC_EMOJI.get(zodiac, "")
    with col2:
        st.markdown(f"""
        <div style="{card_style}; text-align:center; background-color:#E0F7FA;">
            <h3>✨ 별자리</h3>
            <p style="font-size:20px;">{zodiac} {zodiac_emoji}</p>
        </div>
        """ , unsafe_allow_html=True)

    # ---------------- 띠 ----------------
        st.markdown(f"""
        <div style="{card_style}; text-align:center; background-color:#FFF3E0;">
            <h3>🐲 나는 무슨 띠?</h3>
            <p style="font-size:20px;">{color_name} {animal}띠 {animal_emoji}</p>
        </div>
        """ , unsafe_allow_html=True)

    # ---------------- 세계 기념일 ----------------
    days = get_world_days(month, day)
    st.markdown("### 🌍 세계 기념일")
    if days:
        st.markdown("<div style='display:flex; flex-wrap:wrap;'>", unsafe_allow_html=True)
        for d in days:
            st.markdown(f"""
            <div style="margin:5px; padding:15px; border-radius:10px; border:1px solid #ccc; 
                        min-height:60px; background-color:#FFF9C4; flex:1;">
                {d}
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("이 날짜에 등록된 세계 기념일이 없습니다.")
