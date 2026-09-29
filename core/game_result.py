"""
遊戲結果讀取 + AI 評分 helper
- Game 2：畫購物籃（立方體）
- Game 3：畫時鐘（8:10）
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
# Gemini model 輪流試（quota 分開計）
# ═══════════════════════════════════════════
GEMINI_MODELS = [
    "gemini-3.8-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.6-flash",
    "gemini-3.5-flash",
]


def _data_url_to_bytes(data_url: str):
    """將 data:image/jpeg;base64,... 拆成 (mime, bytes)"""
    header, b64 = data_url.split(",", 1)
    mime = header.split(";")[0].replace("data:", "")
    return mime, base64.b64decode(b64)


def _try_gemini_models(prompt: str, mime: str, img_bytes: bytes) -> dict:
    """
    通用：輪流試多個 Gemini model，邊個唔爆就用邊個。
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

    last_error = None
    tried = []

    for model_name in GEMINI_MODELS:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(
                [prompt, {"mime_type": mime, "data": img_bytes}],
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

    return {
        "score": 0,
        "conditions": {},
        "reasons": tried,
        "reason": f"所有 model 都失敗。最後錯誤：{last_error}",
    }


# ═══════════════════════════════════════════
# Game 2：MoCA 立方體評分 prompt
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


def score_cube_with_ai(image_data_url: str) -> dict:
    """Game 2：畫購物籃（立方體）"""
    mime, img_bytes = _data_url_to_bytes(image_data_url)
    return _try_gemini_models(CUBE_PROMPT, mime, img_bytes)


# ═══════════════════════════════════════════
# Game 3：MoCA 畫時鐘評分 prompt（目標時間：8:10）
# ═══════════════════════════════════════════
CLOCK_PROMPT = """
你係受過 MoCA（Montreal Cognitive Assessment）訓練嘅評分員。
根據以下 3 個官方標準，評估呢個時鐘圖（目標時間：8:10）。
每符合一項得 1 分，總分 0–3 分。

【條件 1】輪廓（1 分）
- 鐘面必須為一個圓形
- 只接納輕微歪曲（例如：喺圓形接合點有少少唔靚）
- 如果唔係圓形（例如方形、橢圓、大缺口）→ 0 分

【條件 2】數字（1 分）
- 所有 1–12 數字都要寫上
- 冇任何附加數字（唔可以多過 12 個數字）
- 數字必須順序正確（1、2、3...12）
- 數字位置適當（12 喺頂、3 喺右、6 喺底、9 喺左）
- 羅馬數字都可以接受
- 數字可以寫喺時鐘界線外面
- 任何一項唔符合 → 0 分

【條件 3】時分針（1 分）
- 必須同時見到時針同分針
- 目標時間：8:10
  * 分針（長）指向 2（10 分 = 時鐘上 2 嘅位置）
  * 時針（短）過咗 8，稍微向 9 方向（時針應該指喺 8 同 9 之間，接近 8）
- 時針必須明顯地比分針短
- 時分針必須置於鐘面中央
- 接合點需要接近時鐘中心
- 任何一項唔符合 → 0 分

請獨立評估 3 個條件，每個條件 true / false。
最後 score = contour + numbers + hands（0–3）。

只回傳以下 JSON，唔好加其他文字、唔好加 ```json```：
{
  "score": 0 到 3 嘅整數,
  "conditions": {
    "contour": true/false,
    "numbers": true/false,
    "hands": true/false
  },
  "reasons": ["唔符合嘅原因，用廣東話"],
  "reason": "一句總結"
}
"""


def score_clock_with_ai(image_data_url: str) -> dict:
    """Game 3：畫時鐘（8:10）"""
    mime, img_bytes = _data_url_to_bytes(image_data_url)
    return _try_gemini_models(CLOCK_PROMPT, mime, img_bytes)
