import json
from typing import Any, Dict, List

import streamlit as st

from libs.domeggook import Domeggok
from libs.utils.prettier import icon, interger_prettier

st.set_page_config("도매꾹 상품 검색", "🎪", layout="wide")

icon("🎪")
st.title("도매꾹 상품 검색")


PRODUCT_SIZE = 5
selected_products = st.session_state.get("selected_products", [False] * PRODUCT_SIZE)


def store_list(products: List[Dict[str, Any]]):
    st.session_state.products = products
    st.rerun()


def reset_selected_products():
    st.session_state.selected_products = [False] * PRODUCT_SIZE
    st.rerun()


def set_selected_products(selected_products):
    st.session_state.selected_products = selected_products


def set_page(pg):
    st.session_state.pg = pg


def get_page():
    return st.session_state.get("pg", 1)


def get_search_keyword():
    return st.session_state.get("search_keyword", "").strip()


def get_keyword():
    return st.session_state.get("keyword", "").strip()


@st.cache_data()
def search_keyword_with_store_page_before(search_keyword=None):
    if search_keyword is None:
        search_keyword = get_search_keyword()

    pg = get_page()
    pg = pg - 1 if pg > 1 else 1
    set_page(pg)

    search_keyword_with_store_page(search_keyword)


@st.cache_data()
def search_keyword_with_store_page_next(search_keyword=None):
    if search_keyword is None:
        search_keyword = get_search_keyword()

    pg = get_page()
    pg = pg + 1 if pg < st.session_state.get("number_of_pages", 1) else pg
    set_page(pg)

    search_keyword_with_store_page(search_keyword)


@st.cache_data()
def search_keyword_with_store_page(search_keyword):
    pg = get_page()
    result = Domeggok().getItemList(ev="", ca="", kw=search_keyword, pg=pg, sz=5)

    st.session_state.number_of_items = result["numberOfItems"]
    st.session_state.number_of_pages = result["numberOfPages"]
    store_list(result["list"])


@st.cache_data()
def store_search_keyword():
    if keyword := get_keyword():
        st.session_state.search_keyword = keyword
        st.session_state.keyword = ""

    if search_keyword := get_search_keyword():
        search_keyword_with_store_page(search_keyword)


def save_products():
    selected_products = st.session_state.selected_products
    products = st.session_state.products
    with open("selected_products.txt", "a") as f:
        for selected, product in zip(selected_products, products):
            if selected:
                f.write(json.dumps(product) + "\n")
    reset_selected_products()


# Search
with st.form(key="2_search_box", clear_on_submit=True):
    col1, col2, col3 = st.columns([3, 1, 1])
    keyword = col1.text_input(
        label="검색어",
        placeholder="키워드 검색",
        value=st.session_state.get("keyword", ""),
        key="keyword",
    )
    sorting = col2.selectbox(label="정렬", key="sorting", options=["정확도 순", "최신 순", "가격 순"])
    if col3.form_submit_button(use_container_width=True, on_click=store_search_keyword, label="검색"):
        st.rerun()


with st.container():
    search_products = st.session_state.get("products", [])
    search_keyword = st.session_state.get("search_keyword", "")

    number_of_items = interger_prettier(st.session_state.get("number_of_items", 0))
    number_of_items = f"총 {number_of_items}개"

    sort = st.session_state.get("sorting", "정확도 순")
    col1, col2, col3 = st.columns([3, 1, 1])
    col1.subheader(f"🔍 {search_keyword} 검색 결과 ({number_of_items})" if search_keyword else "")
    if col2.button(
        "업로드",
        key="upload",
        on_click=save_products,
        type="primary",
        disabled=not search_products,
        use_container_width=True,
    ):
        st.toast("상품 업로드 성공", icon="🎉")
    if col3.button(
        "전체 삭제",
        key="delete_all",
        on_click=reset_selected_products,
        type="secondary",
        disabled=not search_products,
        use_container_width=True,
    ):
        st.toast("상품 삭제 성공", icon="🚨")

    st.write("")
    st.write("")

    col1, col2, col3, col4 = st.columns([3, 3, 2, 1])
    col1.write("상품 이미지")
    col2.write("🏷️ 상품명")
    col3.write("💰 상품 가격")
    col4.write("선택 여부")


with st.container(border=True, height=500 if not search_products else None):
    if products := st.session_state.get("products", []):
        if len(selected_products := st.session_state.get("selected_products", [False * len(products)])) != len(
            products
        ):
            selected_products = [False] * len(products)
            set_selected_products(selected_products)

        for idx, product in enumerate(products):
            selected = selected_products[idx]
            col1, col2, col3, col4 = st.columns([2, 5, 2, 1])
            col1.image(product["thumb"], width=100)
            col2.markdown(f"[{product['title']}]({product['url']})")
            col3.write(product["price"])
            if col4.button(
                label="선택" if not selected else "삭제",
                key=idx,
                type="secondary" if not selected else "primary",
                use_container_width=True,
            ):
                selected_products[idx] = True if not selected else False
                set_selected_products(selected_products)
                st.rerun()
            st.divider()
    else:
        if search_keyword:
            st.write("검색 결과가 없습니다.")

with st.container():
    col1, _, col2, col3 = st.columns([1, 5, 7, 1])
    if col1.button(
        "이전",
        key="previous",
        on_click=search_keyword_with_store_page_before,
        disabled=get_page() == 1,
        use_container_width=True,
    ):
        reset_selected_products()
    col2.write(f"{get_page()} 페이지")
    if col3.button(
        "다음",
        key="next",
        on_click=search_keyword_with_store_page_next,
        disabled=get_page() == st.session_state.get("number_of_pages", 1),
        use_container_width=True,
    ):
        reset_selected_products()
