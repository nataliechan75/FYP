"""
第一關：接線遊戲（用 HTML Canvas 嵌入）
"""
import streamlit as st
from pathlib import Path


def render():
    html_path = Path(__file__).parent.parent / "components" / "connect_canvas.html"

    if not html_path.exists():
        st.error("❌ 搵唔到 connect_canvas.html")
        return

    html_content = html_path.read_text(encoding="utf-8")

    st.components.v1.html(
        html_content,
        height=900,
        scrolling=False,
    )
