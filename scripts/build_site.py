"""Build the isolated, public noindex preview from the captured editorial inventory."""
from pathlib import Path
from urllib.parse import urlsplit
from html import escape
import json,re,shutil,sys
from PIL import Image

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'site';DATA=json.loads((ROOT/'content/practice.json').read_text(encoding='utf-8'))
PAGES={urlsplit(p['url']).path.strip('/') or 'home':p for p in DATA['pages']}
CANON='https://ukiahcomputerworks.github.io/pt-preview/'
TITLES={'home':'Life, Unpaused','physical-therapy-1':'Physical Therapy','functional-fitness-classes':'Fitness & Mobility','golf-performance':'Golf Performance','meet-the-team':'Meet The Team','testimonials':'Patient Stories','contact-us':'Contact Us','careers':'Careers','insurance':'Insurance','patient-forms':'Patient Forms','faqs':'Your Questions','about-us':'About The Practice','book-an-appointment':'Plan Your First Visit','sports-rehabilitation':'Back To Sport','healthy-aging':'Everyday Confidence'}
DESCS={'home':'One-on-one physical therapy, fitness and golf performance in Ukiah. A distinctive independent website preview.','sports-rehabilitation':'Your sport, your goals. Explore personalized sports injury rehabilitation at Mendocino Physical Therapy.','healthy-aging':'Your everyday movement matters. Explore geriatric care, postoperative rehabilitation, balance and fitness in Ukiah.'}
STREET_VIEW='https://www.google.com/maps/@39.1428379,-123.2109198,195a,75y,208.53h,93.86t/data=!3m7!1e1!3m5!1s63T1IYwaiUozUyslu1HX7Q!2e0!6shttps:%2F%2Fstreetviewpixels-pa.clients6.google.com%2Fv1%2Fthumbnail%3Fcb_client%3Dmaps_sv.tactile%26w%3D900%26h%3D600%26pitch%3D-3.8591352082990795%26panoid%3D63T1IYwaiUozUyslu1HX7Q%26yaw%3D208.53061980096456!7i16384!8i8192?entry=ttu&g_ep=EgoyMDI2MTAyMC4wIKXMDSoASAFQAw%3D%3D'
MIGRATION=[]
def e(s):return escape(s,quote=True)
def tc(s):
 acr={'pt':'PT','dpt':'DPT','pta':'PTA','tpi':'TPI','faqs':'FAQs','ppo':'PPO','acl':'ACL','cf-l1':'CF-L1'}
 return ' '.join(acr.get(w.lower(),w[:1].upper()+w[1:]) for w in s.split())
def link(route,label,cls='text-link',prefix=''):
 href=prefix+('index.html' if route=='home' else route+'/')
 return f'<a class="{cls}" href="{href}">{label}</a>'
def img(file,alt,cls='',prefix='',loading='eager'):
 pic=Image.open(ROOT/file);w,h=pic.size
 return f'<img class="{cls}" src="{prefix+file}" alt="{e(alt)}" width="{w}" height="{h}" loading="{loading}" decoding="async">'
def media(key,i=0):return [x for x in PAGES[key]['images'] if x['file'] and 'logo' not in x['file']][i]['file']
def block(key,i,tag=None):
 b=PAGES[key]['blocks'][i];tag=tag or ('h2' if b['tag'].startswith('h') else 'p');value=tc(b['text']) if tag.startswith('h') or tag=='summary' else b['text']
 MIGRATION.append({'source':key,'block':i,'text':b['text'],'disposition':'retained','target':key,'id':f'{key}-{i}'})
 # Repeated source page labels remain in the migration map and accessible document,
 # without competing visually with the new page title.
 hidden=' class="sr-only"' if i==0 and key in {'physical-therapy-1','golf-performance','meet-the-team','testimonials','faqs','about-us','insurance','careers','contact-us','book-an-appointment'} else ''
 formatted=e(value)
 for address in ['780 S Dora St, Ukiah CA 95482','780 S Dora Street Ukiah CA 95482']:
  formatted=formatted.replace(e(address),f'<a href="{e(STREET_VIEW)}" aria-label="View The Office From Dora Street In Google Street View">{e(address)}</a>')
 return f'<{tag}{hidden} data-source="{key}-{i}">{formatted}</{tag}>'
