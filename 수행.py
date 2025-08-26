import streamlit as st
import birthdata
from datetime import datetime, date
import hashlib

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
# 함수 정의
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

def date_based_fortune(elem, target_date):
    # 오행별 날짜 기반 고정 운세
    fortunes = {
        "목": ["창의적 하루", "성장 중심", "새로운 도전"],
        "화": ["열정적인 하루", "인간관계 주의", "활동적"],
        "토": ["안정된 하루", "계획 중심", "차분함"],
        "금": ["결단력 있는 하루", "재물 운 주목", "목표 집중"],
        "수": ["지혜로운 하루", "학업/정보 습득", "유연함"]
    }
    key = f"{elem}-{target_date.isoformat()}"
    hash_value = int(hashlib.sha256(key.encode()).hexdigest(), 16)
    index = hash_value % len(fortunes.get(elem, ["평범한 하루"]))
    return fortunes.get(elem, ["평범한 하루"])[index]

# ---------------------------
# 페이지 설정
# ---------------------------
st.set_page_config(page_title="생일 정보 확인", layout="centered")
st.title("🎉 나의 생일 정보 확인 웹사이트")

today = datetime.today()
min_date = date(today.year - 100, today.month, today.day)
max_date = today.date()

dob1 = st.date_input("첫 번째 생년월일 선택", today.date(), min_value=min_date, max_value=max_date)

age = calculate_age(dob1)
d_day = days_to_birthday(dob1)
months, total_days = months_days_since_birth(dob1)
weekday = get_day_of_week(dob1)

st.info(f"🎈 나이: {age}세 | 다음 생일까지 D-{d_day}일 | 태어난 요일: {weekday}")
st.success(f"🗓 태어난지 {months}개월 / {total_days}일 지났습니다")

tab1, tab2, tab3 = st.tabs(["📋 기본 정보", "🔮 사주 보기", "💞 종합 궁합"])

# ---------------------------
# 탭1: 기본 정보
# ---------------------------
with tab1:
    st.subheader(f"🎂 {dob1.strftime('%Y년 %m월 %d일')} 정보")
    col1, col2 = st.columns(2)
    with col1:
        with st.expander("🌸 탄생화", expanded=True):
            month_day_key = f"{dob1.month:02d}-{dob1.day:02d}"
            flower = birthdata.BIRTH_FLOWERS_BY_DAY.get(month_day_key)
            if flower:
                st.markdown(f"{flower['name']} - {flower['meaning']}")
            else:
                st.write("정보 없음")
        with st.expander("💎 탄생석", expanded=True):
            stone = birthdata.BIRTH_STONES.get(dob1.month)
            if stone:
                st.markdown(f"{stone['name']} - {stone['meaning']}")
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
# 탭2: 사주 + 날짜 기반 운세
# ---------------------------
with tab2:
    st.subheader("🔮 사주 해석 & 오늘의 운세")
    elements, branches = saju_elements(dob1)
    col1, col2, col3 = st.columns(3)
    for i, (branch, elem) in enumerate(zip(branches, elements)):
        col = [col1, col2, col3][i]
        col.markdown(
            f"<div style='padding:15px; border-radius:15px; background-color:{ELEM_COLORS[elem]}; text-align:center;'>"
            f"<h4>{branch} ({elem})</h4>"
            f"<p>{ELEM_ADVICE[elem]}</p>"
            f"</div>", unsafe_allow_html=True
        )
    fortune_today = date_based_fortune(elements[0], date.today())
    st.markdown(f"### 🌟 오늘의 운세: {fortune_today}")

# ---------------------------
# 탭3: 종합 궁합
# ---------------------------
with tab3:
    st.subheader("💞 종합 궁합")
    dob2 = st.date_input("두 번째 생년월일 선택", today.date(), min_value=min_date, max_value=max_date, key="dob2")
    
    cz1, zn1 = get_chinese_zodiac(dob1.year)
    cz2, zn2 = get_chinese_zodiac(dob2.year)
    compat1 = ZODIAC_COMPATIBILITY.get(zn1, {"좋음": [], "안좋음": []})
    if zn2 in compat1["좋음"]:
        zodiac_result = f"💖 좋은 궁합: {cz1} × {cz2}"
    elif zn2 in compat1["안좋음"]:
        zodiac_result = f"💔 안 좋은 궁합: {cz1} × {cz2}"
    else:
        zodiac_result = f"💛 보통 궁합: {cz1} × {cz2}"
    st.write(zodiac_result)
    
    saju_score = calculate_saju_compat(dob1, dob2)
    if saju_score >= 70:
        saju_result = "궁합이 매우 좋음 💖💖💖"
    elif saju_score >= 40:
        saju_result = "궁합이 보통 💛💛"
    else:
        saju_result = "궁합이 낮음 💔💔💔"
    st.markdown(f"사주 점수: {saju_score}/100 | {saju_result}")
