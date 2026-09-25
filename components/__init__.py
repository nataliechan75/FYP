import streamlit.components.v1 as components
import os

_FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "frontend")

_component_func = components.declare_component(
    "connect_coins_component",
    path=_FRONTEND_DIR,
)

def connect_coins_component(key=None):
    component_value = _component_func(key=key, default=None)
    return component_value
