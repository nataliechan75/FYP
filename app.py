import streamlit as st
from core.state import init_state, next_game
from games import connect_coins, game2, game3, game4

st.set_page_config(
    page_title="舊香港街市 · 銀碼大挑戰",
    page_icon="🏮",
    layout="centered",
)

init_state()

with st.sidebar:
    st.markdown("### 🏮 街市幫手證")
    st.write(f"幫手：**{st.session_state.player_name or '未登記'}**")
    st.write(f"位置：**{st.session_state.current_game}**")
    if st.session_state.scores:
        st.markdown("**銀包紀錄：**")
        st.json(st.session_state.scores)

current = st.session_state.current_game

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
    name = st.text_input("你嘅名：", value=st.session_state.player_name)
    if st.button("入街市 ▶️") and name.strip():
        st.session_state.player_name = name.strip()
        next_game()

elif current == "connect_coins":
    connect_coins.render()

elif current == "game2":
    game2.render()

elif current == "game3":
    game3.render()

elif current == "game4":
    game4.render()

elif current == "end":
    st.title("🏁 收市")
    st.write(f"多謝幫手，{st.session_state.player_name}！")
    st.write("今日銀包：", st.session_state.scores)
    if st.button("再開一次檔"):
        st.session_state.clear()
        st.rerun()
