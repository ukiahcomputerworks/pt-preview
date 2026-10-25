'use strict';
// Local editorial wayfinding. No diagnostics, storage or collection.
const goalButtons=[...document.querySelectorAll('[data-goal]')];
function selectDestination(key,updateURL=true,fromAction=false){
 const button=goalButtons.find(item=>item.dataset.goal===key);if(!button)return;
 goalButtons.forEach(item=>item.setAttribute('aria-pressed',String(item===button)));
 document.querySelectorAll('.field-guide').forEach(panel=>{panel.hidden=panel.id!==button.getAttribute('aria-controls');});
 const panel=document.getElementById(button.getAttribute('aria-controls'));
 document.querySelector('.guide-dock').dataset.destination=key;
 document.getElementById('guide-status').textContent=button.querySelector('strong').textContent+' Destination guide opened below.';
 if(updateURL)history.replaceState(null,'','#'+key);
 if(fromAction&&matchMedia('(max-width:760px)').matches){panel.querySelector('h2').focus({preventScroll:true});panel.scrollIntoView({block:'start',behavior:matchMedia('(prefers-reduced-motion:reduce)').matches?'instant':'smooth'});}
}
goalButtons.forEach(button=>button.addEventListener('click',()=>selectDestination(button.dataset.goal,true,true)));
selectDestination(location.hash.slice(1),false);
addEventListener('hashchange',()=>selectDestination(location.hash.slice(1),false));
document.querySelectorAll('.change-destination').forEach(link=>link.addEventListener('click',()=>{const selected=goalButtons.find(button=>button.getAttribute('aria-pressed')==='true');if(selected)selected.focus({preventScroll:true});}));
document.addEventListener('keydown',event=>{if(event.key==='Escape')document.querySelectorAll('.menu[open]').forEach(menu=>{menu.removeAttribute('open');menu.querySelector('summary').focus();});});
