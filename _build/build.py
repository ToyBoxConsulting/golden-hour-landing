#!/usr/bin/env python3
"""
Golden Hour Unboxed — static page builder.

The 2026 site was one 2.2 MB HTML file, thirty-four screens tall, with every
image pasted in as base64. This splits the same content across four pages that
share one stylesheet, one script and one nav.

    python3 _build/build.py

Writes: index.html, vendors.html, thanks.html, press.html
Sections live in _build/parts/ — edit those, then re-run.
"""
import os, re, sys, datetime

ROOT  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARTS = os.path.join(ROOT, "_build", "parts")

def part(name):
    with open(os.path.join(PARTS, name + ".html"), encoding="utf-8") as f:
        return f.read().rstrip() + "\n"

CREST = open(os.path.join(PARTS, "_crest.svg"), encoding="utf-8").read().strip()
SUBSTACK = "https://katoyapalmer.substack.com"
NEWSLETTER = ("https://ee4a3130.sibforms.com/serve/MUIFABUzAxbPDJ64KutIUCwq_ZSi9BDEAmJGsGju"
              "ZE_tSJZcJPBmOdNtK80YZTRWZPPk8vhT3qJwY7bOy25aQWk-KmeNSbHSI_XdNg5z9xepGSjKRC7w"
              "BM6RUcpw69BXwLrfbko1xXaVh3lCcRCKiVNxpFE6xcl8LD-Cyr53TiQC-hn38agb2vYTCkF0pble"
              "uc3TkL4cMyUgmEkj9A==")

NAV_ITEMS = [
    ("/#numbers", "The Night",  "home"),
    ("/#gallery", "Gallery",    "home"),
    ("/thanks",   "Thank You",  "thanks"),
    ("/press",    "Press",      "press"),
    ("/updates",  "Updates",    "updates"),
]

# ---------------------------------------------------------------- fragments

def nav(active):
    links = "\n".join(
        '      <a href="%s"%s>%s</a>' % (href, ' aria-current="page"' if key == active else "", label)
        for href, label, key in NAV_ITEMS)
    cta_current = ' aria-current="page"' if active == "vendors" else ""
    return f"""<a class="skip-link" href="#main">Skip to content</a>

<div class="site-header">
<nav class="nav" aria-label="Primary">
  <div class="nav-inner">
    <a href="/" class="nav-brand" aria-label="Golden Hour Unboxed — home">
      <span class="logo-img logo-nav" aria-hidden="true">{CREST}</span>
      <span class="gold-foil">Golden&nbsp;Hour</span> <em style="font-style:italic;font-weight:300;opacity:0.7;margin-left:6px;">Unboxed</em>
    </a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="nav-links">
      <span class="bars" aria-hidden="true"><span></span></span> Menu
    </button>
    <div class="nav-links" id="nav-links">
      <a href="/vendors" class="menu-cta"{cta_current}>Shop Vendors</a>
{links}
    </div>
    <a href="/vendors" class="nav-cta"{cta_current}>Shop Vendors</a>
  </div>
</nav>

<div class="sponsor-strip">
  <a href="/thanks#sponsors">
    <img src="/assets/symetra.png" alt="Symetra" width="76" height="20">
    <b>Title sponsor</b><span>Symetra</span>
  </a>
</div>
</div>
"""

