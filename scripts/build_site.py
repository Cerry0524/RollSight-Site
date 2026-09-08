#!/usr/bin/env python3
"""產生靜態網站；僅使用標準函式庫。修改共用文案後執行 python3 scripts/build_site.py。"""
from pathlib import Path
import html
import re
from transport_content import DEMO, RELEASE, steps as import_steps, crypto

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = 'https://cerry0524.github.io/RollSight-Site/'
STORE = 'https://apps.apple.com/tw/app/%E5%88%B0%E9%BD%8A-rollsight/id6762076423'
NOTICE = '2.0 準備推出，尚未上架。本頁介紹 2.0 預計提供的體驗；實際開放功能與價格以商店及 App 顯示為準。'
TERMS = 'FULL 終身方案NT$99，一次購買，尚未上架；最終價格、幣別與可購買資格以商店付款畫面為準。2.0 改為 FREE 與 FULL 買斷，不再提供新訂閱。舊 BASIC／FULL 訂閱只保留商店確認的有效期間；購買買斷方案不會自動取消舊訂閱，請自行到原商店管理。'
LIMITS = [
 ('單位組數','1 組','不限','不限'),('單位內成員與階層','不限','不限','不限'),
 ('每月點名任務','30 個','200 個','不限'),('座位圖張數','5 張','20 張','不限'),
 ('每張座位圖','50 席','200 席','不限'),('編制席位','50 席','200 席','不限'),
 ('每日圖片匯出','5 張・含浮水印','10 張・無浮水印','不限・無浮水印'),
 ('座位圖點名操作','可檢視','可互動點名','可互動點名'),
 ('下級回報彙整','可接收，不能發起彙整','每任務最多 5 個下級','下級數不限'),
 ('報告範本','精簡統計／僅事故','另含完整報告','完整報告／自訂報告'),
 ('手動畫分區／分區編號','提供','提供','提供'),
 ('走道／分區綁定／分組看板','—','提供','提供'),
 ('九宮格／分區合併／中心優先排列','—','提供','提供'),
 ('編制編輯／自訂情境／預設頭像','—','提供','提供'),
 ('自訂回報時段範本','—','提供','提供'),
 ('自訂出缺勤標籤／勤務角色匯入匯出','—','—','提供'),
 ('編制分發','—','—','提供'),
 ('分區自動建議／綁定模板／區域圖片匯出','—','—','提供'),
 ('7／30 天出勤趨勢','—','—','提供'),
 ('PIN／支援裝置的生物辨識／加密備份','提供','提供','提供')]
FAQ = [
 ('2.0 和 NT$99 終身方案已經上架了嗎？', TERMS + ' 本站不接受預購或付款，也不代表商店已開放 2.0。'),
 ('「終身 FULL」包含什麼？','規劃為一次購買 FULL 權益，無到期日、不按次數扣除、不自動續費，包含本 App FULL 功能與其更新，不另按本 App 的版本更新收費；不包含未開發的雲端服務或獨立產品。功能範圍見方案表。權益以商店確認的有效交易為準，退款或交易撤銷後，對應權益會撤銷；若另有有效訂閱，依有效權益判定。'),
 ('已有訂閱，買終身會自動取消嗎？','不會。2.0 不再提供新訂閱。舊 BASIC／FULL 訂閱在商店確認的有效期間內仍可使用；購買終身方案不會自動取消、折抵或退還既有訂閱，也不會自動將舊訂閱轉為終身。若不再需要續訂，請自行在原商店取消。'),
 ('如何取消訂閱？','iPhone／iPad：開啟系統「設定」→ 你的姓名 →「訂閱項目」，選擇到齊後取消。刪除 App 不等於取消訂閱。<a href="https://support.apple.com/zh-tw/118428">Apple 取消訂閱說明</a>。'),
 ('免費體驗會在 7 天後扣款嗎？','不會。2.0 以 FREE 免費版提供體驗，沒有 7 天後自動扣款的訂閱試用。FULL 是使用者另行確認的一次買斷。舊訂閱是否續訂仍依原商店狀態，不能因更新 App 就假設已停止扣款。'),
 ('换機或重新安裝後如何恢復購買？','請使用購買時的同一商店帳號，連上網路後在 App「完整版買斷與恢復購買」使用「恢復購買」。恢復的是有效付費權益，不是本機名冊或點名資料；換機前請另行確認備份與匯出範圍。'),
 ('iOS、Android 和家庭共享互通嗎？','不保證跨平台轉移、跨商店恢復或家庭共享。請以原購買商店、相同商店帳號及商品頁顯示的支援範圍為準；網站不代表 Android 版本已上架。'),
 ('可以退款嗎？','由原付款商店審核，網站不能核准退款。Apple 購買請參考 <a href="https://support.apple.com/zh-tw/118223">Apple 退款說明</a>，或前往 <a href="https://reportaproblem.apple.com/">申請退款</a>。退款或交易撤銷後，該筆購買的權益會撤銷。'),
 ('取消、到期或降級會刪除資料嗎？','方案變更不會主動刪除既有本機資料；超過目前方案上限時，新增、修改或匯出會重新受限。清除資料、卸載或遺失裝置則是另一回事，請先確認備份。'),
 ('資料會自動同步到雲端嗎？','不會。名冊、座位圖與點名資料以本機保存為主，透過你主動發起的資料碼、檔案或圖片交接。商店購買、恢復購買、支援連結與啟用的診斷服務可能需要網路。'),
 ('每個 QR 都會自動加密、直接套用嗎？','不要把 QR 或報告圖片當成保密通道。請確認接收對象及內容；來源驗證、通聯綁定與防重放不等於所有分享內容都加密。收件匣仍需依畫面確認來源、差異與匯入方式。'),
 ('忘記 PIN 或備份密碼怎麼辦？','開發者不能找回 PIN 或解密備份。請先查看 App 的復原提示；清除並重新設定會移除本機資料，不能當成無損復原方式。')]
