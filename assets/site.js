'use strict';
const goals={
 sport:{kicker:'01 / Back To Sport',title:'Your Game. Your Comeback.',copy:'Recovering from a sports injury or an ACL injury? Talk with the team about your goals, your sport and where you want to go next.',link:'sports-rehabilitation/',label:'Explore Sports Rehabilitation ↗',image:'assets/media/24-tempimageifqpdx.jpg',alt:'Hands-on physical therapy pictured on the practice website',path:'M55 380C210 380 235 300 355 330S550 380 700 235'},
 everyday:{kicker:'02 / Everyday Confidence',title:'Steady Steps. Full Days.',copy:'Walking, balance, everyday strength and feeling more confident in your movement. Explore one-on-one care and fitness opportunities at every stage of life.',link:'healthy-aging/',label:'Explore Everyday Confidence ↗',image:'assets/media/03-tempimagei0xaud.jpg',alt:'Strength and mobility pictured on the practice website',path:'M55 380C190 380 200 300 320 320S530 380 700 250'},
 recovery:{kicker:'03 / After Surgery',title:'A New Knee. Your Own Next Chapter.',copy:'Your recovery goals are personal. The practice offers postoperative rehabilitation with individualized attention, hands-on care and exercise.',link:'physical-therapy-1/',label:'Explore Physical Therapy ↗',image:'assets/media/21-tempimage7gkmq2.jpg',alt:'Individual physical therapy pictured on the practice website',path:'M55 400C170 400 240 360 350 350S530 320 700 260'},
 golf:{kicker:'04 / A Full Round',title:'There’s More To Your Swing.',copy:'A body screen, swing analysis and a personalized corrective exercise program connect golf performance with the way you move.',link:'golf-performance/',label:'Explore Golf Performance ↗',image:'assets/media/22-image-asset.jpg',alt:'Golf photograph from the practice website',path:'M55 380C230 380 250 70 465 75S700 240 520 350'}
};
document.querySelectorAll('[data-goal]').forEach(button=>button.addEventListener('click',()=>{
 const record=goals[button.dataset.goal];
 document.querySelectorAll('[data-goal]').forEach(item=>item.setAttribute('aria-pressed',String(item===button)));
 document.querySelector('[data-scene]').dataset.scene=button.dataset.goal;
 document.getElementById('goal-kicker').textContent=record.kicker;
 document.getElementById('goal-title').textContent=record.title;
 document.getElementById('goal-copy').textContent=record.copy;
 const link=document.getElementById('goal-link');link.href=record.link;link.textContent=record.label;
 const image=document.querySelector('.goal-photo');image.src=record.image;image.alt=record.alt;
 document.getElementById('motion-path').setAttribute('d',record.path);
}));
document.addEventListener('keydown',event=>{if(event.key==='Escape')document.querySelectorAll('.menu[open]').forEach(menu=>{menu.removeAttribute('open');menu.querySelector('summary').focus();});});
