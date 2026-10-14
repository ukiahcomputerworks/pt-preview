"""Public-only bounded source capture. No account access or form submissions."""
from html.parser import HTMLParser
from urllib.request import Request, urlopen
from urllib.parse import urljoin, urlsplit, urlunsplit
from pathlib import Path
import json, re, hashlib, xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
BASE='https://www.mendocinopt.com/'
class Node:
 def __init__(self,tag='',attrs=(),parent=None): self.tag=tag;self.attrs=dict(attrs);self.parent=parent;self.children=[]
 def text(self): return re.sub(r'\s+',' ',''.join(c if isinstance(c,str) else c.text()+' ' for c in self.children)).strip()
 def all(self,tag=None):
  for c in self.children:
   if isinstance(c,Node):
    if tag is None or c.tag==tag: yield c
    yield from c.all(tag)
class DOM(HTMLParser):
 def __init__(self): super().__init__();self.root=Node('document');self.current=self.root
 def handle_starttag(self,tag,attrs):
  n=Node(tag,attrs,self.current);self.current.children.append(n)
  if tag not in {'img','meta','link','br','hr','input','source','wbr','area','embed','param','track','col','base'}: self.current=n
 def handle_startendtag(self,tag,attrs): self.handle_starttag(tag,attrs);self.handle_endtag(tag)
 def handle_endtag(self,tag):
  n=self.current
  while n.parent:
   if n.tag==tag: self.current=n.parent;return
   n=n.parent
 def handle_data(self,data): self.current.children.append(data)
def fetch(url):
 with urlopen(Request(url,headers={'User-Agent':'CWU-Website-Preview-Research/1.0'}),timeout=35) as r:return r.read(),r.geturl(),r.headers.get('Content-Type','')
def canon(url):
 p=urlsplit(urljoin(BASE,url));return urlunsplit(('https','www.mendocinopt.com',p.path.rstrip('/') or '/','',''))
def main():
 out=ROOT/'source';out.mkdir(exist_ok=True)
 pending=[BASE];sitemap=[];errors=[]
 for name in ['sitemap.xml','robots.txt']:
  try:
   raw,final,typ=fetch(BASE+name);(out/name).write_bytes(raw)
   if name.endswith('xml'):
    sitemap=[n.text for n in ET.fromstring(raw).iter() if n.tag.endswith('loc')]
    pending += [canon(u) for u in sitemap if urlsplit(u).netloc=='www.mendocinopt.com' and not u.endswith('.xml')]
  except Exception as e:errors.append({'url':BASE+name,'error':str(e)})
 pages={}
 while pending and len(pages)<60:
  url=pending.pop(0)
  if url in pages:continue
  try: raw,final,typ=fetch(url)
  except Exception as e: errors.append({'url':url,'error':str(e)});continue
  if 'html' not in typ:continue
  dom=DOM();dom.feed(raw.decode('utf-8','replace'));nodes=list(dom.root.all())
  name='home' if urlsplit(url).path=='/' else urlsplit(url).path.strip('/').replace('/','_')
  (out/(name+'.html')).write_bytes(raw)
  mains=[n for n in nodes if n.tag=='main' or n.attrs.get('id')=='page']
  main=mains[0] if mains else dom.root
  blocks=[]
  for n in main.all():
   if n.tag in {'h1','h2','h3','h4','h5','h6','p','li'} and n.text():
    if n.tag=='li' and any(c.tag in {'p','li'} for c in n.all()):continue
    blocks.append({'tag':n.tag,'text':n.text()})
  links=[{'text':n.text(),'url':urljoin(final,n.attrs.get('href',''))} for n in nodes if n.tag=='a' and n.attrs.get('href')]
  images=[]
  for n in nodes:
   if n.tag=='img':
    images.append({'alt':n.attrs.get('alt',''),'url':urljoin(final,n.attrs.get('data-src') or n.attrs.get('src','')),'class':n.attrs.get('class','')})
  # Background images are not always img elements.
  images += [{'alt':'Background','url':m,'class':'background'} for m in re.findall(r'data-background-image="([^"]+)"',raw.decode('utf-8','replace'))]
  pages[url]={'url':url,'final':final,'title':next((n.text() for n in nodes if n.tag=='title'),''),'blocks':blocks,'links':links,'images':images,'sha256':hashlib.sha256(raw).hexdigest()}
  for link in links:
   p=urlsplit(link['url'])
   if p.netloc in {'www.mendocinopt.com','mendocinopt.com'} and not p.query and not re.search(r'\.(pdf|jpg|png|jpeg|gif|webp|svg|xml)$',p.path,re.I):
    target=canon(link['url'])
    if target not in pages and target not in pending:pending.append(target)
 manifest={'source':BASE,'date':'2026-10-14','sitemap':sitemap,'pages':list(pages.values()),'errors':errors}
 (out/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding='utf-8')
 for p in pages.values():print(json.dumps({'url':p['url'],'final':p['final'],'title':p['title'],'blocks':len(p['blocks']),'headings':[b['text'] for b in p['blocks'] if b['tag'].startswith('h')],'links':p['links'],'images':p['images']},ensure_ascii=False))
 print('ERRORS',json.dumps(errors))
if __name__=='__main__':main()
