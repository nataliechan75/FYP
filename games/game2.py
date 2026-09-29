"""
遊戲結果讀取 + AI 評分 helper
"""
import json
import time
import streamlit as st
from openai import OpenAI


# ═══════════════════════════════════════════
# 讀取 URL query param 入面嘅遊戲結果
# ═══════════════════════════════════════════
def read_game_result(param_key: str):
    """
    讀取 URL query param 入面嘅遊戲結果。
    回傳 (skipped: bool, data: dict)
    """
    skipped = True
    data = {}

    if param_key in st.query_params:
        try:
            result_str = st.query_params[param_key]
            data = json.loads(result_str)
            skipped = False
        except Exception as e:
            st.error(f"❌ 讀取失敗：{e}")

    st.query_params.clear()
    return skipped, data


# ═══════════════════════════════════════════
# MoCA 立方體 AI 評分
# ═══════════════════════════════════════════
CUBE_PROMPT = """
你係受過 MoCA（Montreal Cognitive Assessment）訓練嘅評分員。
根據以下 4 個官方標準，評估呢個立方體圖：

1. 畫出來嘅圖案必須為立體（有前後兩個方形 + 4 條連接線）
2. 所有線必須畫出（共 12 條：前 4 + 後 4 + 連接 4）
3. 沒有加上額外的線
4. 線與線之間相對地較平衡，長度應近似（直角棱鏡可以接受）

4 個條件全部符合 = 1 分，否則 = 0 分（冇部分分）。

只回傳以下 JSON，唔好加其他文字：
{
  "score": 0 或 1,
  "conditions": {
    "is_3d": true/false,
    "all_lines_present": true/false,
    "no_extra_lines": true/false,
    "lines_parallel": true/false
  },
  "reasons": ["唔符合嘅原因，用廣東話"],
  "reason": "一句總結"
}
"""


def score_cube_with_ai(image_data_url: str) -> dict:
    """
    用 GPT-4o vision 判斷 MoCA 立方體。
    image_data_url: "data:image/jpeg;base64,..."
    """
    try:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

        resp = client.chat.completions.create(
            model="gpt-4o",
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": CUBE_PROMPT},
                    {"type": "image_url",
                     "image_url": {"url": image_data_url}},
                ],
            }],
            response_format={"type": "json_object"},
            temperature=0,
        )
        return json.loads(resp.choices[0].message.content)

    except Exception as e:
        st.warning(f"⚠️ AI 判斷失敗：{e}")
        return {
            "score": 0,
            "conditions": {},
            "reasons": ["AI 判斷失敗"],
            "reason": str(e),
        }
