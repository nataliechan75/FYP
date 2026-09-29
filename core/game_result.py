"""
遊戲結果讀取 + AI 評分 helper（Gemini 版）
"""
import json
import base64
import streamlit as st
import google.generativeai as genai


def read_game_result(param_key: str):
    skipped = True
    data = {}
    if param_key in st.query_params:
        try:
            data = json.loads(st.query_params[param_key])
            skipped = False
        except Exception as e:
            st.error(f"❌ 讀取失敗：{e}")
    st.query_params.clear()
    return skipped, data


CUBE_PROMPT = """
你係受過 MoCA（Montreal Cognitive Assessment）訓練嘅評分員。
根據以下 4 個官方標準，評估呢個立方體圖：

1. 畫出來嘅圖案必須為立體（有前後兩個方形 + 4 條連接線）
2. 所有線必須畫出（共 12 條：前 4 + 後 4 + 連接 4）
3. 沒有加上額外的線
4. 線與線之間相對地較平衡，長度應近似（直角棱鏡可以接受）

4 個條件全部符合 = 1 分，否則 = 0 分（冇部分分）。

只回傳以下 JSON，唔好加其他文字、唔好加 ```json```：
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


def _data_url_to_bytes(data_url: str):
    header, b64 = data_url.split(",", 1)
    mime = header.split(";")[0].replace("data:", "")
    return mime, base64.b64decode(b64)


def score_cube_with_ai(image_data_url: str) -> dict:
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel("gemini-3.8-flash")

        mime, img_bytes = _data_url_to_bytes(image_data_url)

        response = model.generate_content(
            [
                CUBE_PROMPT,
                {"mime_type": mime, "data": img_bytes},
            ],
            generation_config={
                "temperature": 0,
                "response_mime_type": "application/json",
            },
        )

        text = response.text.strip()
        if text.startswith("```"):
            text = text.strip("`")
            if text.startswith("json"):
                text = text[4:]
            text = text.strip()

        return json.loads(text)

    except Exception as e:
        st.warning(f"⚠️ Gemini 判斷失敗：{e}")
        return {
            "score": 0,
            "conditions": {},
            "reasons": ["AI 判斷失敗"],
            "reason": str(e),
        }
