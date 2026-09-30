"""
全屏 loading overlay
"""
import streamlit as st


def show_loading_overlay(message: str = "⏳ 載入中..."):
    """
    顯示全屏 loading overlay。
    注意：要配合 with 使用，之後會自動消失。
    """
    overlay_html = f"""
    <style>
      #loading-overlay {{
        position: fixed;
        inset: 0;
        background: rgba(42, 24, 16, 0.85);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 9999999;
        pointer-events: all;
      }}
      #loading-overlay .loading-box {{
        background: linear-gradient(180deg, #F5E6C8, #E8D4A8);
        border: 6px solid #7A1F1F;
        border-radius: 24px;
        padding: 40px 60px;
        text-align: center;
        box-shadow: 0 0 0 8px #D4A017, 0 30px 80px rgba(0,0,0,0.6);
      }}
      #loading-overlay .loading-text {{
        font-family: "Noto Sans TC", "PingFang HK", sans-serif;
        font-size: 32px;
        font-weight: 700;
        color: #7A1F1F;
      }}
      #loading-overlay .loading-spinner {{
        font-size: 60px;
        margin-bottom: 16px;
        animation: spin 1.5s linear infinite;
        display: inline-block;
      }}
      @keyframes spin {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
      }}
    </style>
    <div id="loading-overlay">
      <div class="loading-box">
        <div class="loading-spinner">⏳</div>
        <div class="loading-text">{message}</div>
      </div>
    </div>
    """
    return st.markdown(overlay_html, unsafe_allow_html=True)
