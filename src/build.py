# -*- coding: utf-8 -*-
"""Gera o site STMetal v6 (adaptado à referência do cliente): index.html + en/ es/ it/, privacidade, sitemap, robots.
Textos em strings_v6.py. Correr na pasta do site:  python3 src/build.py
"""
import json, os, sys, html
from urllib.parse import quote
sys.path.insert(0, os.path.dirname(__file__))
from strings_v6 import LANGS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SIZES = json.load(open(os.path.join(ROOT, 'assets/img/sizes.json')))
SIZES.update({'stock-hall': [1600, 1063], 'stock-steelworks': [1600, 1067], 'stock-welders': [1600, 900]})
PHONE_PT = ('351931122712', '+351 931 122 712')
PHONE_ES = ('34685328793', '+34 685 328 793')
EMAIL = 'stmetal.servicos@gmail.com'
LINKEDIN = 'https://www.linkedin.com/in/stmetal-solucoes-industriais/'
INSTAGRAM = 'https://www.instagram.com/stmetal.servicos/'
ADDRESS = 'R. do Cruzeiro, UBR, Portuguinho, Lt 13, 2.º Dto — 2400-441 Leiria, Portugal'
MAP = 'https://www.openstreetmap.org/search?query=Rua%20do%20Cruzeiro%20Portuguinho%20Leiria'
COMPLAINTS = 'https://www.livroreclamacoes.pt/'
# Quando houver NIF, escreva aqui (ex.: '512345678') e corra o build de novo. Vazio = a linha não aparece.
NIF = ''
# Quando o domínio estiver escolhido, preencha aqui (ex.: 'https://stmetal.pt') e corra o build de novo:
DOMAIN = ''
CLIENTS = ['CAMETO', 'NEGRATIN', 'AJS', 'CO.GET']

e = html.escape
PATHS = dict((c, p) for c, p, _ in LANGS)


def img(r, name, alt, sizes, cls='', lazy=True):
    w0, h0 = SIZES[name]
    ws = sorted({min(640, w0), min(1024, w0), w0 if w0 <= 1600 else 1600})
    ws = [w for w in ws if os.path.exists(os.path.join(ROOT, f'assets/img/{name}-{w}.webp'))]
    big = ws[-1]
    srcset = ', '.join(f'{r}assets/img/{name}-{w}.webp {w}w' for w in ws)
    load = 'loading="lazy" decoding="async"' if lazy else 'fetchpriority="high" decoding="async"'
    c = f' class="{cls}"' if cls else ''
    mid = ws[1] if len(ws) > 1 else big
    return (f'<img{c} src="{r}assets/img/{name}-{mid}.webp" srcset="{srcset}" sizes="{sizes}" '
            f'width="{big}" height="{round(h0 * big / w0)}" alt="{e(alt)}" {load}>')


ARROW = '<svg class="ic" viewBox="0 0 16 16" aria-hidden="true"><path d="M2 8h11M9 4l4 4-4 4" fill="none" stroke="currentColor" stroke-width="1.8"/></svg>'
NE = '<svg class="ic ic--ne" viewBox="0 0 16 16" aria-hidden="true"><path d="M4 12 12 4M5.5 4H12v6.5" fill="none" stroke="currentColor" stroke-width="1.6"/></svg>'
CHEV = '<svg class="ic ic--chev" viewBox="0 0 12 12" aria-hidden="true"><path d="M2.5 4.5 6 8l3.5-3.5" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>'
FLAGS = {
    'pt': '<svg viewBox="0 0 30 20" class="flag" aria-hidden="true"><rect width="12" height="20" fill="#046a38"/><rect x="12" width="18" height="20" fill="#da291c"/><circle cx="12" cy="10" r="3.6" fill="#ffe900"/></svg>',
    'en': '<svg viewBox="0 0 30 20" class="flag" aria-hidden="true"><rect width="30" height="20" fill="#012169"/><path d="M0 0l30 20M30 0L0 20" stroke="#fff" stroke-width="4"/><path d="M0 0l30 20M30 0L0 20" stroke="#c8102e" stroke-width="1.6"/><path d="M15 0v20M0 10h30" stroke="#fff" stroke-width="6"/><path d="M15 0v20M0 10h30" stroke="#c8102e" stroke-width="3.4"/></svg>',
    'es': '<svg viewBox="0 0 30 20" class="flag" aria-hidden="true"><rect width="30" height="20" fill="#aa151b"/><rect y="5" width="30" height="10" fill="#f1bf00"/></svg>',
    'it': '<svg viewBox="0 0 30 20" class="flag" aria-hidden="true"><rect width="10" height="20" fill="#009246"/><rect x="10" width="10" height="20" fill="#fff"/><rect x="20" width="10" height="20" fill="#ce2b37"/></svg>',
}