FOOTER = f"""<footer>
  <div class="footer-inner">
    <div>
      <span class="logo-img logo-footer" aria-hidden="true">{CREST}</span>
      <div class="footer-brand"><span class="gold-foil">Golden Hour</span> <em style="font-style:italic;font-weight:300;opacity:0.7;">Unboxed</em></div>
      <p class="footer-tag">A free, cross-cultural celebration of Black entrepreneurship on the Eastside, held August&nbsp;23,&nbsp;2026 during National Black Business Month. Year two is in motion. Presented by ToyBox Consulting &amp; Management as part of the City of Bellevue's <a href="https://bellevuewa.gov/city-government/departments/human-resources/diversity-advantage-initiative/cross-cultural-center-without-walls" target="_blank" rel="noopener" style="color: inherit; border-bottom: 1px dotted currentColor;">Cross-Cultural Center without Walls</a>.</p>
    </div>
    <div>
      <h4>The 2026 record</h4>
      <ul>
        <li><a href="/#numbers">The night</a></li>
        <li><a href="/#program">The evening, as it ran</a></li>
        <li><a href="/#gallery">Gallery</a></li>
        <li><a href="/vendors">Shop the vendors</a></li>
        <li><a href="/thanks">Thank you</a></li>
        <li><a href="/press">Press &amp; the public record</a></li>
        <li><a href="/updates">Updates</a></li>
      </ul>
    </div>
    <div>
      <h4>Read &amp; subscribe</h4>
      <ul>
        <li><a href="{SUBSTACK}" target="_blank" rel="noopener">Katoya's Substack</a></li>
        <li><a href="{NEWSLETTER}" target="_blank" rel="noopener">Golden Hour newsletter</a></li>
        <li><a href="/give">Give to Golden Hour</a></li>
        <li style="margin-top:14px"><a href="mailto:katoya@toyboxconsulting.net">katoya@toyboxconsulting.net</a></li>
        <li><a href="https://www.toyboxconsulting.net" target="_blank" rel="noopener">toyboxconsulting.net</a></li>
        <li style="margin-top: 14px; font-size: 12px; letter-spacing: 0.14em; text-transform: uppercase; color: var(--gold-1); opacity: 0.8;">Press &amp; media</li>
        <li><a href="mailto:katoya@toyboxconsulting.net?subject=Media%20Inquiry%20-%20Golden%20Hour">katoya@toyboxconsulting.net</a></li>
      </ul>
    </div>
    <div>
      <h4>Follow</h4>
      <ul>
        <li><a href="https://instagram.com/toyboxconsulting" target="_blank" rel="noopener">Instagram</a></li>
        <li><a href="https://www.linkedin.com/company/toyboxconsulting" target="_blank" rel="noopener">LinkedIn</a></li>
        <li><a href="https://tiktok.com/@toyboxconsulting" target="_blank" rel="noopener">TikTok</a></li>
        <li><a href="https://facebook.com/toyboxcm" target="_blank" rel="noopener">Facebook</a></li>
      </ul>
    </div>
  </div>
  <div class="footer-presented">
    <span class="footer-presented-label">Presented by</span>
    <a href="https://www.toyboxconsulting.net" target="_blank" rel="noopener" class="footer-toybox-link" aria-label="ToyBox Consulting &amp; Management">
      <img src="/assets/toybox-wordmark.png" alt="ToyBox Consulting &amp; Management" width="200" height="72" loading="lazy">
    </a>
  </div>
  <div class="footer-legal">
    <a href="/privacy">Privacy</a> · <a href="/terms">Terms</a> · <a href="/cookies">Cookie notice</a>
    <span style="opacity:.5">&nbsp;·&nbsp; &copy; {datetime.date.today().year} ToyBox Consulting &amp; Management</span>
  </div>
</footer>
"""

