

# ═══════════════════════════════════════════
# MoCA 畫時鐘 AI 評分（官方標準）
# 目標時間：8:10
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
- 時針同分針必須同時指出正確時間
- 目標時間：8:10
  * 分針指向 2（10 分 = 時鐘上 2 嘅位置）
  * 時針過咗 8，稍微向 9 方向（因為 10 分 = 1/6 個鐘頭，時針應該指喺 8 同 9 之間，接近 8）
- 時針必須明顯地比分針短
- 時分針必須置於鐘面中央
- 接合點需要接近時鐘中心
- 任何一項唔符合 → 0 分

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
    """
    用 Gemini 判斷 MoCA 畫時鐘。
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
                [CLOCK_PROMPT, {"mime_type": mime, "data": img_bytes}],
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
