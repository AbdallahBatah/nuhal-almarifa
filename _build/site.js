/* Nuhal Almarifa — shared site script (Arabic + English) */
(function () {
  'use strict';
  var DATA = /*DATA*/null;
  var EN = (document.documentElement.lang || '').slice(0, 2) === 'en';
  var ITEMS = DATA.items, TRACKS = DATA.tracks;
  var L = EN ? {
    months: { 10: 'October', 11: 'November', 12: 'December' }, monthsShort: { 10: 'Oct', 11: 'Nov', 12: 'Dec' },
    days: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
    st: { open: 'Open for registration', live: 'In progress', done: 'Completed' },
    next: 'Next program', details: 'Details', detailsReg: 'Details & registration', register: 'Register',
    matching: ' matching programs', hiddenPast: ' completed programs hidden',
    fDate: 'Dates', fDur: 'Duration', fDays: ' days', fCity: 'Location', fTrack: 'Track',
    doneTitle: 'This program has been held', doneText: 'It can be delivered again for your entity as a custom program. Send us a request from the contact page.', doneBtn: 'Request it for your entity',
    regTitle: 'Registration request', name: 'Full name', org: 'Organization', email: 'Email', phone: 'Phone', role: 'Job title', count: 'Participants',
    regBtn: 'Send registration request', regNote: 'We confirm your seat and fees by email',
    req: 'This field is required', badEmail: 'Enter a valid email, e.g. name@company.ae', badPhone: 'Enter a valid phone number with country code',
    sending: 'Sending…', sentTitle: 'Your request has been sent', sentText: 'Thank you. Our client relations team will contact you within one working day.',
    failTitle: 'We could not send the request automatically', failText: 'Copy your request and send it to one of the addresses below, and we will confirm receipt within one working day.',
    copyReq: 'Copy request', edit: 'Edit details', copied: 'Copied', selectCopy: 'Select the text and copy it',
    regSubject: 'Program registration request', contactSubject: 'Training request from the website',
    t: { prog: 'Program', track: 'Track', date: 'Dates', city: 'City', name: 'Name', org: 'Organization', role: 'Job title', email: 'Email', phone: 'Phone', count: 'Participants', area: 'Area', details: 'Details' }
  } : {
    months: { 10: 'أكتوبر', 11: 'نوفمبر', 12: 'ديسمبر' }, monthsShort: { 10: 'أكتوبر', 11: 'نوفمبر', 12: 'ديسمبر' },
    days: ['الأحد', 'الاثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة', 'السبت'],
    st: { open: 'متاح للتسجيل', live: 'قيد الانعقاد', done: 'منعقد' },
    next: 'البرنامج القادم', details: 'التفاصيل', detailsReg: 'التفاصيل والتسجيل', register: 'سجّل',
    matching: ' برنامجاً مطابقاً', hiddenPast: ' برنامجاً منعقداً مخفي',
    fDate: 'التاريخ', fDur: 'المدة', fDays: ' أيام', fCity: 'مكان الانعقاد', fTrack: 'المسار',
    doneTitle: 'انعقد هذا البرنامج', doneText: 'يمكن تنفيذه مجدداً لجهتكم كبرنامج مخصص. أرسل لنا طلباً من صفحة التواصل.', doneBtn: 'اطلب تنفيذه لجهتك',
    regTitle: 'طلب التسجيل', name: 'الاسم الكامل', org: 'الجهة', email: 'البريد الإلكتروني', phone: 'رقم الهاتف', role: 'المسمى الوظيفي', count: 'عدد المشاركين',
    regBtn: 'إرسال طلب التسجيل', regNote: 'نؤكد المقعد والرسوم بالبريد',
    req: 'هذا الحقل مطلوب', badEmail: 'اكتب بريداً إلكترونياً صحيحاً، مثل name@company.ae', badPhone: 'اكتب رقم هاتف صحيحاً مع رمز الدولة',
    sending: 'جارٍ الإرسال…', sentTitle: 'تم إرسال طلبك', sentText: 'شكراً لك. سيتواصل معك فريق علاقات العملاء خلال يوم عمل.',
    failTitle: 'تعذّر إرسال الطلب تلقائياً', failText: 'انسخ الطلب وأرسله إلى أحد العناوين التالية، وسنؤكد لك الاستلام خلال يوم عمل.',
    copyReq: 'نسخ الطلب', edit: 'تعديل البيانات', copied: 'تم النسخ', selectCopy: 'حدّد النص واضغط نسخ',
    regSubject: 'طلب تسجيل في برنامج تدريبي', contactSubject: 'طلب تدريبي من الموقع',
    t: { prog: 'البرنامج', track: 'المسار', date: 'التاريخ', city: 'المدينة', name: 'الاسم', org: 'الجهة', role: 'المسمى الوظيفي', email: 'البريد', phone: 'الهاتف', count: 'عدد المشاركين', area: 'المجال', details: 'التفاصيل' }
  };
  var ARROW = EN ? 'arrow-right' : 'arrow-left';
  var REL = document.body.getAttribute('data-rel') || '';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
  var ic = function (n) { return '<i data-lucide="' + n + '"></i>'; };
  function icons() { try { if (window.lucide) window.lucide.createIcons({ attrs: { 'aria-hidden': 'true' } }); } catch (e) {} }
  var title = function (it) { return EN ? it.te : it.t; };
  var city = function (it) { return EN ? (DATA.cityEn[it.c] || it.c) : it.c; };
  var tname = function (T) { return EN ? T.ne : T.n; };
  var tshort = function (T) { return EN ? T.se : T.s; };

  ITEMS.forEach(function (it, k) { it.id = k; it.start = new Date(2026, it.m - 1, it.d1); it.end = new Date(2026, it.m - 1, it.d2, 23, 59); });
  var now = new Date();
  function status(it) { return now > it.end ? 'done' : (now >= it.start ? 'live' : 'open'); }
  var CLS = { open: 'st-open', live: 'st-live', done: 'st-done' };
  function pill(it) { var s = status(it); return '<span class="pill ' + CLS[s] + '">' + L.st[s] + '</span>'; }
  function dateTxt(it) { return it.d1 + '–' + it.d2 + ' ' + L.months[it.m] + ' 2026'; }
  function chip(tr) { var T = TRACKS[tr]; return '<span class="chip"><span class="leaf t-' + T.t + '">' + ic(T.i) + '</span>' + esc(tshort(T)) + '</span>'; }
  var sorted = ITEMS.slice().sort(function (a, b) { return a.start - b.start || a.tr - b.tr; });
  var upcoming = sorted.filter(function (x) { return x.start > now; });

  /* ---- live status refresh on static cards ---- */
  $$('[data-st]').forEach(function (el) {
    var it = ITEMS[+el.getAttribute('data-st')]; var s = status(it);
    el.className = 'pill ' + CLS[s]; el.textContent = L.st[s];
    var card = el.closest('.pcard'); if (card) { card.setAttribute('data-status', s); card.classList.toggle('done', s === 'done'); }
  });

  /* ---- home: upcoming & tickets refreshed with today's date ---- */
  var up = $('#upcoming');
  if (up && upcoming.length) {
    up.innerHTML = upcoming.slice(0, 5).map(function (it) {
      return '<div class="lrow"><div class="dstamp"><b>' + it.d1 + '–' + it.d2 + '</b><span>' + L.monthsShort[it.m] + ' · ' + L.days[it.start.getDay()] + '</span></div><h3>' + esc(title(it)) + '</h3>' + chip(it.tr) +
        '<span class="city">' + ic('map-pin') + ' ' + esc(city(it)) + '</span><div class="act"><button class="btn btn-line btn-sm" type="button" data-open="' + it.id + '">' + L.register + ' ' + ic(ARROW) + '</button></div></div>';
    }).join('');
  }
  var next = upcoming[0];
  if (next) {
    var NT = TRACKS[next.tr];
    var ht = $('#heroTicket');
    if (ht) ht.innerHTML = '<div class="row1"><span class="lab">' + ic('calendar-clock') + ' ' + L.next + '</span>' + pill(next) + '</div><b>' + esc(title(next)) + '</b><div class="meta"><span>' + ic('calendar-days') + ' ' + dateTxt(next) + '</span><span>' + ic('map-pin') + ' ' + esc(city(next)) + '</span></div><button class="btn btn-primary btn-sm" type="button" data-open="' + next.id + '" style="justify-self:start">' + L.detailsReg + ' ' + ic(ARROW) + '</button>';
    var mt = $('#megaTicket');
    if (mt) mt.innerHTML = '<span class="lab">' + esc(tshort(NT)) + '</span><b>' + esc(title(next)) + '</b><div class="meta"><span>' + ic('calendar-days') + ' ' + dateTxt(next) + '</span><span>' + ic('map-pin') + ' ' + esc(city(next)) + '</span></div><a class="btn btn-line btn-sm" href="' + REL + 'programs/' + NT.slug + '/#p-' + next.id + '" style="justify-self:start;color:#fff">' + L.details + ' ' + ic(ARROW) + '</a>';
  }

  /* ---- programs hub: filters over static cards ---- */
  var grid = $('#pgrid');
  if (grid) {
    var F = { tr: -1, q: '', city: '', month: '', past: false };
    var cards = $$('.pcard', grid);
    var apply = function () {
      var q = F.q.trim().toLowerCase(), shown = 0, hiddenPast = 0;
      cards.forEach(function (c) {
        var it = ITEMS[+c.id.slice(2)];
        var hay = (it.t + ' ' + it.te).toLowerCase();
        var match = (F.tr < 0 || it.tr === F.tr) && (!F.city || it.c === F.city) && (!F.month || String(it.m) === F.month) && (!q || hay.indexOf(q) > -1);
        var isDone = status(it) === 'done';
        if (match && isDone && !F.past) hiddenPast++;
        var show = match && (F.past || !isDone);
        c.hidden = !show; if (show) shown++;
      });
      $('#resultCount').innerHTML = '<b>' + shown + '</b>' + L.matching + (hiddenPast ? ' · ' + hiddenPast + L.hiddenPast : '');
      $('#emptyState').hidden = shown > 0;
      $$('#trackChips .fchip').forEach(function (b) { b.setAttribute('aria-pressed', String(+b.getAttribute('data-tr') === F.tr)); });
    };
    $('#trackChips').addEventListener('click', function (e) { var b = e.target.closest('[data-tr]'); if (b) { F.tr = +b.getAttribute('data-tr'); apply(); } });
    $('#q').addEventListener('input', function (e) { F.q = e.target.value; apply(); });
    $('#fCity').addEventListener('change', function (e) { F.city = e.target.value; apply(); });
    $('#fMonth').addEventListener('change', function (e) { F.month = e.target.value; apply(); });
    $('#fPast').addEventListener('change', function (e) { F.past = e.target.checked; apply(); });
    $('#resetFilters').addEventListener('click', function () { F = { tr: -1, q: '', city: '', month: '', past: false }; $('#q').value = ''; $('#fCity').value = ''; $('#fMonth').value = ''; $('#fPast').checked = false; apply(); });
    apply();
  }

  /* ---- mega menu ---- */
  var header = $('#siteHeader'), megaTimer, openedAt = 0;
  var hover = window.matchMedia && window.matchMedia('(hover:hover)').matches;
  function closeMegas() { $$('.mega').forEach(function (m) { m.classList.remove('open'); }); $$('.has-mega').forEach(function (li) { li.classList.remove('open'); var b = $('.mt', li); if (b) b.setAttribute('aria-expanded', 'false'); }); }
  function openMega(id) { openedAt = Date.now(); $$('.mega').forEach(function (m) { m.classList.toggle('open', m.id === id); }); $$('.has-mega').forEach(function (li) { var on = li.getAttribute('data-mega') === id; li.classList.toggle('open', on); var b = $('.mt', li); if (b) b.setAttribute('aria-expanded', String(on)); }); }
  $$('.has-mega').forEach(function (li) {
    var id = li.getAttribute('data-mega');
    li.addEventListener('mouseenter', function () { if (hover) { clearTimeout(megaTimer); openMega(id); } });
    $('.mt', li).addEventListener('click', function (e) { e.stopPropagation(); if (li.classList.contains('open') && Date.now() - openedAt > 600) closeMegas(); else openMega(id); });
  });
  $$('.menu > li:not(.has-mega)').forEach(function (li) { li.addEventListener('mouseenter', closeMegas); });
  if (header) {
    header.addEventListener('mouseleave', function () { if (hover) megaTimer = setTimeout(closeMegas, 180); });
    header.addEventListener('mouseenter', function () { clearTimeout(megaTimer); });
  }
  document.addEventListener('click', function (e) { if (!e.target.closest('#siteHeader')) closeMegas(); });

  /* ---- drawer ---- */
  var drawer = $('#drawer'), burger = $('#burger');
  function closeDrawer() { if (!drawer) return; drawer.classList.remove('open'); drawer.setAttribute('aria-hidden', 'true'); if (burger) burger.setAttribute('aria-expanded', 'false'); }
  if (burger) burger.addEventListener('click', function () { drawer.classList.add('open'); drawer.setAttribute('aria-hidden', 'false'); burger.setAttribute('aria-expanded', 'true'); });
  $$('[data-close-drawer]').forEach(function (b) { b.addEventListener('click', closeDrawer); });
  $$('.dacc > button').forEach(function (b) { b.addEventListener('click', function () { var ex = b.getAttribute('aria-expanded') === 'true'; b.setAttribute('aria-expanded', String(!ex)); b.nextElementSibling.hidden = ex; }); });

  /* ---- sending (FormSubmit) ---- */
  function send(subject, fields) {
    var body = { _subject: subject, _cc: DATA.formCc, _template: 'table', _captcha: 'false' };
    Object.keys(fields).forEach(function (k) { body[k] = fields[k]; });
    return fetch('https://formsubmit.co/ajax/' + DATA.formTo, { method: 'POST', headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }, body: JSON.stringify(body) })
      .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { if (!r.ok || String(j.success) !== 'true') throw new Error('send failed'); return j; }); });
  }
  function asText(head, fields) { return head + '\n\n' + Object.keys(fields).map(function (k) { return k + ': ' + fields[k]; }).join('\n'); }
  function sentBox() { return '<div class="sent-box"><h4>' + ic('check-circle') + ' ' + L.sentTitle + '</h4><p style="font-size:15px">' + L.sentText + '</p></div>'; }
  function failBox(text) {
    return '<div class="done-box"><h4>' + ic('mail-warning') + ' ' + L.failTitle + '</h4><p style="font-size:14.5px">' + L.failText + '</p><textarea readonly id="reqText">' + esc(text) +
      '</textarea><div class="form-actions"><button class="btn btn-primary btn-sm" type="button" data-copy-req>' + ic('copy') + ' ' + L.copyReq + '</button><button class="btn btn-line btn-sm" type="button" data-edit>' + L.edit + '</button></div><div class="send-to">' +
      DATA.emails.map(function (m) { return '<span>' + ic('mail') + '<span class="ltr">' + m + '</span></span>'; }).join('') + '<span>' + ic('message-circle') + '<span class="ltr">' + DATA.phones[0] + '</span></span></div></div>';
  }
  function submitFlow(form, box, subject, head, fields, restore) {
    var hp = $('.hp', form); if (hp && hp.value) return;
    var btn = $('button[type="submit"]', form); var label = btn.innerHTML;
    btn.innerHTML = L.sending; form.classList.add('sending');
    send(subject, fields).then(function () { box.innerHTML = sentBox(); icons(); })
      .catch(function () { btn.innerHTML = label; form.classList.remove('sending'); box.innerHTML = failBox(asText(head, fields)); icons(); var ed = $('[data-edit]', box); if (ed) ed.onclick = restore; });
  }

  /* ---- modal ---- */
  var modal = $('#modal'), current = null, lastFocus = null;
  function regForm() {
    return '<h4 style="font-size:17px;margin-bottom:14px">' + L.regTitle + '</h4><form class="form" id="rform" novalidate>' +
      '<label>' + L.name + ' <span class="req">*</span><input class="input" id="r-name" required autocomplete="name"></label>' +
      '<label>' + L.org + ' <span class="req">*</span><input class="input" id="r-org" required autocomplete="organization"></label>' +
      '<label>' + L.email + ' <span class="req">*</span><input class="input" id="r-email" type="email" required dir="ltr" autocomplete="email"></label>' +
      '<label>' + L.phone + ' <span class="req">*</span><input class="input" id="r-phone" type="tel" required dir="ltr" placeholder="+971" autocomplete="tel"></label>' +
      '<label>' + L.role + '<input class="input" id="r-role" autocomplete="organization-title"></label>' +
      '<label>' + L.count + '<input class="input" id="r-count" type="number" min="1" value="1"></label>' +
      '<input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">' +
      '<div class="full form-actions"><button class="btn btn-primary" type="submit">' + ic('send') + ' ' + L.regBtn + '</button><span class="form-note">' + L.regNote + '</span></div></form>';
  }
  function openModal(id) {
    if (!modal) return;
    var it = ITEMS[id], T = TRACKS[it.tr]; current = it; lastFocus = document.activeElement;
    $('#mChip').innerHTML = '<a class="chip" href="' + REL + 'programs/' + T.slug + '/" style="color:#cfe2e3"><span class="leaf t-' + T.t + '" style="background:rgba(255,255,255,.1);color:var(--gold)">' + ic(T.i) + '</span>' + esc(tname(T)) + '</a> &nbsp; ' + pill(it);
    $('#mTitle').textContent = title(it);
    $('#mFacts').innerHTML = [[L.fDate, dateTxt(it)], [L.fDur, (it.d2 - it.d1 + 1) + L.fDays + ' · ' + L.days[it.start.getDay()] + ' – ' + L.days[it.end.getDay()]], [L.fCity, city(it)], [L.fTrack, tshort(T)]]
      .map(function (p) { return '<div><small>' + p[0] + '</small><b>' + esc(p[1]) + '</b></div>'; }).join('');
    var wrap = $('#regWrap');
    if (status(it) === 'done') {
      wrap.innerHTML = '<div class="done-box"><h4>' + ic('history') + ' ' + L.doneTitle + '</h4><p style="font-size:14.5px">' + L.doneText + '</p><a class="btn btn-primary btn-sm" href="' + REL + 'contact/" style="justify-self:start">' + L.doneBtn + ' ' + ic(ARROW) + '</a></div>';
    } else { wrap.innerHTML = regForm(); $('#rform').addEventListener('submit', onReg); }
    modal.hidden = false; document.body.style.overflow = 'hidden'; icons();
    setTimeout(function () { $('#modal .x').focus(); }, 30);
  }
  function closeModal() { if (!modal || modal.hidden) return; modal.hidden = true; document.body.style.overflow = ''; if (lastFocus && lastFocus.focus) lastFocus.focus({ preventScroll: true }); }
  if (modal) modal.addEventListener('click', function (e) { if (e.target.closest('[data-close-modal]')) closeModal(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') { closeMegas(); closeDrawer(); closeModal(); } });

  /* ---- forms ---- */
  function validate(form) {
    $$('.err', form).forEach(function (x) { x.remove(); });
    var ok = true, first = null;
    $$('[required]', form).forEach(function (inp) {
      var v = inp.value.trim(), msg = '';
      if (!v) msg = L.req;
      else if (inp.type === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v)) msg = L.badEmail;
      else if (inp.type === 'tel' && v.replace(/\D/g, '').length < 8) msg = L.badPhone;
      if (msg) { ok = false; first = first || inp; var s = document.createElement('span'); s.className = 'err'; s.textContent = msg; inp.after(s); inp.setAttribute('aria-invalid', 'true'); }
      else inp.removeAttribute('aria-invalid');
    });
    if (first) first.focus();
    return ok;
  }
  function val(id) { var el = document.getElementById(id); return el ? el.value.trim() : ''; }
  function onReg(e) {
    e.preventDefault(); var f = e.target; if (!validate(f)) return;
    var vals = $$('input', f).map(function (i) { return i.value; });
    var t = L.t, fields = {};
    fields[t.prog] = title(current); fields[t.track] = tname(TRACKS[current.tr]); fields[t.date] = dateTxt(current); fields[t.city] = city(current);
    fields[t.name] = val('r-name'); fields[t.org] = val('r-org'); fields[t.role] = val('r-role') || '—'; fields[t.email] = val('r-email'); fields[t.phone] = val('r-phone'); fields[t.count] = val('r-count') || '1';
    var wrap = $('#regWrap');
    submitFlow(f, wrap, L.regSubject + ': ' + title(current), L.regSubject, fields, function () {
      wrap.innerHTML = regForm(); var nf = $('#rform'); $$('input', nf).forEach(function (i, k) { i.value = vals[k] || ''; }); nf.addEventListener('submit', onReg); icons();
    });
  }
  function onContact(e) {
    e.preventDefault(); var f = e.target; if (!validate(f)) return;
    var t = L.t, fields = {};
    fields[t.name] = val('c-name'); fields[t.org] = val('c-org'); fields[t.email] = val('c-email'); fields[t.phone] = val('c-phone');
    fields[t.area] = val('c-track') || '—'; fields[t.count] = val('c-count') || '—'; fields[t.details] = val('c-msg') || '—';
    var box = $('#cformBox'), keep = box.innerHTML, vals = Array.prototype.map.call(f.elements, function (x) { return x.value; });
    submitFlow(f, box, L.contactSubject + ': ' + val('c-org'), L.contactSubject, fields, function () {
      box.innerHTML = keep; var nf = $('#cform'); Array.prototype.forEach.call(nf.elements, function (x, k) { if (vals[k] !== undefined) x.value = vals[k]; }); nf.classList.remove('sending'); nf.addEventListener('submit', onContact); icons();
    });
  }
  var cf = $('#cform'); if (cf) cf.addEventListener('submit', onContact);

  /* ---- copy / toast / delegated clicks ---- */
  var tt;
  function toast(m) { var t = $('#toast'); if (!t) return; t.innerHTML = ic('check') + ' ' + esc(m); icons(); t.classList.add('show'); clearTimeout(tt); tt = setTimeout(function () { t.classList.remove('show'); }, 1800); }
  function copy(text, el) {
    var fallback = function () { if (el) { el.focus(); el.select(); toast(L.selectCopy); } else toast(text); };
    try { navigator.clipboard.writeText(text).then(function () { toast(L.copied); }, fallback); } catch (err) { fallback(); }
  }
  document.addEventListener('click', function (e) {
    var o = e.target.closest('[data-open]'); if (o) { openModal(+o.getAttribute('data-open')); return; }
    var c = e.target.closest('[data-copy]'); if (c) { copy(c.getAttribute('data-copy')); return; }
    if (e.target.closest('[data-copy-req]')) { var ta = $('#reqText'); copy(ta.value, ta); }
  });

  /* ---- deep link to a program card ---- */
  if (/^#p-\d+$/.test(location.hash)) { var card = $(location.hash); if (card) { card.style.outline = '2px solid var(--gold)'; card.style.outlineOffset = '4px'; } }

  icons();
  if (!window.lucide) window.addEventListener('load', icons);
})();
