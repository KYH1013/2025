import streamlit as st
import birthdata
from datetime import datetime

st.set_page_config(page_title="생일 정보 확인", layout="centered")
st.title("🎉 나의 생일 정보 확인 웹사이트")

# 첫 번째 생일 입력
dob1 = st.date_input("첫 번째 생년월일 선택", datetime(2000,1,1), key="dob1")
month1, day1, year1 = dob1.month, dob1.day, dob1.year

tab1, tab2, tab3 = st.tabs(["📋 기본 정보", "🔮 사주 보기", "💞 사주 궁합"])

# ---------------------------
# 기본 정보 탭
# ---------------------------
with tab1:
    st.subheader(f"🎂 {dob1.strftime('%Y년 %m월 %d일')} 정보")
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    month_day_key1 = f"{month1:02d}-{day1:02d}"
    flower = birthdata.BIRTH_FLOWERS_BY_DAY.get(month_day_key1)
    with col1:
        if flower:
            st.markdown(f"<div style='background:#fffaf0; padding:15px; border-radius:15px; text-align:center;'>"
                        f"<h3>🌸 탄생화</h3><p><b>{flower['name']}</b><br>의미: {flower['meaning']}</p></div>", 
                        unsafe_allow_html=True)

    stone = birthdata.BIRTH_STONES.get(month1)
    with col2:
        if stone:
            st.markdown(f"<div style='background:#f0ffff; padding:15px; border-radius:15px; text-align:center;'>"
                        f"<h3>💎 탄생석</h3><p><b>{stone['name']}</b><br>의미: {stone['meaning']}</p></div>", 
                        unsafe_allow_html=True)

    sign, sign_emoji = birthdata.get_zodiac(month1, day1)
    with col3:
        st.markdown(f"<div style='background:#f5f5f5; padding:15px; border-radius:15px; text-align:center;'>"
                    f"<h3>✨ 별자리</h3><p><b>{sign}</b> {sign_emoji}</p></div>", unsafe_allow_html=True)

    chinese_zodiac = birthdata.get_chinese_zodiac(year1)
    with col4:
        st.markdown(f"<div style='background:#f0fff0; padding:15px; border-radius:15px; text-align:center;'>"
                    f"<h3>🐲 띠</h3><p><b>{chinese_zodiac}</b></p></div>", unsafe_allow_html=True)

# ---------------------------
# 사주 보기 탭
# ---------------------------
with tab2:
    st.subheader("🔮 사주풀이 (간단)")

    gan = ["갑","을","병","정","무","기","경","신","임","계"]
    ji  = ["자","축","인","묘","진","사","오","미","신","유","술","해"]

    year_gan = gan[(year1 - 4) % 10]
    year_ji  = ji[(year1 - 4) % 12]
    month_gan = gan[(month1 + year1) % 10]
    month_ji  = ji[(month1 + year1) % 12]
    day_gan = gan[(day1 + year1) % 10]
    day_ji  = ji[(day1 + month1) % 12]

    saju_text = f"{year_gan}{year_ji}년 {month_gan}{month_ji}월 {day_gan}{day_ji}일"
    st.markdown(f"<div style='background:#fff0f5; padding:20px; border-radius:15px; text-align:center;'>"
                f"<h3>사주 (연/월/일)</h3><p style='font-size:22px; font-weight:bold;'>{saju_text}</p></div>", 
                unsafe_allow_html=True)

# ---------------------------
# 사주 궁합 탭
# ---------------------------
with tab3:
    st.subheader("💞 두 사람 사주 궁합")

    dob2 = st.date_input("두 번째 생년월일 선택", datetime(2000,1,1), key="dob2")
    month2, day2, year2 = dob2.month, dob2.day, dob2.year

    # 간단 사주 계산
    def get_saju(y, m, d):
        return {
            "year_gan": gan[(y - 4) % 10],
            "year_ji": ji[(y - 4) % 12],
            "month_gan": gan[(m + y) % 10],
            "month_ji": ji[(m + y) % 12],
            "day_gan": gan[(d + y) % 10],
            "day_ji": ji[(d + m) % 12]
        }

    saju1 = get_saju(year1, month1, day1)
    saju2 = get_saju(year2, month2, day2)

    # 오행
    five_elements = {"갑":"목","을":"목","병":"화","정":"화","무":"토","기":"토","경":"금","신":"금","임":"수","계":"수"}

    def get_elements(saju):
        return [five_elements[saju["year_gan"]], five_elements[saju["month_gan"]], five_elements[saju["day_gan"]]]

    elements1 = get_elements(saju1)
    elements2 = get_elements(saju2)

    # 궁합 분석
    common_elements = set(elements1) & set(elements2)
    match_score = len(common_elements) * 2  # 간단 점수 예시

    # 상세 메시지
    if match_score >= 4:
        message = "🌟 매우 좋은 궁합입니다! 서로 잘 맞고 조화롭습니다."
    elif match_score >= 2:
        message = "🙂 꽤 좋은 궁합입니다. 서로 이해하고 보완 가능합니다."
    else:
        message = "⚠️ 조금 조심해야 하는 궁합입니다. 서로 배려가 필요합니다."

    st.markdown(f"<div style='background:#fffaf0; padding:20px; border-radius:15px; text-align:center;'>"
                f"<h3>오행 기반 궁합 점수: {match_score}/6</h3><p style='font-size:18px;'>{message}</p></div>", 
                unsafe_allow_html=True)

    # 사주 천간/지지 비교
    st.markdown("<h4>📌 연/월/일 천간·지지 비교</h4>", unsafe_allow_html=True)
    st.write(f"연간: {saju1['year_gan']}{saju1['year_ji']} vs {saju2['year_gan']}{saju2['year_ji']}")
    st.write(f"월간: {saju1['month_gan']}{saju1['month_ji']} vs {saju2['month_gan']}{saju2['month_ji']}")
    st.write(f"일간: {saju1['day_gan']}{saju1['day_ji']} vs {saju2['day_gan']}{saju2['day_ji']}")