def excluded(key,i,reason):MIGRATION.append({'source':key,'block':i,'text':PAGES[key]['blocks'][i]['text'],'disposition':'excluded','reason':reason})
def header(key,prefix):
 nav=[('physical-therapy-1','Care'),('meet-the-team','People'),('contact-us','Visit')]
 navhtml=''.join(link(r,t,'nav-link'+(' active' if key==r else ''),prefix) for r,t in nav)
 menu=''.join(link(r,t,'menu-link'+(' active' if key==r else ''),prefix) for r,t in TITLES.items() if r not in ['home'])
 return f'''<a class="skip" href="#main">Skip To Content</a><div class="wrap"><header><a class="brand" href="{prefix}index.html" aria-label="Mendocino Physical Therapy home">{img('assets/media/mendocino-pt-logo.png','Mendocino Physical Therapy',prefix=prefix,loading='eager')}</a><nav aria-label="Main navigation">{navhtml}<details class="menu"><summary>Explore <span aria-hidden="true">+</span></summary><div class="menu-panel">{menu}</div></details><a class="call" href="tel:+17074629784">Call The Office</a></nav></header>'''
def footer(prefix):
 return f'''<footer><div class="footer-directory"><div><strong>Mendocino Physical Therapy</strong><p><a href="{e(STREET_VIEW)}" aria-label="View 780 S Dora Street, Ukiah, CA 95482 In Google Street View From Dora">780 S Dora Street, Ukiah, CA 95482</a><br>Office: <a href="tel:+17074629784">707-462-9784</a> · Fax: 707-313-1723<br>Monday–Friday, 9am–5pm</p></div><div>{link('insurance','Insurance',prefix=prefix)}{link('faqs','FAQs',prefix=prefix)}{link('patient-forms','Patient Forms',prefix=prefix)}{link('careers','Careers',prefix=prefix)}</div><div><a href="https://www.instagram.com/mendocinopt">Instagram</a><a href="https://www.facebook.com/mendocinopt.org/">Facebook</a>{link('preview-information','About This Preview',prefix=prefix)}</div></div><div class="footer-base"><span>Copyright © 2024 Mendocino Physical Therapy<br>All Rights Reserved.</span></div></footer>'''
def cta(prefix):return f'<section class="visit-strip"><div><p class="eyebrow">Your Next Move</p><h2>Talk It Through.</h2><p>Appointments, classes or coverage. Call the office.</p></div><a href="tel:+17074629784">707-462-9784</a></section>'
def pagehead(key,kicker,desc):
 return f'<div class="edition"><a href="../index.html">Life, Unpaused</a><span>Ukiah, California</span></div><section class="page-head"><p class="eyebrow">{kicker}</p><h1>{TITLES[key]}</h1><p class="lede">{desc}</p></section>'
def source_body(key,prefix):
 blocks=PAGES[key]['blocks'];rendered=[]
 for i,b in enumerate(blocks):rendered.append(block(key,i))
 return '<div class="source-copy">'+''.join(rendered)+'</div>'
def home():
 from workshop_home import render
 return render(block,img,media,link,cta,PAGES,DATA)

def physical():
 key='physical-therapy-1';bs=PAGES[key]['blocks'];out=pagehead(key,'Individual Attention. Personal Goals.','Hands-on care and exercise, built around the way you want to move.')
 out+='<div class="care-intro"><div>'+block(key,0,'h2')+block(key,1,'h3')+block(key,2)+'</div>'+img(media(key),'Hands-on care pictured at Mendocino Physical Therapy',prefix='../')+'</div><div class="reader">'
 i=3
 while i<len(bs):
  b=bs[i]
  if b['tag']=='h4':
   out+='<details class="content-detail">'+block(key,i,'summary')+'<div>';i+=1
   while i<len(bs) and not bs[i]['tag'].startswith('h'):out+=block(key,i);i+=1
   out+='</div></details>'
  else:out+=block(key,i,'h2' if b['tag'].startswith('h') else 'p');i+=1
 out+='</div>'+cta('../');return out
