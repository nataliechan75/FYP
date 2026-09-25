"""
第二關：畫購物籃（用 HTML Canvas 嵌入）
"""
import streamlit as st
from pathlib import Path


def render():
    # 檢查係咪完成咗
    if st.query_params.get("game_done") == "game2":
        st.query_params.clear()
        st.session_state.scores["game2"] = {"completed": True}
        from core.state import next_game
        next_game()
        return

    # 載入 HTML
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
