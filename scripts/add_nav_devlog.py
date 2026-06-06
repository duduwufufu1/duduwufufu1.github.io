#!/usr/bin/env python3
"""Add DevLog nav link to all blog HTML pages that don't have it yet."""

import os

SITE_DIR = r"D:\_vsc\github_io"
html_files = [
    "index.html", "about/index.html", "archives/index.html",
    "archives/2025/index.html", "archives/2025/03/index.html",
    "tag/index.html", "category/index.html",
    "2025/03/17/hello-world/index.html", "2025/03/19/blog/index.html",
]

changes = 0
for rel in html_files:
    fp = os.path.join(SITE_DIR, rel)
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content

    # Skip if already has DevLog
    if '/devlog' in content:
        print(f"  Skipped (has DevLog): {rel}")
        continue

    # Desktop navbar: insert before About
    content = content.replace(
        '<a class="menu-item" href="/about">About</a>\n                \n                <input',
        '<a class="menu-item" href="/devlog">DevLog</a>\n                \n                    <a class="menu-item" href="/about">About</a>\n                \n                <input'
    )

    # Mobile navbar: insert before About
    content = content.replace(
        '<a class="menu-item" href="/about">About</a>\n                \n            </div>',
        '<a class="menu-item" href="/devlog">DevLog</a>\n                \n                    <a class="menu-item" href="/about">About</a>\n                \n            </div>'
    )

    if content != original:
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(content)
        changes += 1
        print(f"  Updated: {rel}")
    else:
        print(f"  No change: {rel}")

print(f"\nTotal: {changes} files updated")
