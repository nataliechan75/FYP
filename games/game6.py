"""
第六關：抽象概念（AI 判斷語意）
"""
import time
import json
import streamlit as st
from pathlib import Path

from core.game_result import read_game_result, score_abstraction_with_ai


def render():
    if "game6_start" not in st.session_state:
        st.session_state.game6_start = time.time()

    html_path = Path(__file__).parent.parent / "components" / "game6.html"

    if not html_path.exists():
        st.error("❌ 搵唔到 game6.html")
        return

    html_content = html_path.read_text(encoding="utf-8")

    # ★ 注入 Game 6 嘅 Edge TTS MP3
    audios = st.session_state.get("game6_audio", ["", ""])
    audio_json = json.dumps(audios)

    html_content = html_content.replace(
        "const PRELOADED_AUDIO_GAME6 = [];",
        f"const PRELOADED_AUDIO_GAME6 = {audio_json};"
    )

    ts = int(time.time() * 1000)
    html_content = html_content.replace(
        "</body>",
        f"<!-- iframe_ts: {ts} --></body>"
    )

    st.components.v1.html(html_content, height=900, scrolling=False)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("➡️ 去下一關", use_container_width=True,
                     type="primary", key="next_6"):

            skipped, data = read_game_result("game6_result")

            ai_result = {
                "score": 0,
                "conditions": {},
                "reasons": ["未完成"],
            }

            if not skipped:
                questions = data.get("questions", [])
                answers = data.get("player_answers", [])

                if questions and answers:
                    ai_result = score_abstraction_with_ai(questions, answers)
                else:
                    ai_result = {
                        "score": 0,
                        "conditions": {},
                        "reasons": ["冇題目 / 冇答案"],
                        "reason": "missing data",
                    }
            else:
                ai_result = {
                    "score": 0,
                    "conditions": {},
                    "reasons": ["未完成就撳下一關"],
                    "reason": "skipped",
                }

            raw_score = ai_result.get("score", 0)
            try:
                score = max(0, min(2, int(raw_score)))
            except (ValueError, TypeError):
                score = 0

            st.session_state.scores["abstraction"] = {
                "total_time_sec": round(
                    time.time() - st.session_state.game6_start, 2),
                "completed_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "skipped": skipped,
                "is_correct": score == 2,
                "score": score,
                "conditions": ai_result.get("conditions", {}),
                "reasons": ai_result.get("reasons", []),
                "ai_reason": ai_result.get("reason", ""),
                "questions": data.get("questions", []),
                "player_answers": data.get("player_answers", []),
                "_model_used": ai_result.get("_model_used"),
            }

            from core.state import next_game
            next_game()
