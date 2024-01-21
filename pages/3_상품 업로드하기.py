import json

import streamlit as st

from libs.domeggook import Domeggok
from libs.naver_commerce import NaverCommerce
from libs.utils.prettier import icon, interger_prettier, string_to_interger

st.set_page_config("상품 업로드", "🚥", layout="wide")

icon("🚥")
st.title("상품 업로드")
st.divider()

PRODUCT_SIZE = 7
total_page = -1


def get_page():
    return st.session_state.get("pg", 1)


def set_page(pg: int):
    st.session_state.pg = pg


@st.cache_resource()
def __get_products():
    with open("selected_products.txt", "r") as f:
        products = [json.loads(p.strip()) if isinstance(p, str) else p for p in f.readlines()]
    return products


def get_products(pg: int):
    products = __get_products()
    start = (pg - 1) * PRODUCT_SIZE
    end = pg * PRODUCT_SIZE
    return products[start:end]


def get_products_next():
    page = get_page()
    pg = page + 1
    set_page(pg)


def get_products_before():
    page = get_page()
    pg = page - 1 if page > 1 else 1
    set_page(pg)


def __delete_product(page: int, idx: int):
    delete_line_number = (page - 1) * PRODUCT_SIZE + idx
    print(delete_line_number)
    products = __get_products()
    products.pop(delete_line_number)

    with open("selected_products.txt", "w") as f:
        f.writelines([json.dumps(p) + "\n" for p in products])

    st.rerun()


def delete_product(page: int, idx: int):
    st.toast("삭제되었습니다", icon="❌")
    __delete_product(page, idx)


def upload_product(page, idx, product, sale_price):
    try:
        with open("uploaded_products.txt", "a") as f:
            f.write(json.dumps(__get_products()[(page - 1) * PRODUCT_SIZE + idx]) + "\n")

        dom = Domeggok()
        raw_detail = dom.getItemDetail(product["no"])
        upload_data = dom.change_D_to_Naver(raw_detail, sale_price)
        NaverCommerce().upload(upload_data)
        st.toast("업로드되었습니다", icon="⭕️")
        __delete_product(page, idx)
    except Exception as e:
        st.error(e)
        st.toast("업로드에 실패하였습니다", icon="❌")


def get_button_status(idx: int):
    if st.session_state.get("button", None) is None:
        st.session_state.button = [False] * PRODUCT_SIZE
    return st.session_state.button[idx]


def set_button_status(idx: int, status: bool):
    st.session_state.button[idx] = status


@st.cache_data()
def search_product_detail(*args, **kwargs):
    no = kwargs.get("no")
    dom = Domeggok()
    raw_detail = dom.getItemDetail(no)
    result = dom.get_item_detail_handler(raw_detail)

    for key, val in [
        ["상태", result["status"]],
        ["키워드", ", ".join(result["keywords"])],
        ["가격", interger_prettier(result["price"])],
        ["카테고리", " > ".join([c["name"] for c in result["category"]])],
        ["옵션", result["options"]],
    ]:
        col1, col2 = st.columns([1, 3])
        col1.write(key)
        if "옵션" == key:
            c1, c2, c3 = col2.columns([1, 2, 1])
            c1.write("번호")
            c2.write("옵션명")
            c3.write("가격")
            for i, v in enumerate(val):
                c1.write(f"{i + 1})")
                c2.write(v["name"])
                c3.write(f"+ {interger_prettier(v['domPrice'])} 원")
        else:
            col2.write(val)

    st.write(result["description"], unsafe_allow_html=True)
    st.write(result["detail"], unsafe_allow_html=True)


with st.container():
    col1, col2 = st.columns([4, 1])
    page = get_page()

    products = get_products(pg=page)
    close_box = [False * len(products)]
    for idx, product in enumerate(products):
        col1, col2, col3, col4 = st.columns([2, 4, 1, 1])

        col1.image(product["thumb"], width=100)
        col2.markdown(f"[{product['title']}]({product['url']})")
        c1, c2 = col2.columns([1, 2])
        c1.write("판매가")
        c2.text_input(
            label="hidden",
            label_visibility="collapsed",
            key=f"{idx}_sale_price",
            value=string_to_interger(product["price"]),
            help="판매가를 입력하세요",
        )

        if col3.button(
            "업로드",
            key=f"{idx}_upload",
            use_container_width=True,
            type="primary",
        ):
            upload_product(
                page=get_page(),
                idx=idx,
                product=product,
                sale_price=st.session_state.get(f"{idx}_sale_price", 0),
            )
        if col4.button(
            "삭제",
            key=f"{idx}_delete",
            use_container_width=True,
        ):
            delete_product(page=get_page(), idx=idx)
        st.button(
            "상세 정보 닫기" if get_button_status(idx) else "상세 정보 보기",
            key=f"{idx}_detail",
            use_container_width=True,
            on_click=set_button_status,
            args=(idx, not get_button_status(idx)),
        )
        if get_button_status(idx):
            with st.expander("상세 정보", expanded=True):
                search_product_detail(no=product["no"])

        st.divider()


with st.container():
    col1, _, col2, col3 = st.columns([1, 5, 7, 1])
    total_page = len(__get_products()) // PRODUCT_SIZE + 1

    if col1.button(
        "이전",
        key="previous",
        on_click=get_products_before,
        disabled=get_page() == 1,
        use_container_width=True,
    ):
        st.rerun()

    col2.write(f"{get_page()} / {total_page} 페이지" if total_page > 0 else "")
    if col3.button(
        "다음",
        key="next",
        on_click=get_products_next,
        disabled=len(products) < PRODUCT_SIZE,
        use_container_width=True,
    ):
        st.rerun()