def team():
 key='meet-the-team';bs=PAGES[key]['blocks'];out=pagehead(key,'People Who Know The Place.','Meet the people behind your care, with roots in Ukiah and the surrounding community.')+block(key,0,'h2')
 # Source credentials precede each name. Preserve all biography paragraphs, not only an excerpt.
 starts=[i for i,b in enumerate(bs) if b['tag']=='h3' and not b['text'].lower().startswith('get started')]
 # Keep Mykala directly after Shelby while retaining each source biography and portrait.
 order=[0,1,2,3,5,4]
 for j,source_pos in enumerate(order):
  start=starts[source_pos];end=starts[source_pos+1]-1 if source_pos+1<len(starts) else len(bs)-1
  name=block(key,start,'h2');credentials=block(key,start-1).replace('<p ','<p class="credentials" ',1)
  out+=f'<article class="person" id="person-{j+1}"><div>'+img(media(key,source_pos),bs[start]['text'],prefix='../')+'</div><div>'+name+credentials
  paras=list(range(start+1,end));out+=block(key,paras[0]) if paras else ''
  if len(paras)>1:out+='<details class="bio-detail"><summary>Read The Full Biography <span aria-hidden="true">+</span></summary><div>'+''.join(block(key,i) for i in paras[1:])+'</div></details>'
  out+='</div></article>'
 out+=block(key,len(bs)-1,'h2')+cta('../');return out
def insurance():
 key='insurance';source_title=block(key,0,'h2').replace('class="sr-only"','class="sr-only" aria-hidden="true"',1);out=pagehead(key,'Coverage Without The Runaround.','A clearer way to see the plans the practice lists—and what to ask before your first visit.')+source_title
 out+='<section class="insurance-intro"><div><p class="eyebrow">Start With Your Card.</p><h2>Bring The Details.<br>They’ll Help You Sort Them.</h2>'+block(key,1)+'</div><aside class="coverage-check"><strong>Before You Schedule</strong><p>Call the office with your insurance card available. Coverage and patient costs depend on your specific plan.</p><a class="button-link" href="tel:+17074629784">Call 707-462-9784</a></aside></section>'
 out+='<section class="coverage-section"><div class="coverage-heading"><p class="eyebrow">The Coverage Board</p>'+block(key,2,'h2')+'</div><div class="coverage-board">'
 groups=[('PPO Plans','paper',[3,4,5,6,11]),('Administrators & Other Plans','green',[7,9,10,12]),('Medicare & MedPay','clay',[8,13])]
 for title,style,items in groups:
  out+=f'<section class="coverage-card {style}"><h3>{title}</h3><div>'+''.join(block(key,i) for i in items)+'</div></section>'
 out+='</div></section>'+cta('../');return out
def testimonials():
 key='testimonials';out=pagehead(key,'In Their Own Words.','Stories shared on the practice’s website. Individual experiences vary.')+block(key,0,'h2')
 for j,i in enumerate([1,3,5,7]):
  out+='<figure class="story">'+img(media(key,j),f'Original photograph accompanying {PAGES[key]["blocks"][i+1]["text"]}’s testimonial',prefix='../')+'<div><blockquote>'+block(key,i,'p')+'</blockquote><figcaption>'+block(key,i+1,'p')+'</figcaption></div></figure>'
 return out+block(key,9,'h2')+cta('../')
def faqs():
 key='faqs';bs=PAGES[key]['blocks'];out=pagehead(key,'A Clearer First Step.','What to bring, what to expect and where to ask your questions.')+block(key,0,'h2')+'<div class="reader">';i=1
 while i<len(bs):
  if bs[i]['tag']=='h4':
   title=bs[i]['text'];out+='<details class="content-detail">'+block(key,i,'summary')+'<div>';i+=1;count=0
   while i<len(bs) and bs[i]['tag']!='h4':out+=block(key,i);i+=1;count+=1
   if not count:out+='<p>Call the office at <a href="tel:+17074629784">707-462-9784</a> to discuss '+('referral requirements for your visit.' if 'referral' in title else 'your plan and coverage before your visit.')+'</p>'
   out+='</div></details>'
  else:out+=block(key,i);i+=1
 return out+'</div>'+cta('../')
