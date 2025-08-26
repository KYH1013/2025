st.cache_data.clear()
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

    # 탭 UI 생성
    tab1, tab2 = st.tabs(["📋 기본 정보", "🔮 사주 보기"])

    with tab1:
        st.subheader(f"🎂 {dob.strftime('%Y년 %m월 %d일')} 정보")

        col1, col2 = st.columns(2)

        with col1:
            # 탄생화
            month_day_key = f"{month:02d}-{day:02d}"
            flower = birthdata.BIRTH_FLOWERS_BY_DAY.get(month_day_key)
            if flower:
                st.markdown(f"""
                <div style='background:#fffaf0; padding:15px; border-radius:15px; text-align:center;'>
                    <h3>🌸 탄생화</h3>
                    <p><b>{flower['name']}</b><br>의미: {flower['meaning']}</p>
                </div>
                """, unsafe_allow_html=True)

            # 탄생석
            stone = birthdata.BIRTH_STONES.get(month)
            if stone:
                st.markdown(f"""
                <div style='background:#f0ffff; padding:15px; border-radius:15px; text-align:center;'>
                    <h3>💎 탄생석</h3>
                    <p><b>{stone['name']}</b><br>의미: {stone['meaning']}</p>
                </div>
                """, unsafe_allow_html=True)

        with col2:
            # 별자리
            sign, sign_emoji = birthdata.get_zodiac(month, day)
            st.markdown(f"""
            <div style='background:#f5f5f5; padding:15px; border-radius:15px; text-align:center;'>
                <h3>✨ 별자리</h3>
                <p><b>{sign}</b> {sign_emoji}</p>
            </div>
            """, unsafe_allow_html=True)

            # 띠
            chinese_zodiac = birthdata.get_chinese_zodiac(year)
            st.markdown(f"""
            <div style='background:#f0fff0; padding:15px; border-radius:15px; text-align:center;'>
                <h3>🐲 띠</h3>
                <p><b>{chinese_zodiac}</b></p>
            </div>
            """, unsafe_allow_html=True)

        with tab2:
            st.subheader("🔮 사주 풀이 (생시 제외)")

            # 사주 예시 (연월일만 사용)
            gan = ["갑", "을", "병", "정", "무", "기", "경", "신", "임", "계"]
            ji = ["자", "축", "인", "묘", "진", "사", "오", "미", "신", "유", "술", "해"]

            year_gan = gan[(year - 4) % 10]
            year_ji = ji[(year - 4) % 12]
            month_gan = gan[(month + year) % 10]
            month_ji = ji[(month + year) % 12]
            day_gan = gan[(day + year) % 10]
            day_ji = ji[(day + month) % 12]

            st.markdown(f"""
            <div style='background:#fff0f5; padding:20px; border-radius:15px; text-align:center;'>
                <h3>사주 (연/월/일)</h3>
                <p><b>{year_gan}{year_ji}년 {month_gan}{month_ji}월 {day_gan}{day_ji}일</b></p>
                <p style='color:gray;'>※ 간단한 사주 해석 (생시는 제외됨)</p>
            </div>
            """, unsafe_allow_html=True)