CHAPTERS = [
 ('create-unit','01','單位與人員','先整理一份可以重複使用的名冊。',[
 ('建立單位與階層','从「單位」新增，選擇類別或範本、命名，再建立子單位。免費版可保留一組根單位，單位內人數與階層不限。'),
 ('人員名冊與編制','在成員管理補入姓名、職務與編組；FULL 可編輯編制，涵蓋分組與席位配置。勤務角色的匯入／匯出屬 FULL。'),
 ('檢視與維護','在單位列表、詳細頁與編制表核對資料；移除單位前確認關聯紀錄，永久清除歷史單位會一併刪除相關資料。')]),
 ('seat-map','02','座位圖與分區','把人員和場地位置對起來。',[
 ('建立與重用','從「座位圖」建立版面，使用建立精靈或快速設定，調整行列、座位、朝向與配置；可在後續任務選用。'),
 ('走道、分區與編號','免費版提供手動畫分區及分區編號；FULL 增加走道、單位綁定、分組看板、九宮格配置、合併分區與中心優先排列。'),
 ('进階配置','FULL 提供自動建議綁定、可重用的綁定模板及區域圖片匯出。配置完成後確認座位不足或未安排人員提示。')]),
 ('attendance','03','任務、預判與現場點名','從第一個任務，一路核對到結束。',[
 ('建立任務','到「點名」新增，指定單位、名稱、時間與座位圖。依流程使用草稿、啟動任務；需要預先掌握人數時使用預判／預報。'),
 ('列表與互動點名','在摘要切換統計、列表及座位圖。列表可查找與修改狀態；FULL 可在互動座位圖點選、交換座位或長按修改，FREE 可檢視。'),
 ('狀態與統計','核對應到、實到、事故與待查，查看各單位分布。FULL 可新增出缺勤分類標籤、匯入標籤包並確認對應。'),
 ('結束與歷史','結束前處理待查；若仍有未點名者，App 會提示是否強制結束。可依任務狀態篩選、查歷史；FULL 可看 7／30 天趨勢。刪除任務會連带移除其相關紀錄。')]),
 ('reports','04','報告與圖片匯出','讓對方看得懂這次點名結果。',[
 ('預報與正式報告','由摘要產生報告，區分預判與正式結果，核對報告詞及人數再發布。報告檢視本身不要求升級。'),
 ('選擇報告範本','FREE 可選精簡統計或僅事故；FULL 可使用完整報告並自訂區段、報告詞、座位圖及成員表樣式。'),
 ('圖片與檔案','產生圖片前檢查名冊及狀態。FREE 每日 5 張含浮水印，FULL 不限且無浮水印。設定另提供點名報告匯出／匯入及送收歷史；它們不等同完整資料備份。')]),
 ('inbox','05','資料碼分享與收件匣','交接前後，都留下確認的步驟。',[
 ('傳送與匯入','由任務選擇分享，使用資料碼或圖片交給指定對象。通聯中心可從相簿選取主圖，依提示補齊缺少的圖片；掃描與讀圖入口依 App 顯示。'),
 ('確認來源與重送差異','查看收件匣的來源及驗證結果；同一來源重送時先比較差異，再選擇建立、併入或保留。不是所有收到的內容都會立即寫入正式任務。'),
 ('通聯關係與快速模式','在裝置通聯層級管理綁定、邀請及解除關係；建立關係前核對對方。快速模式需由使用者選擇啟用，仍應檢查匯入結果與錯誤提示。'),
 ('資料保密','QR 的來源驗證不代表內容保密。分享圖片或改用通訊軟體後，也受對方裝置及第三方服務的資料處理方式影響。')]),
 ('coordination','06','彙整與通聯中心','把不同來源的回報放到同一張進度表。',[
 ('彙整下級回報','各方案都能查看收件匣；發起彙整、以彙整資料建立或併入任務需 FULL 買斷；FULL 彙整下級數不限。'),
 ('完整性看板與催報','透過矩陣查看時段與各來源回報進度，使用通聯層級頁核對裝置關係；催報由使用者操作發送，不是背景自動推播服務。'),
 ('時段與編制交接','系統時段範本可用，FULL 可自訂時段名稱與時間窗。FULL 可將編制分發給下級，接收方確認後再更新或回傳。')]),
 ('settings','07','外觀與本機保護','讓自己的裝置符合使用習慣。',[
 ('個人設定與外觀','設定顯示名稱、頭像及 App 提供的閱讀主題；預設頭像選擇依 FULL 權益開放。名稱是本機設定，不是雲端帳號。'),
 ('PIN 與生物辨識','在設定變更 PIN；支援的裝置可開啟生物辨識解鎖。保護能力仍仰賴作業系統與裝置安全，不代表全部本機資料庫皆已加密。'),
 ('備份與還原','設定中的「備份裝置金鑰／還原裝置金鑰」會處理裝置身分及指定本機資料，備份檔以 PIN 衍生金鑰加密。不是所有資料表或歷史都涵蓋；還原前確認內容並保留原始匯出檔。'),
 ('清除與支援','可刪除已移除歷史單位、清除所有資料，或開啟手冊、常見問題、支援與使用條款。清除包含 PIN 與裝置金鑰且無法復原，操作前先確認備份。')])]

