#!/usr/bin/env python3
"""Batch update: remove DevLog from nav, fill about/category/tag content."""

import os, shutil

SITE_DIR = r"D:\_vsc\github_io"

HTML_FILES = [
    "index.html", "about/index.html", "archives/index.html",
    "archives/2025/index.html", "archives/2025/03/index.html",
    "tag/index.html", "category/index.html",
    "2025/03/17/hello-world/index.html", "2025/03/19/blog/index.html",
]

# ===== 1. Remove devlog/ from filesystem =====
devlog_dir = os.path.join(SITE_DIR, "devlog")
if os.path.isdir(devlog_dir):
    shutil.rmtree(devlog_dir)
    print("✅ Deleted devlog/ directory")

# ===== 2. Remove DevLog from all navbars =====
for rel in HTML_FILES:
    fp = os.path.join(SITE_DIR, rel)
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content

    # Desktop navbar: remove DevLog before About
    content = content.replace(
        '<a class="menu-item" href="/devlog">DevLog</a>\n                \n                    <a class="menu-item" href="/about">About</a>',
        '<a class="menu-item" href="/about">About</a>'
    )
    # Mobile navbar: remove DevLog before About
    content = content.replace(
        '<a class="menu-item" href="/devlog">DevLog</a>\n                \n                    <a class="menu-item" href="/about">About</a>\n                \n            </div>',
        '<a class="menu-item" href="/about">About</a>\n                \n            </div>'
    )

    if content != original:
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✅ Nav fix: {rel}")

# ===== 3. Fill About page =====
about_fp = os.path.join(SITE_DIR, "about", "index.html")
with open(about_fp, 'r', encoding='utf-8') as f:
    content = f.read()

about_html = '''        <h2 class="post-title">关于我</h2>
        
        <section class="post-content">
            <p>你好，我是 <strong>富荣达</strong>（duduwufufu1），一名热爱技术的开发者。</p>
            
            <h3>🛠 技术栈</h3>
            <ul>
                <li><strong>前端：</strong>微信小程序原生开发、JavaScript、HTML/CSS</li>
                <li><strong>后端/云：</strong>微信云开发</li>
                <li><strong>工具：</strong>Git、Codex CLI、Hermes Agent、Obsidian</li>
            </ul>

            <h3>📱 项目</h3>
            <ul>
                <li><strong>TasteGood</strong> — 一款城市美食点评微信小程序，支持城市浏览、地图标记、评分记录等功能。</li>
            </ul>

            <h3>📬 联系我</h3>
            <ul>
                <li><strong>GitHub：</strong><a href="https://github.com/duduwufufu1" target="_blank">duduwufufu1</a></li>
                <li><strong>知乎：</strong><a href="https://www.zhihu.com/people/ng-ng-ng-41-47" target="_blank">ng-ng-ng-41-47</a></li>
                <li><strong>QQ：</strong>2250142551</li>
            </ul>

            <h3>📝 关于博客</h3>
            <p>这个博客使用 <a href="https://hexo.io" target="_blank">Hexo</a> 生成，<a href="https://github.com/Siricee/hexo-theme-Chic" target="_blank">Chic</a> 主题，托管在 GitHub Pages 上。记录我的技术学习与项目开发过程。</p>
        </section>'''

content = content.replace(
    '<h2 class="post-title">about</h2>\n        \n        <section class="post-content">\n            \n        </section>',
    about_html
)
with open(about_fp, 'w', encoding='utf-8') as f:
    f.write(content)
print("  ✅ About page: content added")

# ===== 4. Fill Category page =====
cat_fp = os.path.join(SITE_DIR, "category", "index.html")
with open(cat_fp, 'r', encoding='utf-8') as f:
    content = f.read()

cat_html = '''        <h2 class="post-title">分类</h2>
        
        <section class="post-content">
            <p>博客文章按分类归档：</p>
            <ul>
                <li><strong>技术笔记</strong> — 开发过程中的技术总结与踩坑记录</li>
                <li><strong>项目开发</strong> — 项目开发日志与进度追踪</li>
                <li><strong>生活感悟</strong> — 日常思考与生活记录</li>
            </ul>
        </section>'''

content = content.replace(
    '<h2 class="post-title">category</h2>\n        \n        <section class="post-content">\n            \n        </section>',
    cat_html
)
with open(cat_fp, 'w', encoding='utf-8') as f:
    f.write(content)
print("  ✅ Category page: content added")

# ===== 5. Fill Tag page =====
tag_fp = os.path.join(SITE_DIR, "tag", "index.html")
with open(tag_fp, 'r', encoding='utf-8') as f:
    content = f.read()

tag_html = '''        <h2 class="post-title">标签</h2>
        
        <section class="post-content">
            <p>博客文章标签索引：</p>
            <ul>
                <li><code>#Node.js</code></li>
                <li><code>#微信小程序</code></li>
                <li><code>#前端</code></li>
                <li><code>#开发日志</code></li>
                <li><code>#TasteGood</code></li>
            </ul>
        </section>'''

content = content.replace(
    '<h2 class="post-title">tag</h2>\n        \n        <section class="post-content">\n            \n        </section>',
    tag_html
)
with open(tag_fp, 'w', encoding='utf-8') as f:
    f.write(content)
print("  ✅ Tag page: content added")

print("\n✅ All done!")
