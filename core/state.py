"""
遊戲 state 管理
"""
import streamlit as st

# 遊戲順序
GAME_ORDER = ["intro", "connect_coins", "game2", "game3", "game4", "game5", "game6", "end"]

# 遊戲名（中文）
GAME_NAMES = {
    "connect_coins": "接線遊戲",
    "game2": "畫購物籃",
    "game3": "畫時鐘",
    "game4": "重複句子",
    "game5": "講菜名",
    "game6": "抽象概念",
}

# 每個遊戲嘅滿分
GAME_MAX_SCORES = {
    "connect_coins": 1,
    "game2": 1,
    "game3": 3,
    "game4": 2,
    "game5": 1,
    "game6": 2,
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