def faq(items=FAQ):
 return '<div class="faq-list">' + ''.join(f'<details><summary>{q}</summary><div><p>{a}</p></div></details>' for q,a in items) + '</div>'

def table():
 return '<p class="fine-print">手機可左右滑動表格，查看完整比較。</p><div class="table-scroll" role="region" aria-label="方案功能比較，可左右捲動" tabindex="0"><table><caption>2.0 方案能力預覽・新用戶只提供 FREE 與 FULL 終身買斷</caption><thead><tr><th scope="col">功能與容量</th><th scope="col">FREE 免費</th><th scope="col">FULL 完整</th></tr></thead><tbody>' + ''.join('<tr><th scope="row">'+row[0]+'</th>'+''.join('<td>'+x+'</td>' for x in (row[1],row[3]))+'</tr>' for row in LIMITS) + '</tbody></table></div>'

def heading(k,title,desc):
 return f'<header class="page-intro"><p class="eyebrow">{k}</p><h1>{title}</h1><p class="lead">{desc}</p></header>'

def cards(items):
 return '<div class="card-grid">'+''.join(f'<article class="card"><h3>{t}</h3><p>{d}</p></article>' for t,d in items)+'</div>'

def write(path,title,description,body,en=False):
 prefix='../'*(len(Path(path).parts)-1) or './'
 def u(p):return prefix+p
 old=ROOT/path
 oldtext=old.read_text() if old.exists() else ''
 og=re.search(r'<meta property="og:image" content="([^"]+)"',oldtext)
 image=ORIGIN+'assets/site-icon.png'  # 2.0 分享預覽改用中性品牌圖，避免舊訂閱及名冊畫面。
 nav=[('','Home' if en else '首頁'),('user-guide/','Features & guide' if en else '功能導覽'),('user-guide/subscription.html','Plans' if en else '方案比較'),('support/','Support' if en else '支援'),('privacy/','Privacy' if en else '隱私')]
 navhtml=''.join(f'<a href="{u(p)}"'+(' aria-current="page"' if (p=='' and path=='index.html') or (p and path==p+'index.html') or path==p else '')+f'>{label}</a>' for p,label in nav)
 release='2.0 is coming. Not yet released. Features and final prices are subject to the App and store listing.' if en else NOTICE
 footer=f'''<footer class="site-footer"><div><a class="brand" href="{u('')}"><img src="{u('assets/site-icon.png')}" width="32" height="32" alt="">到齊 RollSight</a><p>{'Local first. Share when you choose.' if en else '點名在手，交接有序。'}</p><small>© 2026 RollSight · {'2.0 preview' if en else '2.0 準備推出'}</small></div><nav aria-label="{'Footer' if en else '頁尾導覽'}">{navhtml}<a href="{u('features/qr-share/')}">QR {'sharing' if en else '分享'}</a><a href="{u('features/offline-encrypted/')}">{'Offline & protection' if en else '離線與保護'}</a><a href="{u('use-cases/military-roll-call/')}">{'Use case' if en else '使用情境'}</a><a href="{u('privacy/index.en.html')}">English Privacy</a><a href="mailto:cerry0524@gmail.com">Email</a><a href="https://www.facebook.com/groups/2194278754661166?locale=zh_TW">{'Community' if en else 'Facebook 社群'}</a><a href="{STORE}">{'App Store listing (current version)' if en else 'App Store（現有版本）'}</a></nav></footer>'''
 body=body.replace('@@',prefix)
 s=f'''<!doctype html>
<html lang="{'en' if en else 'zh-Hant'}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}｜RollSight</title><meta name="description" content="{html.escape(description,quote=True)}"><meta name="robots" content="index, follow"><link rel="canonical" href="{ORIGIN+path.removesuffix('index.html')}"><link rel="icon" href="{u('assets/site-icon.png')}"><link rel="stylesheet" href="{u('styles.css')}">
<meta property="og:type" content="website"><meta property="og:title" content="{html.escape(title,quote=True)}"><meta property="og:description" content="{html.escape(description,quote=True)}"><meta property="og:url" content="{ORIGIN+path.removesuffix('index.html')}">
{f'<meta property="og:image" content="{image}">' if image else ''}
</head><body><a class="skip-link" href="#main">{'Skip to content' if en else '跳到主要內容'}</a>
<header class="site-header"><a class="brand" href="{u('')}"><img src="{u('assets/site-icon.png')}" alt="" width="36" height="36"><span>到齊 RollSight <small>2.0</small></span></a><nav class="site-nav" aria-label="{'Main navigation' if en else '主要導覽'}">{navhtml}</nav></header>
<div class="release-notice">{release}</div><main id="main">{body}</main>{footer}</body></html>'''
 old.parent.mkdir(parents=True,exist_ok=True);old.write_text(s)

