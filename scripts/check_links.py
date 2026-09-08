#!/usr/bin/env python3
"""檢查靜態網站內部連結、錨點及圖片；不依賴網路。"""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json
ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
 def __init__(self,text):
  super().__init__();self.links=[];self.ids=[];self.h1=0;self.feed(text)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  if tag=='h1':self.h1+=1
  for key in ('href','src'):
   if key in a:self.links.append(a[key])
pages={p:Page(p.read_text()) for p in ROOT.rglob('*.html') if not any(x.startswith('.') or x=='output' for x in p.relative_to(ROOT).parts)}
errors=[];count=0;external=set()
for p,page in pages.items():
 if page.h1!=1:errors.append(f'{p}: expected one h1')
 if len(page.ids)!=len(set(page.ids)):errors.append(f'{p}: duplicate ids')
 for raw in page.links:
  u=urlsplit(raw)
  if u.scheme or u.netloc:
   if u.scheme in ('http','https'):external.add(raw)
   continue
  count+=1
  target=(p.parent/unquote(u.path)).resolve() if u.path else p
  if target.is_dir():target=target/'index.html'
  if not target.is_file():errors.append(f'{p.relative_to(ROOT)}: missing {raw}')
  elif u.fragment and target in pages and unquote(u.fragment) not in pages[target].ids:errors.append(f'{p.relative_to(ROOT)}: missing anchor {raw}')
result={'pages':len(pages),'local_references':count,'errors':errors,'external_urls':sorted(external)}
print(json.dumps(result,ensure_ascii=False,indent=2))
raise SystemExit(bool(errors))
