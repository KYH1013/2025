import streamlit as st
import birthdata
from datetime import datetime, date, timedelta
import random

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
    return max(0, min(100, score))

def safe_date(year, month, day):
    try:
        return datetime(year, month, day)
    except ValueError:
        if month == 2 and day == 29:
            return datetime(year, 2, 28)
        else:
            raise

def calculate_age(born):
    today = date.today()
    age = today.year - born.year
    if (today.month, today.day) < (born.month, born.day):
        age -= 1
    return age

def days_to_birthday(born):
    today = date.today()
    next_birthday = date(today.year, born.month, born.day)
    if next_birthday < today:
        next_birthday = date(today.year + 1, born.month, born.day)
    return (next_birthday - today).days

def months_days_since_birth(born):
    today = date.today()
    total_days = (today - born).days
    months = total_days // 30
    return months, total_days

def get_day_of_week(born):
    days = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
    return days[born.weekday()]

def simple_weekly_monthly_fortune(elem):
    # 간단 룰 기반 운세 생성
    love = random.choice(["좋음", "보통", "주의"])
    money = random.choice(["좋음", "보통", "주의"])
    health = random.choice(["좋음", "보통", "주의"])
    advice = ELEM_ADVICE.get(elem, "")
    return love, money, health, advice

# ---------------------------
# 페이지 설정
# ---------------------------
st.set_page_config(page_title="생일 정보 확인", layout="centered")
st.title("🎉 나의 생일 정보 확인 웹사이트")

# 오늘 날짜
today = datetime.today()
min_date = safe_date(today.year - 100, today.month, today.day)
max_date = today

# ---------------------------
# 첫 번째 생일 입력
# ---------------------------
dob1 = st.date_input("첫 번째 생년월일 선택", today, min_value=min_date, max_value=max_date)

# ---------------------------
# 나이, D-Day, 개월/일 계산
# ---------------------------
age = calculate_age(dob1)
d_day = days_to_birthday(dob1)
months, total_days = months_days_since_birth(dob1)
weekday = get_day_of_week(dob1)

st.info(f"🎈 나이: {age}세 | 다음 생일까지 D-{d_day}일 | 태어난 요일: {weekday}")
st.success(f"🗓 태어난지 {months}개월 / {total_days}일 지났습니다")

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
            flower = birthdata.BIRTH_FLOWERS_BY_DAY.get(f"{dob1.month:02d}-{dob1.day:02d}")
            if flower:
                st.write(f"{flower['name']} - {flower['meaning']}")
            else:
                st.write("정보 없음")
        with st.expander("💎 탄생석", expanded=True):
            stone = birthdata.BIRTH_STONES.get(dob1.month)
            if stone:
                st.write(f"{stone['name']} - {stone['meaning']}")
            else:
                st.write("정보 없음")
    
    with col2:
        with st.expander("✨ 별자리", expanded=True):
            sign, sign_emoji = birthdata.get_zodiac(dob1.month, dob1.day)
            st.write(f"{sign} {sign_emoji}")
        with st.expander("🐲 띠 & 궁합", expanded=True):
            chinese_zodiac, zodiac_name = get_chinese_zodiac(dob1.year)
            compat = ZODIAC_COMPATIBILITY.get(zodiac_name, {"좋음": [], "안좋음": []})
            st.write(f"{chinese_zodiac}\n💖 {', '.join(compat['좋음'])}\n💔 {', '.join(compat['안좋음'])}")

# ---------------------------
# 탭2: 사주 해석 + 운세
# ---------------------------
with tab2:
    st.subheader("🔮 사주 해석 & 운세")
    elements, branches = saju_elements(dob1)
    
    for branch, elem in zip(branches, elements):
        st.markdown(
            f"<div style='padding:15px; border-radius:15px; background-color:{ELEM_COLORS[elem]}; margin-bottom:10px;'>"
            f"<h4 style='text-align:center;'>{branch} ({elem})</h4>"
            f"<p style='text-align:center;'>{ELEM_ADVICE[elem]}</p>"
            f"</div>",
            unsafe_allow_html=True
        )
    
    # 1번: 간단한 주간/월간 운세
    st.markdown("### 📅 이번 주/이번 달 운세 (간단 룰 기반)")
    love, money, health, advice = simple_weekly_monthly_fortune(elements[0])
    st.write(f"💖 사랑운: {love}")
    st.write(f"💰 금전운: {money}")
    st.write(f"🩺 건강운: {health}")
    st.write(f"🌟 오늘의 조언: {advice}")

# ---------------------------
# 탭3: 종합 궁합
# ---------------------------
with tab3:
    st.subheader("💞 종합 궁합")
    dob2 = st.date_input("두 번째 생년월일 선택", today, min_value=min_date, max_value=max_date, key="dob2")
    
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
