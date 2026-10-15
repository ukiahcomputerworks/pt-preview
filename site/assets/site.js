'use strict';
// Editorial navigation only. No diagnosis, storage, data collection or autoplay.
const destinations={
 sport:{word:'Play.',kicker:'01 / Back To Sport',title:'A Way Back To Your Game.',copy:'An ACL injury or a sports setback brings its own questions. Explore the practice’s sports rehabilitation and meet the people behind your care.',link:'sports-rehabilitation/',label:'Explore Sports Care ↗'},
 everyday:{word:'Everyday.',kicker:'02 / Everyday Independence',title:'The Small Stuff Is Big Stuff.',copy:'Walking, balance, getting through your day. Explore one-on-one care and mobility options with your own starting point in mind.',link:'healthy-aging/',label:'Explore Everyday Care ↗'},
 recovery:{word:'Next.',kicker:'03 / Life After Surgery',title:'A New Knee. A Chapter Of Your Own.',copy:'Postoperative rehabilitation starts with your needs and goals. Find the practice’s care information, then plan a conversation with the office.',link:'physical-therapy-1/',label:'Explore Postoperative Care ↗'},
 golf:{word:'Swing.',kicker:'04 / A Full Round',title:'The Next Round Starts With You.',copy:'Explore the practice’s TPI body screen, swing analysis and personalized corrective exercise program, with golf-specific movement in view.',link:'golf-performance/',label:'Explore Golf Performance ↗'}
};
function selectDestination(key,updateURL=true){
 const record=destinations[key],board=document.querySelector('.unpause');if(!record||!board)return;
 document.querySelectorAll('[data-goal]').forEach(button=>button.setAttribute('aria-pressed',String(button.dataset.goal===key)));
 board.dataset.scene=key;
 document.getElementById('destination-word').textContent=record.word;
 document.getElementById('goal-kicker').textContent=record.kicker;
 document.getElementById('goal-title').textContent=record.title;
 document.getElementById('goal-copy').textContent=record.copy;
 const link=document.getElementById('goal-link');link.setAttribute('href',record.link);link.textContent=record.label;
 board.classList.remove('route-change');void board.offsetWidth;board.classList.add('route-change');
 if(updateURL)history.replaceState(null,'','#'+key);
}
document.querySelectorAll('[data-goal]').forEach(button=>button.addEventListener('click',()=>selectDestination(button.dataset.goal)));
const initial=location.hash.slice(1);if(destinations[initial])selectDestination(initial,false);
addEventListener('hashchange',()=>{const key=location.hash.slice(1);if(destinations[key])selectDestination(key,false);});
document.addEventListener('keydown',event=>{if(event.key==='Escape')document.querySelectorAll('.menu[open]').forEach(menu=>{menu.removeAttribute('open');menu.querySelector('summary').focus();});});
