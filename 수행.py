import streamlit as st
import pandas as pd
from datetime import date
import importlib

st.set_page_config(page_title="생일 인사이트", page_icon="🎂", layout="centered")

# ------------------------------
# 외부 데이터 모듈 불러오기 (requirements에 포함)
# ------------------------------
try:
    import birthdata  # 사용자가 제공할 데이터 모듈
except ImportError:
    st.error("데이터 모듈(birthdata.py)을 불러올 수 없습니다. requirements.txt에 포함해주세요.")
    st.stop()

BIRTH_FLOWERS = birthdata.BIRTH_FLOWERS
BIRTH_STONES = birthdata.BIRTH_STONES
ZODIAC_RANGES = birthdata.ZODIAC_RANGES
HEAVENLY_STEMS = birthdata.HEAVENLY_STEMS
EARTHLY_BRANCHES = birthdata.EARTHLY_BRANCHES
BRANCH_ANIMALS = birthdata.BRANCH_ANIMALS
STEM_ELEMENT = birthdata.STEM_ELEMENT
STEM_YINYANG = birthdata.STEM_YINYANG
WORLD_DAYS = birthdata.WORLD_DAYS

# ------------------------------
# 유틸 함수
# ------------------------------
def to_mmdd(month: int, day: int) -> str:
    return f"{month:02d}-{day:02d}"


def get_zodiac(month: int, day: int) -> str:
    for name, (sm, sd), (em, ed) in ZODIAC_RANGES:
        start = (sm, sd)
        end = (em, ed)
        cur = (month, day)
        if start <= end:
            if start <= cur <= end:
                return name
        else:  # 연말 걸침 (예: 염소자리)
            if cur >= start or cur <= end:
                return name
    return "알 수 없음"


def get_ganzhi_year(y: int):
    stem = HEAVENLY_STEMS[(y - 4) % 10]
    branch = EARTHLY_BRANCHES[(y - 4) % 12]
    animal = BRANCH_ANIMALS[branch]
    element = STEM_ELEMENT[stem]
    yinyang = STEM_YINYANG[stem]
    return {
        "year": y,
        "stem": stem,
        "branch": branch,
        "animal": animal,
        "element": element,
        "yinyang": yinyang,
        "label": f"{stem}{branch}년 ({animal}, {yinyang}{element})",
    }


def get_world_days(month: int, day: int):
    return WORLD_DAYS.get(to_mmdd(month, day), [])


# ------------------------------
# UI
# ------------------------------
st.title("🎂 생일 인사이트 생성기")
st.caption("생년월일을 입력하면 탄생화, 탄생석, 별자리, 간단 사주, 세계 지정일을 한 번에!")

col1, col2 = st.columns([1, 1])
with col1:
    bdate = st.date_input("생년월일", value=date(2000, 1, 1), min_value=date(1900, 1, 1), max_value=date.today())
with col2:
    name = st.text_input("이름 (선택)", placeholder="이름을 입력하면 카드에 표시됩니다")

if bdate:
    year, month, day = bdate.year, bdate.month, bdate.day

    flower = BIRTH_FLOWERS.get(month)
    stone = BIRTH_STONES.get(month)
    zodiac = get_zodiac(month, day)
    gz = get_ganzhi_year(year)
    days = get_world_days(month, day)

    st.markdown("---")
    st.subheader("📇 요약 카드")
    st.markdown(
        f"""
        **{name or '사용자'}님의 생일 카드**

        - 🎉 생일: **{year}년 {month}월 {day}일**
        - 🌸 탄생화: **{flower['name']}** — _{flower['meaning']}_
        - 💎 탄생석: **{stone['name']}** — _{stone['meaning']}_
        - ♑ 별자리: **{zodiac}**
        - 🐲 간단 사주(년주): **{gz['label']}**
        """
    )

    st.subheader("🔎 상세 보기")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### 🌸 탄생화")
        st.write(f"월: {month}월")
        st.write(f"이름: {flower['name']}")
        st.write(f"꽃말: {flower['meaning']}")

        st.markdown("#### 💎 탄생석")
        st.write(f"월: {month}월")
        st.write(f"이름: {stone['name']}")
        st.write(f"의미: {stone['meaning']}")

    with c2:
        st.markdown("#### ♑ 서양 별자리")
        st.write(f"별자리: {zodiac}")

        st.markdown("#### 🐉 간단 사주 (년주)")
        gz_df = pd.DataFrame([
            {"항목": "간지(년)", "값": f"{gz['stem']}{gz['branch']}년"},
            {"항목": "띠", "값": gz["animal"]},
            {"항목": "오행", "값": gz["element"]},
            {"항목": "음양", "값": gz["yinyang"]},
        ])
        st.dataframe(gz_df, hide_index=True)

    st.subheader("🌍 해당 날짜의 세계 지정일")
    if days:
        day_df = pd.DataFrame({"기념일": days})
        st.dataframe(day_df, hide_index=True)
    else:
        st.info("등록된 세계 지정일이 없습니다. birthdata.WORLD_DAYS에 추가해주세요.")

else:
    st.info("왼쪽에서 생년월일을 선택하세요.")
