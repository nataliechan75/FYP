"""
第三關：畫時鐘（AI 判斷 MoCA 畫時鐘）
"""
import time
import streamlit as st
from pathlib import Path

from core.game_result import read_game_result, score_clock_with_ai


def render():
    if "game3_start" not in st.session_state:
        st.session_state.game3_start = time.time()

    html_path = Path(__file__).parent.parent / "components" / "game3.html"

    if not html_path.exists():
        st.error("❌ 搵唔到 game3.html")
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
                     type="primary", key="next_3"):

            skipped, data = read_game_result("game3_result")

            ai_result = {
                "score": 0,
                "conditions": {},
                "reasons": ["未畫"],
            }

            if not skipped and data.get("image"):
                with st.spinner("⏳ 載入中..."):
                    ai_result = score_clock_with_ai(data["image"])
            elif skipped:
                ai_result = {
                    "score": 0,
                    "conditions": {},
                    "reasons": ["未完成就撳下一關"],
                    "reason": "skipped",
                }

            raw_score = ai_result.get("score", 0)
            try:
                score = max(0, min(3, int(raw_score)))
            except (ValueError, TypeError):
                score = 0

            st.session_state.scores["clock"] = {
                "total_time_sec": round(
                    time.time() - st.session_state.game3_start, 2),
                "completed_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "skipped": skipped,
                "is_correct": score >= 2,
                "score": score,
                "conditions": ai_result.get("conditions", {}),
                "reasons": ai_result.get("reasons", []),
                "ai_reason": ai_result.get("reason", ""),
                "stroke_count": data.get("stroke_count"),
                "_model_used": ai_result.get("_model_used"),
            }

            from core.state import next_game
            next_game()