home='''<section class="hero"><div class="hero-copy"><p class="eyebrow">ROLLSIGHT 2.0 / 完整升級，準備推出</p><h1>資料動起來，<br>只交給對的人。</h1><p class="lead">動態 QR Code × 指定裝置加密。<br>從選擇分享內容，到匯入前確認差異，讓每一次交接更清楚。</p><p>點名、名冊與座位圖仍以本機運作。2.0 將加密落實到資料交接，不靠自動雲端同步。</p><div class="actions"><a class="button primary" href="#encrypted-import">看看匯入步驟 <span aria-hidden="true">↘</span></a><a class="button secondary" href="@@user-guide/subscription.html">FULL 買斷預告</a></div><p class="hero-status">新加密發送流程尚待開放；完整 2.0 發行前將完成匯入整合與驗收。</p></div>'''+DEMO+'''</section><section class="section" id="transport"><div class="section-heading"><p class="eyebrow">2.0 的核心改變</p><h2>一份動態 QR，<br>一條有驗證的交接流程。</h2><p>GIF／MP4 將資料拆成連續影格。接收端從相簿原檔直接讀取，收齊所需資料後進入驗證；動態格式本身不是加密，內容另由指定接收者加密保護。</p></div>'''+crypto()+'''<p class="fine-print">加密範圍指新的敏感資料包；不代表既有一般 QR、可讀報告圖片或整個本機資料庫全部加密。正式推出前仍需完成實機、相簿與通訊軟體傳遞驗收。</p></section><section class="section" id="encrypted-import"><div class="section-heading"><p class="eyebrow">STEP BY STEP / 匯入參考流程</p><h2>從發送到匯入，每一步都看得懂。</h2></div>'''+import_steps()+'''<a class="text-link" href="@@features/qr-share/">完整動態 QR 與加密交接說明 →</a></section>
<section class="section" id="features"><div class="section-heading"><p class="eyebrow">日常點名，一樣完整</p><h2>先準備。再確認。<br>最後，交接得清楚。</h2><p>從單位、人員與座位圖開始，讓動態 QR 交接有一份可靠的資料來源。</p></div><div class="workflow-grid">'''
for n,t,d,link in [('01','把資料準備好','單位階層、人員名冊、編制與座位分區，建立後可在任務重複使用。','create-unit'),('02','掌握現場狀態','預判、列表點名、互動座位圖與統計，核對待查後再結束任務。','attendance'),('03','完成回報交接','輸出報告，主動分享資料碼；在收件匣確認來源，彙整各單位結果。','inbox')]:
 home+=f'<a class="workflow" href="@@user-guide/#{link}"><span class="number">{n}</span><h3>{t}</h3><p>{d}</p><span class="text-link">查看操作流程 →</span></a>'
home+='''</div></section><section class="section feature-catalog"><div class="section-heading"><p class="eyebrow">功能導覽</p><h2>日常要做的事，都有位置。</h2></div><div class="catalog-grid">'''
for anchor,n,title,desc,items in CHAPTERS:
 home+=f'<a class="catalog-item" href="@@user-guide/#{anchor}"><span>{n}</span><div><h3>{title}</h3><p>{desc}</p></div><span aria-hidden="true">↗</span></a>'
home+='''<a class="catalog-item" href="@@user-guide/subscription.html"><span>08</span><div><h3>方案與恢復購買</h3><p>比較容量，了解買斷與恢復購買。</p></div><span aria-hidden="true">↗</span></a></div></section>
<section class="section trust-band"><div><p class="eyebrow">LOCAL FIRST</p><h2>你的資料，<br>由你決定何時分享。</h2></div><div><p>日常名冊與點名以本機保存為主。沒有自動雲端同步，也不需要建立 RollSight 雲端帳號。</p><p>PIN 與支援裝置的生物辨識保護操作入口；匯出的備份檔使用 PIN 衍生金鑰加密。分享前仍要確認內容與接收對象。</p><a class="text-link" href="@@features/offline-encrypted/">了解資料保護範圍 →</a></div></section>
<section class="section" id="plans"><div class="section-heading"><p class="eyebrow">依需求選擇</p><h2>從免費開始，留下更多選擇。</h2></div><div class="plan-grid"><article class="plan"><p class="eyebrow">FREE</p><h3>日常起步</h3><p class="price">免費</p><p>1 組單位、每月 30 個任務、5 張座位圖。先建立自己的點名流程。</p><a href="@@user-guide/subscription.html#comparison">查看免費容量 →</a></article><article class="plan featured"><span class="badge">規劃中・尚未上架</span><p class="eyebrow">FULL 終身</p><h3>一次購買，完整使用</h3><p class="price">NT$99</p><p>規劃以一次購買取得 FULL 權益。最終價格以商店為準。</p><a href="@@user-guide/subscription.html#lifetime">閱讀終身方案條件 →</a></article></div><p class="fine-print">購買終身方案不會自動取消既有訂閱。恢復購買需同一商店帳號；退款或交易撤銷會撤銷對應權益。不保證跨平台或家庭共享。</p></section>
<section class="section" id="faq"><div class="section-heading"><p class="eyebrow">先解答幾個問題</p><h2>開始之前，你可能想知道。</h2></div>'''+faq([FAQ[0],FAQ[2],FAQ[9],FAQ[5]])+'''<p><a class="text-link" href="@@user-guide/subscription.html#faq">全部方案 FAQ →</a></p></section>
<section class="section end-band" id="quickstart"><p class="eyebrow">從第一個單位開始</p><h2>下一次點名，準備好了。</h2><p>2.0 尚未上架，先閱讀完整功能導覽與操作手冊。</p><div class="actions"><a class="button primary" href="@@user-guide/">開啟使用手冊</a><a class="button secondary" href="@@support/">取得支援</a></div></section><div id="manual"></div>'''
write('index.html','到齊 2.0 準備推出・動態 QR 與指定裝置加密',NOTICE,home)