def fitness():
 key='functional-fitness-classes';bs=PAGES[key]['blocks'];split=next(i for i,b in enumerate(bs) if b['text'].startswith('Fitness and Mobility Classes'))
 out=pagehead(key,'Strength Has No Single Starting Point.','Two distinct programs. Practical movement, supportive community and room to grow.')
 for j,(lo,hi) in enumerate([(0,split),(split,len(bs))]):
  out+='<section class="program"><div class="program-heading"><p class="eyebrow">'+('Firefly Partnership · Ages 55+' if j==0 else 'At The Dora Street Clinic')+'</p>'+img(media(key),'Fitness class pictured on the practice website',prefix='../')+'</div><div>'
  for i in range(lo,hi):
   if i==1:
    block(key,i);text=bs[i]['text'];cut=text.index(' We believe')
    out+=f'<div class="legends-copy" data-source="{key}-{i}"><p>{e(text[:cut])}</p><p>{e(text[cut+1:])}</p></div>'
   else:out+=block(key,i,'h2' if bs[i]['tag']=='h2' else 'h3' if bs[i]['tag'].startswith('h') else 'p')
  out+=('<div class="action-row"><a class="button-link" href="tel:+17072343239">Call Firefly</a><a class="text-link" href="mailto:crossfitfirefly@gmail.com">Email Firefly</a><a class="text-link" href="https://www.crossfitfirefly.com/">Crossfit Firefly</a></div>' if j==0 else '<a class="button-link" href="https://mendocinopt.as.me/">Reserve A Clinic Class</a>')+'</div></section>'
 return out+'<p class="schedule-note">Confirm current class times and the correct location before attending. Class reservations open the practice’s existing scheduling service.</p>'+cta('../')
def golf():
 key='golf-performance';out=pagehead(key,'The Body Behind Your Swing.','Bring your movement goals to the course.')
 source_title=block(key,0,'h2').replace('class="sr-only"','class="sr-only" aria-hidden="true"',1)
 credential=block(key,1,'h2').replace('<h2 ','<h2 class="tpi-credential" ',1)
 out+='<div class="care-intro"><div>'+source_title+credential+block(key,2)+'</div>'+img(media(key),'Golf photograph from the practice’s golf performance page',prefix='../')+'</div>'
 out+='<section class="tpi-assessment">'+block(key,3,'h2')+'<div class="tpi-cards">'
 for heading,copy in [(4,5),(6,7),(8,9)]:out+='<article>'+block(key,heading,'h3')+block(key,copy)+'</article>'
 out+='</div></section><div class="golf-close">'+block(key,10,'h2')+'</div>'
 return out+cta('../')
def generic(key):
 intros={'about-us':('A Local Practice. A Personal Approach.','Hands-on care, fitness and a connection to this community.'),'insurance':('Before Your Visit.','Find the practice’s listed insurance information and talk through your coverage with the office.'),'careers':('Bring Your Work To Life.','Build your career in a community that values movement.'),'contact-us':('Start With A Conversation.','Speak with the office about appointments, classes or questions.')}
 kicker,desc=intros[key];out=pagehead(key,kicker,desc)
 if key=='contact-us':
  heading=block(key,0,'h2');facts=''.join(block(key,i).replace('<p ','<p class="contact-fact" ',1) for i in range(1,4))
  address_source=block(key,4).replace('<p ','<p class="sr-only" aria-hidden="true" ',1)
  address=f'<p class="contact-address"><span>Dora St. Clinic</span><a href="{e(STREET_VIEW)}" aria-label="View The Office From Dora Street In Google Street View"><span>780 S Dora Street</span><span>Ukiah, CA 95482</span></a></p>'
  out+='<div class="contact-grid"><section class="contact-office">'+heading+facts+address_source+address+'<div class="contact-actions"><a class="button-link" href="tel:+17074629784">Call 707-462-9784</a><a class="button-link secondary" href="https://www.google.com/maps/search/?api=1&query=780+S+Dora+Street+Ukiah+CA+95482">Get Directions</a></div>'+cta('../')+'</section><section class="contact-preview"><p class="eyebrow">Online Message Preview</p><h2>Prefer To Write?</h2><p>Online messages are unavailable in this preview. Please call the office to get in touch.</p><fieldset disabled aria-label="Inactive contact form preview"><label>First Name<input type="text" autocomplete="off"></label><label>Last Name<input type="text" autocomplete="off"></label><label>Email<input type="email" autocomplete="off"></label><label>Message<textarea rows="3"></textarea></label><button type="button" disabled>Send (Preview Only)</button></fieldset></section></div>'
 else:
  if key=='careers':
   source_title=block(key,0,'h2').replace('class="sr-only"','class="sr-only" aria-hidden="true"',1);source_copy=block(key,1).replace('<p ','<p class="sr-only" aria-hidden="true" ',1)
   out+='<div class="careers-layout"><section class="careers-pitch">'+source_title+source_copy+'<p class="careers-intro">We are always looking to hire great physical therapists at Mendocino Physical Therapy.</p><h2>Room To Build Good Work.</h2><ul class="career-benefits"><li>Great compensation packages</li><li>Flexible schedules</li><li>Support for passion projects</li></ul><p class="career-note">That can include coaching a team or teaching a fitness class.</p></section><aside>'+img(media(key),'Physical therapy pictured on the careers page',prefix='../')+'</aside></div>'
  else:
   out+='<div class="editorial-body">'+source_body(key,'../')
   if key=='about-us':out+='<aside>'+img(media(key),'The practice’s facility',prefix='../')+'</aside>'
   out+='</div>'
  if key=='insurance':out+='<p class="schedule-note">A listed insurer does not confirm your individual benefits. Call the office to check your plan and visit requirements.</p>'
  if key=='about-us':out+='<p class="schedule-note">Call the office to confirm the location for your appointment.</p>'
 return out if key=='contact-us' else out+cta('../')
