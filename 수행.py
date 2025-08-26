import streamlit as st
import birthdata
from datetime import datetime

# ---------------------------
# 페이지 설정
# ---------------------------
st.set_page_config(page_title="생일 정보 확인", layout="wide")
st.title("🎉 나의 생일 정보 확인 웹사이트")

# ---------------------------
# 첫 번째 생일 입력
# ---------------------------
dob1 = st.date_input("첫 번째 생년월일 선택", datetime(2000,1,1), key="dob1")
month1, day1, year1 = dob1.month, dob1.day, dob1.year

# ---------------------------
# 탭 생성
# ---------------------------
tab1, tab2, tab3 = st.tabs(["📋 기본 정보", "🔮 사주 보기", "💞 종합 궁합"])

# ---------------------------
# 띠 궁합 데이터
# ---------------------------
ZODIAC_COMPATIBILITY = {
    "쥐": {"좋음": ["용", "원숭이"], "안좋음": ["말", "양"]},
    "소": {"좋음": ["뱀", "닭"], "안좋음": ["말", "양"]},
    "호랑이": {"좋음": ["말", "개"], "안좋음": ["원숭이", "뱀"]},
    "토끼": {"좋음": ["양", "돼지"], "안좋음": ["닭", "뱀"]},
    "용": {"좋음": ["쥐", "원숭이"], "안좋음": ["토끼", "개"]},
    "뱀": {"좋음": ["소", "닭"], "안좋음": ["호랑이", "돼지"]},
    "말": {"좋음": ["호랑이", "개"], "안좋음": ["쥐", "소"]},
    "양": {"좋음": ["토끼", "돼지"], "안좋음": ["쥐", "소"]},
    "원숭이": {"좋음": ["쥐", "용"], "안좋음": ["호랑이", "토끼"]},
    "닭": {"좋음": ["소", "뱀"], "안좋음": ["토끼", "돼지"]},
    "개": {"좋음": ["호랑이", "말"], "안좋음": ["용", "원숭이"]},
    "돼지": {"좋음": ["토끼", "양"], "안좋음": ["뱀", "닭"]}
}

# ---------------------------
# 탭1: 기본 정보
# ---------------------------
with tab1:
    st.subheader(f"🎂 {dob1.strftime('%Y년 %m월 %d일')} 정보")

    col1, col2 = st.columns(2)

    with col1:
        with st.expander("🌸 탄생화", expanded=True, key="exp_flower"):
            flower = birthdata.BIRTH_FLOWERS_BY_DAY.get(f"{month1:02d}-{day1:02d}")
            st.write(f"{flower['name']} - {flower['meaning']}" if flower else "정보 없음")

        with st.expander("💎 탄생석", expanded=True, key="exp_stone"):
            stone = birthdata.BIRTH_STONES.get(month1)
            st.write(f"{stone['name']} - {stone['meaning']}" if stone else "정보 없음")

    with col2:
        with st.expander("✨ 별자리", expanded=True, key="exp_zodiac"):
            sign, sign_emoji = birthdata.get_zodiac(month1, day1)
            st.write(f"{sign} {sign_emoji}")

        with st.expander("🐲 띠 & 궁합", expanded=True, key="exp_chinese"):
            chinese_zodiac = birthdata.get_chinese_zodiac(year1)
            compat = ZODIAC_COMPATIBILITY.get(chinese_zodiac, {"좋음": [], "안좋음": []})
            st.write(f"{chinese_zodiac}\n💖 {', '.join(compat['좋음'])}\n💔 {', '.join(compat['안좋음'])}")

    # 월별 기념일
# ---------------------------
# 사주 해석 + 오행 운세
# ---------------------------
with tab2:
    st.subheader("🔮 사주풀이 (간단)")

    gan = ["갑","을","병","정","무","기","경","신","임","계"]
    ji  = ["자","축","인","묘","진","사","오","미","신","유","술","해"]

    # 연/월/일 사주 계산
    year_gan = gan[(year1 - 4) % 10]
    year_ji  = ji[(year1 - 4) % 12]
    month_gan = gan[(month1 + year1) % 10]
    month_ji  = ji[(month1 + year1) % 12]
    day_gan = gan[(day1 + year1) % 10]
    day_ji  = ji[(day1 + month1) % 12]
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


