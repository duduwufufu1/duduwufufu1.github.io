#!/usr/bin/env python3
"""
Obsidian Devlog → GitHub Pages sync & deploy script.
Run manually or via cron to keep the blog up to date with Obsidian dev logs.
"""

import os, subprocess, sys
from datetime import datetime

SITE_DIR = r"D:\_vsc\github_io"
SCRIPTS_DIR = os.path.join(SITE_DIR, "scripts")

def run(cmd, cwd=None):
    result = subprocess.run(
        cmd, shell=True, capture_output=True, text=True, cwd=cwd or SITE_DIR
    )
    if result.returncode != 0 and result.returncode != 1:
        # exit 1 from git diff means "there are differences" — not an error
        if "diff" in cmd and result.returncode == 1:
            pass
        else:
            print(f"[WARN] exit {result.returncode}: {cmd[:80]}")
    return result.stdout.strip(), result.stderr.strip()

def main():
    print(f"=== DevLog Sync @ {datetime.now().strftime('%Y-%m-%d %H:%M')} ===")

    # Step 1: Regenerate pages
    sync_script = os.path.join(SCRIPTS_DIR, "sync_devlog.py")
    if not os.path.exists(sync_script):
        print(f"[ERROR] sync script not found: {sync_script}")
        return 1

    out, err = run(f'python "{sync_script}"')
    print(out)
    if err:
        print(f"[STDERR] {err}")

    # Step 2: Check for changes
    out, _ = run("git diff --stat")
    if not out:
        print("No changes to deploy.")
        return 0

    print(f"Changes detected:\n{out}")

    # Step 3: Commit and push
    run('git add -A')
    run(f'git commit -m "docs: 自动同步开发日志 {datetime.now().strftime("%Y-%m-%d")}"')
    push_out, push_err = run("git push")
    print(push_out)
    if push_err and "error:" in push_err:
        print(f"[PUSH ERROR] {push_err}")
        return 1

    print("✅ Deployed to GitHub Pages!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