def special(key):
 if key=='patient-forms':
  return pagehead(key,'Get Ready For Your Visit.','A simple place to start.')+'<div class="reader"><h2>Ask The Office For Your Forms.</h2><p>Please call the office for the current new-patient paperwork and instructions for returning it securely.</p><p>This preview does not accept completed forms or health information.</p><a class="button-link" href="tel:+17074629784">Call For Patient Forms</a></div>'+cta('../')
 if key=='book-an-appointment':
  block0=block(key,0,'h2');excluded(key,1,'Unrelated Squarespace business/creative-project template copy, replaced by accurate call-to-schedule guidance')
  return pagehead(key,'Your Starting Point Is Personal.','Speak with the office about scheduling your first visit.')+'<div class="reader">'+block0+'<p>Call <a href="tel:+17074629784">707-462-9784</a> to ask about an appointment. Have your scheduling and insurance questions ready.</p><div class="quick-links">'+link('contact-us','Office & Directions','text-link','../')+link('insurance','Insurance Information','text-link','../')+link('faqs','What To Expect','text-link','../')+'</div></div>'+cta('../')
 sport=key=='sports-rehabilitation'
 return pagehead(key,'Your Goal Sets The Direction.','The right starting point is personal, whether you are returning to sport or rebuilding everyday confidence.')+f'<section class="audience-intro"><div><h2>{"Your Game. Your Comeback." if sport else "Your Independence. Your Pace."}</h2><p>{"An ACL injury, a sports setback or a return to the activities you love can bring different goals to physical therapy. Talk with the team about what matters to you." if sport else "A new knee, a return to walking or more confidence in daily movement can bring different goals to physical therapy. Talk with the team about your starting point."}</p><p>Care is based on your individual needs and goals, rather than age or activity labels.</p></div>'+img(media('physical-therapy-1') if sport else media('home',2),'Physical therapy pictured on the practice website' if sport else 'Strength and mobility pictured on the practice website',prefix='../')+'</section><div class="pathway-links">'+link('physical-therapy-1','One-On-One Physical Therapy ','path-row','../')+link('functional-fitness-classes','Fitness, Mobility & Balance ','path-row','../')+link('meet-the-team','Meet Your Care Team ','path-row','../')+link('book-an-appointment','Plan Your First Visit ','path-row','../')+'</div>'+cta('../')
