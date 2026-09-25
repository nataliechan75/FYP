"""
第一關：接線遊戲（用 HTML Canvas 嵌入）
"""
import streamlit as st
from pathlib import Path


def render():
    # ★ 檢查係咪完成咗（從 URL）
    if st.query_params.get("game_done") == "connect_coins":
        st.query_params.clear()
        st.session_state.scores["connect_coins"] = {"completed": True}
        from core.state import next_game
        next_game()
        return

    # 載入 HTML
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
