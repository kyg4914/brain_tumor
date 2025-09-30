import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np
import time 

# 앱 제목
st.title('(제목) 나의 첫 Streamlit 앱')

# 텍스트 출력
st.write("(단순 글씨 작성) 앱 띄우기 성공! 🎉")

# 버튼 추가
if st.button('(버튼) 눌러보세요'):
    st.balloons()

#큰 제목 (주요 섹션을 나누는데 유용)
st.header("(헤더)기본 텍스트 출력")

#소 제목 (header 하위 제목)
st.subheader("(서브헤더)")

#마크다운 (마크다운 문법 사용)
st.markdown("(마크다운)**굵은 글씨**와 *이탤릭체* 사용")

#설명 (설명이나 주석 작성, 작고 옅은 글씨로 표시됨)
st.caption("(설명) 이것은 캡션(설명)입니다.")

#코드블럭 (파이썬 or 다른 프로그래밍 언어 코드 출력)
st.code("""
        def hello():
            print("Hello, Streamlit!")
        """, language="python")



#큰 제목 (주요 섹션을 나누는데 유용)
st.header("사용자 입력")
    
name = st.text_input("이름을 입력하세요")
st.write(f"입력된 이름: {name}")

age = st.number_input("나이를 입력하세요", min_value=0, max_value=100, step=1)
st.write(f"입력된 나이: {age}")

selected_date = st.date_input("날짜 선택")
st.write(f"선택한 날짜: {selected_date}")

selected_time = st.time_input("시간 선택")
st.write(f"선택한 시간: {selected_time}")

message = st.text_area("메시지를 입력하세요")
st.write(f"입력된 메시지:\n{message}")

uploaded_file = st.file_uploader("파일을 업로드하세요")
if uploaded_file is not None:
    st.write("업로드된 파일:", uploaded_file.name)

#큰 제목 (주요 섹션을 나누는데 유용)
st.header("선택형 입력(버튼 등)")

if st.button("클릭하세요"):
    st.write("버튼이 클릭되었습니다!")

agree = st.checkbox("동의합니다")
if agree:
    st.write("동의하셨습니다!")

selected_option = st.radio("옵션을 선택하세요", ("옵션 1", "옵션 2", "옵션 3"))
st.write(f"선택된 옵션: {selected_option}")

fruit = st.selectbox("과일을 선택하세요", ["사과", "바나나", "오렌지"])
st.write(f"선택한 과일: {fruit}")

planets = st.multiselect("행성을 선택하세요", ["목성", "화성", "해왕성"])
st.write(f"선택한 행성: {planets}")

number = st.slider("숫자를 선택하세요", 0, 50)
st.write(f"선택된 숫자: {number}")

rating = st.select_slider("평가를 선택하세요", ["나쁨", "보통", "좋음", "최고"])
st.write(f"선택한 평가: {rating}")

#큰 제목 (주요 섹션을 나누는데 유용)
st.header("데이터 출력")

#PIL 추가
image = Image.open("brain.jpg")
st.image(image, caption="예제 이미지", use_container_width=True)

st.video("car.mp4")

df = {
    '이름': ['철수', '영희', '민준', '서연'],
    '나이': [24, 21, 29, 25],
    '도시': ['서울', '부산', '서울', '광주']
}

st.write(df)

st.dataframe(df)

st.table(df)

st.metric(label="LG전자", value="78,000원", delta="2.12%")
st.metric(label="현대차", value="150,000원", delta="-1.25%")


st.header("차트/그래프 활용")

#pandas, numpy 추가
df = pd.DataFrame(np.random.randn(10, 2), columns=['x', 'y'])
st.line_chart(df)

df = pd.DataFrame(np.random.randn(10, 2), columns=['x', 'y'])
st.bar_chart(df)

st.header("상태 메시지 및 진행률 표시")

#time 추가
progress_bar = st.progress(0)  # 초기값 0

for percent in range(0, 101, 10):
    time.sleep(0.1)  # 프로세스 진행 시뮬레이션
    progress_bar.progress(percent)  # 진행률 업데이트

with st.spinner("잠시만 기다려 주세요..."):
    time.sleep(5)  # 대기 시간 시뮬레이션
st.success("작업 완료!")

st.error("오류가 발생했습니다. 다시 시도해주세요.")
st.warning("이 작업은 주의가 필요합니다.")
st.info("Streamlit을 사용하면 쉽게 웹 앱을 만들 수 있습니다.")


#Streamlit Component 활용
#1. Sidebar
st.sidebar.title("사이드바 메뉴")
st.sidebar.write("여기에 설정을 추가할 수 있습니다.")
st.sidebar.button("사이드바 버튼")


tab1, tab2 = st.tabs(['Cat', 'Dog'])

with tab1:
    st.header('고양이')
    st.image('https://imgnn.seoul.co.kr/img/upload/2024/08/06/SSC_20240806100040.jpg')

with tab2:
    st.header('강아지')
    st.image('https://i.namu.wiki/i/slmFMXb1Fchs2zN0ZGOzqfuPDvhRS-H9eBp7Gp613-DNKi6i6Ct7eFkTUpauqv5HAYR97mrNqrvvcCDEyBdL_g.webp')