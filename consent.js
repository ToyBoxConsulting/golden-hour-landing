/* ToyBox Consulting & Management — shared cookie consent
   One file, every page, every site. Nothing analytics-related loads until consent.
   Consent is stored in the toybox_consent cookie for 12 months.
   Reopen the chooser anywhere with: toyboxCookieSettings()
*/
(function () {
  'use strict';

  var GA4_ID     = 'G-GVTKETZGVC';
  var CLARITY_ID = 'wzu2tuzmct';
  var COOKIE     = 'toybox_consent';
  var MONTHS     = 12;

  function readChoice() {
    var m = document.cookie.match(new RegExp('(?:^|; )' + COOKIE + '=([^;]*)'));
    return m ? decodeURIComponent(m[1]) : null;
  }
  function writeChoice(v) {
    var d = new Date();
    d.setMonth(d.getMonth() + MONTHS);
    document.cookie = COOKIE + '=' + encodeURIComponent(v) +
      ';expires=' + d.toUTCString() + ';path=/;SameSite=Lax' +
      (location.protocol === 'https:' ? ';Secure' : '');
  }

  /* Consent Mode v2 — denied until the visitor says otherwise. */
  window.dataLayer = window.dataLayer || [];
  function gtag() { dataLayer.push(arguments); }
  window.gtag = window.gtag || gtag;
  gtag('consent', 'default', {
    ad_storage: 'denied',
    ad_user_data: 'denied',
    ad_personalization: 'denied',
    analytics_storage: 'denied',
    functionality_storage: 'granted',
    security_storage: 'granted'
  });

  var loaded = false;
  function loadAnalytics() {
    if (loaded) return;
    loaded = true;
    gtag('consent', 'update', { analytics_storage: 'granted' });

    var g = document.createElement('script');
    g.async = true;
    g.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA4_ID;
    document.head.appendChild(g);
    gtag('js', new Date());
    gtag('config', GA4_ID);

    (function (c, l, a, r, i, t, y) {
      c[a] = c[a] || function () { (c[a].q = c[a].q || []).push(arguments); };
      t = l.createElement(r); t.async = 1; t.src = 'https://www.clarity.ms/tag/' + i;
      y = l.getElementsByTagName(r)[0]; y.parentNode.insertBefore(t, y);
    })(window, document, 'clarity', 'script', CLARITY_ID);
  }

  function styles() {
    if (document.getElementById('tb-consent-css')) return;
    var s = document.createElement('style');
    s.id = 'tb-consent-css';
    s.textContent =
      '#tb-consent{position:fixed;left:16px;right:16px;bottom:16px;z-index:2147483000;' +
      'max-width:760px;margin:0 auto;background:#1F1023;color:#F4EDE3;' +
      'border:1px solid rgba(228,166,90,.42);border-radius:14px;padding:20px 22px;' +
      'box-shadow:0 18px 48px rgba(0,0,0,.5);font-family:"DM Sans",system-ui,-apple-system,sans-serif;' +
      'font-size:14.5px;line-height:1.62;}' +
      '#tb-consent h2{font-family:"Fraunces",Georgia,serif;font-weight:400;font-size:19px;' +
      'margin:0 0 8px;letter-spacing:-.01em;}' +
      '#tb-consent p{margin:0 0 16px;opacity:.88;}' +
      '#tb-consent a{color:#F0CB6A;}' +
      '#tb-consent .tb-row{display:flex;gap:10px;flex-wrap:wrap;align-items:center;}' +
      '#tb-consent button{font:inherit;font-weight:700;cursor:pointer;border-radius:99px;' +
      'padding:10px 20px;border:1px solid transparent;}' +
      '#tb-consent .tb-ok{background:#E4A65A;color:#2A1535;}' +
      '#tb-consent .tb-no{background:transparent;color:#F4EDE3;border-color:rgba(244,237,227,.32);}' +
      '#tb-consent .tb-ok:hover{background:#F0CB6A;}' +
      '#tb-consent .tb-no:hover{border-color:rgba(244,237,227,.6);}' +
      '@media(max-width:560px){#tb-consent{padding:18px;font-size:14px;}' +
      '#tb-consent button{flex:1 1 auto;}}';
    document.head.appendChild(s);
  }

  function dismiss() {
    var el = document.getElementById('tb-consent');
    if (el) el.remove();
  }

  function show() {
    if (document.getElementById('tb-consent')) return;
    styles();
    var box = document.createElement('div');
    box.id = 'tb-consent';
    box.setAttribute('role', 'dialog');
    box.setAttribute('aria-label', 'Cookie choices');
    box.innerHTML =
      '<h2>We measure how this site is used.</h2>' +
      '<p>With your okay we use Google Analytics and Microsoft Clarity to see which pages ' +
      'people read and where they get stuck. Clarity records anonymized session replays. ' +
      'Decline and neither one loads &mdash; the site works exactly the same. ' +
      '<a href="/cookies.html">Cookie Notice</a> &middot; <a href="/privacy.html">Privacy Policy</a></p>' +
      '<div class="tb-row">' +
      '<button class="tb-ok" type="button">Accept analytics</button>' +
      '<button class="tb-no" type="button">Decline</button>' +
      '</div>';
    document.body.appendChild(box);
    box.querySelector('.tb-ok').onclick = function () { writeChoice('granted'); loadAnalytics(); dismiss(); };
    box.querySelector('.tb-no').onclick = function () { writeChoice('denied'); dismiss(); };
  }

  window.toyboxCookieSettings = function () { dismiss(); show(); };
  window.tbReopenConsent = window.toyboxCookieSettings;  /* alias used by cookies.html */

  function start() {
    var c = readChoice();
    if (c === 'granted') { loadAnalytics(); return; }
    if (c === 'denied') { return; }
    show();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start);
  } else {
    start();
  }
})();
