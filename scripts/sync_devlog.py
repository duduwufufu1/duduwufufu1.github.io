#!/usr/bin/env python3
"""
Sync Obsidian devlogs → GitHub Pages blog
Usage: python3 sync_devlog.py
"""

import os, re, datetime
from markdown import markdown

# === CONFIG ===
OBSIDIAN_DIR = r"F:\Study\Obisdian\TasteGooood开发日志"
OUTPUT_DIR = r"D:\_vsc\github_io\devlog"
SITE_DIR = r"D:\_vsc\github_io"
PROJECTS = {
    "tastegood": {
        "name": "TasteGood",
        "title": "TasteGood 微信小程序",
        "desc": "一款城市美食点评微信小程序，基于原生框架 + 微信云开发。",
        "github": "https://github.com/duduwufufu1/TasteGood",
        "icon": "🍽️",
        "obsidian_dir": OBSIDIAN_DIR,
    },
}

# === HEAD TEMPLATES ===
HEAD_TPL = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <meta name="author" content="duduwufufu1">
    <meta name="description" content="duduwufufu1 的项目开发日志">
    <title>{title} | duduwufufu1&#39;s Blog</title>
    <link rel="preconnect" href="https://cdnjs.cloudflare.com" crossorigin>
    <link rel="dns-prefetch" href="https://cdnjs.cloudflare.com">
    <link rel="icon" href="/favicon.ico">
    <link rel="stylesheet" href="/css/style.css">
    <script src="/js/script.js" defer></script>
    <script src="/js/tocbot.min.js" defer></script>
    <meta name="generator" content="Hexo 7.3.0">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js" defer></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js" defer></script>
    <script src="/js/animation.js" defer></script>
</head>'''

NAVBAR_TPL = '''<body>
    <script>
        (() => {
            const currentTheme = window.localStorage && window.localStorage.getItem('theme') || '';
            const isDark = currentTheme === 'dark';
            const pagebody = document.getElementsByTagName('body')[0];
            if (isDark) { pagebody.classList.add('dark-theme');
                document.getElementById("mobile-toggle-theme").innerText = "· Dark";
            } else { pagebody.classList.remove('dark-theme');
                document.getElementById("mobile-toggle-theme").innerText = "· Light"; }
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
                        <a class="menu-item" href="/devlog">DevLog</a>
                        <a class="menu-item" href="/about">About</a>
                        <input id="switch_default" type="checkbox" class="switch_default">
                        <label for="switch_default" class="toggleBtn"></label>
                    </div>
                </div>
            </nav>
            <nav class="navbar-mobile" id="nav-mobile">
                <div class="container">
                    <div class="navbar-header">
                        <div><a href="/">duduwufufu1&#39;s Blog</a><a id="mobile-toggle-theme">·&nbsp;Light</a></div>
                        <div class="menu-toggle" onclick="mobileBtn()">&#9776; Menu</div>
                    </div>
                    <div class="menu" id="mobile-menu">
                        <a class="menu-item" href="/archives">Posts</a>
                        <a class="menu-item" href="/category">Categories</a>
                        <a class="menu-item" href="/tag">Tags</a>
                        <a class="menu-item" href="/devlog">DevLog</a>
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
                   toggleMenu.classList.remove("active");
                    mobileMenu.classList.remove("active");
                }else{
                    toggleMenu.classList.add("active");
                    mobileMenu.classList.add("active");
                }
            };
        </script>'''

FOOTER_HTML = '''
            <footer id="footer" class="footer">
                <div class="copyright">
                    <span>&copy; duduwufufu1 | Powered by <a href="https://hexo.io" target="_blank">Hexo</a> &amp; <a href="https://github.com/Siricee/hexo-theme-Chic" target="_blank">Chic</a></span>
                </div>
            </footer>
        </div>
    </body>
