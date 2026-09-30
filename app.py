"""
舊香港濕街市遊戲 — 主入口
"""
import streamlit as st
import pandas as pd
import time
import base64

from core.state import (
    init_state,
    next_game,
    GAME_NAMES,
    GAME_MAX_SCORES,
)
from core.tts import generate_speech
from games import connect_coins, game2, game3, game4, game5, game6

# 頁面設定
st.set_page_config(
    page_title="舊香港街市 · 銀碼大挑戰",
    page_icon="🏮",
    layout="centered",
)

# 初始化
init_state()

# ★ 預先生成 Game 4 嘅 MP3（靜默，唔顯示 spinner）
SENTENCES_GAME4 = ["姨媽買豬腸", "阿婆煲老火湯"]

if "game4_audio" not in st.session_state:
    audios = []
    for s in SENTENCES_GAME4:
        try:
            mp3_bytes = generate_speech(s, voice_key="female_1", rate="-10%")
            b64 = base64.b64encode(mp3_bytes).decode("utf-8")
            audios.append(f"data:audio/mp3;base64,{b64}")
        except Exception:
            audios.append("")
    st.session_state.game4_audio = audios

# 主流程
current = st.session_state.current_game

# ═══════════════════════════════════════════
# Intro
# ═══════════════════════════════════════════
if current == "intro":
    st.title("🏮 舊香港濕街市")
    st.markdown(
        """
        你踏入咗 1960 年代嘅舊街市：紅膠燈、木頭車、魚檔水花四濺。

        檔主阿婆遞咗條紅繩畀你：

        > 「後生仔，幫我按我嘅規矩，逐個檔口收錢，串起佢啦！」

        準備好未？
        """
    )

    if st.button("入街市 ▶️", type="primary"):
        st.session_state.player_name = "訪客"
        st.session_state.scores = {}
        next_game()

# ═══════════════════════════════════════════
# 遊戲
# ═══════════════════════════════════════════
elif current == "connect_coins":
    connect_coins.render()

elif current == "game2":
    game2.render()

elif current == "game3":
    game3.render()

elif current == "game4":
    game4.render()

elif current == "game5":
    game5.render()

elif current == "game6":
    game6.render()

# ═══════════════════════════════════════════
# End（顯示結果）
# ═══════════════════════════════════════════
elif current == "end":
    st.title("🏁 收市")
    st.markdown("多謝你今日嚟幫手！")

    if st.button("🔄 再開一次檔", type="primary", key="restart_all"):
        st.session_state.clear()
        st.session_state["_reload_ts"] = int(time.time() * 1000)
        st.rerun()

    # ── 隱藏按鈕（只有你睇）──
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔒", key="admin_toggle"):
        st.session_state.show_admin = not st.session_state.show_admin

    # ── 管理員檢視 ──
    if st.session_state.get("show_admin", False):
        st.divider()
        st.subheader("📊 遊戲結果（只有開發者睇到）")

        scores = st.session_state.get("scores", {})

        # ★ DEBUG：顯示所有 key ★
        st.write("**DEBUG - scores 入面有咩 key：**")
        st.write(list(scores.keys()))
        st.write("**DEBUG - 完整 scores：**")
        st.json(scores)
        if not scores:
            st.info("冇數據")
        else:
            # ── 分數摘要 ──
            st.markdown("### 🎯 分數摘要")

            total_score = 0
            total_max = 0

            # 3 欄顯示
            games = list(GAME_MAX_SCORES.keys())
            cols = st.columns(3)
            for i, game_id in enumerate(games):
                game_name = GAME_NAMES.get(game_id, game_id)
                max_score = GAME_MAX_SCORES[game_id]
                total_max += max_score

                data = scores.get(game_id, {})
                score = data.get("score", 0)
                total_score += score

                with cols[i % 3]:
                    st.metric(
                        label=f"{game_name}",
                        value=f"{score} / {max_score}",
                    )

            st.divider()

            # ── 總分 ──
            st.markdown("### 🏆 總分")
            st.metric(
                label="MoCA 總分",
                value=f"{total_score} / {total_max}",
            )

            st.divider()

            # ── 每個遊戲詳細數據 ──
            st.markdown("### 📋 詳細數據")

            for game_id in games:
                game_name = GAME_NAMES.get(game_id, game_id)
                data = scores.get(game_id, {})

                if not data:
                    continue

                with st.expander(f"**{game_name}**", expanded=False):
                    st.write(f"- **完成時間**：{data.get('total_time_sec', '—')} 秒")
                    st.write(f"- **完成時間戳**：{data.get('completed_at', '—')}")
                    st.write(f"- **分數**：{data.get('score', 0)} / {GAME_MAX_SCORES[game_id]}")

                    if "is_correct" in data:
                        st.write(f"- **正確**：{data.get('is_correct')}")
                    if "sequence" in data:
                        st.write(f"- **順序**：{data.get('sequence', [])}")
                    if "undo_count" in data:
                        st.write(f"- **撤銷次數**：{data.get('undo_count', 0)}")
                    if "has_crossing" in data:
                        st.write(f"- **有交叉**：{data.get('has_crossing')}")

                    # 顯示 raw data
                    st.write("**原始數據：**")
                    st.json(data)

            st.divider()

            # ── CSV 下載 ──
            st.markdown("### 📥 下載數據")

            # 整理成 dataframe
            rows = []
            for game_id, data in scores.items():
                row = {
                    "遊戲": GAME_NAMES.get(game_id, game_id),
                    "遊戲 ID": game_id,
                    "分數": data.get("score", 0),
                    "滿分": GAME_MAX_SCORES.get(game_id, 0),
                    "完成時間（秒）": data.get("total_time_sec", None),
                    "完成時間戳": data.get("completed_at", None),
                    "正確": data.get("is_correct", None),
                    "順序": str(data.get("sequence", [])),
                    "撤銷次數": data.get("undo_count", None),
                    "有交叉": data.get("has_crossing", None),
                }
                rows.append(row)

            df = pd.DataFrame(rows)

            st.dataframe(df, use_container_width=True)

            # CSV 下載
            csv = df.to_csv(index=False).encode("utf-8-sig")
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            st.download_button(
                label="📥 下載 CSV",
                data=csv,
                file_name=f"moca_results_{timestamp}.csv",
                mime="text/csv",
                type="primary",
            )
