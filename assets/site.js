'use strict';
const records={
 outdoors:{kicker:'01 / The Outdoors',title:'Take The Long Way Home.',copy:'One-on-one physical therapy, with movement and exercise tailored to your needs and goals.',graphic:'Conceptual illustration of a walking path through a Mendocino-inspired landscape',path:'M65 380C130 343 176 395 250 360S345 280 420 315S545 390 675 293'},
 everyday:{kicker:'02 / Everyday Strength',title:'Make Room For Everyday Wins.',copy:'Explore fitness and mobility classes focused on strength, balance and everyday movement. Ask about clinic classes and the separate 55+ Legends program with Crossfit Firefly.',graphic:'Conceptual illustration of everyday lifting and movement in a landscape',path:'M65 380C180 380 205 270 305 302S475 385 530 270S620 230 675 293'},
 recovery:{kicker:'03 / Life After Surgery',title:'Your Next Chapter Starts Here.',copy:'The practice offers personalized postoperative rehabilitation. Talk with a physical therapist about your recovery needs and the activities that matter to you.',graphic:'Conceptual illustration of a person walking with a support and a gradual path',path:'M65 390C180 390 220 360 315 355S465 325 530 310S620 290 675 270'},
 golf:{kicker:'04 / A Full Round',title:'There’s More To Your Swing.',copy:'A body screen, swing analysis and personalized exercise program connect golf performance with the way you move. Ask the practice about its TPI assessment.',graphic:'Conceptual illustration of a golfer and a swing arc',path:'M65 380C250 380 280 80 470 80S700 250 504 331'}
};
document.querySelectorAll('[data-goal]').forEach(button=>button.addEventListener('click',()=>{
 const key=button.dataset.goal,record=records[key];
 document.querySelectorAll('[data-goal]').forEach(item=>item.setAttribute('aria-pressed',String(item===button)));
 document.querySelector('[data-scene]').dataset.scene=key;
 document.getElementById('goal-kicker').textContent=record.kicker;
 document.getElementById('goal-title').textContent=record.title;
 document.getElementById('goal-copy').textContent=record.copy;
 document.getElementById('scene-title').textContent=record.graphic;
 document.getElementById('motion-path').setAttribute('d',record.path);
}));