def write(key,body):
 prefix='' if key=='home' else '../';path=OUT/'index.html' if key=='home' else OUT/key/'index.html';path.parent.mkdir(parents=True,exist_ok=True)
 title=TITLES.get(key,'About This Preview');desc=DESCS.get(key,title+' at Mendocino Physical Therapy. Independent website preview in Ukiah, California.')
 html=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><meta name="description" content="{e(desc)}"><title>{e(title)} | Mendocino Physical Therapy</title><link rel="canonical" href="{CANON+('' if key=='home' else key+'/')}"><link rel="icon" href="{prefix}assets/favicon.png"><link rel="stylesheet" href="{prefix}assets/style.css?v=20261025-insurance-polish-1"><link rel="stylesheet" href="{prefix}assets/workshop.css?v=20261025-insurance-polish-1"><script src="{prefix}assets/workshop.js?v=20261025-insurance-polish-1" defer></script></head><body class="page-{key}">{header(key,prefix)}<main id="main">{body}</main>{footer(prefix)}</div></body></html>'''
 path.write_text(html,encoding='utf-8')
def main():
 OUT.mkdir(exist_ok=True);(OUT/'assets/media').mkdir(parents=True,exist_ok=True)
 for a in DATA['media']:shutil.copy2(ROOT/a['file'],OUT/a['file'])
 shutil.copy2(ROOT/'assets/media/movement-workshop.webp',OUT/'assets/media/movement-workshop.webp')
 for file in ['style.css','workshop.css','workshop.js','cwu-colophon.css']:shutil.copy2(ROOT/'assets'/file,OUT/'assets'/file)
 Image.open(ROOT/'assets/media/mendocino-pt-logo.png').crop((0,0,265,333)).resize((64,80)).save(OUT/'assets/favicon.png')
 for key in TITLES:
  body=home() if key=='home' else physical() if key=='physical-therapy-1' else team() if key=='meet-the-team' else insurance() if key=='insurance' else testimonials() if key=='testimonials' else faqs() if key=='faqs' else fitness() if key=='functional-fitness-classes' else golf() if key=='golf-performance' else generic(key) if key in ['about-us','careers','contact-us'] else special(key)
  write(key,body)
 write('preview-information','<section class="page-head"><p class="eyebrow">Independent Website Preview</p><h1>About This Preview</h1><p class="lede">A new direction for Mendocino Physical Therapy, created for design review.</p></section><div class="reader"><p>This is an independent website preview, not the practice’s production website. Practice content, photographs and logo have been brought over from its public website for this review. Schedules, benefits and provider information should be confirmed with the office.</p><p>The destination guides provide editorial links only. The miniature objects are AI-generated conceptual illustrations, not photographs of the practice, patients or outcomes. The preview does not accept messages, completed patient forms or health information. Class reservations open the practice’s existing external scheduling service. External services and hosting may process information under their own policies.</p><p>Design and development by <a href="https://computerworks.ai/">ComputerWorks.ai</a>.</p></div>')
 aliases={'home':'','physical-therapy':'physical-therapy-1/','about':'insurance/'}
 for key,target in aliases.items():
  folder=OUT/key;folder.mkdir(exist_ok=True);(folder/'index.html').write_text(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="robots" content="noindex,nofollow"><meta http-equiv="refresh" content="0;url=../{target}"><title>Continue</title></head><body><a href="../{target}">Continue</a></body></html>',encoding='utf-8')
 # Configure the required shared installer and release link guard inside the deploy artifact.
 (OUT/'scripts').mkdir(exist_ok=True)
 for f in ['apply_colophon.py','colophon.html','check_release_links.py']:shutil.copy2(ROOT/'scripts'/f,OUT/'scripts'/f)
 for f in ['site-colophon.json','site-link-policy.json']:shutil.copy2(ROOT/f,OUT/f)
 (OUT/'.nojekyll').write_text('',encoding='utf-8');(OUT/'robots.txt').write_text('User-agent: *\nDisallow: /\n',encoding='utf-8')
 # Import installer explicitly; its git inventory works relative to site/ when queried inside that subdirectory.
 sys.path.insert(0,str(ROOT/'scripts'));from apply_colophon import apply
 apply(OUT)
 (ROOT/'content/migration-map.json').write_text(json.dumps(MIGRATION,indent=2,ensure_ascii=False),encoding='utf-8')
 (ROOT/'content/route-manifest.json').write_text(json.dumps({'base':CANON,'routes':['/' if k=='home' else '/'+k+'/' for k in list(TITLES)+['preview-information']]+['/'+k+'/' for k in aliases],'aliases':aliases,'excludedRoutes':{'/cart':'Empty ecommerce utility with no practice content'}},indent=2),encoding='utf-8')
 print('Built',len(TITLES)+1,'editorial pages,',len(aliases),'aliases,',len(MIGRATION),'source dispositions')
if __name__=='__main__':main()
