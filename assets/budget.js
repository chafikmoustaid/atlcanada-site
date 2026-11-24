/* Calculateur de budget ATL Canada : estimation indicative, aucune donnée envoyée. */
(function(){
var root=document.getElementById('budget-app'); if(!root) return;
var AR=root.getAttribute('data-lang')==='ar', EN=root.getAttribute('data-lang')==='en';
var RDV=EN?'/en/book-consultation/':AR?'/ar/book-consultation/':'/rendez-vous/', HON=EN?'/en/fees/':AR?'/ar/fees/':'/honoraires/', OFF=EN?'/en/official-fees/':AR?'/ar/official-fees/':'/frais-officiels-immigration-canada/';
/* type : single = 1 demandeur ; pr = résidence permanente (conjoint et enfants) */
var S=[
 {id:'cons',h:100,g:0,t:'single',fr:'Consultation initiale (30 min)',en:'Initial consultation (30 min)',ar:'استشارة أولية (30 دقيقة)'},
 {id:'study',h:900,g:150,b:1,t:'single',fr:"Permis d'études",en:'Study permit',ar:'تصريح الدراسة'},
 {id:'work',h:650,g:155,b:1,t:'single',fr:'Permis de travail : prolongation ou postdiplôme',en:'Work permit: extension or post-graduation',ar:'تصريح العمل: التمديد أو ما بعد التخرج'},
 {id:'workx',h:1100,g:155,b:1,t:'single',fr:"Permis de travail exempté d'EIMT",en:'LMIA-exempt work permit',ar:'تصريح عمل معفى من LMIA'},
 {id:'visit',h:450,g:100,b:1,t:'single',fr:'Visa de visiteur',en:'Visitor visa',ar:'تأشيرة الزيارة'},
 {id:'super',h:800,g:100,b:1,t:'single',fr:'Super visa (par demandeur)',en:'Super visa (per applicant)',ar:'السوبر فيزا (لكل مقدِّم طلب)'},
 {id:"ee",h:2150,g:1590,b:1,t:'pr',fr:'Entrée express (profil + résidence permanente)',en:'Express Entry (profile + permanent residence)',ar:'الدخول السريع (الملف + الإقامة الدائمة)'},
 {id:'pnp',h:3000,g:1590,b:1,t:'pr',fr:'Candidat des provinces (hors Entrée express)',en:'Provincial nominee (outside Express Entry)',ar:'برامج المقاطعات (خارج الدخول السريع)'},
 {id:'spouse',h:2200,g:1260,b:1,t:'single',fr:"Parrainage d'un époux ou conjoint",en:'Spousal or partner sponsorship',ar:'كفالة الزوج أو الزوجة'},
 {id:'parent',h:2500,g:1260,b:1,t:'single',fr:'Parrainage de parents ou grands-parents',en:'Parent or grandparent sponsorship',ar:'كفالة الوالدين أو الأجداد'},
 {id:'cit',h:500,g:653,t:'single',fr:'Citoyenneté canadienne (adulte)',en:'Canadian citizenship (adult)',ar:'الجنسية الكندية (بالغ)'},
 {id:'card',h:600,g:50,t:'single',fr:'Renouvellement de la carte de résident permanent',en:'Permanent resident card renewal',ar:'تجديد بطاقة الإقامة الدائمة'}
];
var LE={svc:'Which service are you interested in?',sp:'Is a spouse or partner coming with you?',ch:'Number of dependent children',no:'No',yes:'Yes',res:'Your estimate',hon:'Our fees (starting from)',gov:'Government fees (IRCC)',bio:'Biometrics (if required)',fam:'Additional family members',tot:'Estimated total',note:'Indicative estimate in Canadian dollars. Applicable taxes are added to our fees. The final price is set after the consultation and written in the service agreement. Language tests, translations, medical exams and Quebec fees are not included.',cta:'Book a consultation',wa:'Send to a relative (WhatsApp)',sh:'Canada immigration budget calculator from ATL Canada:',h2:'Our fees',h3:'Official fees'};
var L=EN?LE:AR?{svc:'ما الخدمة التي تهمك؟',sp:'هل يرافقك زوج أو شريك؟',ch:'عدد الأطفال المعالين',no:'لا',yes:'نعم',res:'تقديرك',hon:'أتعابنا (ابتداءً من)',gov:'رسوم الحكومة (IRCC)',bio:'البيانات البيومترية (إن طُلبت)',fam:'أفراد العائلة الإضافيون',tot:'المجموع التقديري',note:'تقدير للمعلومة فقط بالدولار الكندي. الضرائب المطبّقة تُضاف إلى الأتعاب. السعر النهائي يُحدَّد بعد الاستشارة ويُكتب في عقد الخدمات. لا تشمل الرسوم اختبارات اللغة والترجمة والفحص الطبي ورسوم كيبيك.',cta:'احجز استشارة',wa:'أرسل إلى قريب عبر واتساب',sh:'حاسبة ميزانية الهجرة إلى كندا من ATL Canada:',h2:'الأتعاب',h3:'الرسوم الرسمية'}
:{svc:"Quel service vous intéresse ?",sp:"Un époux ou conjoint vous accompagne-t-il ?",ch:"Nombre d'enfants à charge",no:'Non',yes:'Oui',res:'Votre estimation',hon:'Nos honoraires (à partir de)',gov:'Frais du gouvernement (IRCC)',bio:'Biométrie (si requise)',fam:'Membres de la famille en plus',tot:'Total estimé',note:"Estimation indicative en dollars canadiens. Les taxes applicables s'ajoutent aux honoraires. Le prix final est fixé après la consultation et écrit dans l'entente de services. Les tests de langue, traductions, examens médicaux et frais du Québec ne sont pas inclus.",cta:'Prendre rendez-vous',wa:'Envoyer à un proche (WhatsApp)',sh:"Calculateur de budget d'immigration au Canada, ATL Canada :",h2:'Nos honoraires',h3:'Frais officiels'};
function fm(n){var d=(AR||EN)?'.':',';var s=String(Math.round(n*100)/100).replace('.',d);var p=s.split(d);p[0]=p[0].replace(/\B(?=(\d{3})+(?!\d))/g,EN?',':'\u00a0');s=p.join(d);return AR?'<bdi dir="ltr">'+s+' $</bdi>':EN?'$'+s:s+'\u00a0$';}
var h='<div class="bd-card"><label class="bd-l" for="bd-s">'+L.svc+'</label><select id="bd-s">';
S.forEach(function(x,i){h+='<option value="'+i+'">'+(EN?x.en:AR?x.ar:x.fr)+'</option>';});
h+='</select><div id="bd-pr" hidden><label class="bd-l" for="bd-sp">'+L.sp+'</label><select id="bd-sp"><option value="0">'+L.no+'</option><option value="1">'+L.yes+'</option></select>'
+'<label class="bd-l" for="bd-ch">'+L.ch+'</label><input id="bd-ch" type="number" min="0" max="8" value="0" inputmode="numeric"></div></div>'
+'<div class="bd-res" id="bd-out" aria-live="polite"></div>';
root.innerHTML=h;
var s=document.getElementById('bd-s'),pr=document.getElementById('bd-pr'),sp=document.getElementById('bd-sp'),ch=document.getElementById('bd-ch'),out=document.getElementById('bd-out');
function row(k,v,c){return '<tr'+(c?' class="'+c+'"':'')+'><td>'+k+'</td><td class="num">'+v+'</td></tr>';}
function calc(){
 var x=S[+s.value],isPr=x.t==='pr';pr.hidden=!isPr;
 var spo=isPr?+sp.value:0,kids=isPr?Math.max(0,Math.min(8,parseInt(ch.value,10)||0)):0,n=1+spo+kids;
 var hon=x.h+(spo+kids)*400;
 var gov=x.g+spo*1590+kids*270;
 var bio=x.b?Math.min(85*n,n>1?170:85):0;
 var t='<h2>'+L.res+'</h2><table class="tbl bd-t"><tbody>'+row(L.hon,fm(x.h));
 if(spo+kids) t+=row(L.fam+' ('+(spo+kids)+' × '+fm(400)+')',fm((spo+kids)*400));
 t+=row(L.gov,fm(gov));
 if(bio) t+=row(L.bio,fm(bio));
 t+=row(L.tot,fm(hon+gov+bio),'bd-tot')+'</tbody></table><p class="bd-n">'+L.note+'</p><p class="bd-cta"><a class="btn btn-solid" href="'+RDV+'">'+L.cta+'</a> <a class="btn" href="'+HON+'">'+L.h2+'</a> <a class="btn" href="'+OFF+'">'+L.h3+'</a> <a class="btn bd-wa" target="_blank" rel="noopener" href="https://wa.me/?text='+encodeURIComponent(L.sh+' '+location.href)+'">'+L.wa+'</a></p>';
 out.innerHTML=t;
}
[s,sp,ch].forEach(function(e){e.addEventListener('input',calc);e.addEventListener('change',calc);});
calc();
})();
