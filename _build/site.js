/* Nuhal Almarifa — shared site script */
(function () {
  'use strict';
  var DATA = /*DATA*/null;
  var ITEMS = DATA.items, TRACKS = DATA.tracks;
  var MONTHS = { 10: 'أكتوبر', 11: 'نوفمبر', 12: 'ديسمبر' };
  var DAYS = ['الأحد', 'الاثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة', 'السبت'];
  var REL = document.body.getAttribute('data-rel') || '';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
  var ic = function (n) { return '<i data-lucide="' + n + '"></i>'; };
  function icons() { try { if (window.lucide) window.lucide.createIcons({ attrs: { 'aria-hidden': 'true' } }); } catch (e) {} }

  ITEMS.forEach(function (it, k) { it.id = k; it.start = new Date(2026, it.m - 1, it.d1); it.end = new Date(2026, it.m - 1, it.d2, 23, 59); });
  var now = new Date();
  function status(it) { return now > it.end ? 'done' : (now >= it.start ? 'live' : 'open'); }
  var ST = { open: ['st-open', 'متاح للتسجيل'], live: ['st-live', 'قيد الانعقاد'], done: ['st-done', 'منعقد'] };
  function pill(it) { var s = ST[status(it)]; return '<span class="pill ' + s[0] + '">' + s[1] + '</span>'; }
  function dateTxt(it) { return it.d1 + '–' + it.d2 + ' ' + MONTHS[it.m] + ' 2026'; }
  function chip(tr) { var T = TRACKS[tr]; return '<span class="chip"><span class="leaf t-' + T.t + '">' + ic(T.i) + '</span>' + esc(T.s) + '</span>'; }
  var sorted = ITEMS.slice().sort(function (a, b) { return a.start - b.start || a.tr - b.tr; });
  var upcoming = sorted.filter(function (x) { return x.start > now; });

  /* ---- live status refresh on static cards ---- */
  $$('[data-st]').forEach(function (el) {
    var it = ITEMS[+el.getAttribute('data-st')]; var s = ST[status(it)];
    el.className = 'pill ' + s[0]; el.textContent = s[1];
    var card = el.closest('.pcard'); if (card) { card.setAttribute('data-status', status(it)); card.classList.toggle('done', status(it) === 'done'); }
  });

  /* ---- home: upcoming & tickets refreshed with today's date ---- */
  var up = $('#upcoming');
  if (up && upcoming.length) {
    up.innerHTML = upcoming.slice(0, 5).map(function (it) {
      return '<div class="lrow"><div class="dstamp"><b>' + it.d1 + '–' + it.d2 + '</b><span>' + MONTHS[it.m] + ' · ' + DAYS[it.start.getDay()] + '</span></div><h3>' + esc(it.t) + '</h3>' + chip(it.tr) +
        '<span class="city">' + ic('map-pin') + ' ' + esc(it.c) + '</span><div class="act"><button class="btn btn-line btn-sm" type="button" data-open="' + it.id + '">سجّل ' + ic('arrow-left') + '</button></div></div>';
    }).join('');
  }
  var next = upcoming[0];
  if (next) {
    var T = TRACKS[next.tr];
    var ht = $('#heroTicket');
    if (ht) ht.innerHTML = '<div class="row1"><span class="lab">' + ic('calendar-clock') + ' البرنامج القادم</span>' + pill(next) + '</div><b>' + esc(next.t) + '</b><div class="meta"><span>' + ic('calendar-days') + ' ' + dateTxt(next) + '</span><span>' + ic('map-pin') + ' ' + esc(next.c) + '</span></div><button class="btn btn-primary btn-sm" type="button" data-open="' + next.id + '" style="justify-self:start">التفاصيل والتسجيل ' + ic('arrow-left') + '</button>';
    var mt = $('#megaTicket');
    if (mt) mt.innerHTML = '<span class="lab">' + esc(T.s) + '</span><b>' + esc(next.t) + '</b><div class="meta"><span>' + ic('calendar-days') + ' ' + dateTxt(next) + '</span><span>' + ic('map-pin') + ' ' + esc(next.c) + '</span></div><a class="btn btn-line btn-sm" href="' + REL + 'programs/' + T.slug + '/#p-' + next.id + '" style="justify-self:start;color:#fff">التفاصيل ' + ic('arrow-left') + '</a>';
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
        var match = (F.tr < 0 || it.tr === F.tr) && (!F.city || it.c === F.city) && (!F.month || String(it.m) === F.month) && (!q || it.t.toLowerCase().indexOf(q) > -1);
        var isDone = status(it) === 'done';
        if (match && isDone && !F.past) hiddenPast++;
        var show = match && (F.past || !isDone);
        c.hidden = !show; if (show) shown++;
      });
      $('#resultCount').innerHTML = '<b>' + shown + '</b> برنامجاً مطابقاً' + (hiddenPast ? ' · ' + hiddenPast + ' برنامجاً منعقداً مخفي' : '');
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
  var header = $('#siteHeader'), megaTimer;
  var hover = window.matchMedia && window.matchMedia('(hover:hover)').matches;
  function closeMegas() { $$('.mega').forEach(function (m) { m.classList.remove('open'); }); $$('.has-mega').forEach(function (li) { li.classList.remove('open'); var b = $('.mt', li); if (b) b.setAttribute('aria-expanded', 'false'); }); }
  var openedAt = 0;
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

  /* ---- modal ---- */
  var modal = $('#modal'), current = null, lastFocus = null;
  function regForm() {
    return '<h4 style="font-size:17px;margin-bottom:14px">طلب التسجيل</h4><form class="form" id="rform" novalidate>' +
      '<label>الاسم الكامل <span class="req">*</span><input class="input" id="r-name" required autocomplete="name"></label>' +
      '<label>الجهة <span class="req">*</span><input class="input" id="r-org" required autocomplete="organization"></label>' +
      '<label>البريد الإلكتروني <span class="req">*</span><input class="input" id="r-email" type="email" required dir="ltr" autocomplete="email"></label>' +
      '<label>رقم الهاتف <span class="req">*</span><input class="input" id="r-phone" type="tel" required dir="ltr" placeholder="+971" autocomplete="tel"></label>' +
      '<label>المسمى الوظيفي<input class="input" id="r-role" autocomplete="organization-title"></label>' +
      '<label>عدد المشاركين<input class="input" id="r-count" type="number" min="1" value="1"></label>' +
      '<div class="full form-actions"><button class="btn btn-primary" type="submit">' + ic('send') + ' تجهيز طلب التسجيل</button><span class="form-note">نؤكد المقعد والرسوم بالبريد</span></div></form>';
  }
  function openModal(id) {
    if (!modal) return;
    var it = ITEMS[id], T = TRACKS[it.tr]; current = it; lastFocus = document.activeElement;
    $('#mChip').innerHTML = '<a class="chip" href="' + REL + 'programs/' + T.slug + '/" style="color:#cfe2e3"><span class="leaf t-' + T.t + '" style="background:rgba(255,255,255,.1);color:var(--gold)">' + ic(T.i) + '</span>' + esc(T.n) + '</a> &nbsp; ' + pill(it);
    $('#mTitle').textContent = it.t;
    $('#mFacts').innerHTML = [['التاريخ', dateTxt(it)], ['المدة', (it.d2 - it.d1 + 1) + ' أيام · ' + DAYS[it.start.getDay()] + ' – ' + DAYS[it.end.getDay()]], ['مكان الانعقاد', it.c], ['المسار', T.s]]
      .map(function (p) { return '<div><small>' + p[0] + '</small><b>' + esc(p[1]) + '</b></div>'; }).join('');
    var wrap = $('#regWrap');
    if (status(it) === 'done') {
      wrap.innerHTML = '<div class="done-box"><h4>' + ic('history') + ' انعقد هذا البرنامج</h4><p style="font-size:14.5px">يمكن تنفيذه مجدداً لجهتكم كبرنامج مخصص. أرسل لنا طلباً من صفحة التواصل.</p><a class="btn btn-primary btn-sm" href="' + REL + 'contact/" style="justify-self:start">اطلب تنفيذه لجهتك ' + ic('arrow-left') + '</a></div>';
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
      if (!v) msg = 'هذا الحقل مطلوب';
      else if (inp.type === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v)) msg = 'اكتب بريداً إلكترونياً صحيحاً، مثل name@company.ae';
      else if (inp.type === 'tel' && v.replace(/\D/g, '').length < 8) msg = 'اكتب رقم هاتف صحيحاً مع رمز الدولة';
      if (msg) { ok = false; first = first || inp; var s = document.createElement('span'); s.className = 'err'; s.textContent = msg; inp.after(s); inp.setAttribute('aria-invalid', 'true'); }
      else inp.removeAttribute('aria-invalid');
    });
    if (first) first.focus();
    return ok;
  }
  function doneBox(text, title) {
    return '<div class="done-box"><h4>' + ic('check-circle') + ' ' + title + '</h4><p style="font-size:14.5px">انسخ الطلب وأرسله إلى أحد العناوين التالية، وسنؤكد لك الاستلام خلال يوم عمل.</p><textarea readonly id="reqText">' + esc(text) +
      '</textarea><div class="form-actions"><button class="btn btn-primary btn-sm" type="button" data-copy-req>' + ic('copy') + ' نسخ الطلب</button><button class="btn btn-line btn-sm" type="button" data-edit>تعديل البيانات</button></div><div class="send-to">' +
      DATA.emails.map(function (m) { return '<span>' + ic('mail') + '<span class="ltr">' + m + '</span></span>'; }).join('') + '<span>' + ic('message-circle') + '<span class="ltr">' + DATA.phones[0] + '</span></span></div></div>';
  }
  function val(id) { var el = document.getElementById(id); return el ? el.value.trim() : ''; }
  function onReg(e) {
    e.preventDefault(); var f = e.target; if (!validate(f)) return;
    var vals = $$('input', f).map(function (i) { return i.value; });
    var text = 'طلب تسجيل في برنامج تدريبي\n\nالبرنامج: ' + current.t + '\nالمسار: ' + TRACKS[current.tr].n + '\nالتاريخ: ' + dateTxt(current) + '\nالمدينة: ' + current.c +
      '\n\nالاسم: ' + val('r-name') + '\nالجهة: ' + val('r-org') + '\nالمسمى الوظيفي: ' + (val('r-role') || '—') + '\nالبريد: ' + val('r-email') + '\nالهاتف: ' + val('r-phone') + '\nعدد المشاركين: ' + (val('r-count') || 1);
    var wrap = $('#regWrap'); wrap.innerHTML = doneBox(text, 'طلب التسجيل جاهز'); icons();
    $('[data-edit]', wrap).onclick = function () { wrap.innerHTML = regForm(); var nf = $('#rform'); $$('input', nf).forEach(function (i, k) { i.value = vals[k]; }); nf.addEventListener('submit', onReg); icons(); };
  }
  function onContact(e) {
    e.preventDefault(); var f = e.target; if (!validate(f)) return;
    var text = 'طلب برنامج تدريبي\n\nالاسم: ' + val('c-name') + '\nالجهة: ' + val('c-org') + '\nالبريد: ' + val('c-email') + '\nالهاتف: ' + val('c-phone') + '\nالمجال: ' + (val('c-track') || '—') + '\nعدد المشاركين: ' + (val('c-count') || '—') + '\n\nالتفاصيل:\n' + (val('c-msg') || '—');
    var box = $('#cformBox'), keep = box.innerHTML, vals = Array.prototype.map.call(f.elements, function (x) { return x.value; });
    box.innerHTML = '<h3>طلبك جاهز</h3>' + doneBox(text, 'تم تجهيز الطلب'); icons();
    $('[data-edit]', box).onclick = function () { box.innerHTML = keep; var nf = $('#cform'); Array.prototype.forEach.call(nf.elements, function (x, k) { if (vals[k] !== undefined) x.value = vals[k]; }); nf.addEventListener('submit', onContact); icons(); };
  }
  var cf = $('#cform'); if (cf) cf.addEventListener('submit', onContact);

  /* ---- copy / toast / delegated clicks ---- */
  var tt;
  function toast(m) { var t = $('#toast'); if (!t) return; t.innerHTML = ic('check') + ' ' + esc(m); icons(); t.classList.add('show'); clearTimeout(tt); tt = setTimeout(function () { t.classList.remove('show'); }, 1800); }
  function copy(text, el) {
    var fallback = function () { if (el) { el.focus(); el.select(); toast('حدّد النص واضغط نسخ'); } else toast(text); };
    try { navigator.clipboard.writeText(text).then(function () { toast('تم النسخ'); }, fallback); } catch (err) { fallback(); }
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
