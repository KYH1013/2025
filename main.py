import streamlit as st

# Set the page title and header
st.set_page_config(page_title="MBTI 기반 직업 추천 웹사이트")
st.title("🌈 MBTI 기반 직업 추천 🌈")

# Disclaimer
st.warning("⚠️ 이 웹사이트는 재미로 참고하는 용도입니다. 모든 개인은 고유하며, 실제 직업 선택은 개인의 기술, 관심사, 가치관 등을 종합적으로 고려해야 합니다. ⚠️")

# Dictionary of career suggestions for each MBTI type
# These are general suggestions and can be customized.
career_suggestions = {
    "ISTJ": ["회계사 📊", "공무원 🏛️", "데이터 분석가 📈", "경영 컨설턴트 💼"],
    "ISFJ": ["초등학교 교사 👩‍🏫", "사회복지사 🤝", "사서 📚", "보건 의료인 🩺"],
    "INFJ": ["상담사 🗣️", "작가 ✍️", "그래픽 디자이너 🎨", "인사담당자 👥"],
    "INTJ": ["소프트웨어 개발자 💻", "과학 연구원 🔬", "건축가 🏗️", "금융 분석가 💰"],
    "ISTP": ["경찰관 👮", "소방관 🧑‍🚒", "기술자 🛠️", "파일럿 ✈️"],
    "ISFP": ["미술 치료사 🖼️", "요리사 👨‍🍳", "패션 디자이너 👗", "사진작가 📸"],
    "INFP": ["작곡가 🎶", "시인 📝", "심리학자 🤔", "애니메이터 🎬"],
    "INTP": ["컴퓨터 프로그래머 🧑‍💻", "대학 교수 🎓", "철학자 🧘", "과학 연구원 🧪"],
    "ESTP": ["영업 사원 🗣️", "사업가 📈", "경찰관 🚓", "트레이너 💪"],
    "ESFP": ["연예인 🎤", "이벤트 플래너 🎉", "유치원 교사 🧑‍🤝‍🧑", "판매원 🛍️"],
    "ENFP": ["홍보 전문가 📢", "마케터 📊", "강사 🏫", "예술가 🎭"],
    "ENTP": ["창업가 🚀", "변호사 ⚖️", "언론인 📰", "정치인 🗳️"],
    "ESTJ": ["경영자 👔", "프로젝트 매니저 📋", "군 장교 🎖️", "건설 현장 관리자 👷"],
    "ESFJ": ["간호사 👩‍⚕️", "승무원 🧑‍✈️", "교사 🧑‍🏫", "조직 관리자 📝"],
    "ENFJ": ["교사 🍎", "목사 🙏", "정치인 🗣️", "HR 매니저 🤝"],
    "ENTJ": ["CEO 👑", "변호사 ⚖️", "경영 컨설턴트 💼", "투자은행가 📈"]
}

# Create a select box for the user to choose their MBTI type
selected_mbti = st.selectbox(
    "💡 당신의 MBTI 유형을 선택하세요:",
    options=[""] + list(career_suggestions.keys())
)

# Display career suggestions based on the selected MBTI type
if selected_mbti:
    st.subheader(f"✨ {selected_mbti} 유형에게 추천하는 직업 ✨")
    st.markdown("---")
    
    # Get the list of careers
    careers = career_suggestions.get(selected_mbti, [])
    
    # Display each career as a list item
    for career in careers:
        st.write(f"👉 {career}")
