"""
第六關：抽象概念（用 HTML + Web Speech API 嵌入）
"""
import streamlit as st
from pathlib import Path


def render():
    html_path = Path(__file__).parent.parent / "components" / "game6.html"

    if not html_path.exists():
        st.error("❌ 搵唔到 game6.html")
        return

    html_content = html_path.read_text(encoding="utf-8")

    st.components.v1.html(
        html_content,
        height=800,
        scrolling=False,
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("➡️ 去下一關", use_container_width=True, type="primary", key="next_6"):
            from core.state import next_game
            next_game()