def lang_menu(code, r, here, t):
    items = []
    for c, path, tt in LANGS:
        href = f'{r}{path}{here or "index.html"}'
        cur = ' aria-current="true"' if c == code else ''
        items.append(f'<li><a href="{href}" lang="{tt["lang"]}" hreflang="{tt["lang"]}"{cur}>{FLAGS[c]}<b>{c.upper()}</b> {tt["name_lang"]}</a></li>')
    return (f'<details class="lang"><summary aria-label="{e(t["lang_label"])}: {t["name_lang"]}">{FLAGS[code]}<b>{code.upper()}</b>{CHEV}</summary>'
            f'<ul class="lang__list">{"".join(items)}</ul></details>')


def head(t, r, code, page='', title=None, desc=None):
    title = title or t['title']; desc = desc or t['desc']
    alts = ''
    if DOMAIN:
        for c, path, tt in LANGS:
            alts += f'<link rel="alternate" hreflang="{tt["lang"]}" href="{DOMAIN}/{path}{page}">\n'
        alts += f'<link rel="alternate" hreflang="x-default" href="{DOMAIN}/{page}">\n'
        alts += f'<link rel="canonical" href="{DOMAIN}/{PATHS[code]}{page}">\n'
    og_img = f'{DOMAIN}/share.jpg' if DOMAIN else f'{r}share.jpg'
    return f'''<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="theme-color" content="#0c0d11">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{og_img}">
<meta property="og:locale" content="{t['og_locale']}">
{alts}<link rel="icon" href="{r}assets/img/gear.png">
<link rel="stylesheet" href="{r}assets/fonts-v6.css">
<link rel="stylesheet" href="{r}assets/v6.css">'''


def topbar(t, r, code, here):
    return f'''<div class="topbar">
  <div class="wrap topbar__in">
    <p class="topbar__contacts mono">
      <a href="tel:+{PHONE_PT[0]}"><span>PT</span> {PHONE_PT[1]}</a>
      <a href="tel:+{PHONE_ES[0]}"><span>ES</span> {PHONE_ES[1]}</a>
      <a class="topbar__mail" href="mailto:{EMAIL}">{EMAIL}</a>
    </p>
    <div class="topbar__right">
      {lang_menu(code, r, here, t)}
      <a class="mono" href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a>
      <a class="mono" href="{INSTAGRAM}" target="_blank" rel="noopener">Instagram</a>
    </div>
  </div>
</div>'''


def header(t, r, code, home_page=True):
    pre = '' if home_page else f'{r}{PATHS[code]}index.html'
    links = ''.join(f'<li><a href="{pre}#{a}">{e(l)}</a></li>' for a, l in t['nav'])
    home = f'{r}{PATHS[code]}index.html'
    return f'''<header class="hdr" data-hdr>
  <div class="wrap hdr__in">
    <a class="logo" href="{home}" aria-label="STMetal"><img src="{r}assets/img/logo-stmetal-240.png" width="240" height="74" alt="STMetal"></a>
    <nav class="nav" id="nav" aria-label="{e(t['menu'])}">
      <ul>{links}</ul>
      <a class="btn btn--orange nav__cta" href="{pre}#orcamento">{e(t['cta'])}</a>
    </nav>
    <button class="burger" type="button" aria-expanded="false" aria-controls="nav" data-open="{e(t['menu'])}" data-close="{e(t['close'])}"><span></span><span></span><b class="sr">{e(t['menu'])}</b></button>
  </div>
</header>'''


