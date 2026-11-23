/* Évaluer mon dossier : mini-questionnaire d'orientation (ATL Canada). Aucune donnée envoyée. */
(function(){
var root=document.getElementById('eval-app'); if(!root) return;
var AR=root.getAttribute('data-lang')==='ar';
var P=AR?'/ar/':'/';
var U={study:AR?'/ar/study-permit-morocco/':'/permis-etudes-canada-maroc/',work:AR?'/ar/work-permit/':'/permis-de-travail-canada/',pr:AR?'/ar/permanent-residence/':'/residence-permanente-canada/',ee:AR?'/ar/express-entry/':'/entree-express-canada/',eef:AR?'/ar/express-entry-french/':'/entree-express-francophone-maroc/',pnp:AR?'/ar/provincial-nominee/':'/candidats-provinces-canada/',qc:AR?'/ar/immigrate-to-quebec/':'/immigration-quebec-canada/',fam:AR?'/ar/family-sponsorship/':'/parrainage-familial-canada/',visit:AR?'/ar/visitor-visa-super-visa/':'/visa-visiteur-super-visa-canada/',biz:AR?'/ar/business-immigration/':'/gens-affaires-immigration-canada/',cit:AR?'/ar/canadian-citizenship/':'/citoyennete-canadienne/',docs:AR?'/ar/moroccan-documents/':'/documents-maroc-immigration-canada/',calc:AR?'/ar/express-entry-calculator/':'/calculateur-entree-express/'};
var T=AR?{
 q:[
  ['ما هدفك الرئيسي؟','goal',[['study','الدراسة في كندا'],['work','العمل في كندا'],['pr','الإقامة الدائمة'],['qc','الاستقرار في كيبيك'],['fam','كفالة فرد من العائلة'],['visit','زيارة أو سوبر فيزا'],['biz','مشروع أو استثمار'],['cit','الجنسية الكندية']]],
  ['أين تقيم حاليًا؟','res',[['ma','المغرب'],['ca','كندا'],['xx','بلد آخر']]],
  ['ما فئتك العمرية؟','age',[['a','18 إلى 29 سنة'],['b','30 إلى 35 سنة'],['c','36 إلى 44 سنة'],['d','45 سنة فأكثر']]],
  ['ما أعلى مستوى دراسي لديك؟','edu',[['sec','الثانوي'],['pro','دبلوم مهني أو تقني'],['bac','إجازة أو بكالوريوس'],['mst','ماستر أو دكتوراه']]],
  ['ما وضعك اللغوي؟','lang',[['fr','أتقن الفرنسية'],['en','أتقن الإنجليزية'],['both','أتقن اللغتين'],['none','لا أملك مستوى جيدًا بعد']]]],
 next:'التالي',back:'رجوع',restart:'إعادة التقييم',step:function(a,b){return 'السؤال '+a+' من '+b},
 title:'توجيهنا الأولي لك',lead:'هذا توجيه عام انطلاقًا من إجاباتك، وليس تقييمًا قانونيًا لملفك. لا تُرسل إجاباتك ولا تُحفظ.',
 main:'الصفحة الأنسب لك',more:'قد يهمك أيضًا',points:'نقاط نناقشها في الاستشارة',
 cta:'احجز استشارة مع مستشار مرخَّص',call:'اتصل: <bdi dir="ltr">+1 514 295 6635</bdi>',wa:'واتساب',
 note:'لا يمكن لأي مستشار ضمان نتيجة: القرار يعود حصريًا للسلطات الكندية والكيبيكية.',
 tx:{
  calc:'قدّر درجتك في الدخول السريع',ee:'الدخول السريع',eef:'الدخول السريع للناطقين بالفرنسية',pnp:'برامج المقاطعات',docs:'وثائق المغرب المطلوبة',pr:'الإقامة الدائمة',qc:'الهجرة إلى كيبيك',study:'تصريح الدراسة',work:'تصريح العمل',fam:'الكفالة العائلية',visit:'تأشيرة الزيارة والسوبر فيزا',biz:'الهجرة لرجال الأعمال',cit:'الجنسية الكندية'},
 pt:{
  nolang:'الخطوة الأولى غالبًا هي اختبار لغة معتمد (TEF أو TCF للفرنسية، IELTS أو CELPIP للإنجليزية).',
  age45:'تتراجع نقاط العمر في الدخول السريع مع التقدم في السن؛ نقارن لذلك مسارات أخرى كبرامج المقاطعات.',
  fr:'إتقان الفرنسية ميزة مهمة، خصوصًا لكيبيك وللمسارات المخصصة للناطقين بالفرنسية.',
  qcfr:'تُشترط معرفة مرضية بالفرنسية للاستقرار في كيبيك.',
  edu:'نتحقق من معادلة شهاداتك (تقييم الشهادات الأجنبية) لأنها تؤثر في النقاط.',
  ca:'بما أنك في كندا: نتحقق من تاريخ انتهاء وضعك الحالي قبل أي خطوة، لأن الحفاظ على الوضع القانوني أولوية.',
  ma:'نراجع الوثائق اللازمة من المغرب (سجل عدلي، عقود، شهادات) مبكرًا لتفادي التأخير.',
  stu:'نراجع قدرتك المالية واختيار المؤسسة التعليمية قبل تقديم الطلب.',
  job:'نبحث هل عرض العمل أو التجربة المهنية تتيح مسارًا واقعيًا.',
  gen:'نقارن المسارات الواقعية لملفك قبل أي مصروف.'}
}:{
 q:[
  ['Quel est votre objectif principal ?','goal',[['study','Étudier au Canada'],['work','Travailler au Canada'],['pr','Obtenir la résidence permanente'],['qc','M\'établir au Québec'],['fam','Parrainer un proche'],['visit','Visite ou super visa'],['biz','Projet d\'affaires ou investissement'],['cit','Devenir citoyen canadien']]],
  ['Où habitez-vous actuellement ?','res',[['ma','Au Maroc'],['ca','Au Canada'],['xx','Dans un autre pays']]],
  ['Votre tranche d\'âge ?','age',[['a','18 à 29 ans'],['b','30 à 35 ans'],['c','36 à 44 ans'],['d','45 ans et plus']]],
  ['Votre plus haut niveau d\'études ?','edu',[['sec','Secondaire'],['pro','Diplôme professionnel ou technique'],['bac','Licence ou baccalauréat'],['mst','Maîtrise ou doctorat']]],
  ['Votre situation linguistique ?','lang',[['fr','Je maîtrise le français'],['en','Je maîtrise l\'anglais'],['both','Je maîtrise les deux'],['none','Pas encore de bon niveau']]]],
 next:'Suivant',back:'Retour',restart:'Recommencer',step:function(a,b){return 'Question '+a+' sur '+b},
 title:'Notre orientation pour vous',lead:'Il s\'agit d\'une orientation générale d\'après vos réponses, pas d\'une évaluation juridique de votre dossier. Vos réponses ne sont ni envoyées ni enregistrées.',
 main:'La page la plus adaptée',more:'À regarder aussi',points:'Points à voir en consultation',
 cta:'Réserver une consultation avec un consultant réglementé',call:'Appeler : +1 514 295 6635',wa:'WhatsApp',
 note:'Aucun consultant ne peut garantir un résultat : la décision appartient uniquement aux autorités canadiennes et québécoises.',
 tx:{
  calc:'Estimer mon score Entrée express',ee:'Entrée express',eef:'Entrée express pour les francophones',pnp:'Candidats des provinces',docs:'Documents du Maroc',pr:'Résidence permanente',qc:'Immigrer au Québec',study:'Permis d\'études',work:'Permis de travail',fam:'Parrainage familial',visit:'Visa de visiteur et super visa',biz:'Gens d\'affaires',cit:'Citoyenneté canadienne'},
 pt:{
  nolang:'La première étape est souvent un test de langue reconnu (TEF ou TCF pour le français, IELTS ou CELPIP pour l\'anglais).',
  age45:'Les points d\'âge d\'Entrée express diminuent avec l\'âge : nous comparons donc d\'autres voies, comme les programmes des provinces.',
  fr:'Maîtriser le français est un atout, notamment pour le Québec et pour les voies réservées aux francophones.',
  qcfr:'Une connaissance satisfaisante du français est exigée pour s\'établir au Québec.',
  edu:'Nous vérifions l\'équivalence de vos diplômes (évaluation des diplômes étrangers), car elle influence les points.',
  ca:'Comme vous êtes au Canada, nous vérifions d\'abord la date d\'expiration de votre statut : conserver un statut valide est la priorité.',
  ma:'Nous préparons tôt les documents à obtenir au Maroc (casier judiciaire, attestations, diplômes) pour éviter les retards.',
  stu:'Nous examinons votre capacité financière et le choix de l\'établissement avant le dépôt.',
  job:'Nous regardons si une offre d\'emploi ou votre expérience ouvre une voie réaliste.',
  gen:'Nous comparons les voies réalistes pour votre profil avant toute dépense.'}
};
function h(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
var ans={},i=0,Q=T.q;
function result(){
 var g=ans.goal,main,more=[],pts=[],tx=T.tx,pt=T.pt;
 var skilled=(ans.edu==='bac'||ans.edu==='mst'||ans.edu==='pro');
 var fr=(ans.lang==='fr'||ans.lang==='both');
 if(g==='pr'){
  main=(fr&&ans.res==='ma')?'eef':'ee'; more=[main==='eef'?'ee':'eef','calc','pnp','qc'];
  if(ans.lang==='none')pts.push(pt.nolang);
  if(ans.age==='d')pts.push(pt.age45);
  if(skilled)pts.push(pt.edu);
 } else if(g==='qc'){
  main='qc'; more=['pr','pnp','study']; pts.push(pt.qcfr); if(!fr)pts.push(pt.nolang); if(skilled)pts.push(pt.edu);
 } else if(g==='study'){
  main='study'; more=['work','qc']; pts.push(pt.stu); if(ans.lang==='none')pts.push(pt.nolang);
 } else if(g==='work'){
  main='work'; more=['pr','ee']; pts.push(pt.job); if(ans.lang==='none')pts.push(pt.nolang);
 } else { main=g; more=g==='fam'?['pr','visit']:g==='visit'?['fam','work']:g==='biz'?['pr','pnp','qc']:['pr']; pts.push(pt.gen); }
 if(fr&&g!=='pr'&&g!=='qc')pts.push(pt.fr);
 if(ans.res==='ca')pts.unshift(pt.ca);
 if(ans.res==='ma'){ pts.push(pt.ma); if(more.indexOf('docs')<0)more.push('docs'); }
 var seen={};seen[main]=1;more=more.filter(function(k){if(seen[k])return false;seen[k]=1;return true}).slice(0,4);
 var o='<div class="ev-res"><h2>'+h(T.title)+'</h2><p class="help">'+h(T.lead)+'</p>';
 o+='<div class="ev-main"><span>'+h(T.main)+'</span><a class="btn btn-solid" href="'+U[main]+'">'+h(tx[main])+(AR?' ←':' →')+'</a></div>';
 o+='<h3>'+h(T.more)+'</h3><ul class="ev-more">'+more.map(function(k){return '<li><a href="'+U[k]+'">'+h(tx[k])+'</a></li>'}).join('')+'</ul>';
 o+='<h3>'+h(T.points)+'</h3><ul class="ev-pts">'+pts.map(function(x){return '<li>'+h(x)+'</li>'}).join('')+'</ul>';
 o+='<div class="ev-cta"><a class="btn btn-solid" href="tel:+15142956635">'+T.call+'</a> <a class="btn" href="https://wa.me/15142956635" rel="noopener">'+h(T.wa)+'</a></div>';
 o+='<p class="note">'+h(T.note)+'</p><p><button type="button" class="ev-link" id="ev-restart">'+h(T.restart)+'</button></p></div>';
 return o;
}
function render(){
 if(i>=Q.length){root.innerHTML=result();root.querySelector('#ev-restart').onclick=function(){ans={};i=0;render();root.scrollIntoView({behavior:'smooth',block:'start'})};return}
 var q=Q[i],key=q[1],opts=q[2]||q[2];
 if(key==='goal'){opts=q[2]}
 var o='<div class="ev-step"><div class="ev-bar"><i style="width:'+Math.round(i/Q.length*100)+'%"></i></div><p class="ev-count">'+h(T.step(i+1,Q.length))+'</p><fieldset><legend>'+h(q[0])+'</legend><div class="ev-opts">';
 opts.forEach(function(op){o+='<label class="ev-opt"><input type="radio" name="q" value="'+op[0]+'"'+(ans[key]===op[0]?' checked':'')+'><span>'+h(op[1])+'</span></label>'});
 o+='</div></fieldset><div class="ev-nav">'+(i>0?'<button type="button" class="btn" id="ev-back">'+h(T.back)+'</button>':'')+'<button type="button" class="btn btn-solid" id="ev-next" disabled>'+h(T.next)+'</button></div></div>';
 root.innerHTML=o;
 var nx=root.querySelector('#ev-next');
 if(ans[key])nx.disabled=false;
 root.querySelectorAll('input[name=q]').forEach(function(r){r.onchange=function(){ans[key]=r.value;nx.disabled=false}});
 nx.onclick=function(){i++;render()};
 var b=root.querySelector('#ev-back'); if(b)b.onclick=function(){i--;render()};
}
render();
})();
