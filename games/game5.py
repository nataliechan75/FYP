"""
第五關：語言流暢度 - 講菜名（直接 JS 計分，唔用 AI）
"""
import time
import streamlit as st
from pathlib import Path

from core.game_result import read_game_result


PASS_THRESHOLD = 11   # ★ 同 HTML 一致


def render():
    if "game5_start" not in st.session_state:
        st.session_state.game5_start = time.time()

    html_path = Path(__file__).parent.parent / "components" / "game5.html"

    if not html_path.exists():
        st.error("❌ 搵唔到 game5.html")
        return

    html_content = html_path.read_text(encoding="utf-8")

    # ★ 加 timestamp 強制 reload iframe
    ts = int(time.time() * 1000)
    html_content = html_content.replace(
        "</body>",
        f"<!-- iframe_ts: {ts} --></body>"
    )

    st.components.v1.html(html_content, height=900, scrolling=False)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("➡️ 去下一關", use_container_width=True,
                     type="primary", key="next_5"):

            skipped, data = read_game_result("game5_result")

            if skipped:
                score = 0
                total_veg = 0
                reasons = ["未完成就撳下一關"]
            else:
                score = data.get("score", 0)
                total_veg = data.get("total_vegetables", 0)
                reasons = []

                if score == 0:
                    reasons = [
                        f"一分鐘內只講到 {total_veg} 個菜名"
                        f"（需要 ≥ {PASS_THRESHOLD} 個）"
                    ]

            try:
                score = max(0, min(1, int(score)))
            except (ValueError, TypeError):
                score = 0

            st.session_state.scores["naming"] = {
                "total_time_sec": round(
                    time.time() - st.session_state.game5_start, 2),
                "completed_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "skipped": skipped,
                "is_correct": score == 1,
                "score": score,
                "total_vegetables": total_veg,
                "pass_threshold": PASS_THRESHOLD,
                "vegetables_found": data.get("vegetables_found", []),
                "full_text": data.get("full_text", ""),
                "reasons": reasons,
            }

            from core.state import next_game
            next_game()
