"""
Connect Coins Component - Streamlit 自訂 component
"""
import streamlit.components.v1 as components
import os

# 指定 frontend 資料夾
_FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "frontend")

# 註冊 component
_component_func = components.declare_component(
    "connect_coins_component",
    path=_FRONTEND_DIR,
)


def connect_coins_component(key=None):
    """
    渲染 component 並回傳玩家數據。
    玩家完成遊戲時，component 會回傳 dict。
    """
    component_value = _component_func(key=key, default=None)
    return component_value
