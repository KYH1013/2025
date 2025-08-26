import streamlit as st
import birthdata
from datetime import datetime

# ---------------------------
# CHINESE ZODIAC & Compatibility
# ---------------------------
CHINESE_ZODIAC = [
    "쥐띠 🐭", "소띠 🐮", "호랑이띠 🐯", "토끼띠 🐰",
    "용띠 🐲", "뱀띠 🐍", "말띠 🐴", "양띠 🐑",
    "원숭이띠 🐵", "닭띠 🐔", "개띠 🐶", "돼지띠 🐷"
]

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
# 페이지 설정
# ---------------------------
st.set_page_config(page_title="생일 정보 확인", layout="centered")
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
# 탭1: 기본 정보
# ---------------------------
with tab1:
    st.subheader(f"🎂 {dob1.strftime('%Y년 %m월 %d일')} 정보")

    # 2*2 카드 배열
    col1, col2 = st.columns(2)
    
    with col1:
        # 탄생화
        with st.expander("🌸 탄생화", expanded=True):
            month_day_key = f"{month1:02d}-{day1:02d}"
            flower = birthdata.BIRTH_FLOWERS_BY_DAY.get(month_day_key)
            if flower:
                st.write(f"{flower['name']} - {flower['meaning']}")
            else:
                st.write("정보 없음")

        # 탄생석
        with st.expander("💎 탄생석", expanded=True):
            stone = birthdata.BIRTH_STONES.get(month1)
            if stone:
                st.write(f"{stone['name']} - {stone['meaning']}")
            else:
                st.write("정보 없음")
    
    with col2:
        # 별자리
        with st.expander("✨ 별자리", expanded=True):
            sign, sign_emoji = birthdata.get_zodiac(month1, day1)
            st.write(f"{sign} {sign_emoji}")
        
        # 띠 & 궁합
        with st.expander("🐲 띠 & 궁합", expanded=True):
            chinese_zodiac = CHINESE_ZODIAC[(year1 - 4) % 12]
            zodiac_name = chinese_zodiac[:chinese_zodiac.find("띠")]
            compat = ZODIAC_COMPATIBILITY.get(zodiac_name, {"좋음": [], "안좋음": []})
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
    st.subheader("💞 종합 궁합")

    # ---------------------------
    # 1. 띠 궁합
    # ---------------------------
    st.markdown("### 🐲 띠 궁합")
    # dob1.year 기준으로 띠 계산
    chinese_zodiac = CHINESE_ZODIAC[(dob1.year - 4) % 12]
    zodiac_name = chinese_zodiac[:chinese_zodiac.find("띠")]
    compat = ZODIAC_COMPATIBILITY.get(zodiac_name, {"좋음": [], "안좋음": []})
    st.write(f"{chinese_zodiac}\n💖 {', '.join(compat['좋음'])}\n💔 {', '.join(compat['안좋음'])}")

    # ---------------------------
    # 2. 사주 궁합 (간단 오행 기반)
    # ---------------------------
    st.markdown("### 🔮 사주 궁합 (간단 오행 기반)")

    def calculate_saju_compat(dob):
        """
        간단 예시: 연,월,일 기반 오행 점수 계산
        실제 오행 궁합 알고리즘은 더 복잡하게 구현 가능
        """
        # 예시 계산: (연도 마지막 자리 * 3 + 월 * 2 + 일) % 100
        score = ((dob.year % 10) * 3 + dob.month * 2 + dob.day) % 100
        return score

    saju_score = calculate_saju_compat(dob1)

    # 점수별 해석
    if saju_score >= 70:
        saju_result = "궁합이 매우 좋음 💖💖💖"
    elif saju_score >= 40:
        saju_result = "궁합이 보통 💛💛"
    else:
        saju_result = "궁합이 낮음 💔💔💔"

    # 카드 형식으로 표시
    st.markdown(
        f"<div style='padding:20px; border-radius:10px; background-color:#f0f8ff; text-align:center;'>"
        f"<h3>사주 점수: {saju_score}/100</h3>"
        f"<p>{saju_result}</p>"
        f"</div>",
        unsafe_allow_html=True
    )
