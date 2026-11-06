/* Calculateur de points Entrée express (SCG/CRS), barème IRCC en vigueur depuis le 3 novembre 2026.
   Estimation indicative : ne remplace ni l'outil officiel d'IRCC ni une évaluation par un consultant. */
(function () {
  var root = document.getElementById('crs-app');
  if (!root) return;
  var AR = (root.getAttribute('data-lang') || 'fr') === 'ar';

  var T = AR ? {
    sec1: 'المعلومات الشخصية', age: 'عمرك (بالسنوات)',
    spouse: 'هل سيرافقك زوجك/زوجتك (أو شريك حياتك) في الهجرة؟', yes: 'نعم', no: 'لا',
    secEdu: 'التعليم', edu: 'أعلى مستوى دراسي', canStudy: 'دراسة في كندا (بعد المرحلة الثانوية)',
    secLang: 'اللغة', first: 'لغتك الرسمية الأولى', second: 'لغتك الرسمية الثانية',
    fr: 'الفرنسية', en: 'الإنجليزية', level: 'مستوى CLB/NCLC (الكفاءات الأربع)', detail: 'تحديد المستوى لكل مهارة',
    lis: 'الاستماع', spk: 'التحدث', rea: 'القراءة', wri: 'الكتابة', none: 'بلا اختبار', lt4: 'أقل من 4', p10: '10 أو أكثر',
    secWork: 'العمل', canWork: 'خبرة عمل كندية مؤهلة (سنوات)', hw: 'خبرة كندية في مهن ذات أجر مرتفع (12 شهرًا فأكثر)',
    foreign: 'خبرة عمل أجنبية (سنوات)', offer: 'عرض عمل صالح في مهنة ذات أجر مرتفع', cert: 'شهادة تأهيل مهني كندية (المهن)',
    secExtra: 'نقاط إضافية', pnp: 'ترشيح من مقاطعة أو إقليم', sibling: 'أخ أو أخت في كندا (مواطن أو مقيم دائم، 18 سنة فأكثر)',
    secSp: 'الزوج/الزوجة', spEdu: 'تعليم الزوج/الزوجة', spLang: 'لغة الزوج/الزوجة (CLB)', spCan: 'خبرة الزوج/الزوجة في كندا (سنوات)',
    total: 'درجتك التقديرية', of: 'من 1 200', core: 'العوامل الأساسية', spouseL: 'الزوج/الزوجة', trans: 'قابلية نقل المهارات', add: 'نقاط إضافية',
    note: 'هذا تقدير إرشادي وفق جدول IRCC المعمول به منذ 3 نوفمبر 2026، ولا يضمن أي دعوة. تتغير الجولات والقواعد؛ تحقق من وضعك مع مستشار.',
    cta: 'تحقق من درجتي مع مستشار', ctaHref: '/#contact',
    tiers: ['بلا', 'أجر ≥ 1.3× المتوسط', 'أجر ≥ 1.5× المتوسط', 'أجر ≥ 2× المتوسط'],
    cert0: 'بلا', y: function (n) { return n === 5 ? '5 فأكثر' : String(n); },
    eduOpts: ['أقل من الثانوية', 'شهادة ثانوية', 'برنامج لسنة واحدة', 'برنامج لسنتين', 'بكالوريوس أو برنامج 3 سنوات فأكثر', 'شهادتان أو أكثر (إحداها 3 سنوات فأكثر)', 'ماجستير أو شهادة مهنية', 'دكتوراه'],
    studyOpts: ['لا', 'برنامج 1 إلى 2 سنة', 'برنامج 3 سنوات فأكثر'],
    foreignOpts: ['لا شيء', '1 إلى 2 سنة', '3 سنوات فأكثر'],
    capNote: 'حدّ أقصى 600 نقطة للعوامل الأساسية (بما فيها الزوج وقابلية النقل).'
  } : {
    sec1: 'Informations personnelles', age: 'Votre âge (années)',
    spouse: 'Votre conjoint(e) ou partenaire immigrera-t-il/elle avec vous ?', yes: 'Oui', no: 'Non',
    secEdu: 'Études', edu: "Votre plus haut niveau d'études", canStudy: 'Études postsecondaires au Canada',
    secLang: 'Langues', first: 'Votre première langue officielle', second: 'Votre seconde langue officielle',
    fr: 'Français', en: 'Anglais', level: 'Niveau CLB/NCLC (4 compétences)', detail: 'Préciser par compétence',
    lis: 'Compréhension orale', spk: 'Expression orale', rea: 'Compréhension écrite', wri: 'Expression écrite', none: 'Aucun test', lt4: 'Moins de 4', p10: '10 ou plus',
    secWork: 'Expérience de travail', canWork: 'Expérience de travail canadienne qualifiée (années)', hw: 'Expérience canadienne dans une profession à salaire élevé (12 mois ou plus)',
    foreign: "Expérience de travail à l'étranger (années)", offer: "Offre d'emploi valide dans une profession à salaire élevé", cert: 'Certificat de qualification canadien (métiers)',
    secExtra: 'Points additionnels', pnp: "Désignation d'une province ou d'un territoire", sibling: 'Frère ou sœur au Canada (citoyen ou résident permanent, 18 ans ou plus)',
    secSp: 'Conjoint(e) ou partenaire', spEdu: 'Études du conjoint', spLang: 'Langue du conjoint (CLB)', spCan: 'Expérience canadienne du conjoint (années)',
    total: 'Votre score estimé', of: 'sur 1 200', core: 'Facteurs de base', spouseL: 'Conjoint(e)', trans: 'Transférabilité des compétences', add: 'Points additionnels',
    note: "Estimation indicative selon la grille d'IRCC en vigueur depuis le 3 novembre 2026. Elle ne garantit aucune invitation. Les rondes et les règles évoluent : faites valider votre situation par un consultant.",
    cta: 'Faire valider mon score', ctaHref: '/#contact',
    tiers: ['Aucune', 'Salaire ≥ 1,3 × la médiane', 'Salaire ≥ 1,5 × la médiane', 'Salaire ≥ 2 × la médiane'],
    cert0: 'Non', y: function (n) { return n === 5 ? '5 ou plus' : String(n); },
    eduOpts: ['Moins que le secondaire', 'Diplôme du secondaire', "Programme d'un an", 'Programme de deux ans', "Baccalauréat ou programme de 3 ans ou plus", 'Deux diplômes ou plus (dont un de 3 ans ou plus)', 'Maîtrise ou diplôme professionnel', 'Doctorat'],
    studyOpts: ['Non', 'Programme de 1 à 2 ans', 'Programme de 3 ans ou plus'],
    foreignOpts: ['Aucune', '1 à 2 ans', '3 ans ou plus'],
    capNote: 'Plafond de 600 points pour la partie de base (conjoint et transférabilité inclus).'
  };

  /* ---------- Barèmes IRCC (indices : 0 = sans conjoint, 1 = avec conjoint) ---------- */
  var AGE = { 18: [99, 90], 19: [105, 95], 30: [105, 95], 31: [99, 90], 32: [94, 85], 33: [88, 80], 34: [83, 75], 35: [77, 70], 36: [72, 65], 37: [66, 60], 38: [61, 55], 39: [55, 50], 40: [50, 45], 41: [39, 35], 42: [28, 25], 43: [17, 15], 44: [6, 5] };
  function agePts(a, sp) {
    if (a <= 17 || a >= 45) return 0;
    if (a >= 20 && a <= 29) return sp ? 100 : 110;
    return AGE[a][sp ? 1 : 0];
  }
  var EDU = [[0, 0], [30, 28], [90, 84], [98, 91], [120, 112], [128, 119], [135, 126], [150, 140]]; /* [sans, avec] */
  var EDU_TR = [0, 0, 1, 1, 1, 2, 2, 2];                 /* classe de transférabilité */
  var SP_EDU = [0, 2, 6, 7, 8, 9, 10, 10];
  var L1 = { 0: [0, 0], 3: [0, 0], 4: [6, 6], 5: [6, 6], 6: [9, 8], 7: [17, 16], 8: [23, 22], 9: [31, 29], 10: [34, 32] };
  function l1(c, sp) { return L1[c][sp ? 1 : 0]; }
  function l2(c) { return c >= 9 ? 6 : c >= 7 ? 3 : c >= 5 ? 1 : 0; }
  function spL(c) { return c >= 9 ? 5 : c >= 7 ? 3 : c >= 5 ? 1 : 0; }
  var CAN = [[0, 0], [40, 35], [53, 46], [64, 56], [72, 63], [80, 70]];
  var SP_CAN = [0, 5, 7, 8, 9, 10];
  var HW = [0, 20, 40, 70], OFFER = [0, 50, 70, 100];

  /* ---------- Construction de l'interface ---------- */
  function el(tag, attrs, html) { var e = document.createElement(tag); for (var k in attrs || {}) e.setAttribute(k, attrs[k]); if (html != null) e.innerHTML = html; return e; }
  function opts(list, start) { return list.map(function (t, i) { return '<option value="' + (i + (start || 0)) + '">' + t + '</option>'; }).join(''); }
  function field(id, label, inner) { return '<div class="f"><label for="' + id + '">' + label + '</label>' + inner + '</div>'; }
  function sel(id, o, val) { return '<select id="' + id + '">' + o + '</select>'; }
  function yn(id) { return sel(id, '<option value="0">' + T.no + '</option><option value="1">' + T.yes + '</option>'); }
  function clbOpts(none) {
    var o = none ? '<option value="0">' + T.none + '</option>' : '';
    o += '<option value="3">' + T.lt4 + '</option>';
    for (var i = 4; i <= 9; i++) o += '<option value="' + i + '">' + i + '</option>';
    return o + '<option value="10">' + T.p10 + '</option>';
  }
  function langBlock(id, none, def) {
    var abil = [T.lis, T.spk, T.rea, T.wri].map(function (t, i) {
      return field(id + i, t, sel(id + i, clbOpts(none)));
    }).join('');
    return field(id, T.level, sel(id, clbOpts(none))) +
      '<details><summary>' + T.detail + '</summary><div class="row" style="margin-top:10px">' + abil + '</div></details>';
  }

  var form = el('div', { 'class': 'crs-form' });
  form.innerHTML =
    '<fieldset><legend>' + T.sec1 + '</legend><div class="row">' +
      field('age', T.age, '<input type="number" id="age" min="17" max="60" value="29" inputmode="numeric">') +
      field('sp', T.spouse, yn('sp')) +
    '</div></fieldset>' +
    '<fieldset><legend>' + T.secEdu + '</legend><div class="row">' +
      field('edu', T.edu, sel('edu', opts(T.eduOpts))) +
      field('study', T.canStudy, sel('study', opts(T.studyOpts))) +
    '</div></fieldset>' +
    '<fieldset><legend>' + T.secLang + '</legend><div class="row langs">' +
      '<div class="lblock">' +
        field('l1', T.first, sel('l1', '<option value="fr">' + T.fr + '</option><option value="en">' + T.en + '</option>')) +
        '<div class="gap">' + langBlock('c1', false) + '</div>' +
      '</div>' +
      '<div class="lblock">' +
        '<div class="f"><span class="lbl" id="l2lbl"></span></div>' +
        '<div class="gap">' + langBlock('c2', true) + '</div>' +
      '</div></div>' +
      '<p class="help" style="margin-top:12px">' + (AR ? 'يحتسب الدخول السريع نقاطًا إضافية للفرنسية (NCLC 7 فأكثر في الكفاءات الأربع).' : "Le français rapporte des points additionnels à partir du NCLC 7 dans les 4 compétences.") + '</p>' +
    '</fieldset>' +
    '<fieldset><legend>' + T.secWork + '</legend><div class="row">' +
      field('can', T.canWork, sel('can', [0, 1, 2, 3, 4, 5].map(function (n) { return '<option value="' + n + '">' + T.y(n) + '</option>'; }).join(''))) +
      field('hw', T.hw, sel('hw', opts(T.tiers))) +
      field('for', T.foreign, sel('for', opts(T.foreignOpts))) +
      field('offer', T.offer, sel('offer', opts(T.tiers))) +
      field('cert', T.cert, yn('cert')) +
    '</div><p class="help" style="margin-top:10px">' + (AR ? 'تُحتسب إما نقاط الخبرة الكندية أو نقاط عرض العمل، أيهما أعلى، وليس كلاهما.' : "On retient les points d'expérience canadienne ou ceux de l'offre d'emploi, selon le plus élevé, jamais les deux.") + '</p></fieldset>' +
    '<fieldset><legend>' + T.secExtra + '</legend><div class="row">' +
      field('pnp', T.pnp, yn('pnp')) +
      field('sib', T.sibling, yn('sib')) +
    '</div></fieldset>' +
    '<fieldset id="spbox" class="hide"><legend>' + T.secSp + '</legend><div class="row">' +
      field('spedu', T.spEdu, sel('spedu', opts(T.eduOpts))) +
      field('splang', T.spLang, sel('splang', clbOpts(true))) +
      field('spcan', T.spCan, sel('spcan', [0, 1, 2, 3, 4, 5].map(function (n) { return '<option value="' + n + '">' + T.y(n) + '</option>'; }).join(''))) +
    '</div></fieldset>';

  var side = el('aside', { 'class': 'crs-side', 'aria-live': 'polite' });
  side.innerHTML =
    '<h3>' + T.total + '</h3><div class="crs-total"><span id="o-total">0</span> <small>' + T.of + '</small></div>' +
    '<div class="crs-bar"><i id="o-bar"></i></div>' +
    '<ul class="crs-lines">' +
      '<li><span>' + T.core + '</span><b><em id="o-core">0</em><small id="m-core"> / 570</small></b></li>' +
      '<li><span>' + T.spouseL + '</span><b><em id="o-sp">0</em><small> / 40</small></b></li>' +
      '<li><span>' + T.trans + '</span><b><em id="o-tr">0</em><small> / 100</small></b></li>' +
      '<li><span>' + T.add + '</span><b><em id="o-ad">0</em><small> / 600</small></b></li>' +
    '</ul>' +
    '<p class="crs-note">' + T.note + '</p>' +
    '<a class="crs-cta" href="' + T.ctaHref + '">' + T.cta + '</a>';

  var mini = el('div', { 'class': 'crs-mini', 'aria-hidden': 'true' }, T.total + ' <b id="o-mini">0</b>');
  root.appendChild(form); root.appendChild(side); root.appendChild(mini);

  function $(id) { return document.getElementById(id); }
  function num(id) { return parseInt($(id).value, 10) || 0; }

  /* synchronisation liste globale -> 4 compétences */
  ['c1', 'c2'].forEach(function (id) {
    $(id).addEventListener('change', function () { for (var i = 0; i < 4; i++) $(id + i).value = $(id).value; });
    $(id).value = id === 'c1' ? '7' : '0';
    for (var i = 0; i < 4; i++) $(id + i).value = $(id).value;
  });
  function minOf(id) { var m = 99; for (var i = 0; i < 4; i++) m = Math.min(m, num(id + i)); return m; }
  function langPts(id, f) { var s = 0; for (var i = 0; i < 4; i++) s += f(num(id + i)); return s; }

  function updateLabels() {
    var fr = $('l1').value === 'fr';
    $('l2lbl').textContent = T.second + ' (' + (fr ? T.en : T.fr) + ')';
  }

  function calc() {
    var sp = num('sp') === 1;
    $('spbox').className = sp ? '' : 'hide';
    updateLabels();

    var age = agePts(num('age'), sp);
    var edu = EDU[num('edu')][sp ? 1 : 0];
    var first = langPts('c1', function (c) { return l1(c, sp); });
    var second = Math.min(langPts('c2', l2), sp ? 22 : 24);
    var langs = Math.min(first + second, sp ? 150 : 160);

    var can = num('can');
    var hw = can >= 1 ? HW[num('hw')] : 0;
    var canTotal = CAN[can][sp ? 1 : 0] + hw;
    var offer = OFFER[num('offer')];
    var lmi = Math.max(canTotal, offer);

    var coreBase = age + edu + langs + lmi;

    var spouse = 0;
    if (sp) {
      spouse = SP_EDU[num('spedu')] + Math.min(4 * spL(num('splang')), 20) + SP_CAN[num('spcan')];
    }

    /* transférabilité (limite 100 ; 50 par bloc) */
    var cls = EDU_TR[num('edu')], clb = minOf('c1');
    var eLang = clb >= 9 ? (cls === 2 ? 50 : cls === 1 ? 25 : 0) : clb >= 7 ? (cls === 2 ? 25 : cls === 1 ? 13 : 0) : 0;
    var eCan = can >= 2 ? (cls === 2 ? 50 : cls === 1 ? 25 : 0) : can === 1 ? (cls === 2 ? 25 : cls === 1 ? 13 : 0) : 0;
    var eduTr = Math.min(50, eLang + eCan);
    var fy = num('for'); /* 0 aucune, 1 = 1-2 ans, 2 = 3 ans ou plus */
    var fLang = clb >= 9 ? (fy === 2 ? 50 : fy === 1 ? 25 : 0) : clb >= 7 ? (fy === 2 ? 25 : fy === 1 ? 13 : 0) : 0;
    var fCan = can >= 2 ? (fy === 2 ? 50 : fy === 1 ? 25 : 0) : can === 1 ? (fy === 2 ? 25 : fy === 1 ? 13 : 0) : 0;
    var forTr = Math.min(50, fLang + fCan);
    var certTr = num('cert') === 1 ? (clb >= 7 ? 50 : clb >= 5 ? 25 : 0) : 0;
    var trans = Math.min(100, eduTr + forTr + certTr);

    var core = Math.min(600, coreBase + spouse + trans);
    var coreShown = Math.min(coreBase, core);
    var spShown = Math.min(spouse, Math.max(0, core - coreShown));
    var trShown = Math.max(0, core - coreShown - spShown);

    /* points additionnels (limite 600) */
    var frMin = $('l1').value === 'fr' ? minOf('c1') : minOf('c2');
    var enMin = $('l1').value === 'fr' ? minOf('c2') : minOf('c1');
    var frBonus = frMin >= 7 ? (enMin >= 5 ? 50 : 25) : 0;
    var add = Math.min(600, (num('pnp') === 1 ? 600 : 0) + [0, 15, 30][num('study')] + frBonus + (num('sib') === 1 ? 15 : 0));

    var total = Math.min(1200, core + add);
    $('o-total').textContent = total;
    $('o-mini').textContent = total;
    $('o-core').textContent = coreShown;
    $('o-sp').textContent = spShown;
    $('o-tr').textContent = trShown;
    $('o-ad').textContent = add;
    $('m-core').textContent = ' / ' + (sp ? 530 : 570);
    $('o-bar').style.width = (total / 1200 * 100).toFixed(1) + '%';
  }

  root.addEventListener('input', calc);
  root.addEventListener('change', calc);
  calc();
})();
