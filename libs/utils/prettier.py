import re
from typing import Union

import streamlit as st


def icon(emoji: str):
    """Shows an emoji as a Notion-style page icon."""
    return st.write(
        f'<span style="font-size: 78px; line-height: 1">{emoji}</span>',
        unsafe_allow_html=True,
    )


def interger_prettier(val: Union[str, int]):
    """Shows a val with comma."""
    if isinstance(val, str):
        val = re.sub(r"[^\d]", "", val)
        val = int(val)
    return f"{val:,}"


def string_to_interger(val: Union[str, int]):
    if isinstance(val, str):
        val = re.sub(r"[^\d]", "", val)
        val = int(val)
    return val
