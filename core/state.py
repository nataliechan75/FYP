"""
遊戲 state 管理
"""
import streamlit as st

# 遊戲順序
GAME_ORDER = [
    "intro",
    "game1",          # ★ 由 connect_coins 改成 game1
    "game2",
    "game3",
    "game4",
    "game5",
    "game6",
    "end",
]

# 遊戲名（中文）
GAME_NAMES = {
    "game1": "接線遊戲",         # ★ 改
    "cube_copy": "畫購物籃",
    "clock": "畫時鐘",
    "sentence_repeat": "重複句子",
    "naming": "講菜名",
    "abstraction": "抽象概念",
}

# 每個遊戲嘅滿分
GAME_MAX_SCORES = {
    "game1": 1,                  # ★ 改
    "cube_copy": 1,
    "clock": 3,
    "sentence_repeat": 2,
    "naming": 1,
    "abstraction": 2,
}


def init_state():
    defaults = {
        "current_game": "intro",
        "player_name": "訪客",
        "scores": {},
        "show_admin": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def next_game():
    idx = GAME_ORDER.index(st.session_state.current_game)
    if idx + 1 < len(GAME_ORDER):
        st.session_state.current_game = GAME_ORDER[idx + 1]
    st.rerun()
