import streamlit as st
from ultralytics import YOLO
import tempfile
import os
import shutil

# 캐싱: 모델을 한 번만 로드하여 앱 실행 속도를 높입니다.
@st.cache_resource
def load_model(model_path):
    """지정된 경로에서 YOLO 모델을 로드합니다."""
    model = YOLO(model_path)
    return model

st.title("동물 트래킹 앱")

model = load_model("best.pt")
# 동영상 업로드 위젯
uploaded_file = st.file_uploader("동물 영상을 업로드하세요", type=["mp4", "mov", "avi"])

if uploaded_file:
    # 새 영상이 업로드되면 이전 결과 삭제
    if 'result_video_bytes' in st.session_state:
        del st.session_state.result_video_bytes
    
    col1, col2 = st.columns(2)

    # --- 원본 영상 표시 ---
    with col1:
        st.header("원본 영상")
        st.video(uploaded_file)
        
        if st.button("탐지 실행"):
            with st.spinner("영상을 처리 중입니다..."):
                # 1. 업로드된 영상을 임시 파일로 저장
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tfile:
                    tfile.write(uploaded_file.getvalue())
                    video_path = tfile.name
                
                # 2. YOLO 모델로 영상 트래킹 실행
                results = model.track(video_path, save=True)
                
                # 3. 결과 처리
                if results:
                    save_dir = results[0].save_dir
                    # 결과 폴더에서 비디오 파일 찾기
                    result_video_files = [f for f in os.listdir(save_dir) if f.endswith(('.mp4', '.avi', '.mov'))]
                    
                    if result_video_files:
                        result_video_path = os.path.join(save_dir, result_video_files[0])
                        # 결과 영상을 읽어서 메모리(bytes)에 저장
                        with open(result_video_path, 'rb') as f:
                            video_bytes = f.read()
                        st.session_state.result_video_bytes = video_bytes
                    else:
                        st.error("처리된 결과 비디오를 찾지 못했습니다.")

                    # 처리 후 임시 결과 폴더 삭제
                    shutil.rmtree(save_dir)
                else:
                    st.error("트래킹 결과가 없습니다.")
                
                # 처리 후 임시 입력 파일 삭제
                os.unlink(video_path)

    # --- 탐지 결과 표시 ---
    with col2:
        st.header("탐지 결과")
        if 'result_video_bytes' in st.session_state:
            st.video(st.session_state.result_video_bytes)
        else:
            st.write("'탐지 실행' 버튼을 눌러주세요.")
else:
    st.info("동물 영상을 업로드하여 트래킹을 시작하세요.")

