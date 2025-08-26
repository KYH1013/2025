import streamlit as st
import birthdata
from datetime import datetime

# ---------------------------
# 상수 정의
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

TWELVE_EARTHLY_BRANCHES = ["자","축","인","묘","진","사","오","미","신","유","술","해"]
BRANCH_TO_ELEM = {"자":"수","축":"토","인":"목","묘":"목","진":"토","사":"화",
                  "오":"화","미":"토","신":"금","유":"금","술":"토","해":"수"}
ELEM_COLORS = {"목":"#b0f2b6","화":"#ffb3b3","토":"#f0e68c","금":"#d1d1d1","수":"#a0c4ff"}
ELEM_ADVICE = {
    "목": "창의력과 성장을 중시하세요. 새로운 도전이 행운을 가져옵니다.",
    "화": "열정과 활동성을 살리세요. 인간관계와 의사소통이 중요합니다.",
    "토": "안정과 책임을 중시하세요. 계획을 세우고 차분히 진행하세요.",
    "금": "결단력과 자기주장을 발휘하세요. 목표 설정이 성공의 열쇠입니다.",
    "수": "지혜와 유연함을 살리세요. 학문, 공부, 정보 습득에 집중하세요."
}
ELEMS_SUPPORT = {"목":"화","화":"토","토":"금","금":"수","수":"목"}
ELEMS_CONFLICT = {"목":"금","화":"수","토":"목","금":"화","수":"화"}

# ---------------------------
# 공통 함수
# ---------------------------
def get_chinese_zodiac(year):
    zodiac = CHINESE_ZODIAC[(year - 4) % 12]
    zodiac_name = zodiac.replace("띠", "").split()[0]
    return zodiac, zodiac_name

def saju_elements(dob):
    year_branch = TWELVE_EARTHLY_BRANCHES[(dob.year - 4) % 12]
    month_branch = TWELVE_EARTHLY_BRANCHES[(dob.month + 1) % 12]
    day_branch = TWELVE_EARTHLY_BRANCHES[(dob.day - 1) % 12]
    elements = [BRANCH_TO_ELEM[year_branch], BRANCH_TO_ELEM[month_branch], BRANCH_TO_ELEM[day_branch]]
    return elements, [year_branch, month_branch, day_branch]

def calculate_saju_compat(dob1, dob2):
    elems1, _ = saju_elements(dob1)
    elems2, _ = saju_elements(dob2)
    score = 50
    for e1, e2 in zip(elems1, elems2):
        if ELEMS_SUPPORT.get(e1) == e2:
            score += 15
        elif ELEMS_CONFLICT.get(e1) == e2:
            score -= 15
    score = max(0, min(100, score))
    return score

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
    col1, col2 = st.columns(2)
    
    with col1:
        with st.expander("🌸 탄생화", expanded=True):
            flower = birthdata.BIRTH_FLOWERS_BY_DAY.get(f"{month1:02d}-{day1:02d}")
            if flower:
                st.write(f"{flower['name']} - {flower['meaning']}")
            else:
                st.write("정보 없음")
        with st.expander("💎 탄생석", expanded=True):
            stone = birthdata.BIRTH_STONES.get(month1)
            if stone:
                st.write(f"{stone['name']} - {stone['meaning']}")
            else:
                st.write("정보 없음")
    
    with col2:
        with st.expander("✨ 별자리", expanded=True):
            sign, sign_emoji = birthdata.get_zodiac(month1, day1)
            st.write(f"{sign} {sign_emoji}")
        with st.expander("🐲 띠 & 궁합", expanded=True):
            chinese_zodiac, zodiac_name = get_chinese_zodiac(year1)
            compat = ZODIAC_COMPATIBILITY.get(zodiac_name, {"좋음": [], "안좋음": []})
            st.write(f"{chinese_zodiac}\n💖 {', '.join(compat['좋음'])}\n💔 {', '.join(compat['안좋음'])}")

# ---------------------------
# 탭2: 사주 해석
# ---------------------------
with tab2:
    st.subheader("🔮 사주 해석")
    elements, branches = saju_elements(dob1)
    
    for branch, elem in zip(branches, elements):
        st.markdown(
            f"<div style='padding:15px; border-radius:15px; background-color:{ELEM_COLORS[elem]}; margin-bottom:10px;'>"
            f"<h4 style='text-align:center;'>{branch} ({elem})</h4>"
            f"<p style='text-align:center;'>{ELEM_ADVICE[elem]}</p>"
            f"</div>",
            unsafe_allow_html=True
        )

# ---------------------------
# 탭3: 종합 궁합
# ---------------------------
with tab3:
    st.subheader("💞 종합 궁합")
    dob2 = st.date_input("두 번째 생년월일 선택", datetime(2000,1,1), key="dob2")
    
    # 띠 궁합
    cz1, zn1 = get_chinese_zodiac(dob1.year)
    cz2, zn2 = get_chinese_zodiac(dob2.year)
    compat1 = ZODIAC_COMPATIBILITY.get(zn1, {"좋음": [], "안좋음": []})
    if zn2 in compat1["좋음"]:
        zodiac_result = f"💖 좋은 궁합: {cz1} × {cz2}"
    elif zn2 in compat1["안좋음"]:
        zodiac_result = f"💔 안 좋은 궁합: {cz1} × {cz2}"
    else:
        zodiac_result = f"💛 보통 궁합: {cz1} × {cz2}"
    st.markdown(f"<div style='padding:15px; border-radius:10px; background-color:#fff0f5; text-align:center;'>{zodiac_result}</div>", unsafe_allow_html=True)
    
    # 사주 궁합
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
