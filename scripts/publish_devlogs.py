#!/usr/bin/env python3
"""Convert Obsidian dev logs → Chic blog posts & update archives."""

import os, re
from markdown import markdown
from datetime import datetime

SITE_DIR = r"D:\_vsc\github_io"
OBSIDIAN_DIR = r"F:\Study\Obisdian\TasteGooood开发日志"

# ===== HEAD & FOOTER templates (same as existing blog pages) =====
HEAD = '''<!DOCTYPE html>
<html lang="zh-CN">

<head>
    <meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="X-UA-Compatible" content="ie=edge">

    <meta name="author" content="duduwufufu1">




<title>{title}</title>



    <link rel="preconnect" href="https://cdnjs.cloudflare.com" crossorigin>
    <link rel="dns-prefetch" href="https://cdnjs.cloudflare.com">

    <link rel="icon" href="/favicon.ico">



    <!-- stylesheets list from _config.yml -->
    
    <link rel="stylesheet" href="/css/style.css">
    



    <!-- scripts list from _config.yml -->
    
    <script src="/js/script.js" defer></script>
    
    <script src="/js/tocbot.min.js" defer></script>
    


    
    

<meta name="generator" content="Hexo 7.3.0">
    
    <!-- GSAP Animation Library -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js" defer></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js" defer></script>
    
    <!-- Custom Animations -->
    <script src="/js/animation.js" defer></script>
</head>'''

NAV_OPEN = '''<body>
    <script>
        // this function is used to check current theme before page loaded.
        (() => {
            const currentTheme = window.localStorage && window.localStorage.getItem('theme') || '';
            const isDark = currentTheme === 'dark';
            const pagebody = document.getElementsByTagName('body')[0]
            if (isDark) {
                pagebody.classList.add('dark-theme');
                // mobile
                document.getElementById("mobile-toggle-theme").innerText = "· Dark"
            } else {
                pagebody.classList.remove('dark-theme');
                // mobile
                document.getElementById("mobile-toggle-theme").innerText = "· Light"
            }
        })();
    </script>

    <div class="wrapper">
        <header>
    <nav class="navbar">
        <div class="container">
            <div class="navbar-header header-logo"><a href="/">duduwufufu1&#39;s Blog</a></div>
            <div class="menu navbar-right">
                
                    <a class="menu-item" href="/archives">Posts</a>
                
                    <a class="menu-item" href="/category">Categories</a>
                
                    <a class="menu-item" href="/tag">Tags</a>
                
                    <a class="menu-item" href="/about">About</a>
                
                <input id="switch_default" type="checkbox" class="switch_default">
                <label for="switch_default" class="toggleBtn"></label>
            </div>
        </div>
    </nav>

    
    <nav class="navbar-mobile" id="nav-mobile">
        <div class="container">
            <div class="navbar-header">
                <div>
                    <a href="/">duduwufufu1&#39;s Blog</a><a id="mobile-toggle-theme">·&nbsp;Light</a>
                </div>
                <div class="menu-toggle" onclick="mobileBtn()">&#9776; Menu</div>
            </div>
            <div class="menu" id="mobile-menu">
                
                    <a class="menu-item" href="/archives">Posts</a>
                
                    <a class="menu-item" href="/category">Categories</a>
                
                    <a class="menu-item" href="/tag">Tags</a>
                
                    <a class="menu-item" href="/about">About</a>
                
            </div>
        </div>
    </nav>

</header>
<script>
    var mobileBtn = function f() {
        var toggleMenu = document.getElementsByClassName("menu-toggle")[0];
        var mobileMenu = document.getElementById("mobile-menu");
        if(toggleMenu.classList.contains("active")){
           toggleMenu.classList.remove("active")
            mobileMenu.classList.remove("active")
        }else{
            toggleMenu.classList.add("active")
            mobileMenu.classList.add("active")
        }
    }
</script>'''

FOOTER = '''            <footer id="footer" class="footer">
    <div class="copyright">
        <span>&copy; duduwufufu1 | Powered by <a href="https://hexo.io" target="_blank">Hexo</a> &amp; <a href="https://github.com/Siricee/hexo-theme-Chic" target="_blank">Chic</a></span>
    </div>
</footer>

    </div>
</body>

</html>'''

