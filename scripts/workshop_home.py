"""Tangible destination navigation, with useful care and visit guides."""
from html import escape

DESTINATIONS = [
 dict(key='sport', number='01', title='The Game.', subtitle='Sports & ACL Injury', color='court',
      heading='Your Sport. Your Starting Point.',
      copy='An injury changes the plan. Start with the movement you want back, then explore the care and people behind it.',
      routes=[('sports-rehabilitation','Sports Rehabilitation','Start with your activity and your goals.'),('physical-therapy-1','How PT Works','Explore the practice’s care approach and techniques.'),('meet-the-team','Meet Your Team','Read the clinicians’ backgrounds before you call.')],
      question='“I want to get back to my sport. What should I bring to my first visit?”'),
 dict(key='everyday', number='02', title='The Everyday.', subtitle='Walking, Stairs & Balance', color='porch',
      heading='The Front Steps Count, Too.',
      copy='Getting out the door, feeling steadier, doing your day. Everyday movement deserves its own starting point.',
      routes=[('healthy-aging','Everyday Confidence','Explore care around mobility and independence.'),('functional-fitness-classes','Fitness & Mobility','Compare the practice’s two class programs and locations.'),('physical-therapy-1','One-On-One Care','Read about the practice’s individual approach.')],
      question='“I want help with everyday movement. Should I ask about a PT visit or a class?”'),
 dict(key='recovery', number='03', title='What’s Next.', subtitle='After Surgery / New Knee', color='hinge',
      heading='A New Knee. Your Next Chapter.',
      copy='Recovery has a starting point of its own. Explore the practice’s postoperative care information and prepare your questions for the office.',
      routes=[('physical-therapy-1','Postoperative Care','Find postoperative rehabilitation in the care information.'),('faqs','Before You Arrive','Review visit questions and what to bring.'),('insurance','Insurance & Coverage','Check the listed plans, then confirm your own benefits.')],
      question='“I have had surgery. What referral, instructions or paperwork does your office need?”'),
 dict(key='golf', number='04', title='A Full Round.', subtitle='Golf & TPI Performance', color='green',
      heading='Look At The Body Behind The Swing.',
      copy='A golf-specific way in: explore the TPI body screen, swing analysis and corrective exercise program described by the practice.',
      routes=[('golf-performance','Golf Performance','Read about the TPI assessment and golf program.'),('meet-the-team','People Behind The Program','Explore the team’s training and backgrounds.'),('contact-us','Ask About An Assessment','Speak with the office about the golf program.')],
      question='“I am interested in golf performance. How do I ask about a TPI assessment?”'),
]

def render(block,img,media,link,cta,pages,data):
 from home_design import render_reference
 out='''<section class="workshop" aria-labelledby="headline"><div class="workshop-intro"><div><p class="eyebrow">Mendocino Physical Therapy / Ukiah, California</p><h1 id="headline">Your Life Has<br><em>Places To Be.</em></h1></div><div class="workshop-manifesto"><span class="workshop-seal" aria-hidden="true">Start Where<br>You Are.</span><p>A court. The front steps. The next round.<br> Pick what matters to you. We’ll help you find your way into the practice.</p><p class="workshop-services">One-On-One PT · Fitness · Golf Performance</p></div></div><div class="workshop-toolbar"><h2>Where Do You Want To Go?</h2><span>Open A Destination Guide</span></div><div class="object-gateways" id="destinations" role="group" aria-label="Choose a destination guide">'''
 for d in DESTINATIONS:
  out+=f'''<button class="object-gateway {d['color']}" type="button" data-goal="{d['key']}" aria-pressed="false" aria-controls="guide-{d['key']}"><span class="object-art" aria-hidden="true"></span><span class="object-label"><strong>{d['title']}</strong><small>{d['subtitle']}</small><span class="open-guide">Open Guide</span></span></button>'''
 out+='''</div><p id="guide-status" class="sr-only" role="status"></p><noscript><nav class="no-script-choices" aria-label="Care destinations"><a href="sports-rehabilitation/">Sports Rehabilitation</a><a href="healthy-aging/">Everyday Confidence</a><a href="physical-therapy-1/">After Surgery</a><a href="golf-performance/">Golf Performance</a></nav></noscript></section><div class="guide-dock"><section class="field-guide overview-guide" id="guide-overview" aria-labelledby="overview-title"><div class="guide-intro"><p class="eyebrow">Your Way In</p><h2 id="overview-title">No Two Starting <br>Points Alike.</h2><p>Choose an object above for care information, useful links and a question to start the conversation.</p></div><div class="guide-overview-links"><a href="physical-therapy-1/"><span>Know What You Need?</span><strong>Go Straight To Care </strong></a><a href="book-an-appointment/"><span>Ready To Talk?</span><strong>Plan Your First Visit </strong></a><a href="functional-fitness-classes/"><span>Looking For Classes?</span><strong>Find Fitness & Mobility </strong></a></div></section>'''
 for d in DESTINATIONS:
  out+=f'''<section class="field-guide" id="guide-{d['key']}" hidden aria-labelledby="guide-title-{d['key']}"><div class="guide-intro"><p class="eyebrow">Your Destination Guide</p><h2 id="guide-title-{d['key']}" tabindex="-1">{d['heading']}</h2><p>{d['copy']}</p><a class="change-destination" href="#destinations">Choose Another Destination</a></div><div class="guide-content"><nav class="guide-routes" aria-label="{d['subtitle']} resources">'''
  for n,(route,title,desc) in enumerate(d['routes'],1):
   out+=f'<a href="{route}/"><span><strong>{title}</strong><small>{desc}</small></span></a>'
  out+=f'''</nav><details class="conversation-note"><summary>A Question To Start With <span aria-hidden="true">+</span></summary><div><p>{escape(d['question'])}</p><a href="tel:+17074629784">Call 707-462-9784</a><a href="book-an-appointment/">First-Visit Information</a></div></details></div></section>'''
 out+='</div>'
 return out+render_reference(block,img,media,link,cta,pages,data)
