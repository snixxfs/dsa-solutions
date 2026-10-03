"""Rebuilds the solutions table in README.md from the header comments of each solution file."""
import os
import re

SITES = ["codechef", "leetcode"]
START, END = "<!-- TABLE-START -->", "<!-- TABLE-END -->"


def parse(path):
    info = {}
    with open(path, encoding="utf-8", errors="ignore") as f:
        for line in f.readlines()[:12]:
            m = re.match(r"^\s*(?:#|//)\s*(\w+):\s*(.*)$", line)
            if m:
                info[m.group(1).lower()] = m.group(2).strip()
    return info


rows, counts = [], {}
for site in SITES:
    files = sorted(f for f in os.listdir(site) if not f.startswith("."))
    counts[site] = len(files)
    for fn in files:
        d = parse(os.path.join(site, fn))
        name = d.get("problem", os.path.splitext(fn)[0])
        link = f"[{name}]({d['link']})" if d.get("link") else name
        rows.append(f"| {site} | {link} | {d.get('topic', '')} | {d.get('difficulty', '')} "
                    f"| {d.get('complexity', '')} | [code]({site}/{fn}) |")

table = "\n".join([
    f"**Solved: {sum(counts.values())}** (" + ", ".join(f"{k}: {v}" for k, v in counts.items()) + ")",
    "",
    "| Site | Problem | Topic | Difficulty | Complexity | Solution |",
    "|------|---------|-------|------------|------------|----------|",
    *rows,
])

with open("README.md", encoding="utf-8") as f:
    text = f.read()
pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)
with open("README.md", "w", encoding="utf-8") as f:
    f.write(pattern.sub(f"{START}\n{table}\n{END}", text))
print("README updated:", sum(counts.values()), "solutions")