intro=heading('操作手冊 / 2.0 預覽','每一步，都有依據。','先了解 2.0 動態 QR 與加密匯入，再查單位、點名及報告操作。所有推出前限制均列在對應步驟；既有版本介面可能不同。')
guide=intro+'<div class="guide-layout"><nav class="guide-index" aria-label="手冊章節"><a href="#encrypted-import">2.0 加密匯入步驟</a>'+''.join(f'<a href="#{a}">{n} {t}</a>' for a,n,t,d,it in CHAPTERS)+'<a href="#subscription">08 方案與購買</a></nav><div class="guide-content"><section class="chapter" id="encrypted-import"><p class="eyebrow">2.0 / STEP BY STEP</p><h2>動態 QR 與加密匯入</h2>'+import_steps()+'</section>'
for anchor,n,title,desc,items in CHAPTERS:
 guide+=f'<section class="chapter" id="{anchor}"><p class="eyebrow">CHAPTER {n}</p><h2>{title}</h2><p class="lead">{desc}</p><ol class="steps">'+''.join(f'<li><h3>{t}</h3><p>{d}</p></li>' for t,d in items)+'</ol></section>'
guide+='<section class="chapter" id="subscription"><p class="eyebrow">CHAPTER 08</p><h2>方案與購買</h2><p>'+TERMS+'</p><p>恢復購買需購買時的同一商店帳號，不會恢復本機資料。退款或交易撤銷會撤銷對應權益；不保證跨平台或家庭共享。</p><a class="button primary" href="@@user-guide/subscription.html">完整方案比較與 FAQ</a></section></div></div>'
write('user-guide/index.html','2.0 功能導覽與使用者手冊','單位、人員、座位圖、預判點名、報告、收件匣、彙整及本機設定的操作導覽。',guide)

plans=heading('PLANS / 方案預覽','適合現在，也能繼續往前。',TERMS)
plans+='<section class="section" id="lifetime"><div class="offer"><div><span class="badge">尚未上架</span><h2>FULL 終身・一次購買</h2><p class="price">NT$99</p></div><div><p>一次購買取得 FULL 功能層級，不是另一種自動續訂商品。沒有預購入口，上架時間另行公告。</p><p>「終身」指有效購買的 FULL 權益無到期日，包含本 App FULL 功能與其更新，不另按本 App 的版本更新收費；退款或交易撤銷時，對應權益也會撤銷。不是無條件跨平台、家庭共享或永久相容所有未來系統的承諾。</p><p><strong>原訂閱不會自動取消。</strong>若購買後不再需要原訂閱，請自行到原商店取消續訂。</p></div></div></section><section class="section" id="comparison"><h2>先看你需要的功能</h2><p>2.0 不再銷售月／年訂閱，也沒有自動扣款試用；下表是 FREE 與 FULL 買斷的能力預覽。不限表示沒有方案數量上限，仍受裝置效能與實際操作限制。</p>'+table()+'</section><section class="section" id="legacy"><h2>給既有訂閱用戶</h2><p>更新 2.0 不會強迫你立即重買。商店確認有效的舊 BASIC／FULL 訂閱，會在原有效期間內保留對應權益；不會自動贈送、折抵或轉成終身。</p><p>舊 BASIC 有效期間仍適用每月 200 個任務、20 張座位圖、每圖 200 席、每日 10 張無浮水印匯出、最多 5 個下級彙整及原 BASIC 功能。舊 FULL 在有效期間保留 FULL 功能；到期後若沒有其他有效購買，回到 FREE。</p><p>2.0 不再提供新訂閱，但這不代表原商店已自動停止續扣。請自行檢查及取消不再需要的舊訂閱。買斷後也不會自動取消。</p><a href="https://support.apple.com/zh-tw/118428">Apple 訂閱管理說明</a></section><section class="section" id="faq"><p class="eyebrow">購買前，說清楚</p><h2>方案常見問題</h2>'+faq()+'</section><section class="section end-band"><h2>購買狀態還沒更新？</h2><p>先連線、確認原商店帳號，再使用恢復購買。</p><a class="button primary" href="@@support/">查看支援方式</a></section>'
write('user-guide/subscription.html','2.0 方案比較・FULL 終身NT$99',TERMS,plans)

