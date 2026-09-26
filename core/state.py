import streamlit as st

GAME_ORDER = ["intro", "connect_coins", "game2", "game3", "game4", "end"]

CORRECT_SEQUENCE = ["10¢", "$1", "20¢", "$2", "50¢", "$5", "$10"]

COINS = {
    "10¢": {"display": "一毫子",  "value": 0.10, "stall": "🥬 菜檔"},
    "20¢": {"display": "兩毫子",  "value": 0.20, "stall": "🐟 魚檔"},
    "50¢": {"display": "五毫子",  "value": 0.50, "stall": "🍜 麵檔"},
    "$1":  {"display": "一蚊",    "value": 1.00, "stall": "🧺 豆腐檔"},
    "$2":  {"display": "兩蚊",    "value": 2.00, "stall": "⚖️ 豬肉檔"},
    "$5":  {"display": "五蚊",    "value": 5.00, "stall": "🍗 燒味檔"},
    "$10": {"display": "十蚊",    "value": 10.00,"stall": "🏮 雜貨檔"},
}


def init_state():
    defaults = {
        "current_game": "intro",
        "player_name": "",
        "scores": {},
        "connected": [],
        "game_finished": False,
        "attempts": 0,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def next_game():
    idx = GAME_ORDER.index(st.session_state.current_game)
    if idx + 1 < len(GAME_ORDER):
        st.session_state.current_game = GAME_ORDER[idx + 1]
    st.rerun()
