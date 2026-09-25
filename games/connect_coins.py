"""
第一關：接線遊戲（用自訂 Streamlit Component）
"""
import streamlit as st


def render():
    # 用 component
    from components.connect_coins_component import connect_coins_component

    result = connect_coins_component(key="connect_coins_1")

    # 玩家完成時，result 會有數據
    if result and result.get("completed"):
        # 儲存數據
        st.session_state.scores["connect_coins"] = result
        # 跳下一關
        from core.state import next_game
        next_game()
