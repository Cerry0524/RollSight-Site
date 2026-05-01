# RollSight 公開網站維護清單

> 每次 App Store 送審、版本更新、訂閱方案調整或截圖重拍前，先跑完這份清單。

## 1. App Store URL

- Marketing URL: `https://cerry0524.github.io/RollSight-Site/`
- Support URL: `https://cerry0524.github.io/RollSight-Site/support/`
- Privacy Policy URL zh-Hant: `https://cerry0524.github.io/RollSight-Site/privacy/index.zh-Hant.html`
- Privacy Policy URL en: `https://cerry0524.github.io/RollSight-Site/privacy/index.en.html`

檢查方式：

```sh
curl -I https://cerry0524.github.io/RollSight-Site/
curl -I https://cerry0524.github.io/RollSight-Site/support/
curl -I https://cerry0524.github.io/RollSight-Site/privacy/index.zh-Hant.html
curl -I https://cerry0524.github.io/RollSight-Site/privacy/index.en.html
```

## 2. 每次發版前必查

### 截圖與產品畫面

- 對照 `assets/screenshots/` 是否仍符合目前 App UI。
- 避免公開圖片出現真實單位、人名、旗幟、徽章、地址、位置資訊或測試用敏感字樣。
- 首頁 hero 圖應優先使用中性畫面；若要換 QR 圖，先確認 QR 畫面沒有測試單位名。

### 訂閱與匯出文案

- 對照主 App：
  - `tactical-app/src/config/tier-gate.config.ts`
  - `tactical-app/src/config/tier-gate-descriptions.ts`
  - `tactical-app/src/schemas/image-export.schema.ts`
- 公開網站不要寫死未確認價格。
- 若 BASIC/FULL 權益或額度變動，同步更新首頁、Privacy、Support 與 App Store metadata。

### 隱私與安全文案

- 對照主 App：
  - `tactical-app/src/services/backup/backup.service.ts`
  - `tactical-app/ios/RollSight/PrivacyInfo.xcprivacy`
  - `docs/app-store-release/04-privacy-policy.md`
- QR 同步只描述點對點、簽章驗證、防重放與裝置綁定。
- 備份檔才描述 PIN 衍生金鑰加密。
- 不使用「無法破解」「軍規加密」「全部資料都端對端加密」等絕對承諾。

### 使用手冊

- 對照主 App：
  - `docs/user-guide/建立單位.md`
  - `docs/user-guide/建立座位圖.md`
  - `docs/user-guide/建立點名任務.md`
  - `docs/user-guide/訂閱方案與付費哲學.md`
- 如果手冊已拆成公開頁，首頁「完整手冊」索引也要同步更新。
- 如果仍只是索引，不要宣稱所有 markdown 已網頁化。

### App Store metadata

- 對照主 App：
  - `docs/app-store-release/02-asc-metadata.md`
  - `docs/app-store-release/05-review-notes.md`
  - `docs/app-store-release/06-screenshot-shotlist.md`
- 上架前確認主 App 文件內的 URL 是 `/RollSight-Site/`，不是舊的 `/RollSight/`。
- App Store description、screenshots、review notes 與公開網站的隱私/訂閱敘述要一致。

## 3. 發布前 QA

- `git diff --check`
- 掃描高風險字串：

```sh
rg -n "建制|下轄|夜視|軍規|無法破解|端對端加密|NT\\$|\\[Support URL\\]|\\[Privacy Policy URL\\]" .
```

- 檢查本機 HTML 連結與資產引用沒有缺檔。
- 用桌機與手機 viewport 截圖檢查：
  - 首頁
  - Privacy entry
  - zh-Hant Privacy Policy
  - English Privacy Policy
  - Support

## 4. GitHub Pages 健康檢查

- 每次合併 `main` 後確認 Pages workflow 成功。
- 以 `curl -I` 檢查公開 URL 皆為 HTTP 200。
- 若移除敏感或舊素材，檢查舊資產 URL 回傳 404。
- 記錄最新部署 commit SHA 與 Pages workflow URL 到 Linear issue。