def head(title, desc, canonical, extra=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="theme-color" content="#1F3A57">
<meta name="msapplication-TileColor" content="#1F3A57">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://goldenhourunboxed.com{canonical}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="https://goldenhourunboxed.com{canonical}">
<meta property="og:image" content="https://goldenhourunboxed.com/og-image.png">
<meta property="og:site_name" content="Golden Hour Unboxed">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@toyboxconsulting">
<meta name="twitter:creator" content="@katoyapalmer">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,300;9..144,400;9..144,500;9..144,600;9..144,700&family=DM+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css">
<script src="/assets/ghu.js" defer></script>
<script src="/consent.js"></script>
{extra}</head>
<body>
"""

def intro(eyebrow, h1, lede):
    return f"""<div class="page-intro" id="main">
  <span class="eyebrow">{eyebrow}</span>
  <h1>{h1}</h1>
  <p>{lede}</p>
</div>
"""

def write(name, html):
    with open(os.path.join(ROOT, name), "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  {name:16} {len(html.encode()):>9,} bytes")

# ---------------------------------------------------------------- the pages

def build_home():
    routes = """
<section class="band" id="more">
  <div class="band-inner">
    <span class="eyebrow" style="justify-content:center;">Keep going</span>
    <h2 class="section-title" style="text-align:center;">Three doors out of this <em>page.</em></h2>
    <div class="routes" style="margin-top:34px;">
      <a class="route" href="/vendors">
        <h3>Shop the vendors</h3>
        <p>Every Black-owned business and artist who tabled in the garden, still linked, still open. Search by what you are looking for.</p>
        <span class="arrow">Shop Black-owned &rarr;</span>
      </a>
      <a class="route" href="/thanks">
        <h3>Thank you</h3>
        <p>The sponsors, partners, volunteers and civic champions who made a free evening free &mdash; and what people said afterward, unprompted.</p>
        <span class="arrow">See who made it &rarr;</span>
      </a>
      <a class="route" href="/press">
        <h3>The public record</h3>
        <p>Two proclamations, the press coverage, and the documents behind the night.</p>
        <span class="arrow">Read the record &rarr;</span>
      </a>
    </div>
  </div>
</section>
"""
    substack = f"""
<section class="band" style="text-align:center">
  <div class="band-inner">
    <span class="drive-badge">Behind the evening</span>
    <h3>How a free event actually gets funded.</h3>
    <p style="max-width:600px;margin:0 auto 6px">Katoya writes about the work underneath &mdash; the budget, the licensing, the asks that landed and the ones that did not &mdash; on Substack.</p>
    <p style="max-width:600px;margin:0 auto 26px;font-size:15px;opacity:.8">Plus what year two looks like, as it is being built.</p>
    <a href="{SUBSTACK}" target="_blank" rel="noopener" class="btn btn-gold">Read on Substack <span class="arrow">&rarr;</span></a>
  </div>
</section>
"""
    body = "".join([
        nav("home"),
        '<main id="main">\n',
        part("_hero"), part("about"), part("numbers"), part("why-this-event"),
        part("program"), part("gallery"),
        routes, substack, part("drive"), part("follow"),
        part("built-by"), part("final-cta"),
        "</main>\n",
    ])
    return head(
        "Golden Hour Unboxed 2026 — The Record · Bellevue Botanical Garden",
        "The record of Golden Hour Unboxed 2026: a free evening of Black entrepreneurship at "
        "Bellevue Botanical Garden, held during National Black Business Month. The night, the "
        "program, the pictures.",
        "/", extra=FAQ_LD) + body + FOOTER + "</body>\n</html>\n"

def build_vendors():
    search = """
<div class="vsearch">
  <label for="vendor-search" class="visually-hidden" style="position:absolute;left:-9999px">Search vendors</label>
  <input type="search" id="vendor-search" placeholder="Search &mdash; candles, hair, travel, art&hellip;" autocomplete="off">
  <svg viewBox="0 0 24 24" fill="none" stroke-width="2" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
</div>
<div class="vsearch-count" id="vendor-search-count" role="status" aria-live="polite"></div>
"""
    body = "".join([
        nav("vendors"),
        intro("Vendor Village",
              "Shop <em>Black-owned.</em>",
              "The businesses and artists who tabled in the garden on August 23 &mdash; and the ones "
              "who could not make this one. All of them are still open. All of them still want your order."),
        search,
        '<main>\n', part("tabling"), '</main>\n',
    ])
    return head(
        "Shop the vendors — Golden Hour Unboxed",
        "Every Black-owned business and community organization that tabled at Golden Hour Unboxed "
        "2026 in Bellevue. Search by what you are looking for and shop them directly.",
        "/vendors") + body + FOOTER + "</body>\n</html>\n"

def build_thanks():
    body = "".join([
        nav("thanks"),
        intro("Thank you",
              "Paid for, staffed, and <em>vouched for.</em>",
              "A free evening reaches people because someone covered it, someone ran it, and "
              "someone put their name on it. This page is the receipt."),
        '<main>\n',
        part("words"), part("sponsors"), part("behind"), part("who-made-it"),
        part("civic"), part("endorsements"),
        '</main>\n',
    ])
    return head(
        "Thank you — Golden Hour Unboxed",
        "The sponsors, partners, volunteers, civic champions and endorsing organizations behind "
        "Golden Hour Unboxed 2026, and what attendees said afterward in their own words.",
        "/thanks") + body + FOOTER + "</body>\n</html>\n"

def build_press():
    body = "".join([
        nav("press"),
        intro("The public record",
              "On the record, <em>in public.</em>",
              "Two proclamations, the press coverage, and the documents behind the night. "
              "Everything here is public and quotable. Media inquiries: "
              "<a href=\"mailto:katoya@toyboxconsulting.net?subject=Media%20Inquiry%20-%20Golden%20Hour\">"
              "katoya@toyboxconsulting.net</a>."),
        '<main>\n', part("press-archive"), '</main>\n',
    ])
    return head(
        "Press & the public record — Golden Hour Unboxed",
        "Proclamations from King County and the City of Bellevue, press coverage, and the public "
        "documents behind Golden Hour Unboxed 2026.",
        "/press") + body + FOOTER + "</body>\n</html>\n"

FAQ_LD = """<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Event","name":"Golden Hour Unboxed 2026",
"startDate":"2026-08-23T17:00-07:00","endDate":"2026-08-23T20:00-07:00",
"eventStatus":"https://schema.org/EventScheduled",
"eventAttendanceMode":"https://schema.org/OfflineEventAttendanceMode",
"location":{"@type":"Place","name":"Bellevue Botanical Garden",
 "address":{"@type":"PostalAddress","streetAddress":"12001 Main St","addressLocality":"Bellevue",
 "addressRegion":"WA","postalCode":"98005","addressCountry":"US"}},
"organizer":{"@type":"Organization","name":"ToyBox Consulting & Management",
 "url":"https://www.toyboxconsulting.net"},
"image":"https://goldenhourunboxed.com/og-image.png",
"url":"https://goldenhourunboxed.com/",
"isAccessibleForFree":true,
"description":"A free, cross-cultural celebration of Black entrepreneurship on the Eastside, held during National Black Business Month at Bellevue Botanical Garden."}
</script>
"""

if __name__ == "__main__":
    print("building golden-hour-landing …")
    write("index.html",   build_home())
    write("vendors.html", build_vendors())
    write("thanks.html",  build_thanks())
    write("press.html",   build_press())
    print("done.")
