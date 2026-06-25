#!/usr/bin/env python3
"""Fix 3 mobile responsiveness issues across all HTML files."""

import os
import re
import glob

HTML_DIR = "/Users/reshma/growprogress-redesign"

# ─── CSS to inject (hamburger + mobile drawer) ───────────────────────────────
BURGER_CSS = """
    /* ── MOBILE NAV ── */
    .nav-burger{display:none;background:none;border:none;cursor:pointer;padding:.5rem;color:var(--white);line-height:0;}
    .mobile-nav{position:fixed;inset:0;z-index:9999;visibility:hidden;pointer-events:none;}
    .mobile-nav.open{visibility:visible;pointer-events:auto;}
    .mobile-nav-overlay{position:absolute;inset:0;background:rgba(0,0,0,.55);opacity:0;transition:opacity .25s;}
    .mobile-nav.open .mobile-nav-overlay{opacity:1;}
    .mobile-nav-drawer{position:absolute;top:0;right:0;bottom:0;width:min(320px,90vw);background:var(--ink);display:flex;flex-direction:column;transform:translateX(100%);transition:transform .3s cubic-bezier(.4,0,.2,1);overflow-y:auto;}
    .mobile-nav.open .mobile-nav-drawer{transform:translateX(0);}
    .mobile-nav-head{display:flex;align-items:center;justify-content:space-between;padding:1.25rem 1.5rem;border-bottom:1px solid rgba(255,255,255,.08);}
    .mobile-nav-close{background:none;border:none;cursor:pointer;color:var(--white);padding:.25rem;line-height:0;}
    .mobile-nav-close:hover{color:var(--lavender);}
    .mobile-nav-body{padding:1.5rem 0;flex:1;}
    .mobile-nav-section{margin-bottom:1.5rem;}
    .mobile-nav-section-label{font-family:var(--font-h);font-size:.7rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--faint);padding:.25rem 1.5rem .5rem;display:block;}
    .mobile-nav-body a{display:block;padding:.7rem 1.5rem;color:var(--white);text-decoration:none;font-family:var(--font-b);font-size:1rem;transition:background .15s,color .15s;border-radius:0;}
    .mobile-nav-body a:hover{background:rgba(255,255,255,.07);color:var(--lavender);}
    .mobile-nav-body .mobile-nav-sub a{padding:.6rem 1.5rem .6rem 2.5rem;font-size:.9375rem;color:rgba(255,255,255,.75);}
    .mobile-nav-body .mobile-nav-sub a:hover{color:var(--lavender);}
    .mobile-nav-footer{padding:1.25rem 1.5rem;border-top:1px solid rgba(255,255,255,.08);}
    .mobile-nav-footer .btn{display:block;text-align:center;padding:.875rem 1.5rem;background:var(--purple);color:var(--white);text-decoration:none;border-radius:var(--r-md);font-family:var(--font-h);font-weight:700;font-size:.9375rem;transition:background .15s;}
    .mobile-nav-footer .btn:hover{background:var(--mid);}
    @media (max-width:640px){
      .nav-burger{display:flex;align-items:center;justify-content:center;}
      .nav-actions,.nav-right{display:none!important;}
    }"""

# ─── Hamburger button HTML ────────────────────────────────────────────────────
BURGER_BTN = """  <button class="nav-burger" aria-label="Open menu" onclick="document.getElementById('mobileNav').classList.add('open');document.body.style.overflow='hidden';">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
  </button>"""

