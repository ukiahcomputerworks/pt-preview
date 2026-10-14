from capture_source import ROOT, fetch
from pathlib import Path
from urllib.parse import urlsplit,unquote
from concurrent.futures import ThreadPoolExecutor
import json,hashlib,re
from PIL import Image,ImageOps,ImageDraw
from io import BytesIO

def main():
 m=json.loads((ROOT/'source/manifest.json').read_text(encoding='utf-8'))
 urls=list(dict.fromkeys(i['url'].split('?')[0] for p in m['pages'] for i in p['images'] if 'squarespace-cdn.com' in i['url']))
 rawdir=ROOT/'source/media';rawdir.mkdir(exist_ok=True)
 out=ROOT/'assets/media';out.mkdir(exist_ok=True)
 def one(pair):
  idx,url=pair;raw,final,typ=fetch(url);im=Image.open(BytesIO(raw));original=unquote(urlsplit(url).path.split('/')[-1]);slug=re.sub('[^a-z0-9]+','-',original.lower()).strip('-')[:65]
  (rawdir/(str(idx).zfill(2)+'-'+slug)).write_bytes(raw)
  logo='Logo.png' in url or 'Logo' in original
  opaque=im.mode!='RGBA' or im.getchannel('A').getextrema()==(255,255)
  name='mendocino-pt-logo.png' if logo else str(idx).zfill(2)+'-'+slug.rsplit('-',1)[0]+('.jpg' if opaque else '.png')
  pic=ImageOps.exif_transpose(im);pic.thumbnail((1500,1500) if logo else (1400,1200))
  if name.endswith('.jpg'):pic.convert('RGB').save(out/name,quality=87,optimize=True)
  else:pic.save(out/name,optimize=True)
  result={'url':url,'file':'assets/media/'+name,'sourceName':original,'sha256':hashlib.sha256(raw).hexdigest(),'sourceSize':im.size,'publicSize':pic.size,'mode':im.mode,'bytes':(out/name).stat().st_size}
  if logo:result['alphaExtrema']=im.getchannel('A').getextrema() if im.mode=='RGBA' else None
  return result
 with ThreadPoolExecutor(max_workers=5) as pool: assets=list(pool.map(one,enumerate(urls)))
 (ROOT/'source/media-manifest.json').write_text(json.dumps(assets,indent=2,ensure_ascii=False),encoding='utf-8')
 # A labeled contact sheet is review evidence, not a public composition.
 sheet=Image.new('RGB',(1000,((len(assets)+4)//5)*160),'#eee9dc');draw=ImageDraw.Draw(sheet)
 for j,a in enumerate(assets):
  pic=Image.open(ROOT/a['file']).convert('RGBA');pic.thumbnail((190,125));x=(j%5)*200;y=(j//5)*160;sheet.paste(pic,(x,y),pic);draw.text((x+2,y+128),a['file'].split('/')[-1][:26],fill='black')
 sheet.save(ROOT/'evidence/source-media-contact-sheet.jpg')
 print(json.dumps(assets,indent=2,ensure_ascii=True))
if __name__=='__main__':main()
