import streamlit as st
from core.state import COINS, CORRECT_SEQUENCE, next_game

STYLE = """
<style>
.stApp {
    background-color: #F5E6C8;
    font-family: "Noto Sans TC", "PingFang HK", sans-serif;
}
h1, h2, h3 { color: #3B2A1A; }
.stButton > button {
    background-color: #8B3A2B;
    color: #F5E6C8;
    border: 2px solid #D4A017;
    border-radius: 8px;
    font-weight: 600;
    white-space: pre-line;
    line-height: 1.3;
}
.stButton > button:hover:not(:disabled) {
    background-color: #D4A017;
    color: #3B2A1A;
}
.stButton > button:disabled {
    background-color: #C9B99A;
    color: #7A6A55;
    border-color: #A89878;
}
.market-banner {
    background: #8B3A2B;
    color: #F5E6C8;
    padding: 10px 16px;
    border-radius: 8px;
    border: 2px solid #D4A017;
    text-align: center;
    margin-bottom: 12px;
}
.rule-box {
    background: #FFF8E7;
    border-left: 6px solid #8B3A2B;
    padding: 12px 16px;
    border-radius: 6px;
    color: #3B2A1A;
}
.chain-box {
    background: #FFF8E7;
    border: 2px dashed #8B3A2B;
    padding: 12px;
    border-radius: 8px;
    text-align: center;
    font-size: 1.1em;
    color: #3B2A1A;
}
</style>
"""


def render():
    st.markdown(STYLE, unsafe_allow_html=True)

    st.markdown(
        '<div class="market-banner">🏮 舊香港濕街市 · 收銀大挑戰 🏮</div>',
        unsafe_allow_html=True,
    )

    st.header("🔗 第一關：串起街市嘅銀碼")

    with st.expander("📜 阿婆嘅規矩", expanded=True):
        st.markdown(
            """
            <div class="rule-box">
            <b>場景：</b>你係街市幫手。檔主阿婆要你按佢嘅方式，
            用條紅繩串起所有硬幣。<br><br>

            <b>規矩：</b><br>
            1. 阿婆嘅排列方式係 —— <b>一個毫子，跟住一個蚊，
               再一個毫子，再一個蚊</b>，如此類推。<br>
            2. 每組入面，銀碼要跟住上一個遞增。<br>
            3. 由最細嘅銀碼開始，逐個點擊。<br>
            4. 全部 7 個硬幣串好之後，撳「交數」睇結果。<br><br>

            <i>檔口提示：每個硬幣都嚟自唔同檔口，順住街市嘅路行就啱㗎喇。</i>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()

    st.subheader("🧵 你手上嘅紅繩")
    if st.session_state.connected:
        chain = " 🪙—🪙 ".join(
            f"**{COINS[c]['display']}**" for c in st.session_state.connected
        )
        st.markdown(
            f'<div class="chain-box">🪙 {chain} 🪙</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="chain-box">（紅繩仲未開始串…）</div>',
            unsafe_allow_html=True,
        )

    st.divider()

    st.subheader("🏪 行街市 · 揀硬幣")

    labels = list(COINS.keys())
    for row_start in range(0, len(labels), 4):
        row = labels[row_start:row_start + 4]
        cols = st.columns(4)
        for i, label in enumerate(row):
            info = COINS[label]
            with cols[i]:
                already = label in st.session_state.connected
                st.caption(info["stall"])
                if st.button(
                    f"{info['display']}\n({label})",
                    key=f"coin_{label}",
                    disabled=already or st.session_state.game_finished,
                    use_container_width=True,
                ):
                    _handle_click(label)

    st.divider()

    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔄 解開條繩再嚟過", use_container_width=True):
            st.session_state.connected = []
            st.session_state.game_finished = False
            st.rerun()
    with c2:
        if st.button(
            "🧮 交數",
            use_container_width=True,
            disabled=len(st.session_state.connected) < len(COINS)
                    or st.session_state.game_finished,
        ):
            _check_answer()

    if st.session_state.game_finished:
        st.divider()
        if st.session_state.connected == CORRECT_SEQUENCE:
            st.success("🎉 阿婆好滿意！你成功串起晒所有硬幣，數目啱晒！")
            st.session_state.scores["connect_coins"] = 100
        else:
            st.session_state.attempts += 1
            st.error("❌ 阿婆皺眉頭：條繩串錯咗喇，再行多次街市啦。")
            st.session_state.scores["connect_coins"] = 0

        if st.button("➡️ 去下一關", key="next_after_connect"):
            next_game()


def _handle_click(label: str):
    if label in st.session_state.connected:
        return
    st.session_state.connected.append(label)
    st.rerun()


def _check_answer():
    st.session_state.game_finished = True
