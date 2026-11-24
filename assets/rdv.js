/* Prise de rendez-vous (ATL Canada) : envoi par FormSubmit, comme le formulaire de contact. */
(function(){
var root=document.getElementById('rdv-app'); if(!root) return;
var AR=root.getAttribute('data-lang')==='ar', EN=root.getAttribute('data-lang')==='en';
var SE={
 fn:'First name',ln:'Last name',ph:'Phone or WhatsApp (with country code)',em:'Email (optional)',co:'Country of residence',
 co_o:['Morocco','Canada','Another country'],top:'Consultation topic',
 top_o:['General review of my situation','Studying in Canada','Working in Canada','Permanent residence (Express Entry, provinces)','Immigrating to Quebec','Family sponsorship','Visit or super visa','Citizenship','Other'],
 mode:'Consultation format',mode_o:['Phone call','WhatsApp','Video call (Teams)','Montréal office','Casablanca office'],
 day:'Preferred day',slot:'Preferred time slot (Montréal time)',slot_h:'Choose the day first',
 msg:'Anything useful for us to know (optional)',cons:'I have read the <a href="/confidentialite/" target="_blank">privacy policy</a> (in French) and agree that my information is used to answer my request.',
 send:'Send my appointment request',sending:'Sending…',ok:'Thank you! We have your request and will contact you shortly to confirm the time.',
 ko:'Unable to send right now. Email us at contact@atlcanada.com or call +1 514 295 6635.',
 sun:'The office is closed on Sunday. Please choose another day.',auto:'Thank you for your request. We have received your appointment request with ATL Canada and will contact you soon to confirm the time. This is not yet a confirmed appointment. For urgent matters: +1 514 295 6635 (call or WhatsApp).',note:'This request is not a confirmed appointment: we will contact you to set the time.',subj:'New appointment request (English) from atlcanada.com'
};
var S=EN?SE:AR?{
 fn:'الاسم الشخصي',ln:'الاسم العائلي',ph:'رقم الهاتف أو واتساب (مع رمز البلد)',em:'البريد الإلكتروني (اختياري)',co:'بلد الإقامة',
 co_o:['المغرب','كندا','بلد آخر'],top:'موضوع الاستشارة',
 top_o:['تقييم عام لملفي','الدراسة في كندا','العمل في كندا','الإقامة الدائمة (الدخول السريع، المقاطعات)','الهجرة إلى كيبيك','كفالة فرد من العائلة','زيارة أو سوبر فيزا','الجنسية','موضوع آخر'],
 mode:'طريقة الاستشارة',mode_o:['مكالمة هاتفية','واتساب','فيديو (Teams)','في مكتب مونتريال','في مكتب الدار البيضاء'],
 day:'اليوم المفضل',slot:'الفترة المفضلة (بتوقيت مونتريال)',slot_h:'اختر اليوم أولًا',
 msg:'ما يهمنا أن نعرفه عن وضعك (اختياري)',cons:'قرأت <a href="/confidentialite/" target="_blank">سياسة الخصوصية</a> وأوافق على استخدام معلوماتي للرد على طلبي.',
 send:'أرسل طلب الموعد',sending:'جارٍ الإرسال…',ok:'شكرًا! وصلنا طلبك. سنتصل بك لتأكيد الموعد في أقرب وقت.',
 ko:'تعذّر الإرسال حاليًا. راسلنا على contact@atlcanada.com أو اتصل على +1 514 295 6635.',
 sun:'المكتب مغلق يوم الأحد. اختر يومًا آخر.',auto:'شكرًا لطلبكم. وصلنا طلب موعدكم مع ATL Canada، وسنتصل بكم قريبًا لتأكيد الوقت. هذا الطلب ليس موعدًا مؤكدًا بعد. للاستعجال: +1 514 295 6635 (اتصال أو واتساب).',note:'هذا الطلب ليس موعدًا مؤكدًا: نتصل بك لتأكيد الوقت.',subj:'طلب موعد جديد (النسخة العربية) من atlcanada.com'
}:{
 fn:'Prénom',ln:'Nom',ph:'Téléphone ou WhatsApp (avec l\'indicatif du pays)',em:'Courriel (facultatif)',co:'Pays de résidence',
 co_o:['Maroc','Canada','Autre pays'],top:'Sujet de la consultation',
 top_o:['Évaluation générale de mon dossier','Études au Canada','Travail au Canada','Résidence permanente (Entrée express, provinces)','Immigration au Québec','Parrainage familial','Visite ou super visa','Citoyenneté','Autre sujet'],
 mode:'Mode de consultation',mode_o:['Appel téléphonique','WhatsApp','Visioconférence (Teams)','Bureau de Montréal','Bureau de Casablanca'],
 day:'Jour souhaité',slot:'Plage horaire souhaitée (heure de Montréal)',slot_h:'Choisissez d\'abord le jour',
 msg:'Ce qu\'il est utile que nous sachions (facultatif)',cons:'J\'ai lu la <a href="/confidentialite/" target="_blank">politique de confidentialité</a> et j\'accepte que mes renseignements servent à répondre à ma demande.',
 send:'Envoyer ma demande de rendez-vous',sending:'Envoi en cours…',ok:'Merci ! Votre demande est bien reçue. Nous vous contacterons rapidement pour confirmer l\'heure.',
 ko:'Envoi impossible pour le moment. Écrivez-nous à contact@atlcanada.com ou appelez le +1 514 295 6635.',
 sun:'Le bureau est fermé le dimanche. Choisissez un autre jour.',auto:'Merci pour votre demande. Nous avons bien reçu votre demande de rendez-vous avec ATL Canada et nous vous contactons bientôt pour confirmer l\'heure. Ce n\'est pas encore un rendez-vous confirmé. Pour une urgence : +1 514 295 6635 (appel ou WhatsApp).',note:'Cette demande n\'est pas un rendez-vous confirmé : nous vous contactons pour fixer l\'heure.',subj:'Nouvelle demande de rendez-vous depuis atlcanada.com'
};
var WK=EN?['10:00 a.m. to 12:00 p.m.','12:00 p.m. to 3:00 p.m.','3:00 p.m. to 6:00 p.m.']:AR?['من 10:00 إلى 12:00','من 12:00 إلى 15:00','من 15:00 إلى 18:00']:['10 h à 12 h','12 h à 15 h','15 h à 18 h'];
var SA=EN?['10:00 a.m. to 12:30 p.m.']:AR?['من 10:00 إلى 12:30']:['10 h à 12 h 30'];
function opt(a){return a.map(function(x){return '<option>'+x+'</option>'}).join('')}
function iso(d){return d.getFullYear()+'-'+('0'+(d.getMonth()+1)).slice(-2)+'-'+('0'+d.getDate()).slice(-2)}
var t=new Date(); t.setDate(t.getDate()+1); var mx=new Date(); mx.setDate(mx.getDate()+60);
root.innerHTML='<form id="rdv-form" class="rdv-form" action="https://formsubmit.co/contact@atlcanada.com" method="POST">'
+'<input type="hidden" name="_subject" value="'+S.subj+'"><input type="hidden" name="_template" value="table"><input type="hidden" name="_autoresponse" value="'+S.auto+'"><input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off">'
+'<div class="rdv-row"><div><label for="r-fn">'+S.fn+'</label><input id="r-fn" name="prenom" required autocomplete="given-name"></div><div><label for="r-ln">'+S.ln+'</label><input id="r-ln" name="nom" required autocomplete="family-name"></div></div>'
+'<div class="rdv-row"><div><label for="r-ph">'+S.ph+'</label><input id="r-ph" name="telephone" type="tel" required autocomplete="tel" dir="ltr"></div><div><label for="r-em">'+S.em+'</label><input id="r-em" name="email" type="email" autocomplete="email" dir="ltr"></div></div>'
+'<div class="rdv-row"><div><label for="r-co">'+S.co+'</label><select id="r-co" name="pays">'+opt(S.co_o)+'</select></div><div><label for="r-tp">'+S.top+'</label><select id="r-tp" name="sujet">'+opt(S.top_o)+'</select></div></div>'
+'<div class="rdv-row"><div><label for="r-md">'+S.mode+'</label><select id="r-md" name="mode">'+opt(S.mode_o)+'</select></div><div><label for="r-dy">'+S.day+'</label><input id="r-dy" name="jour" type="date" required min="'+iso(t)+'" max="'+iso(mx)+'"></div></div>'
+'<div><label for="r-sl">'+S.slot+'</label><select id="r-sl" name="plage" required><option value="">'+S.slot_h+'</option></select></div>'
+'<div><label for="r-ms">'+S.msg+'</label><textarea id="r-ms" name="message" rows="4"></textarea></div>'
+'<label class="rdv-consent"><input type="checkbox" name="consentement" value="oui" required><span>'+S.cons+'</span></label>'
+'<button class="btn btn-solid" type="submit">'+S.send+'</button><p class="help">'+S.note+'</p><p id="rdv-status" role="status" aria-live="polite" class="rdv-status"></p></form>';
var f=root.querySelector('#rdv-form'),dy=f.querySelector('#r-dy'),sl=f.querySelector('#r-sl'),st=f.querySelector('#rdv-status'),bt=f.querySelector('button[type=submit]');
function say(m,ok){st.textContent=m;st.style.color=ok?'#2F6B3A':'#B5342A'}
dy.addEventListener('change',function(){
 var d=dy.value?new Date(dy.value+'T12:00:00'):null; dy.setCustomValidity('');
 if(!d){sl.innerHTML='<option value="">'+S.slot_h+'</option>';return}
 var w=d.getDay();
 if(w===0){dy.setCustomValidity(S.sun);dy.reportValidity();sl.innerHTML='<option value="">'+S.slot_h+'</option>';return}
 sl.innerHTML=(w===6?SA:WK).map(function(x){return '<option>'+x+'</option>'}).join('');
});
f.addEventListener('submit',function(e){
 if(!window.fetch||!window.FormData) return;
 e.preventDefault(); bt.disabled=true; say(S.sending,true);
 fetch('https://formsubmit.co/ajax/contact@atlcanada.com',{method:'POST',headers:{'Accept':'application/json'},body:new FormData(f)})
 .then(function(r){return r.json()}).then(function(d){
  if(d&&(d.success===true||d.success==='true')){f.reset();sl.innerHTML='<option value="">'+S.slot_h+'</option>';say(S.ok,true)}else throw 0;
 }).catch(function(){say(S.ko,false)}).then(function(){bt.disabled=false});
});
})();
