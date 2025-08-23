import streamlit as st
import birthdata
from datetime import datetime

st.set_page_config(page_title="생일 정보 확인", layout="centered")
st.title("🎉 나의 생일 정보 확인 웹사이트")

# 날짜 선택
dob = st.date_input("생년월일을 선택하세요", datetime(2000, 1, 1))

if dob:
    month = dob.month
    day = dob.day
    year = dob.year

    st.subheader(f"🎂 {dob.strftime('%Y년 %m월 %d일')} 정보")

    # 카드 스타일 + 2*2 그리드 (한눈에 보이도록 조정)
    st.markdown("""
        <style>
        .grid-container {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            justify-content: space-between;  /* 좌우 여백을 자동으로 맞춤 */
            margin-top: 20px;
        }
        .card {
            flex: 0 0 calc(50% - 20px); /* 두 개씩 배치, 카드 간격을 20px로 유지 */
            background-color: #f8f9fc;
            border-radius: 15px;
            padding: 20px;
            box-sizing: border-box;
            min-width: 250px;
            max-width: 300px;  /* 카드 크기 최적화 */
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            text-align: center;
            transition: all 0.2s ease;
        }
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
        }
        .card h3 {
            font-size: 22px;
            color: #333333;
            margin-bottom: 10px;
            font-weight: bold;
        }
        .card p {
            font-size: 16px;
            color: #555555;
            line-height: 1.5;
            margin-bottom: 0;
        }
        .card .emoji {
            font-size: 35px;
            margin-bottom: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

    month_day_key = f"{month:02d}-{day:02d}"

    # 카드 컨테이너 시작
    st.markdown('<div class="grid-container">', unsafe_allow_html=True)

    # 탄생화
    flower = birthdata.BIRTH_FLOWERS_BY_DAY.get(month_day_key)
    if flower:
        st.markdown(f"""
        <div class="card">
            <div class="emoji">🌸</div>
            <h3>탄생화</h3>
            <p><strong>{flower['name']}</strong><br><i>{flower['meaning']}</i></p>
        </div>
        """, unsafe_allow_html=True)

    # 탄생석
    stone = birthdata.BIRTH_STONES.get(month)
    if stone:
        st.markdown(f"""
        <div class="card">
            <div class="emoji">💎</div>
            <h3>탄생석</h3>
            <p><strong>{stone['name']}</strong><br><i>{stone['meaning']}</i></p>
        </div>
        """, unsafe_allow_html=True)

    # 별자리
    sign, sign_emoji = birthdata.get_zodiac(month, day)
    st.markdown(f"""
    <div class="card">
        <div class="emoji">✨</div>
        <h3>별자리</h3>
        <p><strong>{sign}</strong> {sign_emoji}</p>
    </div>
    """, unsafe_allow_html=True)

    # 띠
    chinese_zodiac = birthdata.get_chinese_zodiac(year)
    st.markdown(f"""
    <div class="card">
        <div class="emoji">🐲</div>
        <h3>띠</h3>
        <p><strong>{chinese_zodiac}</strong></p>
    </div>
    """, unsafe_allow_html=True)

    # 카드 컨테이너 닫기
    st.markdown('</div>', unsafe_allow_html=True)

    # 기념일은 별도 출력
    holidays = birthdata.HOLIDAYS_BY_DAY.get(month_day_key, [])
    if holidays:
        st.markdown(f"""
        <div class="card" style="max-width:600px; margin:20px auto; background-color: #fff4e6; border: 2px solid #ffcc99;">
            <h3>🎉 기념일</h3>
            <p>{', '.join(holidays)}</p>
        </div>
        """, unsafe_allow_html=True)

# 버튼 추가 예시
if st.button("더 많은 정보 보기"):
    st.write("여기에 추가적인 생일 정보가 표시됩니다!")
