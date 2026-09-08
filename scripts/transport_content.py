"""2.0 動態 QR／指定裝置加密說明；推出前狀態與完整發行目標分開。"""
RELEASE = '2.0 完整發行目標：動態 QR、指定裝置加密與分階段匯入。目前仍在推出前驗收；新加密資料包發送尚未開放，部分匯入處理方式仍有限制。'
DEMO = '''<figure class="transport-demo"><div class="shot-label"><span>2.0 / 動態 QR 傳輸</span><span>流程示意</span></div><div class="demo-recipient"><span>指定接收裝置</span><strong>接收端 A</strong></div><input class="pause-motion" type="checkbox" id="pause-qr"><label for="pause-qr">暫停示意動畫</label><div class="qr-frames" role="img" aria-label="輪播三個示意 QR 影格，不含實際點名資料，不能匯入 App"><img src="@@assets/qr-demo/frame-1.svg" width="230" height="230" alt=""><img src="@@assets/qr-demo/frame-2.svg" width="230" height="230" alt=""><img src="@@assets/qr-demo/frame-3.svg" width="230" height="230" alt=""></div><div class="demo-chain"><span>選定內容</span><span>加密</span><span>逐幀傳遞</span></div><figcaption>示意碼，非實際加密資料包<br>GIF／MP4 傳遞・從相簿讀取</figcaption></figure>'''
STEPS = [
 ('01','選擇內容與對象','發送端','在分享前確認任務、座位圖、單位與人員揭露範圍。姓名可依可用選項採匿名、只姓或全名；只姓須使用預先設定的分享姓氏，不由 App 猜測。'),
 ('02','為接收裝置加密','發送端・待開放','確認對方已完成通聯及加密金鑰驗證。開放後，新敏感資料包會針對每位接收者獨立加密，再產生動態 QR；對象或金鑰不符時，不改送明文。'),
 ('03','保留原檔，從相簿讀取','接收端','接收 GIF／MP4 原檔後，在通聯的相簿匯入入口選取。App 直接讀取影格並顯示進度，不必等動畫完整播放；不要用單張截圖取代動畫。'),
 ('04','先看「暫存預覽」','接收端・第 1 頁','完成接收者、來源簽章、期限與解密驗證後，查看來源及新增、變更、相同、衝突等差異。預覽或返回不會寫入正式資料。'),
 ('05','選擇「區段處理方式」','接收端・第 2 頁','依各區段選擇可執行的方式。目前介面僅開放「略過／僅供參考」；建立副本、正式對應與合併將在完整 2.0 發行前補齊並驗收。未揭露的內容不等於刪除。'),
 ('06','確認差異，再套用','接收端・第 3 頁','核對最後差異與處理筆數後按「確認並套用」。全部略過時不可套用；若本機資料已變動，需重新檢查差異。驗證失敗時停止，不會默默改用舊資料。')]
def steps():
 return '<p class="callout">'+RELEASE+'</p><ol class="import-steps">'+''.join(f'<li><span class="step-index">{n}</span><div><p class="eyebrow">{who}</p><h3>{title}</h3><p>{desc}</p></div></li>' for n,title,who,desc in STEPS)+'</ol>'
def crypto():
 return '''<div class="crypto-grid"><article><p class="eyebrow">01 / 對象</p><h3>金鑰綁定接收裝置</h3><p>X25519 與 HKDF-SHA256 建立每位接收者的加密金鑰；簽章身分與加密金鑰分離。</p></article><article><p class="eyebrow">02 / 內容</p><h3>敏感內容先加密</h3><p>XChaCha20-Poly1305 保護資料內容與完整性；密文綁定發送者、接收者及金鑰版本，不能任意換對象。</p></article><article><p class="eyebrow">03 / 匯入</p><h3>驗證通過，才進預覽</h3><p>Ed25519 簽章核對來源，再檢查接收者、期限與重放。指定裝置才能解密；失敗就停止，不降級成明文。</p></article></div>'''
