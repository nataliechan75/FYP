"""
第一關：接線遊戲（用 HTML Canvas 嵌入 + streamlit-js-eval）
"""
import streamlit as st
import streamlit.components.v1 as components
from streamlit_js_eval import streamlit_js_eval
from pathlib import Path
import time
import json


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

    # 顯示 HTML 遊戲
    components.html(html_content, height=600, scrolling=False)

    # ★ 用 streamlit_js_eval 讀 HTML 內部變數 ★
    # ⚠️ 但 iframe 內部嘅 window 同 top frame 唔同
    # 所以要先喺 HTML 內部將數據寫入 top frame
    result_str = streamlit_js_eval(
        js_expressions="window.parent.gameResult || window.gameResult || null",
        key="game1_result",
    )

    # 顯示 debug（你睇到）
    if result_str:
        st.write("**接收數據：**", result_str)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("➡️ 去下一關", use_container_width=True, type="primary", key="next_1"):
            data = {}
            if result_str:
                try:
                    data = json.loads(result_str) if isinstance(result_str, str) else result_str
                except Exception as e:
                    data = {"raw": str(result_str), "error": str(e)}

            elapsed = time.time() - st.session_state.game1_start

            st.session_state.scores["game1"] = {
                "total_time_sec": round(elapsed, 2),
                "completed_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "is_correct": data.get("is_correct", None),
                "sequence": data.get("sequence", []),
                "undo_count": data.get("undo_count", 0),
                "has_crossing": data.get("has_crossing", None),
                "is_order_correct": data.get("is_order_correct", None),
                "score": 1 if data.get("is_correct") else 0,
            }

            from core.state import next_game
            next_game()
