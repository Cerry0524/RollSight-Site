# 到齊 RollSight 2.0 公開網站

既有 GitHub Pages 靜態網站，沒有執行階段套件或外部字型依賴。2.0 完整發行以動態 QR、指定裝置加密、分階段匯入及 FULL 一次買斷為主軸，目前全站標示準備推出。

## 修改及本機驗證

- `scripts/build_site.py`：共用導覽、方案、FAQ、頁面正文的單一來源。
- `scripts/transport_content.py`：動態 QR、加密及逐步匯入流程的共用文案。
- `styles.css`：手機與桌機設計。
- 修改後執行 `python3 scripts/build_site.py` 產生 10 個 HTML 頁面。
- 執行 `python3 scripts/check_links.py` 檢查連結、錨點及資產。
- 以 `python3 -m http.server 8876 --bind 127.0.0.1` 啟動本機預覽。
- 瀏覽器 QA 使用 `scripts/browser_qa.js`（Playwright CLI 的 run-code 片段），結果見 `docs/browser-qa.txt`。

維護者請先讀 `MAINTENANCE.md` 與 `docs/2.0-design-audit.md`。不要直接修改產生後的 HTML 而漏改生成器。

## 發布邊界

2.0 新用戶方案只有 FREE 與 FULL 終身買斷，暫定 NT$99，實際以商店為準。BASIC/FULL 舊訂閱只保留有效期間及恢復、取消說明，不提供新訂閱銷售。

原有路由及商店連結保留；App Store 連結明標現有版本。QR 示意影格僅含公開展示字串，不能匯入 App，不是加密成功證據。既有截圖保留在資產庫，但新頁面不展示姓名或舊訂閱畫面；分享預覽統一使用中性品牌圖。

本輪沒有 commit、push 或 deploy，網站發行必須另依 App 與商店驗收安排執行。
