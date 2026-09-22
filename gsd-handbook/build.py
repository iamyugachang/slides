#!/usr/bin/env python3
"""Build the dependency-free handbook; checked-in output is served by Pages."""
import html
import re
from html.parser import HTMLParser
from content import CHAPTERS, ROOT

TOKENS = {'GSD': '$gsd-', 'CLI': 'codex', 'INSTALL': '--codex'}
def render(s):
    for key, value in TOKENS.items():
        s = s.replace('{{' + key + '}}', f'<span data-token="{key}">{value}</span>')
    return s

nav, sections = [], []
for i, c in enumerate(CHAPTERS):
    nav.append(f'<a href="#{c["id"]}" data-chapter="{c["id"]}"><span class="nav-num">{i:02}</span><span>{c["title"]}</span><span class="nav-check" aria-hidden="true"></span></a>')
    links = []
    if i:
        prev = CHAPTERS[i-1]
        links.append(f'<a href="#{prev["id"]}">← {prev["title"]}</a>')
    if i < len(CHAPTERS)-1:
        nxt = CHAPTERS[i+1]
        links.append(f'<a href="#{nxt["id"]}">{nxt["title"]} →</a>')
    check = f'<label class="complete"><input type="checkbox" data-complete="{c["id"]}"><span>我已完成這一章的練習，並確認出口條件</span></label>' if c['practice'] else ''
    sections.append(f'<section class="chapter" id="{c["id"]}" aria-labelledby="heading-{c["id"]}"><header class="chapter-header"><p class="eyebrow">{c["kicker"]}</p><h1 id="heading-{c["id"]}" tabindex="-1">{c["title"]}</h1><p class="intro">{c["intro"]}</p></header>{render(c["body"])}{check}<nav class="chapter-footer" aria-label="章節翻頁">{"".join(links)}</nav></section>')

page = '''<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>GSD × SDLC 實戰手冊 — Habit Quest</title>
<meta name="description" content="從習慣養成遊戲的初步構想出發，練習 GSD Core 的探索、需求、規劃、實作、驗收與交付。附指令速查、可下載練習本與查證來源。">
<meta name="theme-color" content="#182643"><link rel="stylesheet" href="styles.css"></head>
<body><a class="skip" href="#main">跳到主要內容</a>
<aside class="rail" id="rail"><a class="brand" href="#start"><span class="brand-mark">G<span>↗</span></span><span>GSD × SDLC<small>THE PRACTICE HANDBOOK</small></span></a>
<div class="rail-version">FIELD EDITION <span>v1.14.0</span></div>
<nav class="chapters-nav" aria-label="手冊章節">{{NAV}}</nav>
<div class="rail-bottom"><label for="reading-progress">練習完成 <span id="progress-label">0 / 10</span></label><progress id="reading-progress" max="10" value="0"></progress><a href="../">← 回到 Slides 首頁</a></div></aside>
<div class="page"><header class="topbar"><button id="menu-toggle" type="button" aria-expanded="false" aria-controls="rail">☰ 章節</button><span class="edition">HABIT QUEST / 學習路線</span><label class="runtime-label" for="runtime">使用工具<select id="runtime"><option value="codex">Codex</option><option value="claude">Claude Code</option><option value="opencode">OpenCode</option></select></label><button id="print" type="button" title="列印完整手冊">列印</button></header>
<main id="main"><noscript><p class="callout">目前顯示完整手冊（Codex 指令）。啟用 JavaScript 可切換工具、保存筆記與練習進度。</p></noscript>{{SECTIONS}}</main>
<footer class="site-footer">原創教學案例 · 官方版本 + 社群經驗 + 可修改假設<br><a href="#sources">來源與查核範圍</a> · <a href="handbook.md" download>下載完整手冊</a> · 2026-09-22</footer></div>
<div id="status" role="status" aria-live="polite"></div><script src="app.js"></script></body></html>'''
(ROOT / 'index.html').write_text(page.replace('{{NAV}}', ''.join(nav)).replace('{{SECTIONS}}', ''.join(sections)))

class Markdown(HTMLParser):
    def __init__(self):
        super().__init__(); self.out=[]; self.skip=0; self.pre=False; self.links=[]
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if self.skip:
            self.skip += 1; return
        if tag in ('button','input','progress','textarea') or 'code-bar' in a.get('class',''):
            if tag not in ('input',): self.skip=1
            return
        if tag in ('h2','h3'): self.out.append('\n\n' + '#' * int(tag[1]) + ' ')
        elif tag in ('p','div','aside','article','table','tr','ul','ol'): self.out.append('\n')
        elif tag=='li': self.out.append('\n- ')
        elif tag=='br': self.out.append('\n')
        elif tag=='pre': self.pre=True; self.out.append('\n\n```text\n')
        elif tag=='code' and not self.pre: self.out.append('`')
        elif tag=='a': self.links.append(a.get('href','')); self.out.append('[')
        elif tag in ('strong','th'): self.out.append('**')
    def handle_endtag(self, tag):
        if self.skip:
            self.skip -= 1; return
        if tag=='pre': self.pre=False; self.out.append('\n```\n\n')
        elif tag=='code' and not self.pre: self.out.append('`')
        elif tag=='a' and self.links: self.out.append('](' + self.links.pop() + ')')
        elif tag in ('strong','th'): self.out.append('**' + (' | ' if tag=='th' else ''))
        elif tag=='td': self.out.append(' | ')
        elif tag in ('h2','h3','p','div','aside','article','tr','li'): self.out.append('\n')
    def handle_data(self, data):
        if not self.skip: self.out.append(data)

md=['# GSD × SDLC 實戰手冊\n\n固定版本：1.14.0 · 查核：2026-09-22\n\n線上版：https://iamyugachang.github.io/slides/gsd-handbook/\n\n以下使用 Codex 入口。Claude Code / OpenCode 的 `$gsd-` 改為 `/gsd-`；shell 的 `--codex` 與 `codex` 改成對應 runtime。\n']
for c in CHAPTERS:
    body=c['body']
    for k,v in TOKENS.items(): body=body.replace('{{'+k+'}}',v)
    p=Markdown(); p.feed(body)
    text=re.sub(r'\n{3,}', '\n\n', ''.join(p.out))
    md.append(f'\n<a id="{c["id"]}"></a>\n\n## {c["title"]}\n\n{c["intro"]}\n{text}')
(ROOT / 'handbook.md').write_text('\n'.join(md))
print(f'Built {len(CHAPTERS)} chapters; index.html and handbook.md')
