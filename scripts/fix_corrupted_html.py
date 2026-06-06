#!/usr/bin/env python3
"""Fix corrupted HTML files: restore from git & re-apply all modifications."""

import os

SITE_DIR = r"D:\_vsc\github_io"

FILES = [
    "about/index.html",
    "archives/index.html",
    "archives/2025/index.html",
    "archives/2025/03/index.html",
    "tag/index.html",
    "category/index.html",
    "2025/03/17/hello-world/index.html",
    "2025/03/19/blog/index.html",
]

def fix_file(rel):
    fp = os.path.join(SITE_DIR, rel)
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content

    # 1. lang="ch" → lang="zh-CN"
    content = content.replace('lang="ch"', 'lang="zh-CN"')

    # 2. Fix viewport meta (multi-line → one line, remove max-scale)
    content = content.replace(
        '<meta name="viewport"\n      content="width=device-width, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
    )

    # 3. Add defer to script.js
    content = content.replace(
        '<script src="/js/script.js"></script>',
        '<script src="/js/script.js" defer></script>'
    )

    # 4. Add defer to tocbot.min.js
    content = content.replace(
        '<script src="/js/tocbot.min.js"></script>',
        '<script src="/js/tocbot.min.js" defer></script>'
    )

    # 5. Add GSAP + animation.js before </head>
    content = content.replace(
        '<meta name="generator" content="Hexo 7.3.0"></head>',
        '<meta name="generator" content="Hexo 7.3.0">\n    \n    <!-- GSAP Animation Library -->\n    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js" defer></script>\n    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js" defer></script>\n    \n    <!-- Custom Animations -->\n    <script src="/js/animation.js" defer></script>\n</head>'
    )

    # 6. Add preconnect before favicon
    content = content.replace(
        '    <link rel="icon" href="/favicon.ico">',
        '    <link rel="preconnect" href="https://cdnjs.cloudflare.com" crossorigin>\n    <link rel="dns-prefetch" href="https://cdnjs.cloudflare.com">\n\n    <link rel="icon" href="/favicon.ico">'
    )

    # 7. Add DevLog to desktop navbar (before About)
    content = content.replace(
        '<a class="menu-item" href="/about">About</a>\n                \n                <input id="switch_default"',
        '<a class="menu-item" href="/devlog">DevLog</a>\n                \n                    <a class="menu-item" href="/about">About</a>\n                \n                <input id="switch_default"'
    )

    # 8. Add DevLog to mobile navbar (before About)
    content = content.replace(
        '<a class="menu-item" href="/about">About</a>\n                \n            </div>\n        </div>\n    </nav>',
        '<a class="menu-item" href="/devlog">DevLog</a>\n                \n                    <a class="menu-item" href="/about">About</a>\n                \n            </div>\n        </div>\n    </nav>'
    )

    if content != original:
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✅ Fixed: {rel}")
        return True
    print(f"  ⚠️  No changes: {rel}")
    return False

count = 0
for rel in FILES:
    if fix_file(rel):
        count += 1

print(f"\nFixed {count}/{len(FILES)} files")