def footer(t, r, code):
    home = f'{r}{PATHS[code]}'
    nif = f'<li>NIF {NIF}</li>' if NIF else ''
    return f'''<footer class="ftr">
  <div class="wrap">
    <p class="mono ftr__label">{e(t['ft_legal'])}</p>
    <ul class="ftr__links">
      <li><a href="{COMPLAINTS}" target="_blank" rel="noopener">{e(t['ft_complaints'])} {NE}</a></li>
      <li><a href="{home}privacidade.html">{e(t['ft_privacy'])}</a></li>
      {nif}
    </ul>
    <div class="ftr__base mono"><span>{e(t['ft_tag'])}</span><span>© 2026 STMETAL</span></div>
    <svg class="ftr__mark" viewBox="0 0 1000 150" aria-hidden="true"><text x="0" y="132" textLength="1000" lengthAdjust="spacingAndGlyphs">STMETAL</text></svg>
  </div>
</footer>'''


def eyebrow(s, cls=''):
    return f'<p class="eyebrow{(" " + cls) if cls else ""}" data-r>{e(s)}</p>'


def page(code, path, t):
    r = '../' if path else ''
    wa_pt, wa_es = PHONE_PT[0], PHONE_ES[0]

    strip = ''.join(f'<p>{e(a)}<em>{e(b)}</em></p>' for a, b in t['strip'])
    values = ''.join(f'<li data-r>{e(v)}</li>' for v in t['values'])
    stats = ''.join(f'<li data-r><b data-count="{n}">{n}</b><span>{e(l)}</span></li>' for n, l in t['stats'])
    boxes = ''.join(f'<li data-r><h3>{e(a)}</h3><p>{e(b)}</p></li>' for a, b in t['about_boxes'])

    cards = []
    for i, (im, title, intro, rows, alt) in enumerate(t['skills'], 1):
        lis = ''.join(f'<li><b>{e(b)}</b>{(" " + e(x)) if x else ""}</li>' for b, x in rows)
        cards.append(f'''<li class="card" data-r>
        <figure class="card__img">{img(r, im, alt, '(min-width: 1000px) 400px, (min-width: 640px) 50vw, 100vw')}</figure>
        <div class="card__body"><p class="card__n mono">{i:02d}</p><h3>{e(title)}</h3><p>{e(intro)}</p><ul>{lis}</ul></div>
      </li>''')
    cards.append(f'''<li class="card card--cta" data-r><a href="#orcamento"><span class="mono">{e(t['skills_cta_eyebrow'])}</span><b>{e(t['skills_cta'])} <i aria-hidden="true">→</i></b></a></li>''')

    prin = ''.join(f'<li data-r><h3>{e(a)}</h3><p>{e(b)}</p></li>' for a, b in t['prin'])

    work = []
    for i, (im, country, name, tags, desc, alt) in enumerate(t['work']):
        kind = ['wide', 'wide wide--rev', 'half', 'half'][i]
        sizes = '(min-width: 1000px) 760px, 100vw' if i < 2 else '(min-width: 1000px) 620px, 100vw'
        work.append(f'''<article class="obra obra--{kind}" data-r>
        <figure class="obra__img">{img(r, im, alt, sizes)}</figure>
        <div class="obra__txt"><p class="mono obra__country">{e(country)}</p><h3>{e(name)}</h3><p class="mono obra__tags">{e(tags)}</p><p>{e(desc)}</p></div>
      </article>''')
    clients = ''.join(f'<li data-r>{c}</li>' for c in CLIENTS)
    quality = ''.join(f'<li data-r><span class="num">{i:02d}</span><div><h3>{e(a)}</h3><p>{e(b)}</p></div></li>' for i, (a, b) in enumerate(t['q'], 1))
    why = ''.join(f'<li data-r><span class="mono">{i:02d}</span><h3>{e(a)}</h3><p>{e(b)}</p></li>' for i, (a, b) in enumerate(t['why'], 1))
    how = ''.join(f'<li data-step><span class="num">{i:02d}</span><h3>{e(a)}</h3><p>{e(b)}</p></li>' for i, (a, b) in enumerate(t['how'], 1))
    roles = ''.join(f'<li>{e(x)}</li>' for x in t['jobs_roles'])
    jobs_mail = f"mailto:{EMAIL}?subject={quote(t['jobs_subject'])}&body={quote(t['jobs_body'])}"
    jobs_wa = f"https://wa.me/{wa_pt}?text={quote(t['jobs_wa_text'])}"

    chips = ''.join(f'<label class="chip"><input type="checkbox" name="servico" value="{e(s)}"{" checked" if i == 0 else ""}><span>{e(s)}</span></label>' for i, s in enumerate(t['f_services']))
    mats = ''.join(f'<option>{e(m)}</option>' for m in t['f_materials'])
    countries = ''.join(f'<option>{e(c)}</option>' for c in t['f_countries'])
    msgs = json.dumps({k: t[k].replace('{email}', EMAIL) for k in ('f_locked', 'f_send', 'f_subject', 'f_need', 'f_done', 'f_l_service', 'f_l_material', 'f_l_country', 'f_l_name', 'f_l_company')}, ensure_ascii=False)

    ld = {'@context': 'https://schema.org', '@type': 'LocalBusiness', 'name': 'STMetal', 'email': EMAIL, 'telephone': PHONE_PT[1],
          'address': {'@type': 'PostalAddress', 'streetAddress': 'R. do Cruzeiro, UBR, Portuguinho, Lt 13, 2.º Dto', 'postalCode': '2400-441', 'addressLocality': 'Leiria', 'addressCountry': 'PT'},
          'areaServed': ['PT', 'ES', 'IT'], 'sameAs': [LINKEDIN, INSTAGRAM]}

    h1_words = t['hero_h1'].split(' ')
    h1 = ' '.join(f'<span class="w"><span style="--i:{i}">{e(w)}</span></span>' for i, w in enumerate(h1_words))

    return f'''<!doctype html>
<html lang="{t['lang']}">
<head>
{head(t, r, code)}
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<script>document.documentElement.classList.add('js')</script>
</head>
<body>
<a class="skip" href="#conteudo">{e(t['skip'])}</a>
{topbar(t, r, code, '')}
{header(t, r, code)}
<main id="conteudo">

  <section class="hero" aria-labelledby="hero-h">
    <div class="hero__bg" data-parallax>{img(r, 'estruturas', t['hero_alt'], '100vw', lazy=False)}</div>
    <div class="wrap hero__in">
      <p class="eyebrow hero__eyebrow">{e(t['hero_eyebrow'])}</p>
      <h1 id="hero-h" class="hero__h">{h1}</h1>
      <div class="hero__foot">
        <div>
          <p class="hero__p">{e(t['hero_p'])}</p>
          <p class="mono hero__note">{e(t['hero_note'])}</p>
        </div>
        <p class="hero__btns"><a class="btn btn--orange btn--lg" href="#orcamento">{e(t['cta'])}</a><a class="btn btn--ghost btn--lg" href="https://wa.me/{wa_pt}" target="_blank" rel="noopener">{e(t['hero_wa'])}</a></p>
      </div>
    </div>
  </section>

  <div class="strip"><div class="wrap strip__in">{strip}</div></div>

  <section class="values sec--cream" aria-label="{e(t['about_tag'])}">
    <div class="wrap">
      <ul class="values__list mono">{values}</ul>
      <ul class="stats">{stats}</ul>
    </div>
  </section>

  <section class="sec about" id="quem-somos">
    <div class="wrap split">
      <div>
        {eyebrow(t['about_eyebrow'])}
        <h2 class="h2" data-r>{e(t['about_h2'])}</h2>
        <p class="lead" data-r>{e(t['about_p1'])}</p>
        <p class="muted" data-r>{e(t['about_p2'])}</p>
        <p class="mono tag" data-r>{e(t['about_tag'])}</p>
      </div>
      <ul class="boxes">{boxes}</ul>
    </div>
  </section>

  <section class="sec sec--navy skills" id="competencias">
    <div class="wrap">
      <div class="sec__head">
        <div>{eyebrow(t['skills_eyebrow'])}<h2 class="h2" data-r>{e(t['skills_h2'])}</h2></div>
        <p class="muted" data-r>{e(t['skills_p'])}</p>
      </div>
      <ul class="cards">{''.join(cards)}</ul>
    </div>
  </section>

  <section class="sec sec--cream prin">
    <div class="wrap split">
      <div>{eyebrow(t['prin_eyebrow'])}<h2 class="h2" data-r>{e(t['prin_h2'])}</h2><p class="muted" data-r>{e(t['prin_p'])}</p></div>
      <ul class="grid2">{prin}</ul>
    </div>
  </section>

  <section class="sec work" id="obras">
    <div class="wrap">
      <div class="sec__head">
        <div>{eyebrow(t['work_eyebrow'])}<h2 class="h2" data-r>{e(t['work_h2'])}</h2></div>
        <p class="muted" data-r>{e(t['work_p'])}</p>
      </div>
      <div class="obras">{''.join(work)}</div>
      <div class="clients">
        <div class="clients__head"><h3 data-r>{e(t['clients_h'])}</h3><p class="muted" data-r>{e(t['clients_p'])}</p></div>
        <ul class="clients__list">{clients}</ul>
      </div>
    </div>
  </section>

  <section class="sec sec--navy quality">
    <div class="wrap">
      <div class="sec__head sec__head--end">
        <div>{eyebrow(t['q_eyebrow'])}<h2 class="h2" data-r>{e(t['q_h2'])}</h2></div>
        <p class="muted" data-r>{e(t['q_p'])}</p>
      </div>
      <ul class="pillars">{quality}</ul>
    </div>
  </section>

  <section class="sec sec--cream why">
    <div class="wrap split">
      <div>{eyebrow(t['why_eyebrow'])}<h2 class="h2" data-r>{e(t['why_h2'])}</h2><p class="muted" data-r>{e(t['why_p'])}</p></div>
      <ol class="why__list">{why}</ol>
    </div>
  </section>

  <section class="sec how" id="como-trabalhamos">
    <div class="wrap">
      {eyebrow(t['how_eyebrow'])}
      <h2 class="h2" data-r>{e(t['how_h2'])}</h2>
      <p class="muted" data-r>{e(t['how_p'])}</p>
      <ol class="steps" data-steps><i class="steps__bar" aria-hidden="true"></i>{how}</ol>
    </div>
  </section>

  <section class="sec sec--navy contact" id="contactos">
    <div class="wrap split">
      <div>{eyebrow(t['ct_eyebrow'])}<h2 class="h2" data-r>{e(t['ct_h2'])}</h2><p class="muted" data-r>{e(t['ct_p'])}</p></div>
      <div>
        <ul class="rows">
          <li data-r><div><h3>WhatsApp</h3><p>{e(t['ct_pt'])}</p></div><a class="mono" href="https://wa.me/{wa_pt}" target="_blank" rel="noopener">{PHONE_PT[1]} {NE}</a></li>
          <li data-r><div><h3>WhatsApp</h3><p>{e(t['ct_es'])}</p></div><a class="mono" href="https://wa.me/{wa_es}" target="_blank" rel="noopener">{PHONE_ES[1]} {NE}</a></li>
          <li data-r><div><h3>E-mail</h3><p>{e(t['ct_mail'])}</p></div><a class="mono" href="mailto:{EMAIL}">{EMAIL} {NE}</a></li>
        </ul>
        <p class="mono rows__note" data-r>{e(t['ct_note'])}</p>
      </div>
    </div>
  </section>

  <section class="jobs" id="recrutamento">
    <div class="jobs__bg" data-parallax="strong">{img(r, 'stock-hall', '', '100vw')}</div>
    <div class="wrap jobs__in">
      <div>{eyebrow(t['jobs_eyebrow'])}<h2 class="h2" data-r>{e(t['jobs_h2'])}</h2><p data-r>{e(t['jobs_p'])}</p></div>
      <div class="jobs__side" data-r>
        <ul class="roles">{roles}</ul>
        <p class="jobs__btns"><a class="btn btn--cream" href="{e(jobs_mail)}">{e(t['jobs_mail'])}</a><a class="btn btn--ghost" href="{e(jobs_wa)}" target="_blank" rel="noopener">{e(t['jobs_wa'])}</a></p>
      </div>
    </div>
  </section>

  <section class="sec quote" id="orcamento">
    <div class="wrap split split--form">
      <div>
        {eyebrow(t['qt_eyebrow'])}
        <h2 class="h2 h2--xl" data-r>{e(t['qt_h2a'])} <em>{e(t['qt_h2b'])}</em></h2>
        <p class="mono tag" data-r>{e(t['qt_tag'])}</p>
        <p data-r>{e(t['qt_p'])}</p>
        <div class="quote__info" data-r>
          <p class="muted">{e(ADDRESS)}</p>
          <p><a class="link" href="mailto:{EMAIL}">{EMAIL}</a></p>
          <p><a class="link" href="{MAP}" target="_blank" rel="noopener">{e(t['qt_map'])} ↗</a></p>
        </div>
      </div>
      <form class="form" data-form data-email="{EMAIL}" novalidate data-r>
        <fieldset><legend>{e(t['f_service'])}</legend><div class="chips">{chips}</div></fieldset>
        <div class="form__row">
          <label><span>{e(t['f_material'])}</span><span class="sel"><select name="material">{mats}</select>{CHEV}</span></label>
          <label><span>{e(t['f_country'])}</span><span class="sel"><select name="pais">{countries}</select>{CHEV}</span></label>
        </div>
        <label><span>{e(t['f_desc'])}</span><textarea name="descricao" rows="4" placeholder="{e(t['f_desc_ph'])}"></textarea></label>
        <div class="form__row">
          <label><span>{e(t['f_name'])}</span><input name="nome" autocomplete="name"></label>
          <label><span>{e(t['f_company'])}</span><input name="empresa" autocomplete="organization"></label>
        </div>
        <label class="check"><input type="checkbox" name="consent" data-consent><span>{e(t['f_consent'])}</span></label>
        <button class="btn btn--submit" type="submit" disabled data-submit>{e(t['f_locked'])}</button>
        <p class="form__msg" role="status" aria-live="polite" data-msg></p>
        <script type="application/json" data-msgs>{msgs}</script>
      </form>
    </div>
  </section>

</main>
{footer(t, r, code)}
<script src="{r}assets/v6.js" defer></script>
</body>
</html>
'''


