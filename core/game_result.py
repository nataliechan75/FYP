"""
遊戲結果讀取 + AI 評分 helper（Gemini 新 model 輪流）
"""
import json
import base64
import time
import streamlit as st
import google.generativeai as genai


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


# ★ 新 model 名（根據錯誤訊息 + 官方文檔）
GEMINI_MODELS = [
    "gemini-3.8-flash",        # 你而家用緊
    "gemini-3.5-flash-lite",   # 錯誤訊息建議用呢個
    "gemini-3.6-flash",        # 官方文檔提到
    "gemini-3.5-flash",        # 官方文檔提到
]


def _data_url_to_bytes(data_url: str):
    header, b64 = data_url.split(",", 1)
    mime = header.split(";")[0].replace("data:", "")
    return mime, base64.b64decode(b64)


def score_cube_with_ai(image_data_url: str) -> dict:
    """
    輪流試多個 Gemini 新 model，邊個唔爆就用邊個。
    """
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    except Exception as e:
        return {
            "score": 0,
            "conditions": {},
            "reasons": [f"GEMINI_API_KEY 未設定：{e}"],
            "reason": str(e),
        }

    mime, img_bytes = _data_url_to_bytes(image_data_url)

    last_error = None
    tried = []

    for model_name in GEMINI_MODELS:
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

            if "429" in err:
                tried.append(f"{model_name}: 429 爆 quota")
            elif "404" in err:
                tried.append(f"{model_name}: 404 唔支援")
            else:
                tried.append(f"{model_name}: {type(e).__name__}")
            continue

    # 全部 model 都爆
    return {
        "score": 0,
        "conditions": {},
        "reasons": tried,
        "reason": f"所有 model 都失敗。最後錯誤：{last_error}",
    }
