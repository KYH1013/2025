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
    # 사주 보기 탭
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

        # ---------------------------
        # 사주 해석 (예시)
        # ---------------------------
        st.markdown("<h4>📌 간단 사주 해석</h4>", unsafe_allow_html=True)

        # 예시: 연/월/일 오행 조합 기반 간단 성향
        # 실제 사주풀이보다 단순 요약용
        interpretations = []
        if year_gan in ["갑","을"]: interpretations.append("총명하고 지도력이 있음")
        if month_gan in ["병","정"]: interpretations.append("활발하고 외향적임")
        if day_gan in ["무","기"]: interpretations.append("신중하고 조심스러움")

        if not interpretations:
            interpretations.append("평범하고 안정적인 성향")

        st.write(" | ".join(interpretations))
