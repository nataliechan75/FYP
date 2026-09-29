"""
遊戲結果讀取 + AI 評分 helper
Mistral 優先，Gemini fallback
"""
import json
import base64
import time
import streamlit as st


# ═══════════════════════════════════════════
# 讀取 URL query param
# ═══════════════════════════════════════════
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


# ═══════════════════════════════════════════
# MoCA 立方體評分 prompt
# ═══════════════════════════════════════════
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


# ═══════════════════════════════════════════
# Mistral（香港可用、免費 tier）
# ═══════════════════════════════════════════
def _score_with_mistral(image_data_url: str) -> dict:
    from mistralai import Mistral

    client = Mistral(api_key=st.secrets["MISTRAL_API_KEY"])

    resp = client.chat.complete(
        model="pixtral-12b-2409",
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

    text = resp.choices[0].message.content.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.startswith("json"):
            text = text[4:]
        text = text.strip()

    result = json.loads(text)
    result["_model_used"] = "mistral-pixtral-12b"
    return result


# ═══════════════════════════════════════════
# Gemini（fallback）
# ═══════════════════════════════════════════
def _score_with_gemini(image_data_url: str) -> dict:
    import google.generativeai as genai

    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

    MODELS = [
        "gemini-2.5-flash",
        "gemini-2.0-flash",
        "gemini-2.5-flash-lite",
    ]

    mime, img_bytes = _data_url_to_bytes(image_data_url)
    last_error = None

    for model_name in MODELS:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(
                [CUBE_PROMPT, {"mime_type": mime, "data": img_bytes}],
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

            result = json.loads(text)
            result["_model_used"] = model_name
            return result

        except Exception as e:
            last_error = e
            err = str(e)
            if "429" in err or "404" in err:
                continue
            raise

    raise last_error


# ═══════════════════════════════════════════
# 主入口：Mistral 優先，Gemini fallback
# ═══════════════════════════════════════════
def score_cube_with_ai(image_data_url: str) -> dict:
    """
    先試 Mistral（香港可用、快）
    Mistral 爆 → 試 Gemini
    兩個都爆 → 返回失敗
    """
    # ★ 試 Mistral
    if "MISTRAL_API_KEY" in st.secrets:
        try:
            return _score_with_mistral(image_data_url)
        except Exception as e:
            st.info(f"⏳ Mistral 忙碌，試 Gemini...")

    # ★ Fallback：Gemini
    if "GEMINI_API_KEY" in st.secrets:
        try:
            return _score_with_gemini(image_data_url)
        except Exception as e:
            st.warning(f"⚠️ Gemini 都失敗：{e}")

    # ★ 全部失敗
    return {
        "score": 0,
        "conditions": {},
        "reasons": ["所有 AI 都失敗"],
        "reason": "所有 AI 都失敗",
    }
