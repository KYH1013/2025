import streamlit as st
import birthdata
from datetime import datetime

st.set_page_config(page_title="생일 정보 확인", layout="centered")
st.title("🎉 나의 생일 정보 확인 웹사이트")

dob = st.date_input("생년월일을 선택하세요", datetime(2000,1,1))

if dob:
    month = dob.month
    day = dob.day
    year = dob.year

    st.subheader(f"🎂 {dob.strftime('%Y년 %m월 %d일')} 정보")

    # ----- 2x2 카드 레이아웃 -----
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    # 탄생화
    month_day_key = f"{month:02d}-{day:02d}"   # 예: 01-01
    flower = birthdata.BIRTH_FLOWERS_BY_DAY.get(month_day_key)
    with col1:
        if flower:
            st.markdown(f"""
            <div style="background:#fff0f6; border-radius:12px; padding:20px; text-align:center; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
                <h3>🌸 탄생화</h3>
                <p style="font-size:20px; font-weight:bold;">{flower['name']}</p>
                <p>{flower['meaning']}</p>
            </div>
            """, unsafe_allow_html=True)

    # 탄생석
    stone = birthdata.BIRTH_STONES.get(month)
    with col2:
        if stone:
            st.markdown(f"""
            <div style="background:#e6f7ff; border-radius:12px; padding:20px; text-align:center; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
                <h3>💎 탄생석</h3>
                <p style="font-size:20px; font-weight:bold;">{stone['name']}</p>
                <p>{stone['meaning']}</p>
            </div>
            """, unsafe_allow_html=True)

    # 별자리
    sign, sign_emoji = birthdata.get_zodiac(month, day)
    with col3:
        st.markdown(f"""
        <div style="background:#f9f9f9; border-radius:12px; padding:20px; text-align:center; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
            <h3>✨ 별자리</h3>
            <p style="font-size:20px; font-weight:bold;">{sign} {sign_emoji}</p>
        </div>
        """, unsafe_allow_html=True)

    # 띠
    chinese_zodiac = birthdata.get_chinese_zodiac(year)
    with col4:
        st.markdown(f"""
        <div style="background:#f6ffed; border-radius:12px; padding:20px; text-align:center; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
            <h3>🐲 띠</h3>
            <p style="font-size:20px; font-weight:bold;">{chinese_zodiac}</p>
        </div>
        """, unsafe_allow_html=True)

    # 월별 기념일
    month_day_key = f"{month:02d}-{day:02d}"
    holidays = birthdata.HOLIDAYS_BY_DAY.get(month_day_key, [])
    if holidays:
        st.write(f"🎉 **기념일:** {', '.join(holidays)}")


# -------------------------------
# 🔮 사주 코드 추가 (이전 코드 유지)
# -------------------------------

st.subheader("🔮 사주 팔자 간단 보기")

include_hour = st.checkbox("태어난 시 입력하기")
hour = None
if include_hour:
    hour = st.selectbox("태어난 시(24시간제)", list(range(24)), format_func=lambda x: f"{x}시")

def get_saju(year, month, day, hour=None):
    gan = ["갑","을","병","정","무","기","경","신","임","계"]
    ji  = ["자","축","인","묘","진","사","오","미","신","유","술","해"]

    year_gan = gan[year % 10]
    year_ji  = ji[year % 12]

    month_gan = gan[(year + month) % 10]
    month_ji  = ji[month % 12]

    day_gan = gan[(year + month + day) % 10]
    day_ji  = ji[day % 12]

    saju = {
        "년주": f"{year_gan}{year_ji}",
        "월주": f"{month_gan}{month_ji}",
        "일주": f"{day_gan}{day_ji}",
    }

    if hour is not None:
        hour_gan = gan[(day + hour) % 10]
        hour_ji  = ji[(hour % 12)]
        saju["시주"] = f"{hour_gan}{hour_ji}"

    return saju

if dob:
    saju = get_saju(dob.year, dob.month, dob.day, hour)

    cols = st.columns(4 if "시주" in saju else 3)
    i = 0
    for key, value in saju.items():
        with cols[i]:
            st.markdown(f"""
            <div style="
                background:#fdfdfd;
                border-radius:12px;
                padding:20px;
                text-align:center;
                box-shadow:0 4px 10px rgba(0,0,0,0.1);
                ">
                <h3>{key}</h3>
                <p style="font-size:24px; font-weight:bold;">{value}</p>
            </div>
            """, unsafe_allow_html=True)
        i += 1
