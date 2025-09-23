import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# 페이지 제목 설정
st.set_page_config(
    page_title="나의 미래를 만들어보자😎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 세션 상태 초기화
# 그래프에 사용될 데이터 포인트를 저장하기 위한 리스트를 세션 상태에 저장합니다.
if "dream_path" not in st.session_state:
    st.session_state.dream_path = pd.DataFrame(columns=['age', 'happiness'])
if "realistic_path" not in st.session_state:
    st.session_state.realistic_path = pd.DataFrame(columns=['age', 'happiness'])

st.title("나의 두 가지 인생 그래프")
st.markdown("선택에 따라 달라지는 나의 미래를 그려보아요.")

st.info("🎨 **사용 방법**\n\n- 아래 슬라이더를 이용해 나이와 행복지수를 설정하고 '점 추가하기' 버튼을 누르면 그래프에 점이 추가됩니다.\n- '초기화' 버튼으로 언제든 다시 시작할 수 있어요.")

# --- 그래프 1: 내가 정말 원하는 선택을 했을 때 ---
st.header("💖 인생 그래프 1: 내가 정말 원하는 선택을 했을 때")
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("##### 점 추가하기")
    # 사용자가 나이와 행복지수를 입력할 수 있는 슬라이더를 만듭니다.
    add_age1 = st.slider("나이 (세)", min_value=15, max_value=80, value=25, key='age1')
    add_happiness1 = st.slider("행복 지수 (1-10)", min_value=1, max_value=10, value=7, key='happiness1')
    
    # 점을 추가하는 버튼을 만듭니다.
    if st.button("점 추가하기", key='add1'):
        new_point = pd.DataFrame([{'age': add_age1, 'happiness': add_happiness1}])
        st.session_state.dream_path = pd.concat([st.session_state.dream_path, new_point], ignore_index=True)
        st.session_state.dream_path = st.session_state.dream_path.sort_values(by='age')

    # 그래프를 초기화하는 버튼을 만듭니다.
    if st.button("그래프 초기화", key='reset1'):
        st.session_state.dream_path = pd.DataFrame(columns=['age', 'happiness'])

with col2:
    # Plotly를 사용하여 선 그래프를 그립니다.
    fig1 = go.Figure(
        data=go.Scatter(
            x=st.session_state.dream_path['age'], 
            y=st.session_state.dream_path['happiness'], 
            mode='lines+markers',
            marker_size=10,
            marker_color='teal',
            line_color='teal'
        )
    )
    # 그래프 레이아웃을 설정합니다.
    fig1.update_layout(
        title='내가 정말 원하는 선택을 했을 때',
        xaxis_title='나이',
        yaxis_title='행복 지수 / 만족도',
        yaxis=dict(range=[0, 10]),
        template='plotly_white',
        height=400
    )
    st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")

# --- 그래프 2: 또 다른 선택을 했을 때 ---
st.header("🧭 인생 그래프 2: 또 다른 선택을 했을 때")
col3, col4 = st.columns([1, 2])

with col3:
    st.markdown("##### 점 추가하기")
    add_age2 = st.slider("나이 (세)", min_value=15, max_value=80, value=25, key='age2')
    add_happiness2 = st.slider("행복 지수 (1-10)", min_value=1, max_value=10, value=7, key='happiness2')
    
    if st.button("점 추가하기", key='add2'):
        new_point = pd.DataFrame([{'age': add_age2, 'happiness': add_happiness2}])
        st.session_state.realistic_path = pd.concat([st.session_state.realistic_path, new_point], ignore_index=True)
        st.session_state.realistic_path = st.session_state.realistic_path.sort_values(by='age')

    if st.button("그래프 초기화", key='reset2'):
        st.session_state.realistic_path = pd.DataFrame(columns=['age', 'happiness'])

with col4:
    fig2 = go.Figure(
        data=go.Scatter(
            x=st.session_state.realistic_path['age'], 
            y=st.session_state.realistic_path['happiness'], 
            mode='lines+markers',
            marker_size=10,
            marker_color='indigo',
            line_color='indigo'
        )
    )
    fig2.update_layout(
        title='또 다른 선택을 했을 때',
        xaxis_title='나이',
        yaxis_title='행복 지수 / 만족도',
        yaxis=dict(range=[0, 10]),
        template='plotly_white',
        height=400
    )
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# --- 나의 자서전에 담을 그래프 선택하기 ---
st.header("🤔 나의 자서전에 담을 그래프 선택하기")
st.markdown("두 그래프를 비교해보고, 어떤 삶이 '가장 나다운 삶'이라고 생각되는지, 그 이유는 무엇인지 자유롭게 적어보세요.")
st.text_area(
    "나의 생각", 
    placeholder="어떤 인생 그래프가 더 마음에 와닿나요? 그 이유는 무엇인가요? 여러분의 생각을 들려주세요.",
    height=200
)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>© 2025 나의 미래 그리기 프로젝트. All rights reserved.</p>", unsafe_allow_html=True)
