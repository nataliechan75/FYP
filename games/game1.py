"""
第一關：接線遊戲（用 HTML 嵌入）
"""
import time
import json
import streamlit as st
from pathlib import Path


def render():
    if "game1_start" not in st.session_state:
        st.session_state.game1_start = time.time()

    html_path = (
        Path(__file__).parent.parent
        / "components"
        / "game1.html"
    )

    if not html_path.exists():
        st.error("❌ 搵唔到 game1.html")
        return

    html_content = html_path.read_text(encoding="utf-8")

    # ★ 加 timestamp 強制 reload iframe
    ts = int(time.time() * 1000)
    html_content = html_content.replace(
        "</body>",
        f"<!-- iframe_ts: {ts} --></body>"
    )

    st.components.v1.html(html_content, height=650, scrolling=False)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("➡️ 去下一關", use_container_width=True,
                     type="primary", key="next_1"):

            skipped = True
            data = {}

            if "game1_result" in st.query_params:
                try:
                    result_str = st.query_params["game1_result"]
                    data = json.loads(result_str)
                    skipped = False
                except Exception as e:
                    st.error(f"❌ 讀取失敗：{e}")

            st.query_params.clear()

            elapsed = time.time() - st.session_state.game1_start

            st.session_state.scores["game1"] = {     # ★ 由 connect_coins 改成 game1
                "total_time_sec": round(elapsed, 2),
                "completed_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "skipped": skipped,
                "is_correct": data.get("is_correct", None),
                "sequence": data.get("sequence", []),
                "undo_count": data.get("undo_count", 0),
                "has_crossing": data.get("has_crossing", None),
                "is_order_correct": data.get("is_order_correct", None),
                "score": 1 if data.get("is_correct") else 0,
            }

            from core.state import next_game
            next_game()