TOCBOT_JS = '''        <div class="post-toc">
    <div class="tocbot-list">
    </div>
    <div class="tocbot-list-menu">
        <a class="tocbot-toc-expand" onclick="expand_toc()">Expand all</a>
        <a onclick="go_top()">Back to top</a>
        <a onclick="go_bottom()">Go to bottom</a>
    </div>
</div>

<script>
    var tocbot_timer;
    var DEPTH_MAX = 6;
    var tocbot_default_config = {
        tocSelector: '.tocbot-list',
        contentSelector: '.post-content',
        headingSelector: 'h1, h2, h3, h4, h5',
        orderedList: false,
        scrollSmooth: true,
        onClick: extend_click,
    };

    function extend_click() {
        clearTimeout(tocbot_timer);
        tocbot_timer = setTimeout(function() {
            tocbot.refresh(obj_merge(tocbot_default_config, {
                hasInnerContainers: true
            }));
        }, 420);
    }

    document.ready(function() {
        tocbot.init(obj_merge(tocbot_default_config, {
            collapseDepth: 1
        }));
    });

    function expand_toc() {
        var b = document.querySelector('.tocbot-toc-expand');
        var expanded = b.getAttribute('data-expanded');
        expanded ? b.removeAttribute('data-expanded') : b.setAttribute('data-expanded', true);
        tocbot.refresh(obj_merge(tocbot_default_config, {
            collapseDepth: expanded ? 1 : DEPTH_MAX
        }));
        b.innerText = expanded ? 'Expand all' : 'Collapse all';
    }

    function go_top() {
        window.scrollTo(0, 0);
    }

    function go_bottom() {
        window.scrollTo(0, document.body.scrollHeight);
    }

    function obj_merge(target, source) {
        for (var item in source) {
            if (source.hasOwnProperty(item)) {
                target[item] = source[item];
            }
        }
        return target;
    }
</script>'''

# ===== Helpers =====
def strip_frontmatter(text):
    return re.sub(r'^---\n.*?\n---\n', '', text, flags=re.DOTALL)

def fix_wikilinks(text):
    return re.sub(r'\[\[([^\]]+)\]\]', r'\1', text)

def fix_checkboxes(text):
    text = re.sub(r'- \[x\]', '✅', text)
    text = re.sub(r'- \[ \]', '⬜', text)
    return text

def md_to_html(md_text):
    md_text = strip_frontmatter(md_text)
    md_text = fix_wikilinks(md_text)
    md_text = fix_checkboxes(md_text)
    return markdown(md_text, extensions=['fenced_code', 'tables', 'nl2br'])

def add_headerlink(html):
    """Add headerlink anchors to h2/h3/h4 for tocbot."""
    for tag in ['h2', 'h3', 'h4']:
        html = re.sub(
            rf'<{tag}>(.+?)</{tag}>',
            rf'<{tag} id="\1"><a href="#\1" class="headerlink" title="\1"></a>\1</{tag}>',
            html
        )
    return html

# ===== Read & convert dev logs =====
files = sorted(os.listdir(OBSIDIAN_DIR), reverse=True)
posts = []
for fname in files:
    if not fname.endswith('.md'):
        continue
    m = re.search(r'(\d{4})-(\d{2})-(\d{2})', fname)
    if not m:
        continue
    year, month, day = m.group(1), m.group(2), m.group(3)
    date_obj = datetime(int(year), int(month), int(day))
    date_str = f"{date_obj.strftime('%B')} {int(day)}, {year}"

    with open(os.path.join(OBSIDIAN_DIR, fname), 'r', encoding='utf-8') as f:
        raw = f.read()

    html_content = md_to_html(raw)
    html_content = add_headerlink(html_content)

    title_m = re.search(r'<h1>(.+?)</h1>', html_content)
    raw_title = title_m.group(1) if title_m else f"TasteGood 开发日志 {year}-{month}-{day}"
    # Clean title for URL use
    slug = f"tastegood-devlog-{year}-{month}-{day}"
    short_title = f"TasteGood 开发日志 ({year}-{month}-{day})"
    display_title = raw_title

    posts.append({
        "year": year, "month": month, "day": day,
        "date_str": date_str,
        "slug": slug,
        "short_title": short_title,
        "display_title": display_title,
        "html": html_content,
    })

print(f"📖 Found {len(posts)} dev log entries")

