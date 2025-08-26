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
    st.subheader("🔮 사주 해석")

    # 첫 번째 생일 입력 기준
    dob = dob1
    year, month, day = dob.year, dob.month, dob.day

    # ---------------------------
    # 간단 사주 요소
    # ---------------------------
    TWELVE_EARTHLY_BRANCHES = ["자","축","인","묘","진","사","오","미","신","유","술","해"]
    BRANCH_TO_ELEM = {"자":"수","축":"토","인":"목","묘":"목","진":"토","사":"화",
                      "오":"화","미":"토","신":"금","유":"금","술":"토","해":"수"}

    year_branch = TWELVE_EARTHLY_BRANCHES[(year - 4) % 12]
    month_branch = TWELVE_EARTHLY_BRANCHES[(month + 1) % 12]
    day_branch = TWELVE_EARTHLY_BRANCHES[(day - 1) % 12]

    # ---------------------------
    # 오행 조언
    # ---------------------------
    ELEM_ADVICE = {
        "목": "창의력과 성장을 중시하세요. 새로운 도전이 행운을 가져옵니다.",
        "화": "열정과 활동성을 살리세요. 인간관계와 의사소통이 중요합니다.",
        "토": "안정과 책임을 중시하세요. 계획을 세우고 차분히 진행하세요.",
        "금": "결단력과 자기주장을 발휘하세요. 목표 설정이 성공의 열쇠입니다.",
        "수": "지혜와 유연함을 살리세요. 학문, 공부, 정보 습득에 집중하세요."
    }

    elements = [BRANCH_TO_ELEM[year_branch], BRANCH_TO_ELEM[month_branch], BRANCH_TO_ELEM[day_branch]]

    # ---------------------------
    # 카드형식 UI
    # ---------------------------
    st.markdown(
        f"<div style='padding:20px; border-radius:15px; background-color:#fffaf0; margin-bottom:15px;'>"
        f"<h3 style='text-align:center;'>📅 생일: {dob.strftime('%Y년 %m월 %d일')}</h3>"
        f"<p style='text-align:center;'>연지: {year_branch} ({BRANCH_TO_ELEM[year_branch]})</p>"
        f"<p style='text-align:center;'>월지: {month_branch} ({BRANCH_TO_ELEM[month_branch]})</p>"
        f"<p style='text-align:center;'>일지: {day_branch} ({BRANCH_TO_ELEM[day_branch]})</p>"
        f"</div>",
        unsafe_allow_html=True
    )

    # ---------------------------
    # 오행 해석 + 조언
    # ---------------------------
    st.markdown(
        f"<div style='padding:15px; border-radius:15px; background-color:#e6f7ff;'>"
        f"<h4>🌟 사주 오행 해석 & 조언</h4>"
        f"<ul>"
        f"<li>연지({year_branch}) - {BRANCH_TO_ELEM[year_branch]}: {ELEM_ADVICE[BRANCH_TO_ELEM[year_branch]]}</li>"
        f"<li>월지({month_branch}) - {BRANCH_TO_ELEM[month_branch]}: {ELEM_ADVICE[BRANCH_TO_ELEM[month_branch]]}</li>"
        f"<li>일지({day_branch}) - {BRANCH_TO_ELEM[day_branch]}: {ELEM_ADVICE[BRANCH_TO_ELEM[day_branch]]}</li>"
        f"</ul>"
        f"</div>",
        unsafe_allow_html=True
    )

# ---------------------------
# 탭3: 종합 궁합
# ---------------------------
with tab3:
    st.subheader("💞 종합 궁합")

    # ---------------------------
    # 두 번째 생일 입력
    # ---------------------------
    dob2 = st.date_input("두 번째 생년월일 선택", datetime(2000,1,1), key="dob2")
    month2, day2, year2 = dob2.month, dob2.day, dob2.year

    # ---------------------------
    # 1. 띠 궁합
    # ---------------------------
    st.markdown("### 🐲 띠 궁합")
    chinese_zodiac1 = CHINESE_ZODIAC[(dob1.year - 4) % 12]
    zodiac_name1 = chinese_zodiac1[:chinese_zodiac1.find("띠")]
    chinese_zodiac2 = CHINESE_ZODIAC[(dob2.year - 4) % 12]
    zodiac_name2 = chinese_zodiac2[:chinese_zodiac2.find("띠")]

    compat1 = ZODIAC_COMPATIBILITY.get(zodiac_name1, {"좋음": [], "안좋음": []})
    if zodiac_name2 in compat1["좋음"]:
        zodiac_result = f"💖 좋은 궁합: {chinese_zodiac1} × {chinese_zodiac2}"
    elif zodiac_name2 in compat1["안좋음"]:
        zodiac_result = f"💔 안 좋은 궁합: {chinese_zodiac1} × {chinese_zodiac2}"
    else:
        zodiac_result = f"💛 보통 궁합: {chinese_zodiac1} × {chinese_zodiac2}"

    st.write(zodiac_result)

    # ---------------------------
    # 2. 사주 궁합 (오행 기반)
    # ---------------------------
    st.markdown("### 🔮 사주 궁합 (오행 기반)")

    # 오행 계산용 데이터
    TEN_HEAVENLY_STEMS = ["갑","을","병","정","무","기","경","신","임","계"]
    TWELVE_EARTHLY_BRANCHES = ["자","축","인","묘","진","사","오","미","신","유","술","해"]
    BRANCH_TO_ELEM = {"자":"수","축":"토","인":"목","묘":"목","진":"토","사":"화",
                      "오":"화","미":"토","신":"금","유":"금","술":"토","해":"수"}
    ELEMS_SUPPORT = {"목":"화","화":"토","토":"금","금":"수","수":"목"}
    ELEMS_CONFLICT = {"목":"금","화":"수","토":"목","금":"화","수":"화"}

    def saju_elements(dob):
        year_branch = TWELVE_EARTHLY_BRANCHES[(dob.year - 4) % 12]
        month_branch = TWELVE_EARTHLY_BRANCHES[(dob.month + 1) % 12]
        day_branch = TWELVE_EARTHLY_BRANCHES[(dob.day - 1) % 12]
        elements = [BRANCH_TO_ELEM[year_branch], BRANCH_TO_ELEM[month_branch], BRANCH_TO_ELEM[day_branch]]
        return elements

    def calculate_saju_compat(dob1, dob2):
        elems1 = saju_elements(dob1)
        elems2 = saju_elements(dob2)
        score = 50  # 기본 점수
        for e1, e2 in zip(elems1, elems2):
            if ELEMS_SUPPORT.get(e1) == e2:
                score += 15
            elif ELEMS_CONFLICT.get(e1) == e2:
                score -= 15
        score = max(0, min(100, score))
        return score

    saju_score = calculate_saju_compat(dob1, dob2)

    if saju_score >= 70:
        saju_result = "궁합이 매우 좋음 💖💖💖"
    elif saju_score >= 40:
        saju_result = "궁합이 보통 💛💛"
    else:
        saju_result = "궁합이 낮음 💔💔💔"

    st.markdown(
        f"<div style='padding:20px; border-radius:10px; background-color:#f0f8ff; text-align:center;'>"
        f"<h3>사주 점수: {saju_score}/100</h3>"
        f"<p>{saju_result}</p>"
        f"</div>",
        unsafe_allow_html=True
    )