# ---------------------------
# 탭3: 종합 궁합
# ---------------------------
with tab3:
    st.subheader("💞 두 사람 종합 궁합")
    dob2 = st.date_input("두 번째 생년월일 선택", datetime(2000,1,1), key="dob2")
    month2, day2, year2 = dob2.month, dob2.day, dob2.year

    # 사주 계산 함수
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

    # 별자리
    sign1, _ = birthdata.get_zodiac(month1, day1)
    sign2, _ = birthdata.get_zodiac(month2, day2)

    # -----------------------
    # 상세 점수 계산
    # -----------------------
    score = 0
    details = []

    # 1) 사주 비교
    for k, label in [("year_gan","연간"), ("year_ji","연지"), 
                     ("month_gan","월간"), ("month_ji","월지"), 
                     ("day_gan","일간"), ("day_ji","일지")]:
        if saju1[k] == saju2[k]:
            details.append(f"{label}: 같음 ✅")
            score += 1
        else:
            details.append(f"{label}: 다름 ⚠️")

    # 2) 오행 비교
    common_elements = set(elements1) & set(elements2)
    score += len(common_elements)
    details.append(f"오행 겹치는 요소: {', '.join(common_elements) if common_elements else '없음'}")

    # 3) 별자리 비교 (간단)
    compatible_pairs = {("양", "사"), ("사", "양"), ("쥐","용"), ("용","쥐")} # 예시
    if (sign1[:1], sign2[:1]) in compatible_pairs:
        score += 1
        details.append(f"별자리 궁합: 좋음 ✅ ({sign1} vs {sign2})")
    else:
        details.append(f"별자리 궁합: 보통 ⚠️ ({sign1} vs {sign2})")

    # 4) 최종 메시지
    if score >= 8:
        message = "🌟 매우 좋은 궁합입니다! 서로 잘 맞고 조화롭습니다."
    elif score >= 5:
        message = "🙂 꽤 좋은 궁합입니다. 서로 이해하고 보완 가능합니다."
    else:
        message = "⚠️ 조금 조심해야 하는 궁합입니다. 서로 배려가 필요합니다."

    # -----------------------
    # 카드형 UI 출력 (점수 + 분류 기준)
    # -----------------------
    st.markdown(f"""
    <div style='background:#fffaf0; padding:20px; border-radius:15px; text-align:center;'>
        <h3>💞 종합 궁합 점수: {score} / 10</h3>
        <p style='font-size:16px;'>점수 기준:</p>
        <ul style='text-align:left; display:inline-block;'>
            <li>🌟 8-10점: 매우 좋은 궁합</li>
            <li>🙂 5-7점: 꽤 좋은 궁합</li>
            <li>⚠️ 0-4점: 주의 필요</li>
        </ul>
        <p style='font-size:18px; margin-top:10px;'>{message}</p>
    </div>
    """, unsafe_allow_html=True)

    # -----------------------
    # 상세 비교 카드
    # -----------------------
    st.markdown("<h4>📌 상세 비교</h4>", unsafe_allow_html=True)
    for detail in details:
        st.markdown(f"<div style='background:#f5f5f5; padding:10px; border-radius:10px; margin-bottom:5px;'>{detail}</div>", unsafe_allow_html=True)

    # -----------------------
    # 사주/오행/별자리 비교
    # -----------------------
    st.markdown("<h4>📌 사주/오행/별자리 비교</h4>", unsafe_allow_html=True)
    st.write(f"사주1: {saju1['year_gan']}{saju1['year_ji']}년 {saju1['month_gan']}{saju1['month_ji']}월 {saju1['day_gan']}{saju1['day_ji']}일")
    st.write(f"사주2: {saju2['year_gan']}{saju2['year_ji']}년 {saju2['month_gan']}{saju2['month_ji']}월 {saju2['day_gan']}{saju2['day_ji']}일")
    st.write(f"오행1: {elements1} / 오행2: {elements2}")
    st.write(f"별자리: {sign1} vs {sign2}")
