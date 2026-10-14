"""Validate meaningful migration completeness and the deploy artifact before publication."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
import json,re,sys,subprocess
from capture_source import DOM
ROOT=Path(__file__).resolve().parents[1];SITE=ROOT/'site'
class Page(HTMLParser):
 def __init__(self):super().__init__();self.ids=[];self.tags=[];self.images=[];self.attrs=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs);self.tags.append(tag);self.attrs.append((tag,a))
  if a.get('data-source'):self.ids.append(a['data-source'])
  if tag=='img':self.images.append(a)
def main():
 data=json.loads((ROOT/'content/practice.json').read_text(encoding='utf-8'));mapping=json.loads((ROOT/'content/migration-map.json').read_text(encoding='utf-8'))
 allids=[];errors=[];routes=[];rendered={}
 for file in SITE.rglob('*.html'):
  if 'scripts' in file.relative_to(SITE).parts:continue
  text=file.read_text(encoding='utf-8');p=Page();p.feed(text);allids+=p.ids;routes.append(file.relative_to(SITE).as_posix())
  dom=DOM();dom.feed(text)
  rendered.update({n.attrs['data-source']:n.text() for n in dom.root.all() if n.attrs.get('data-source')})
  if 'http-equiv="refresh"' in text:continue
  if p.tags.count('h1')!=1:errors.append(str(file)+' h1 count')
  if 'noindex,nofollow' not in text:errors.append(str(file)+' noindex missing')
  if text.count('id="cwu-colophon"')!=1:errors.append(str(file)+' colophon')
  if 'Description text goes here' in text or 'It all begins with an idea.' in text:errors.append(str(file)+' template copy')
  for im in p.images:
   if not (file.parent/im['src']).resolve().is_file():errors.append(im['src'])
   if 'alt' not in im or not im.get('width') or not im.get('height'):errors.append(str(file)+' image metadata')
  for tag,a in p.attrs:
   if tag in {'input','textarea','select'} and 'disabled' not in text:errors.append(str(file)+' active form control')
   if tag=='script' and urlsplit(a.get('src','')).netloc:errors.append(str(file)+' remote script')
 expected=sum(len(p['blocks']) for p in data['pages'])
 if len(mapping)!=expected:errors.append('source disposition count')
 for item in mapping:
  if item['disposition']=='retained' and item['id'] not in allids:errors.append(item['id'])
  if item['disposition']=='retained' and re.sub(r'\s+',' ',rendered.get(item['id'],'')).strip().casefold()!=re.sub(r'\s+',' ',item['text']).strip().casefold():errors.append(item['id']+' text mismatch')
 if len(set(allids))!=len(allids):errors.append('duplicate source block ids')
 if errors:raise SystemExit('\n'.join(errors))
 for command in [[sys.executable,str(SITE/'scripts/apply_colophon.py'),'--check'],[sys.executable,str(SITE/'scripts/check_release_links.py')]]:subprocess.run(command,check=True)
 result={'sourcePages':len(data['pages']),'sourceBlocks':expected,'retained':len(allids),'exclusions':[i for i in mapping if i['disposition']=='excluded'],'routes':routes,'status':'PASS'}
 (ROOT/'evidence/static-validation.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
 print('PASS',expected,'source dispositions,',len(allids),'rendered blocks,',len(routes),'routes')
if __name__=='__main__':main()