# ===== Generate blog post pages =====
for p in posts:
    post_body = f'''            <div class="main">
                <div class="container">
    {TOCBOT_JS}
    
    <article class="post-wrap">
        <header class="post-header">
            <h1 class="post-title">{p["display_title"]}</h1>
            
                <div class="post-meta">
                    
                        Author: <a itemprop="author" rel="author" href="/">duduwufufu1</a>
                    

                    
                        <span class="post-time">
                        Date: <a href="#">{p["date_str"]}</a>
                        </span>
                    
                    
                        <span class="post-category">
                            Category: <a href="/category/">项目开发</a>
                        </span>
                    
                </div>
            
        </header>

        <div class="post-content">
            {p["html"]}
        </div>

        
            <section class="post-copyright">
                
                    <p class="copyright-item">
                        <span>Author:</span>
                        <span>duduwufufu1</span>
                    </p>
                
                
                    <p class="copyright-item">
                        <span>Permalink:</span>
                        <span><a href="http://example.com/{p["year"]}/{p["month"]}/{p["day"]}/{p["slug"]}/">http://example.com/{p["year"]}/{p["month"]}/{p["day"]}/{p["slug"]}/</a></span>
                    </p>
                
                
                    <p class="copyright-item">
                        <span>License:</span>
                        <span>Copyright (c) 2019 <a target="_blank" rel="noopener" href="http://creativecommons.org/licenses/by-nc/4.0/">CC-BY-NC-4.0</a> LICENSE</span>
                    </p>
                
                
                     <p class="copyright-item">
                         <span>Slogan:</span>
                         <span>Do you believe in <strong>DESTINY</strong>?</span>
                     </p>
                

            </section>
        
        <section class="post-tags">
            <div>
                <span>Tag(s):</span>
                <span class="tag">
                    
                        <a class="tag" href="/tag/">#微信小程序</a>
                    
                        <a class="tag" href="/tag/">#TasteGood</a>
                    
                        <a class="tag" href="/tag/">#开发日志</a>
                    
                </span>
            </div>
            <div>
                <a href="javascript:window.history.back();">back</a>
                <span>· </span>
                <a href="/">home</a>
            </div>
        </section>
        <section class="post-nav">
            
            
        </section>


    </article>
</div>
            </div>'''

    full_html = HEAD.format(title=f"{p['display_title']} | duduwufufu1&#39;s Blog") + NAV_OPEN + post_body + FOOTER

    post_dir = os.path.join(SITE_DIR, p["year"], p["month"], p["day"], p["slug"])
    os.makedirs(post_dir, exist_ok=True)
    with open(os.path.join(post_dir, "index.html"), 'w', encoding='utf-8') as f:
        f.write(full_html)
    print(f"  ✅ Created: {p['year']}/{p['month']}/{p['day']}/{p['slug']}/")

# ===== Generate archives/2026/ and archives/2026/06/ =====
# Read existing archive style
def make_archive_page(year, posts_list, title, header_year=None):
    items = []
    for p in posts_list:
        link = f'/{p["year"]}/{p["month"]}/{p["day"]}/{p["slug"]}/'
        items.append(f'''
        <article class="archive-item">
            <a class="archive-item-link" href="{link}">{p["short_title"]}</a>
            <span class="archive-item-date">{p["date_str"]}</span>
        </article>''')

    year_header = f'<h3>{header_year or year}</h3>' if header_year else ''

    body = f'''            <div class="main">
                <div class="post-wrap archive">
    
    {year_header}
    {"".join(items)}

</div>
            </div>'''
    return HEAD.format(title=title) + NAV_OPEN + body + FOOTER

# archives/2026/06/
month_posts = [p for p in posts if p["month"] == "06"]
html = make_archive_page("2026", month_posts, "June 2026 | duduwufufu1&#39;s Blog")
os.makedirs(os.path.join(SITE_DIR, "archives", "2026", "06"), exist_ok=True)
with open(os.path.join(SITE_DIR, "archives", "2026", "06", "index.html"), 'w', encoding='utf-8') as f:
    f.write(html)
print("  ✅ Created: archives/2026/06/")

# archives/2026/
html = make_archive_page("2026", posts, "2026 | duduwufufu1&#39;s Blog", header_year="2026")
os.makedirs(os.path.join(SITE_DIR, "archives", "2026"), exist_ok=True)
with open(os.path.join(SITE_DIR, "archives", "2026", "index.html"), 'w', encoding='utf-8') as f:
    f.write(html)
print("  ✅ Created: archives/2026/")

# ===== Update archives/index.html =====
archives_fp = os.path.join(SITE_DIR, "archives", "index.html")
with open(archives_fp, 'r', encoding='utf-8') as f:
    content = f.read()

# Add 2026 entries after the </div> before the </div> of post-wrap archive
# Find 2025 archive section and add 2026 after it
new_archive_items = []
for p in posts:
    new_archive_items.append(f'''
        <article class="archive-item">
            <a class="archive-item-link" href="/{p["year"]}/{p["month"]}/{p["day"]}/{p["slug"]}/">{p["short_title"]}</a>
            <span class="archive-item-date">{p["date_str"]}</span>
        </article>''')

new_section = f'''
            <h3>2026</h3>
        {"".join(new_archive_items)}'''

# Insert after the 2025 section end (before the closing </div> of post-wrap archive)
content = content.replace(
    '    \n    \n</div>',
    f'{new_section}\n    \n</div>'
)

with open(archives_fp, 'w', encoding='utf-8') as f:
    f.write(content)
print("  ✅ Updated: archives/index.html")

print("\n🎉 All done! Dev logs are now blog posts under Archives.")
