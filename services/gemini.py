import base64
import requests
import os

# 環境変数に Gemini API Key を入れておく
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Gemini API エンドポイント
GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/"
    "models/gemini-2.5-flash:generateContent"
)

def analyze_timetable_image(image_path: str) -> str:
    """
    時間割のスクリーンショット画像を Gemini に送信し、
    時間割内容をテキストとして返す
    """

    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY が設定されていません")

    # 画像を base64 に変換
    with open(image_path, "rb") as f:
        image_base64 = base64.b64encode(f.read()).decode("utf-8")

    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": (
                            "この画像は大学の時間割表です。"
                            "曜日・時限・授業名が分かるように、"
                            "文章で整理して出力してください。"
                        )
                    },
                    {
                        "inlineData": {
                            "mimeType": "image/png",
                            "data": image_base64
                        }
                    }
                ]
            }
        ]
    }

    response = requests.post(
        f"{GEMINI_URL}?key={GEMINI_API_KEY}",
        headers=headers,
        json=payload
    )

    try:
        response.raise_for_status()
        result = response.json()
    except requests.exceptions.HTTPError as exc:
        # API のエンドポイント不一致やキー無効などで 4xx/5xx が返る場合に
        # 呼び出し元に分かりやすく伝える
        status = getattr(exc.response, "status_code", None)
        body = None
        try:
            body = exc.response.json()
        except Exception:
            body = exc.response.text if exc.response is not None else None
        raise RuntimeError(f"Gemini API error: status={status}, body={body}") from exc

    # Geminiの返答テキストを取り出す
    try:
        text = result["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        text = "時間割を解析できませんでした。"

    return text


def analyze_with_gemini(image_path: str):
    """
    互換性用ラッパー。既存の `routes.timetable` から
    `analyze_with_gemini` をインポートしているため、
    ここで簡単なラップを提供する。

    戻り値は JSON シリアライズ可能な形（辞書）で返す。
    """
    try:
        text = analyze_timetable_image(image_path)
        return {"text": text}
    except RuntimeError as e:
        # GEMINI_API_KEY 未設定や API エラーなどをフロントに返す
        return {"error": str(e)}
    except FileNotFoundError as e:
        return {"error": f"画像ファイルが見つかりません: {e.filename}"}
    except Exception as e:
        return {"error": f"予期せぬエラー: {str(e)}"}
