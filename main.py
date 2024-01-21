from typing import List

import streamlit as st

from libs.utils.prettier import icon

st.set_page_config("메인 페이지", "💨", layout="wide")
COLUMN_SIZE = [4, 1]

icon("💨")
st.title("메인 페이지")
st.subheader("사용방법", anchor="usage")
st.write("1. OpenAI와의 대화를 통해 상품 키워드를 추천받습니다.")
st.write("2. 도매샵 검색 API를 사용하여 해당 키워드로 나온 상품들을 대시보드 리스트로 확인합니다.")
st.write("3. 원하는 상품을 선택하고 업로드 버튼을 클릭합니다.")
st.write("4. 도매샵 상세 정보 검색 API를 통해 올릴 상품에 대한 정보를 가져온 후, 네이버 스마트스토어 상품 업로드 API를 사용하여 상품을 올립니다.")

st.write("")
st.write("")
st.subheader("피드백 요청 사항", anchor="feedback")


def save_feedback():
    feedback = st.session_state.feedback
    with open("feedback.txt", "a") as f:
        f.writelines(feedback.strip() + "\n")
    st.session_state.feedback = ""


def read_feedback():
    with open("feedback.txt", "r") as f:
        feedbacks = f.readlines()
    return feedbacks


def pop_feedback(feedbacks: List[str], idx: int):
    feedbacks.pop(idx)
    with open("feedback.txt", "w") as f:
        f.writelines(feedbacks)
    st.rerun()


# set feedback text and button in one line
with st.form(key="1_feedback_box", clear_on_submit=True):
    col1, col2 = st.columns(COLUMN_SIZE)
    col1.text_input(
        label="피드백",
        label_visibility="hidden",
        key="feedback",
        placeholder="피드백을 입력해주세요.",
        max_chars=1000,
        value=st.session_state.get("feedback", ""),
    )
    col2.form_submit_button(use_container_width=True, on_click=save_feedback)

with st.container():
    feedbacks = read_feedback()
    for idx, feedback in enumerate(feedbacks[::-1]):
        col1, col2 = st.columns(COLUMN_SIZE)
        col1.write(f"✔️ {feedback}")

        if col2.button("Delete", key=f"delete_{idx}", use_container_width=True):
            pop_feedback(feedbacks, len(feedbacks) - 1 - idx)