def privacy(code, path, t):
    r = '../' if path else ''
    home = f'{r}{path}index.html'
    body = ''.join(f'<p>{e(p)}</p>' for p in t['pv_body'])
    return f'''<!doctype html>
<html lang="{t['lang']}">
<head>
{head(t, r, code, 'privacidade.html', t['pv_title'], t['pv_body'][0])}
<meta name="robots" content="noindex">
<script>document.documentElement.classList.add('js')</script>
</head>
<body class="legal">
<a class="skip" href="#conteudo">{e(t['skip'])}</a>
{topbar(t, r, code, 'privacidade.html')}
{header(t, r, code, home_page=False)}
<main id="conteudo">
  <section class="sec">
    <div class="wrap measure">
      <p class="eyebrow">{e(t['ft_legal'])}</p>
      <h1 class="h2">{e(t['pv_h1'])}</h1>
      {body}
      <h2 class="h3">{e(t['credits_h'])}</h2>
      <p>{e(t['credits_p'])}</p>
      <ul class="credits">
        <li><a href="https://commons.wikimedia.org/wiki/File:Heavy_industry_(Unsplash).jpg" rel="noopener">Heavy industry (Unsplash)</a>, Ant Rozetsky, CC0</li>
      </ul>
      <p><a class="btn btn--ghost" href="{home}">{e(t['pv_back'])}</a></p>
    </div>
  </section>
</main>
{footer(t, r, code)}
<script src="{r}assets/v6.js" defer></script>
</body>
</html>
'''


def main():
    for code, path, t in LANGS:
        d = os.path.join(ROOT, path)
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, 'index.html'), 'w').write(page(code, path, t))
        open(os.path.join(d, 'privacidade.html'), 'w').write(privacy(code, path, t))
    base = DOMAIN or ''
    urls = ''.join(f'  <url><loc>{base}/{p}</loc></url>\n' for _, p, _ in LANGS)
    open(os.path.join(ROOT, 'sitemap.xml'), 'w').write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    print('ok')


if __name__ == '__main__':
    main()
