"""
第一關：接線遊戲（用 HTML Canvas 嵌入 + JS 注入數據）
"""
import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import time
import json


def render():
    # 記錄開始時間
    if "game1_start" not in st.session_state:
        st.session_state.game1_start = time.time()

    # 載入 HTML
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

    # 顯示 HTML
    components.html(html_content, height=500, scrolling=False)

    # ★ 隱藏 text_input（接收 HTML 注入嘅數據）★
    with st.form(key="game1_form", clear_on_submit=False):
        # 隱藏嘅 input（玩家睇唔到）
        result_json = st.text_input(
            "result",
            key="game1_result",
            label_visibility="collapsed",
        )

        # 完成按鈕
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submitted = st.form_submit_button(
                "➡️ 去下一關",
                use_container_width=True,
                type="primary",
            )

        if submitted:
            # 讀 HTML 注入嘅數據
            data = {}
            if result_json:
                try:
                    data = json.loads(result_json)
                except Exception as e:
                    data = {"raw": result_json, "error": str(e)}

            # 記錄時間
            elapsed = time.time() - st.session_state.game1_start

            # 儲存數據
            st.session_state.scores["game1"] = {
                "total_time_sec": round(elapsed, 2),
                "completed_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "is_correct": data.get("is_correct", None),
                "sequence": data.get("sequence", []),
                "undo_count": data.get("undo_count", 0),
                "score": 1 if data.get("is_correct") else 0,
            }

            # 跳下一關
            from core.state import next_game
            next_game()
