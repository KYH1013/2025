import streamlit as st

st.set_page_config(page_title="생일 정보 조회", page_icon="🎂", layout="centered")

st.title("🎂 내 생일의 숨은 의미 찾기")
st.write("생일을 입력하면 탄생화, 탄생석, 해당 날짜의 기념일을 알려드립니다!")

# ===== 데이터 딕셔너리 =====
flowers = {
    # 여기에 탄생화 데이터 붙여넣기 (예: (1,1): "수선화 - 존경과 자존심")
}

stones = {
    # 여기에 탄생석 데이터 붙여넣기 (예: (1,1): "가넷 - 진실과 우정")
}

anniversaries = {
    # 여기에 기념일 데이터 붙여넣기 (예: (1,1): "세계 평화의 날")
}

# ===== 사용자 입력 =====
col1, col2 = st.columns(2)
with col1:
    month = st.number_input("월", min_value=1, max_value=12, step=1)
with col2:
    day = st.number_input("일", min_value=1, max_value=31, step=1)

# ===== 결과 출력 =====
if st.button("조회하기"):
    key = (month, day)
    if key in flowers and key in stones and key in anniversaries:
        st.subheader(f"📅 {month}월 {day}일의 정보")
        st.write(f"**🌸 탄생화:** {flowers[key]}")
        st.write(f"**💎 탄생석:** {stones[key]}")
        st.write(f"**📌 기념일:** {anniversaries[key]}")
    else:
        st.warning("해당 날짜에 대한 데이터가 없습니다. 데이터셋을 확인해주세요.")