support=heading('SUPPORT','一起把問題釐清。','2.0 動態 QR 與加密匯入尚在推出前驗收。先從對應流程排查；仍有問題，請提供 App 版本、系統版本與操作步驟。截圖請遮住姓名、單位資料、QR 內容與交易個資。')
support+='<section class="section">'+cards([('點名或座位圖','核對任務是否已結束、方案容量、未安排人員與座位不足提示。<a href="@@user-guide/#attendance">點名操作手冊 →</a>'),('資料碼讀取或收件匣','動態 QR 需保留 GIF／MP4 原檔，單張截圖不等於完整資料。確認接收裝置、金鑰、來源與期限。<a href="@@features/qr-share/#steps">動態 QR 匯入步驟 →</a>不要直接將未確認資料套用。<a href="@@user-guide/#inbox">收件匣手冊 →</a>'),('購買與恢復','使用原商店帳號並連線，至完整版買斷與恢復購買使用恢復購買；資料備份另行處理。<a href="@@user-guide/subscription.html#faq">購買 FAQ →</a>'),('備份與 PIN','備份僅涵蓋指定資料，開發者無法解密或找回 PIN；清除資料不是無損復原。<a href="@@user-guide/#settings">備份操作說明 →</a>')])+'</section><section class="section"><h2>2.0 與終身方案預告</h2><p>'+TERMS+'</p><p>恢復購買限同一商店帳號的有效權益；退款或交易撤銷會撤銷對應權益。不保證跨平台與家庭共享。</p><a class="text-link" href="@@user-guide/subscription.html">完整條件與方案比較 →</a></section><section class="section contact-band"><p class="eyebrow">正式問題回報</p><h2>告訴我們發生了什麼。</h2><p>請附上版本、裝置型號、重現步驟、預期結果與實際結果。不要寄送 PIN、金鑰、完整名冊或原始資料碼。購買問題請先遮蔽收據個資。</p><a class="button primary" href="mailto:cerry0524@gmail.com">cerry0524@gmail.com</a><p><a href="https://www.facebook.com/groups/2194278754661166?locale=zh_TW">Facebook 使用者社群</a> 適合一般交流；個資或交易問題請使用信箱。</p><p>退款由原商店審核。<a href="https://support.apple.com/zh-tw/118223">Apple 退款說明</a> · <a href="@@privacy/">隱私政策</a></p></section>'
write('support/index.html','2.0 支援與聯絡','RollSight 操作排查、購買恢復、備份及隱私問題支援。',support)

qr=heading('2.0 / ANIMATED QR & ENCRYPTION','資料傳得動，也守得住。','動態 QR 負責傳遞，指定接收者加密保護敏感內容，匯入預覽讓你確認如何處理。三件事串起 2.0 的完整交接流程。')
qr+='<section class="section"><h2>加密如何落實在交接中？</h2>'+crypto()+'<p class="fine-print">此處介紹已實作的 2.0 核心設計，仍在推出前整合與實機驗收；不代表所有歷史格式都加密，也不是無法破解的保證。</p></section><section class="section" id="steps"><p class="eyebrow">STEP BY STEP</p><h2>動態 QR 匯入參考流程</h2>'+import_steps()+'</section><section class="section"><h2>遇到問題，先確認這四件事</h2>'+cards([('只存到一張靜態截圖？','動態 QR 需要完整 GIF／MP4 原檔，請向發送者索取原始檔案，避免聊天軟體轉成靜態圖片。'),('接收者或金鑰不符？','確認使用指定接收裝置及已驗證的通聯關係；金鑰更新或重新綁定需按 App 流程處理，不能改用明文繞過。'),('資料過期或驗證失敗？','請核對來源、裝置與檔案是否完整；需要時由發送者重新產生有效資料，不要重複套用來源不明的檔案。'),('處理方式顯示未支援？','目前新資料包預覽僅能略過或僅供參考；不要將按鈕可見視為正式合併功能已開放。完整 2.0 將補齊後再推出。')])+'</section><section class="section trust-band"><div><h2>既有圖片交接<br>依然有不同邊界。</h2></div><div><p>舊版 PNG 主圖與一般報告圖片保留相容讀取方式，可能包含可直接閱讀的姓名與狀態。不要把動態格式、來源驗章和內容加密混為同一件事。</p><a class="text-link" href="@@user-guide/#inbox">既有收件匣操作 →</a></div></section>'
write('features/qr-share/index.html','2.0 動態 QR 與加密交接・逐步匯入導覽','了解動態 GIF/MP4、指定裝置加密與三頁式差異預覽的匯入流程及推出前限制。',qr)
offline=heading('OFFLINE / LOCAL FIRST','離線作業，清楚知道資料在哪。','名冊、座位圖與點名任務以裝置本機保存為主；需要交接時才由你操作分享。')
offline+='<section class="section"><h2>2.0：加密延伸到資料交接</h2><p>新敏感資料包以 X25519、HKDF-SHA256 與 XChaCha20-Poly1305 針對指定裝置保護內容，另以 Ed25519 簽章核對來源。動態 QR 僅承載傳輸，不會自動替所有圖片加密。</p><p>'+RELEASE+'</p><a class="text-link" href="@@features/qr-share/">查看加密與匯入步驟 →</a></section><section class="section">'+cards([('日常資料','以本機儲存運作，不提供自動雲端同步或雲端名冊帳號。換機需自己處理資料交接。'),('裝置入口','PIN 與支援裝置的生物辨識用於解鎖；請同時保護手機的系統密碼。不要視為完整資料庫加密的保證。'),('備份檔案','備份裝置身分及指定資料表，匯出時用 PIN 衍生金鑰加密；不是所有資料或歷史的完整備份。')])+'</section><section class="section"><h2>哪些時候會用到網路？</h2><p>商店購買、恢復購買、權益更新、外部支援網頁與啟用的錯誤診斷可能使用網路。這和名冊自動雲端同步是不同的資料處理流程。</p><h2>分享前，再確認一次</h2><p>資料碼的簽章驗證保護來源與完整性，不能代表所有輸出內容均保密。圖片與檔案由你選擇傳送對象，對方可保存副本。</p><div class="actions"><a class="button primary" href="@@privacy/">閱讀隱私政策</a><a class="button secondary" href="@@user-guide/#settings">備份與設定操作</a></div></section>'
write('features/offline-encrypted/index.html','2.0 離線使用與本機資料保護','本機保存、PIN、生物辨識、加密備份的實際範圍與網路使用邊界。',offline)
case=heading('使用情境 / 現場點名','從集合，到一份清楚的回報。','適合單位內部、訓練與活動的名冊核對、位置確認及回報交接。RollSight 是行政輔助工具，不是官方軍用認證系統。')
case+='<section class="section">'+cards([('集合與隊形','使用列表確認出缺勤；FULL 可用互動座位圖依位置標記。'),('寢室與車輛','使用座位圖保存位置與分區，檢查未安排及座位不足的人員。'),('多單位回報','各自完成點名後主動交接；在收件匣確認來源，再彙整進度與人數。')])+'</section><section class="section"><h2>一次點名的五個步驟</h2><ol class="steps">'+''.join(f'<li><h3>{t}</h3><p>{d}</p></li>' for t,d in [('整理資料','建立單位、人員與適合的座位圖。'),('建立任務','指定時間、情境與單位，確認任務狀態。'),('標記現場','切換列表或座位圖，處理待查与事故。'),('核對摘要','確認各單位人數、預判或正式報告。'),('主動交接','選擇圖片或資料碼，接收方核對後再處理。')])+'</ol><a class="button primary" href="@@user-guide/">查看完整操作手冊</a></section>'
write('use-cases/military-roll-call/index.html','2.0 單位與軍中點名使用情境','現場集合、座位位置與下級回報的離線作業流程。',case)

