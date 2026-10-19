"""ETF 入門小助手：使用 uv 執行，呼叫本地 Ollama 並串流顯示結果。"""

import json
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

MODEL = "qwen2.5:0.5b"
PROMPT = "請用繁體中文列出 3 點，讓初學者快速理解 ETF 是什麼、優點及風險。每點不超過 35 字。"
API = "http://127.0.0.1:11434/api/generate"
RESULT_FILE = Path(__file__).resolve().parent / "docs" / "result.txt"


def main() -> int:
    payload = json.dumps({"model": MODEL, "prompt": PROMPT, "stream": True}).encode("utf-8")
    request = Request(API, data=payload, headers={"Content-Type": "application/json"})
    parts = []

    print(f"使用模型：{MODEL}\nAI 回答：\n", flush=True)
    try:
        with urlopen(request, timeout=120) as response:
            for line in response:  # Ollama 每產生一段文字，就送出一行 JSON。
                if not line.strip():
                    continue
                chunk = json.loads(line)
                if chunk.get("error"):
                    raise RuntimeError(chunk["error"])
                text = chunk.get("response", "")
                print(text, end="", flush=True)
                parts.append(text)
                if chunk.get("done"):
                    break
    except (URLError, HTTPError, RuntimeError, ValueError) as error:
        print(f"\n執行失敗：{error}", file=sys.stderr)
        print("請確認 Ollama 已啟動，並先執行 ollama pull qwen2.5:0.5b", file=sys.stderr)
        return 1

    answer = "".join(parts).strip()
    if not answer:
        print("\n模型沒有回傳文字。", file=sys.stderr)
        return 1

    RESULT_FILE.write_text(answer + "\n", encoding="utf-8")
    print(f"\n\n已儲存到 {RESULT_FILE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
