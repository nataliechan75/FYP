"""
第二關：畫購物籃（用 HTML Canvas 嵌入）
"""
import streamlit as st
from pathlib import Path


def render():
    html_path = Path(__file__).parent.parent / "components" / "game2.html"

    if not html_path.exists():
        st.error("❌ 搵唔到 game2.html")
        return

    html_content = html_path.read_text(encoding="utf-8")

    st.components.v1.html(
        html_content,
        height=900,
        scrolling=False,
    )

    st.divider()
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("➡️ 去下一關", use_container_width=True, type="primary"):
            from core.state import next_game
            next_game()
