"""
第四關：重複句子（直接文字比對，唔用 AI）
"""
import time
import streamlit as st
from pathlib import Path

from core.game_result import read_game_result


def render():
    if "game4_start" not in st.session_state:
        st.session_state.game4_start = time.time()

    html_path = Path(__file__).parent.parent / "components" / "game4.html"

    if not html_path.exists():
        st.error("❌ 搵唔到 game4.html")
        return

    html_content = html_path.read_text(encoding="utf-8")
    st.components.v1.html(html_content, height=900, scrolling=False)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("➡️ 去下一關", use_container_width=True,
                     type="primary", key="next_4"):

            skipped, data = read_game_result("game4_result")

            if skipped:
                score = 0
                conditions = {}
                reasons = ["未完成就撳下一關"]
            else:
                score = data.get("score", 0)
                conditions = data.get("conditions", {})
                reasons = data.get("reasons", [])

            try:
                score = max(0, min(2, int(score)))
            except (ValueError, TypeError):
                score = 0

            st.session_state.scores["sentence_repeat"] = {
                "total_time_sec": round(
                    time.time() - st.session_state.game4_start, 2),
                "completed_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "skipped": skipped,
                "is_correct": score == 2,
                "score": score,
                "conditions": conditions,
                "reasons": reasons,
                "sentences": data.get("sentences", []),
                "player_said": data.get("player_said", []),
            }

            from core.state import next_game
            next_game()
