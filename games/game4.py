"""
第四關：重複句子（Edge TTS + 文字比對）
"""
import time
import base64
import json
import streamlit as st
from pathlib import Path

from core.game_result import read_game_result
from core.tts import generate_speech


SENTENCES = ["姨媽買魚腩", "阿婆煲老火湯"]


def render():
    if "game4_start" not in st.session_state:
        st.session_state.game4_start = time.time()

    html_path = Path(__file__).parent.parent / "components" / "game4.html"

    if not html_path.exists():
        st.error("❌ 搵唔到 game4.html")
        return

    # ★ 預先生成 MP3（cache 喺 session_state）
    if "game4_audio" not in st.session_state:
        with st.spinner("🎵 生成語音中（第一次要等幾秒）..."):
            audios = []
            for s in SENTENCES:
                try:
                    mp3_bytes = generate_speech(s, voice_key="female_2", rate="-10%")
                    b64 = base64.b64encode(mp3_bytes).decode("utf-8")
                    audios.append(f"data:audio/mp3;base64,{b64}")
                except Exception as e:
                    st.error(f"❌ 生成語音失敗：{e}")
                    audios.append("")
            st.session_state.game4_audio = audios

    html_content = html_path.read_text(encoding="utf-8")

    # ★ 將音頻 base64 注入 HTML
    audio_json = json.dumps(st.session_state.game4_audio)
    html_content = html_content.replace(
        "const PRELOADED_AUDIO = [];",
        f"const PRELOADED_AUDIO = {audio_json};"
    )

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
