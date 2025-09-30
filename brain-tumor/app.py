import streamlit as st
from PIL import Image
from ultralytics import YOLO

# 캐싱 (결과를 메모리에 저장해두고 재사용 -> 시간이 오래 걸리고 무거운 작업을 매번 반복하지 않게 해줌 => 효율 상승)
@st.cache_resource
def load_model(model_path):
    model = YOLO(model_path)
    return model

st.title("뇌종양 탐지 앱")

# 모델 로드 (앱이 실행될 때 한 번만 로드됩니다)
model = load_model("./best.pt")

# 사용자에게 이미지 업로드 받기 (형식 지정할 수 있음)
uploaded_file = st.file_uploader("MRI 이미지를 업로드하세요", type=["png", "jpg", "jpeg"])

#streamlit은 사용자 이벤트가 발생하면 스크립트의 전체가 처음부터 끝까지 다시 실행이됨
#=> 변수를 설정할 경우 계속 기억하는게 아니라 이벤트가 발생할 때 마다 초기화 됨
#st.session_state : 단기 기억 저장소 사용
#이미지를 업로드하여 결과를 본 상황 -> 해당 이미지 저장
#이미지를 삭제하거나 다른 이미지를 업로드 -> 해당 이미지를 삭제

#st.session_state['result_image'] = result_image => streamlit 객체

if uploaded_file is not None:
    # 새로운 파일이 업로드되면 이전 탐지 결과 이미지를 세션 상태에서 제거합니다.
    # 이렇게 하면 새로운 이미지 업로드 시 '탐지 실행' 버튼을 누르기 전까지는 결과 이미지가 보이지 않습니다.
    if 'result_image' in st.session_state:
        del st.session_state.result_image
    
    # 업로드된 이미지를 PIL 이미지로 변환
    original_image = Image.open(uploaded_file)
    
    # 가로 배치를 위해 2개의 컬럼을 생성합니다.
    col1, col2 = st.columns(2)

    # 첫 번째 컬럼(col1)에 원본 이미지와 '탐지 실행' 버튼을 배치합니다.
    with col1:
        st.header("원본 이미지")
        st.image(original_image, use_container_width=True)
        
        # '탐지 실행' 버튼을 원본 이미지 아래에 위치시킵니다.
        if st.button("탐지 실행"):
            # 버튼이 눌리면 모델 추론을 실행합니다.
            with st.spinner("탐지 중..."):
                results = model(original_image)
                result_plot = results[0].plot()
                #YOLO와 PIL의 색상 표준이 다름 YOLO(BGR) / PIL(RGB)
                result_image = Image.fromarray(result_plot[..., ::-1])
                
                # 결과 이미지를 session_state에 저장하여 상태를 유지합니다.
                st.session_state.result_image = result_image
        
    # 두 번째 컬럼(col2)에 탐지 결과를 표시합니다.
    with col2:
        st.header("탐지 결과")
        
        # session_state에 결과 이미지가 있으면 표시합니다.
        if 'result_image' in st.session_state:
            st.image(st.session_state.result_image, use_container_width=True)
        else:
            # 버튼을 누르기 전, 안내 문구를 표시합니다.
            st.write("'탐지 실행' 버튼을 눌러주세요.")
else:
    # 파일이 업로드되지 않았을 때 (초기 상태 또는 파일 삭제 시)
    # result_image 세션 상태를 초기화하여 이전 결과가 보이지 않게 합니다.
    if 'result_image' in st.session_state:
        del st.session_state.result_image
    st.write("MRI 이미지를 업로드하여 뇌종양을 탐지하세요")