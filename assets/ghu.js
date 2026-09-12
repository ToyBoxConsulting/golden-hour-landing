/* Golden Hour Unboxed — shared site behaviour
   2026-09-12 · multi-page restructure
   Contents: 1) legacy anchor redirects  2) mobile menu  3) vendor search      */
(function () {
  'use strict';

  /* ----------------------------------------------------------------------
     1 · LEGACY ANCHOR REDIRECTS
     Every scheduled post, sent email and printed QR from the 2026 campaign
     points at an anchor on the single-page site. Those sections now live on
     their own pages. This keeps every one of those links working.
     Runs on the home page only.
     -------------------------------------------------------------------- */
  var MOVED = {
    'shop-vendors':   '/vendors#shop-vendors',
    'vendors':        '/vendors#shop-vendors',
    'tabling':        '/vendors#tabling',
    'community-tables': '/vendors#tabling',
    'sponsors':       '/thanks#sponsors',
    'who-made-it':    '/thanks#who-made-it',
    'endorsements':   '/thanks#endorsements',
    'civic':          '/thanks#civic',
    'behind':         '/thanks#behind',
    'press-archive':  '/press#press-archive',
    'exec-welcome':   '/press#exec-welcome',
    'sponsor-2027':   '/sponsor',
    'storytellers':   '/#program'
  };

  function redirectHash() {
    var p = location.pathname;
    if (p !== '/' && p !== '/index.html' && p !== '/index') return;
    var h = location.hash.replace(/^#/, '');
    if (h && MOVED[h]) { location.replace(MOVED[h]); return true; }
  }
  if (redirectHash()) return;            // stop; we are leaving the page
  window.addEventListener('hashchange', redirectHash);

  /* In-page links that point at a moved section get rewritten in place, so
     they never flash the home page first. */
  document.addEventListener('DOMContentLoaded', function () {
    var links = document.querySelectorAll('a[href^="#"], a[href^="/#"]');
    for (var i = 0; i < links.length; i++) {
      var id = links[i].getAttribute('href').replace(/^\/?#/, '');
      if (MOVED[id]) links[i].setAttribute('href', MOVED[id]);
    }
  });

  /* ----------------------------------------------------------------------
     2 · MOBILE MENU
     -------------------------------------------------------------------- */
  document.addEventListener('DOMContentLoaded', function () {
    var btn = document.querySelector('.nav-toggle');
    var menu = document.getElementById('nav-links');
    if (!btn || !menu) return;
    btn.addEventListener('click', function () {
      var open = menu.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    menu.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') {
        menu.classList.remove('open');
        btn.setAttribute('aria-expanded', 'false');
      }
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && menu.classList.contains('open')) {
        menu.classList.remove('open');
        btn.setAttribute('aria-expanded', 'false');
        btn.focus();
      }
    });
  });

  /* ----------------------------------------------------------------------
     3 · VENDOR SEARCH  (/vendors)
     Filters both the Vendor Village grid and the community tables as you
     type. Matches business name, category and the card's own description,
     so "candle", "hair", "travel" and "Zara" all find something.
     -------------------------------------------------------------------- */
  document.addEventListener('DOMContentLoaded', function () {
    var input = document.getElementById('vendor-search');
    if (!input) return;
    var count = document.getElementById('vendor-search-count');
    var cards = [].slice.call(document.querySelectorAll('[data-vendor], [data-org]'));
    if (!cards.length) return;

    cards.forEach(function (c) {
      c.__hay = ((c.getAttribute('data-vendor') || '') + ' ' +
                 (c.getAttribute('data-tags') || '') + ' ' +
                 (c.textContent || '') + ' ' +
                 (c.getAttribute('title') || '')).toLowerCase().replace(/\s+/g, ' ');
    });

    var total = cards.length;

    /* "candles" finds candle, "arts" finds art, "beaut" finds beauty */
    function match(hay, t) {
      if (hay.indexOf(t) > -1) return true;
      if (t.length > 3 && t.slice(-2) === 'es' && hay.indexOf(t.slice(0, -2)) > -1) return true;
      if (t.length > 3 && t.slice(-1) === 's'  && hay.indexOf(t.slice(0, -1)) > -1) return true;
      return false;
    }

    function apply() {
      var q = input.value.trim().toLowerCase();
      if (!q) {
        cards.forEach(function (c) { c.classList.remove('vhide'); });
        showGroups();
        count.textContent = '';
        return;
      }
      var terms = q.split(/\s+/), shown = 0;
      cards.forEach(function (c) {
        var hit = terms.every(function (t) { return match(c.__hay, t); });
        c.classList.toggle('vhide', !hit);
        if (hit) shown++;
      });
      showGroups();
      count.textContent = shown === 0
        ? 'Try another word — candles, hair, art, travel, food.'
        : shown + ' of ' + total + ' shown';
    }

    /* hide a whole group heading when nothing inside it survives the filter */
    function showGroups() {
      [].slice.call(document.querySelectorAll('[data-vgroup]')).forEach(function (g) {
        var kids = g.querySelectorAll('[data-vendor], [data-org]');
        var any = [].slice.call(kids).some(function (k) { return !k.classList.contains('vhide'); });
        g.classList.toggle('vhide', kids.length > 0 && !any);
      });
    }

    var t;
    input.addEventListener('input', function () { clearTimeout(t); t = setTimeout(apply, 90); });
    input.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { input.value = ''; apply(); }
    });

    /* deep link: /vendors?q=candles */
    var pre = new URLSearchParams(location.search).get('q');
    if (pre) { input.value = pre; apply(); }
  });
})();
