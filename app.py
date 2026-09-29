"""
舊香港街市遊戲 — 主入口
"""
import streamlit as st
from core.state import init_state, next_game
from games import connect_coins, game2, game3, game4, game5, game6

# 頁面設定
st.set_page_config(
    page_title="舊香港街市",
    page_icon="🏮",
    layout="centered",
)

# 初始化 state
init_state()

# 主流程
current = st.session_state.current_game

if current == "intro":
    st.title("🏮 舊香港街市")
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
        next_game()

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

elif current == "end":
    st.title("🏁 收市")
    st.markdown("多謝你今日嚟幫手！")

    if st.button("再開一次檔", type="primary"):
        st.session_state.clear()
        st.rerun()
