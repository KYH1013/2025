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

    tab1, tab2 = st.tabs(["📋 기본 정보", "🔮 사주 보기"])

    # ---------------------------
    # 기본 정보 탭
    # ---------------------------
    with tab1:
        st.subheader(f"🎂 {dob.strftime('%Y년 %m월 %d일')} 정보")
        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)

        # 탄생화
        month_day_key = f"{month:02d}-{day:02d}"
        flower = birthdata.BIRTH_FLOWERS_BY_DAY.get(month_day_key)
        with col1:
            if flower:
                st.markdown(f"""
                <div style='background:#fffaf0; padding:15px; border-radius:15px; text-align:center;'>
                    <h3>🌸 탄생화</h3>
                    <p><b>{flower['name']}</b><br>의미: {flower['meaning']}</p>
                </div>
                """, unsafe_allow_html=True)

        # 탄생석
        stone = birthdata.BIRTH_STONES.get(month)
        with col2:
            if stone:
                st.markdown(f"""
                <div style='background:#f0ffff; padding:15px; border-radius:15px; text-align:center;'>
                    <h3>💎 탄생석</h3>
                    <p><b>{stone['name']}</b><br>의미: {stone['meaning']}</p>
                </div>
                """, unsafe_allow_html=True)

        # 별자리
        sign, sign_emoji = birthdata.get_zodiac(month, day)
        with col3:
            st.markdown(f"""
            <div style='background:#f5f5f5; padding:15px; border-radius:15px; text-align:center;'>
                <h3>✨ 별자리</h3>
                <p><b>{sign}</b> {sign_emoji}</p>
            </div>
            """, unsafe_allow_html=True)

        # 띠
        chinese_zodiac = birthdata.get_chinese_zodiac(year)
        with col4:
            st.markdown(f"""
            <div style='background:#f0fff0; padding:15px; border-radius:15px; text-align:center;'>
                <h3>🐲 띠</h3>
                <p><b>{chinese_zodiac}</b></p>
            </div>
            """, unsafe_allow_html=True)

   # ---------------------------
# 사주 해석 + 오행 운세
# ---------------------------
with tab2:
    st.subheader("🔮 사주풀이 (간단)")

    gan = ["갑","을","병","정","무","기","경","신","임","계"]
    ji  = ["자","축","인","묘","진","사","오","미","신","유","술","해"]

    # 연/월/일 사주 계산
    year_gan = gan[(year - 4) % 10]
    year_ji  = ji[(year - 4) % 12]
    month_gan = gan[(month + year) % 10]
    month_ji  = ji[(month + year) % 12]
    day_gan = gan[(day + year) % 10]
    day_ji  = ji[(day + month) % 12]

    saju_text = f"{year_gan}{year_ji}년 {month_gan}{month_ji}월 {day_gan}{day_ji}일"

    st.markdown(f"""
    <div style='background:#fff0f5; padding:20px; border-radius:15px; text-align:center; box-shadow:0 4px 10px rgba(0,0,0,0.1);'>
        <h3>사주 (연/월/일)</h3>
        <p style='font-size:22px; font-weight:bold;'>{saju_text}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<h4>📌 간단 사주 해석</h4>", unsafe_allow_html=True)

    # ---------------------------
    # 오행 기반 간단 운세
    # ---------------------------
    # 예시: 연/월/일 천간의 오행 분류
    five_elements = {
        "갑": "목", "을": "목",
        "병": "화", "정": "화",
        "무": "토", "기": "토",
        "경": "금", "신": "금",
        "임": "수", "계": "수"
    }

    elements = [five_elements[year_gan], five_elements[month_gan], five_elements[day_gan]]

    # 오행 운세 해석 예시
    element_messages = {
        "목": "성장과 발전이 기대됩니다 🌱",
        "화": "열정과 활동이 중요합니다 🔥",
        "토": "안정과 신중함이 필요합니다 🌾",
        "금": "결단력과 집중력이 필요합니다 ⚔️",
        "수": "유연함과 지혜를 발휘하세요 💧"
    }

    # 각 오행 메시지 중복 제거 후 표시
    unique_messages = list({element_messages[e] for e in elements})

    st.write(" | ".join(unique_messages))

