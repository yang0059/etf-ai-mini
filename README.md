# ETF 入門小助手（Python + uv + Ollama）

這個小專案用 Python 呼叫本地 Ollama 的 `qwen2.5:0.5b`，示範 **LLM 串流輸出（streaming）**，並透過 GitHub Actions 自動部署 GitHub Pages。

## 1. 本機執行

1. 安裝 [Ollama](https://ollama.com/download) 並開啟（確認服務正在運作）。
2. 安裝 [uv](https://docs.astral.sh/uv/getting-started/installation/)（若已安裝可略過）。Windows PowerShell 安裝指令：

   ```powershell
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

3. 在專案資料夾的終端機執行：

   ```powershell
   ollama pull qwen2.5:0.5b
   uv run main.py
   ```

   - `ollama pull` 只需在第一次下載模型時執行；模型約 398 MB。
   - 文字會一段段印出（streaming）。
   - 完成後自動覆寫 `docs/result.txt`。
   - 若出現連線錯誤，檢查 Ollama 是否已啟動；若顯示找不到模型，重新執行 `ollama pull`。

## 2. 上傳 GitHub

到 GitHub 建立**公開** repository，名稱建議 `etf-ai-mini`（不要勾選自動建立 README）。在這個資料夾執行：

```bash
git init
git add .
git commit -m "Add ETF AI mini project"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/etf-ai-mini.git
git push -u origin main
```

把 `YOUR_USERNAME` 改成你的 GitHub 使用者名稱。此操作需先登入 GitHub，並設定好 git 的使用者名稱與電子郵件。

## 3. GitHub Pages 自動部署

1. 在 repository 開啟 **Settings → Pages**。
2. **Build and deployment → Source** 選擇 **GitHub Actions**。
3. `main` 分支推送後，`.github/workflows/deploy.yml` 會自動部署 `docs/`。
4. 在 **Actions** 查看部署狀態；成功後的網站通常是：
   `https://YOUR_USERNAME.github.io/etf-ai-mini/`

**重要：** GitHub Pages 是靜態網站，不會自動呼叫你電腦上的 Ollama。若想公開真正的模型結果，請先在自己電腦執行 `uv run main.py`，再 `git add docs/result.txt && git commit -m "Update AI result" && git push`。

## 4. 作業檢核

| 要求 | 對應 |
| --- | --- |
| Python（uv）呼叫本地 Ollama 或雲端模型 | `pyproject.toml`、`main.py`，使用 `uv run main.py` 呼叫 Ollama |
| 至少一種進階能力 | `main.py` 的 `stream: true` 和逐段顯示結果 |
| 至少一個 Actions workflow，自動部署 GitHub Pages | `.github/workflows/deploy.yml` |
| 作品頁：做了什麼、怎麼執行、執行結果、AI 使用說明 | `docs/index.html`，四個區塊齊全 |

> 提醒：本打包專案中的 `docs/result.txt` 初始為「尚未執行」提示，不應把示意結果宣稱為模型實測。必須在有 Ollama 的電腦實際跑過，才有真實輸出。
