"""
第一關：接線遊戲
"""
import streamlit as st
import streamlit.components.v1 as components
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

    # 1. 遊戲
    components.html(html_content, height=630, scrolling=False)

    # 2. text_input
    result_json = st.text_input(
        "result",  # ← 冇 label_visibility
        key="game1_result",
    )

    # 3. 完成按鈕
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        submitted = st.button(
            "➡️ 去下一關",
            use_container_width=True,
            type="primary",
            key="next_1",
        )

    # 4. 提交
    if submitted:
        # ★ 用 session_state 攞最新值（唔靠 result_json 變數）★
        latest_result = st.session_state.get("game1_result", "")

        # DEBUG
        st.write("**DEBUG - result_json 變數：**", repr(result_json))
        st.write("**DEBUG - session_state 最新值：**", repr(latest_result))

        data = {}
        if latest_result:
            try:
                data = json.loads(latest_result)
            except Exception as e:
                data = {"raw": latest_result, "error": str(e)}

        st.write("**DEBUG - 解析後：**", data)

        elapsed = time.time() - st.session_state.game1_start

        st.session_state.scores["connect_coins"] = {
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