write('privacy/index.html','隱私政策・語言選擇','選擇繁體中文或英文閱讀 RollSight 隱私政策。',heading('PRIVACY','清楚了解資料如何處理。','政策涵蓋本機資料、主動分享、購買權益、備份與診斷服務；2.0 與終身方案仍為推出前預告。')+'<section class="section language-grid"><a class="language-card" href="@@privacy/index.zh-Hant.html"><span>繁體中文</span><h2>隱私政策</h2><span>閱讀政策 →</span></a><a class="language-card" href="@@privacy/index.en.html" lang="en"><span>English</span><h2>Privacy Policy</h2><span>Read policy →</span></a></section>')
zhsections=[('1. 關於到齊','到齊 RollSight 由獨立開發者提供，是離線優先的點名與單位行政工具，不隸屬政府或軍事機關。'),('2. 你建立的資料','單位、人員姓名、職務、點名狀態、時間、註記與座位圖主要保存在裝置本機。App 不提供自動雲端名冊同步，也不需要 RollSight 雲端帳號。你主動匯出、分享或聯絡支援時，內容可能離開裝置。'),('3. 資料碼與檔案交接','2.0 新敏感資料包設計採每接收裝置獨立加密，使用 X25519／HKDF-SHA256／XChaCha20-Poly1305，搭配 Ed25519 來源簽章；發送與完整匯入流程尚待開放。App 提供使用者主動發起的 QR、圖片與檔案交接。來源簽章、通聯綁定與防重放用於降低誤收或竄改風險，不代表所有分享內容均加密。透過外部通訊或儲存服務傳送時，該服務及接收方可能保存副本，請先核對內容與對象。'),('4. 訂閱與一次購買',TERMS+' 商店處理付款，App 不接觸信用卡資訊。RevenueCat 用於購買驗證及權益狀態處理，可能涉及匿名 App 使用者識別碼、商品、交易與收據相關資訊；並非點名資料雲端同步。恢復購買需原購買商店的同一帳號；退款或交易撤銷會撤銷對應權益。不保證跨平台或家庭共享。'),('5. 備份與本機保護','PIN 與支援裝置的生物辨識保護解鎖操作；這不代表整個本機資料庫都已加密。備份功能匯出裝置身分與指定資料表，以 PIN 衍生金鑰加密，不是完整資料庫備份。開發者不能找回 PIN 或解密備份。請妥善保管匯出檔與 PIN，並在還原前確認影響範圍。'),('6. 診斷資料','若發布版本啟用 Sentry，App 可傳送錯誤堆疊、裝置／系統及 App 版本等診斷資料，用於排錯與效能改善。程式會移除部分請求、附加內容與導覽訊息，關閉畫面重播及截圖，並停用預設個資傳送；仍應以實際發布設定與第三方政策確認處理範圍。'),('7. 資料控制與刪除','你可在 App 內檢視與管理資料，或使用清除所有資料功能。方案到期或降級不會主動刪除本機資料，但會重新套用功能限制。刪除 App、清除資料或遺失裝置可能使本機資料無法復原；自己匯出的副本與接收者持有的資料不會一起刪除。恢復購買也不會恢復名冊。'),('8. 第三方服務','Apple App Store 處理購買；RevenueCat 協助權益管理；若啟用，Sentry 處理診斷。<a href="https://www.apple.com/legal/privacy/">Apple 隱私政策</a>、<a href="https://www.revenuecat.com/privacy">RevenueCat 隱私政策</a>、<a href="https://sentry.io/privacy/">Sentry 隱私政策</a>。網站由 GitHub Pages 提供，造訪網站時亦受其服務處理方式影響。'),('9. 聯絡與政策更新','隱私疑問請寄至 <a href="mailto:cerry0524@gmail.com">cerry0524@gmail.com</a>。來信內容會用於處理你的問題；請勿寄送 PIN、金鑰或未遮蔽的名冊。重大資料處理變更會更新本頁；2.0 上架前仍需與實際發布版本核對。')]
ensections=[('1. About RollSight','RollSight is an offline-first attendance and unit administration app provided by an independent developer. It is not affiliated with a government or military authority.'),('2. Data you create','Units, member names, roles, attendance status, timestamps, notes and seat layouts are primarily stored locally on your device. There is no automatic cloud roster sync or RollSight cloud account. Content may leave your device when you choose to export, share or contact support.'),('3. QR and file transfer','The new 2.0 sensitive bundle uses per-recipient encryption (X25519, HKDF-SHA256 and XChaCha20-Poly1305) with Ed25519 signatures. Sending and the complete import workflow are not yet released. Transfers are initiated by you through QR codes, images or files. Signatures, device bindings and replay protection reduce source and integrity risks; they do not mean every shared output is encrypted. External messaging or storage services and recipients may retain copies. Check the content and recipient before sharing.'),('4. Subscriptions and one-time purchase','Version 2.0 and the proposed FULL lifetime purchase are not yet released. The tentative price is NT$99 for a one-time FULL entitlement without an expiry date, usage depletion or automatic renewal, including FULL features and updates within this App with no separate 2.x minor-version fee; the final price, currency and availability are determined by the store payment screen. Version 2.0 offers FREE and a FULL one-time purchase, with no new monthly or annual subscriptions and no automatically charged seven-day trial. Existing BASIC/FULL subscriptions retain their store-confirmed valid period; they are not automatically converted to lifetime. A lifetime purchase will not automatically cancel an existing subscription: manage it in the original store. The store handles payment; the App does not receive credit card details. RevenueCat processes purchase validation and entitlement status, which may involve an anonymous App user identifier and product, transaction and receipt information. Restore purchases with the same account in the original store. Refunds or revoked transactions revoke the associated entitlement. Cross-platform portability and Family Sharing are not guaranteed.'),('5. Backup and device protection','PIN and supported biometrics protect unlocking; this does not mean the entire local database is encrypted. Exported backups contain device identity and selected tables, encrypted using a PIN-derived key. They are not full database backups. The developer cannot recover your PIN or decrypt your backup. Keep exports and your PIN safe and check the scope before restoring.'),('6. Diagnostics','If Sentry is enabled in the release, the App may send error stack traces, device, OS and App information for troubleshooting and performance improvement. The code removes selected request data, extras and navigation messages, disables replay and screenshots, and disables default PII collection. Processing depends on the release configuration and provider policies.'),('7. Control and deletion','You can view and manage local records and clear App data. Expiry or downgrade does not itself delete local data but re-applies feature limits. Uninstalling, clearing data or losing a device may make local data unrecoverable. Your exports and recipients’ copies are not deleted with the App. Restoring a purchase does not restore rosters.'),('8. Third-party services','Apple App Store handles purchases; RevenueCat manages entitlements; Sentry processes diagnostics when enabled. See the <a href="https://www.apple.com/legal/privacy/">Apple Privacy Policy</a>, <a href="https://www.revenuecat.com/privacy">RevenueCat Privacy Policy</a> and <a href="https://sentry.io/privacy/">Sentry Privacy Policy</a>. This website is served by GitHub Pages; visits are also subject to that service’s data processing.'),('9. Contact and changes','Contact <a href="mailto:cerry0524@gmail.com">cerry0524@gmail.com</a> for privacy questions. Your message is used to handle your request; do not send PINs, keys or unredacted rosters. Material processing changes will be reflected here. The policy must be checked against the actual release before version 2.0 is published.')]
for lang,sections in [('zh-Hant',zhsections),('en',ensections)]:
 en=lang=='en'
 content=heading('PRIVACY / 2026-09-08','Privacy Policy' if en else '隱私政策','Updated 2026-09-08 · Includes the unreleased 2.0 purchase proposal.' if en else '更新日期 2026-09-08・含尚未上架的 2.0 方案預告。')
 content+='<article class="policy-content">'+''.join(f'<section><h2>{t}</h2><p>{d}</p></section>' for t,d in sections)+f'<p><a href="@@privacy/index.{"zh-Hant" if en else "en"}.html">{"繁體中文版本" if en else "English version"}</a></p></article>'
 write(f'privacy/index.{lang}.html','Privacy Policy' if en else '隱私政策','Local data, sharing, payments, backups and diagnostics.' if en else '本機資料、主動分享、付費權益、備份與診斷資料說明。',content,en)
# 統一簡繁及維護 sitemap 日期。
for p in ROOT.rglob('*.html'):
 if 'output' not in p.parts:
  p.write_text(p.read_text().replace('换機','換機').replace('从「','從「').replace('进階','進階').replace('连带','連帶').replace('連带','連帶').replace('服务','服務').replace('与事故','與事故'))
p=ROOT/'sitemap.xml';p.write_text(re.sub(r'<lastmod>.*?</lastmod>','<lastmod>2026-09-08</lastmod>',p.read_text()))
print('Generated 10 static pages.')
