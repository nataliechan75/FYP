"""
第一關：接線遊戲（用 HTML Canvas 嵌入）
"""
import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import time


def render():
    if "game1_start" not in st.session_state:
        st.session_state.game1_start = time.time()

    html_path = (
        Path(__file__).parent.parent
        / "components"
        / "connect_coins_component"
        / "frontend"
        / "index.html"
    )

    if not html_path.exists():
        st.error("❌ 搵唔到 index.html")
        return

    html_content = html_path.read_text(encoding="utf-8")

    components.html(html_content, height=500, scrolling=False)

    # 完成按鈕
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("➡️ 去下一關", type="primary", use_container_width=True, key="next_1"):
            elapsed = time.time() - st.session_state.game1_start

            st.session_state.scores["game1"] = {
                "total_time_sec": round(elapsed, 2),
                "completed_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            }

            from core.state import next_game
            next_game()
