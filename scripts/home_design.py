"""Source-backed reference, people and practical sections for the homepage."""
def render_reference(block,img,media,link,cta,pages,data):
 out=''
 out+='''<div class="practical-rail"><span>Before You Visit</span><a href="insurance/">Insurance ↗</a><a href="faqs/">What To Bring ↗</a><a href="contact-us/">Find Us ↗</a></div>'''
 names=[b['text'] for b in pages['meet-the-team']['blocks'] if b['tag']=='h3' and not b['text'].startswith('Get started')]
 out+='<section class="real-people"><div class="people-intro"><p class="eyebrow">People From Here</p><h2>The People Behind Your Next Step.</h2><p>Meet the team. Read their stories.</p>'+link('meet-the-team','Meet The Whole Team ↗')+'</div><div class="people-strip">'
 for i,name in enumerate(names):out+=f'<a href="meet-the-team/#person-{i+1}">'+img(media('meet-the-team',i),'')+f'<span>{name}</span></a>'
 out+='</div></section><section class="practice-reference"><div class="reference-heading"><p class="eyebrow">Care, In Plain Sight.</p><h2>The Practice, <br>In Detail.</h2></div><div class="reference-rows"><details class="content-detail"><summary>How We Work</summary><div class="reference-copy">'
 for i in range(8):out+=block('home',i,'h3' if pages['home']['blocks'][i]['tag'].startswith('h') else 'p')
 out+=img(media('home',0),'Outdoor photograph featured by Mendocino Physical Therapy','reference-photo')+'</div></details><details class="content-detail"><summary>Care Areas</summary><div>'+block('home',8,'p')+'<div class="expertise-list">'
 icons=[a['file'] for a in data['media'] if any(x in a['file'] for x in ['04-tape','05-heart','06-lungs','07-pelvis','08-dumbell'])]
 for j,i in enumerate(range(9,14)):out+='<a href="physical-therapy-1/">'+img(icons[j],'')+block('home',i,'h3')+'<span aria-hidden="true">↗</span></a>'
 out+='</div></div></details><details class="content-detail"><summary>Fitness & Community</summary><div class="reference-copy">'+block('home',14,'h3')+block('home',15)+img(media('home',8),'Fitness class pictured on the practice website','reference-photo')+link('functional-fitness-classes','Schedules, Classes & Registration ↗')+'</div></details></div></section>'
 return out+cta('')
