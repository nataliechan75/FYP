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
        / "game1.html"
    )

    if not html_path.exists():
        st.error("❌ 搵唔到 index.html")
        return

    html_content = html_path.read_text(encoding="utf-8")

    # 顯示遊戲
    components.html(html_content, height=650, scrolling=False)

    # 完成按鈕
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(
            "➡️ 去下一關",
            use_container_width=True,
            type="primary",
            key="next_1",
        ):
            # ★ 檢查有冇完成（URL query params 只有完成時才有）★
            skipped = True
            data = {}

            if "game1_result" in st.query_params:
                try:
                    result_str = st.query_params["game1_result"]
                    data = json.loads(result_str)
                    skipped = False  # 有結果 → 玩家完成
                except Exception as e:
                    st.error(f"❌ 讀取失敗：{e}")

            # 清走 query param
            st.query_params.clear()

            elapsed = time.time() - st.session_state.game1_start

            st.session_state.scores["connect_coins"] = {
                "total_time_sec": round(elapsed, 2),
                "completed_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "skipped": skipped,  # ★ 新增 ★
                "is_correct": data.get("is_correct", None),
                "sequence": data.get("sequence", []),
                "undo_count": data.get("undo_count", 0),
                "has_crossing": data.get("has_crossing", None),
                "is_order_correct": data.get("is_order_correct", None),
                "score": 1 if data.get("is_correct") else 0,
            }

            from core.state import next_game
            next_game()