# ─── Mobile nav drawer HTML ───────────────────────────────────────────────────
MOBILE_NAV_HTML = """
<div class="mobile-nav" id="mobileNav" role="dialog" aria-modal="true" aria-label="Navigation menu">
  <div class="mobile-nav-overlay" onclick="document.getElementById('mobileNav').classList.remove('open');document.body.style.overflow='';"></div>
  <div class="mobile-nav-drawer">
    <div class="mobile-nav-head">
      <img src="gp-logo-light.svg" alt="Grow Progress" style="height:28px;">
      <button class="mobile-nav-close" aria-label="Close menu" onclick="document.getElementById('mobileNav').classList.remove('open');document.body.style.overflow='';">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M18 6 6 18M6 6l12 12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
      </button>
    </div>
    <nav class="mobile-nav-body">
      <div class="mobile-nav-section">
        <span class="mobile-nav-section-label">Platform</span>
        <div class="mobile-nav-sub">
          <a href="audience-understanding.html">Audience Understanding</a>
          <a href="rapid-message-testing.html">Rapid Message Testing</a>
          <a href="pulse-surveys.html">Pulse Surveys</a>
          <a href="persuasion-library.html">Persuasion Library</a>
          <a href="persuasion-sandbox.html">Persuasion Sandbox</a>
          <a href="how-it-works.html">How It Works</a>
        </div>
      </div>
      <div class="mobile-nav-section">
        <span class="mobile-nav-section-label">Who We Serve</span>
        <div class="mobile-nav-sub">
          <a href="politics.html">Political Campaigns</a>
          <a href="advocacy.html">Advocacy Organizations</a>
          <a href="nonprofits.html">Nonprofits</a>
          <a href="labor.html">Labor Unions</a>
        </div>
      </div>
      <a href="about.html">About</a>
      <a href="insights.html">Insights</a>
    </nav>
    <div class="mobile-nav-footer">
      <a href="demo.html" class="btn">Request a Demo</a>
    </div>
  </div>
</div>"""

# ─── JS for keyboard close ────────────────────────────────────────────────────
MOBILE_NAV_JS = """<script>
(function(){
  document.addEventListener('keydown',function(e){
    if(e.key==='Escape'){
      var mn=document.getElementById('mobileNav');
      if(mn){mn.classList.remove('open');document.body.style.overflow='';}
    }
  });
})();
</script>"""


def fix_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    changed = False

    # ── Fix 1: Broken @media rule ─────────────────────────────────────────────
    broken = '(max-width:768px){.newsletter-inner{grid-template-columns:1fr;gap:2rem;}.nl-row{grid-template-columns:1fr;}}'
    fixed  = '@media (max-width:768px){.newsletter-inner{grid-template-columns:1fr;gap:2rem;}.nl-row{grid-template-columns:1fr;}}'
    if broken in html and not fixed in html:
        html = html.replace(broken, fixed)
        changed = True

    # ── Fix 2: Footer duplicate "Labor Unions" ────────────────────────────────
    dup = '<li><a href="#">Labor Unions</a></li>'
    if dup in html:
        html = html.replace(dup, '', 1)
        changed = True

    # ── Fix 3: Hamburger + mobile nav ─────────────────────────────────────────
    needs_burger = BURGER_BTN not in html
    needs_drawer = 'id="mobileNav"' not in html
    needs_css    = '.nav-burger' not in html
    needs_js     = 'mobileNav' not in html or (needs_drawer and MOBILE_NAV_JS.strip() not in html)

    if needs_css:
        # Inject CSS before closing </style> of the first <style> block
        html = html.replace('</style>', BURGER_CSS + '\n  </style>', 1)
        changed = True

    if needs_burger:
        # Add hamburger button just before </nav>
        html = html.replace('</nav>', BURGER_BTN + '\n</nav>', 1)
        changed = True

    if needs_drawer:
        # Add mobile nav drawer right after </nav>
        html = html.replace('</nav>', '</nav>' + MOBILE_NAV_HTML, 1)
        changed = True

    if needs_js and 'id="mobileNav"' in html:
        # Inject JS before </body>
        if MOBILE_NAV_JS.strip() not in html:
            html = html.replace('</body>', MOBILE_NAV_JS + '\n</body>', 1)
            changed = True

    if changed:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)

    return changed


def main():
    files = sorted(glob.glob(os.path.join(HTML_DIR, '*.html')))
    modified = 0
    skipped = 0
    for path in files:
        if fix_file(path):
            modified += 1
            print(f'  FIXED: {os.path.basename(path)}')
        else:
            skipped += 1
            print(f'  skip : {os.path.basename(path)}')
    print(f'\nDone. {modified} files modified, {skipped} already clean.')


if __name__ == '__main__':
    main()