</html>'''

DEVLOG_CSS = '''
<style>
.devlog-project-list {
    display: flex;
    flex-direction: column;
    gap: 1em;
    margin-top: 1.5em;
}
.devlog-project-card {
    display: flex;
    flex-direction: column;
    gap: 0.4em;
    padding: 1.5em;
    border: 1px solid var(--color-border, #e6e6e6);
    border-radius: var(--radius-md, 8px);
    background: var(--color-card-bg, #fff);
    box-shadow: var(--shadow-sm, 0 1px 3px rgba(0,0,0,0.06));
    transition: box-shadow var(--transition-base, 0.3s), transform var(--transition-base, 0.3s);
    text-decoration: none;
    color: inherit;
}
.devlog-project-card:hover {
    box-shadow: var(--shadow-md, 0 4px 12px rgba(0,0,0,0.08));
    transform: translateY(-2px);
}
.dark-theme .devlog-project-card {
    background: var(--color-card-bg-dark, #333436);
    border-color: var(--color-border-dark, #3a3b3e);
}
.devlog-project-icon { font-size: 2rem; }
.devlog-project-name { font-size: 1.3rem; font-weight: 700; }
.devlog-project-desc { font-size: 0.95rem; color: var(--color-text-secondary, #5c5c5c); line-height: 1.6; }
.dark-theme .devlog-project-desc { color: var(--color-text-secondary-dark, #888891); }
.devlog-project-link { font-size: 0.85rem; color: var(--color-link-hover, #2d96bd); word-break: break-all; }

.devlog-entry {
    margin-bottom: 2.5em;
    padding-bottom: 2em;
    border-bottom: 1px solid var(--color-border, #e6e6e6);
}
.dark-theme .devlog-entry { border-color: var(--color-border-dark, #3a3b3e); }
.devlog-entry:last-child { border-bottom: none; margin-bottom: 0; padding-bottom: 0; }
.devlog-entry-title {
    font-size: 1.3rem;
    margin-bottom: 0.3em;
}
.devlog-entry-title a { color: inherit; text-decoration: none; }
.devlog-entry-title a:hover { color: var(--color-link-hover, #2d96bd); }
.devlog-entry-date {
    display: inline-block;
    font-size: 0.85rem;
    color: var(--color-text-secondary, #5c5c5c);
    margin-bottom: 1em;
    padding: 0.2em 0.8em;
    background: var(--color-bg-alt, #f8f9fa);
    border-radius: 4px;
}
.dark-theme .devlog-entry-date {
    color: var(--color-text-secondary-dark, #888891);
    background: var(--color-bg-alt-dark, #222325);
}
.devlog-entry-content h2 { font-size: 1.1rem; margin-top: 1.2em; }
.devlog-entry-content h3 { font-size: 1rem; margin-top: 1em; }
.devlog-entry-content h4 { font-size: 0.95rem; margin-top: 0.8em; }
.devlog-entry-content table {
    width: 100%;
    border-collapse: collapse;
    margin: 1em 0;
    font-size: 0.9rem;
}
.devlog-entry-content th, .devlog-entry-content td {
    border: 1px solid var(--color-border, #e6e6e6);
    padding: 0.5em 0.8em;
    text-align: left;
}
.dark-theme .devlog-entry-content th,
.dark-theme .devlog-entry-content td {
    border-color: var(--color-border-dark, #3a3b3e);
}
.devlog-entry-content th {
    background: var(--color-bg-alt, #f8f9fa);
    font-weight: 600;
}
.dark-theme .devlog-entry-content th {
    background: var(--color-bg-alt-dark, #222325);
}
.devlog-entry-content pre {
    background: #f5f5f5;
    border-radius: 6px;
    padding: 1em;
    overflow-x: auto;
    font-size: 0.85rem;
    line-height: 1.5;
}
.dark-theme .devlog-entry-content pre {
    background: #1e1e1e;
}
.devlog-entry-content code {
    font-family: 'Fira Code', 'Cascadia Code', 'Consolas', monospace;
    font-size: 0.85em;
    padding: 0.15em 0.3em;
    background: #f0f0f0;
    border-radius: 3px;
}
.dark-theme .devlog-entry-content code {
    background: #333;
}
.devlog-entry-content ul, .devlog-entry-content ol {
    padding-left: 1.5em;
    line-height: 1.8;
}
.devlog-entry-content blockquote {
    border-left: 3px solid var(--color-accent, #1abc9c);
    margin: 1em 0;
    padding: 0.5em 1em;
    background: var(--color-bg-alt, #f8f9fa);
    border-radius: 0 6px 6px 0;
}
.dark-theme .devlog-entry-content blockquote {
    background: var(--color-bg-alt-dark, #222325);
}
.devlog-back-link {
    display: inline-block;
    margin-bottom: 1.5em;
    font-size: 0.9rem;
    color: var(--color-link-hover, #2d96bd);
}
.devlog-back-link:hover { text-decoration: underline; }
</style>
'''

# === HELPERS ===
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

def read_devlogs(obsidian_dir):
    if not os.path.isdir(obsidian_dir):
        return []
    files = sorted(os.listdir(obsidian_dir), reverse=True)
    entries = []
    for fname in files:
        if not fname.endswith('.md'):
            continue
        m = re.search(r'(\d{4}-\d{2}-\d{2})', fname)
        date_str = m.group(1) if m else "unknown"
        with open(os.path.join(obsidian_dir, fname), 'r', encoding='utf-8') as f:
            raw = f.read()
        html_content = md_to_html(raw)
        title_m = re.search(r'<h1>(.+?)</h1>', html_content)
        title = title_m.group(1) if title_m else f"更新于 {date_str}"
        entries.append({"date": date_str, "title": title, "html": html_content})
    return entries

def build_page(title, content_body):
    return (HEAD_TPL.format(title=title) + NAVBAR_TPL
            + '\n            <div class="main">\n                <div class="container" style="max-width: 800px;">\n'
            + content_body
            + '\n                </div>\n            </div>\n'
            + FOOTER_HTML)

# === GENERATE /devlog/index.html ===
project_cards = []
for slug, proj in PROJECTS.items():
    entries = read_devlogs(proj["obsidian_dir"])
    entry_count = len(entries)
    last_updated = entries[0]["date"] if entries else "暂无"
    project_cards.append(f'''
            <a class="devlog-project-card" href="/devlog/{slug}/">
                <div class="devlog-project-icon">{proj["icon"]}</div>
                <div class="devlog-project-name">{proj["name"]}</div>
                <div class="devlog-project-desc">{proj["desc"]}</div>
                <div class="devlog-project-link">{proj["github"]}</div>
                <div style="font-size:0.85rem;color:var(--color-text-secondary,#5c5c5c);margin-top:0.3em;">
                    {entry_count} 篇日志 · 最近更新 {last_updated}
                </div>
            </a>''')

index_body = f'''
                    <article class="post-wrap page">
                        <h1 class="post-title">📋 开发日志</h1>
                        <section class="post-content">
                            <p>项目开发过程中的日志记录。按项目分类，自动从 Obsidian 同步。</p>
                            {DEVLOG_CSS}
                            <div class="devlog-project-list">
                                {"".join(project_cards)}
                            </div>
                        </section>
                    </article>'''

os.makedirs(OUTPUT_DIR, exist_ok=True)
with open(os.path.join(OUTPUT_DIR, "index.html"), 'w', encoding='utf-8') as f:
    f.write(build_page("DevLog", index_body))
print("✅ Created /devlog/index.html")

# === GENERATE PROJECT PAGES ===
for slug, proj in PROJECTS.items():
    entries = read_devlogs(proj["obsidian_dir"])
    if not entries:
        print(f"⚠️  No entries for {slug}")
        continue

    entry_htmls = []
    for i, e in enumerate(entries):
        entry_htmls.append(f'''
        <div class="devlog-entry gsap-fade">
            <h2 class="devlog-entry-title"><a href="#entry-{e['date']}" id="entry-{e['date']}">{e['title']}</a></h2>
            <div class="devlog-entry-date">📅 {e['date']}</div>
            <div class="devlog-entry-content">
                {e['html']}
            </div>
        </div>''')

    proj_body = f'''
                    <article class="post-wrap page">
                        <h1 class="post-title">{proj["icon"]} {proj["name"]} 开发日志</h1>
                        <section class="post-content">
                            <a class="devlog-back-link" href="/devlog/">← 返回项目列表</a>
                            <p>{proj["desc"]}</p>
                            <p><a href="{proj["github"]}" target="_blank" rel="noopener">{proj["github"]}</a></p>
                            {DEVLOG_CSS}
                            <hr>
                            {"".join(entry_htmls)}
                        </section>
                    </article>'''

    proj_dir = os.path.join(OUTPUT_DIR, slug)
    os.makedirs(proj_dir, exist_ok=True)
    with open(os.path.join(proj_dir, "index.html"), 'w', encoding='utf-8') as f:
        f.write(build_page(f"{proj['name']} DevLog", proj_body))
    print(f"✅ Created /devlog/{slug}/index.html ({len(entries)} entries)")

print("\n🎉 DevLog sync complete!")
