import streamlit as st
import time
from datetime import datetime
import birthdata

st.set_page_config(page_title="🎉 Birthday Insights", page_icon="🎂", layout="wide")

st.title("🎂 Birthday Insights")
st.markdown(
    "생년월일을 선택하면 당신의 **탄생화, 탄생석, 별자리, 띠(연도별 색상), 세계 기념일**을 알려드립니다!"
)

birth_date = st.date_input("생년월일을 선택하세요", value=None)

if birth_date:
    with st.spinner("🔮 잠시만요, 생일을 분석하는 중입니다..."):
        time.sleep(2)

    month, day, year = birth_date.month, birth_date.day, birth_date.year

    # --- 탄생화, 탄생석 ---
    def get_birth_flower(month, day):
        key = f"{month:02d}-{day:02d}"
        return birthdata.BIRTH_FLOWERS_BY_DAY.get(key, None)

    def get_birthstone(month):
        return birthdata.BIRTHSTONES.get(month, None)

    # --- 별자리 ---
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

    # --- 60간지 계산 ---
    tian_gan = ['갑', '을', '병', '정', '무', '기', '경', '신', '임', '계']
    di_zhi = ['자', '축', '인', '묘', '진', '사', '오', '미', '신', '유', '술', '해']
    colors_by_tian_gan = {
        '갑':'푸른', '을':'푸른',  # 청색
        '병':'붉은', '정':'붉은',  # 적색
        '무':'황금', '기':'황금',    # 황색
        '경':'흰', '신':'흰',      # 백색
        '임':'검은', '계':'검은',  # 흑색
    }
    animals_by_di_zhi = {
        '자':'쥐','축':'소','인':'호랑이','묘':'토끼','진':'용','사':'뱀',
        '오':'말','미':'양','신':'원숭이','유':'닭','술':'개','해':'돼지'
    }
    emojis_by_animal = {
        '쥐':'🐀','소':'🐂','호랑이':'🐅','토끼':'🐇','용':'🐉','뱀':'🐍',
        '말':'🐎','양':'🐑','원숭이':'🐒','닭':'🐓','개':'🐕','돼지':'🐖'
    }

    # 천간과 지지 계산
    tg_index = (year - 4) % 10
    dz_index = (year - 4) % 12
    tg = tian_gan[tg_index]
    dz = di_zhi[dz_index]
    animal = animals_by_di_zhi[dz]
    animal_emoji = emojis_by_animal[animal]
    color_name = colors_by_tian_gan[tg]

    # --- 세계 기념일 ---
    def get_world_days(month, day):
        key = f"{month:02d}-{day:02d}"
        return birthdata.WORLD_DAYS.get(key, [])

    st.success("✨ 분석 완료! 당신의 생일 정보입니다.")

    # ----------------------------
    # 탄생화
    # ----------------------------
    flower = get_birth_flower(month, day)
    if flower:
        with st.expander(f"🌸 {month}월 {day}일의 탄생화 보기"):
            st.write(f"**{flower['name']}** — {flower['meaning']}")
    else:
        st.info("해당 날짜의 탄생화 정보가 없습니다.")

    # ----------------------------
    # 탄생석
    # ----------------------------
    stone = get_birthstone(month)
    if stone:
        with st.expander(f"💎 {month}월의 탄생석 보기"):
            st.write(f"**{stone['name']}** — {stone['meaning']}")
    else:
        st.info("해당 월의 탄생석 정보가 없습니다.")

    # ----------------------------
    # 별자리
    # ----------------------------
    zodiac = get_zodiac_sign(month, day)
    emoji = ZODIAC_EMOJI.get(zodiac, "")
    with st.expander(f"✨ 별자리 보기"):
        st.write(f"{zodiac} {emoji}")

    # ----------------------------
    # 띠
    # ----------------------------
    with st.expander("🐲 나는 무슨 띠?"):
        st.write(f"{color_name} {animal}띠 {animal_emoji}")

    # ----------------------------
    # 세계 기념일
    # ----------------------------
    days = get_world_days(month, day)
    if days:
        with st.expander("🌍 세계 기념일 보기"):
            for d in days:
                st.write(f"- {d}")
    else:
        st.info("이 날짜에 등록된 세계 기념일이 없습니다.")
