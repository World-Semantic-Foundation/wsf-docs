#!/usr/bin/env python3
"""
WSF Docs Site Builder
=====================

Generates the static concept reference site from:
- wsf/concepts/*.md        (canonical concept definitions, sibling repo)
- wsf-docs content         (tutorials, principles, deep-dive)

Output: ./_site with index.html + one page per document.

Sibling layout expected:

    <parent>/
    ├── wsf/
    └── wsf-docs/   (this repo)
"""

import glob
import html
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.normpath(os.path.join(HERE, ".."))
WSF_DIR = os.path.normpath(os.path.join(DOCS_DIR, "..", "wsf"))
OUT_DIR = os.path.join(DOCS_DIR, "_site")


def md_to_html_body(md_text: str) -> str:
    """Minimal, dependency-free Markdown to HTML for the reference site."""
    lines = md_text.split("\n")
    out = []
    in_code = False
    code_buf = []
    in_list = False

    def flush_list():
        nonlocal in_list
        if in_list:
            out.append("</ul>")
            in_list = False

    for line in lines:
        if line.strip().startswith("```"):
            if in_code:
                out.append("<pre><code>" + html.escape("\n".join(code_buf)) + "</code></pre>")
                code_buf = []
                in_code = False
            else:
                flush_list()
                in_code = True
            continue
        if in_code:
            code_buf.append(line)
            continue

        stripped = line.strip()
        if not stripped:
            flush_list()
            continue
        if stripped.startswith("|") and stripped.endswith("|"):
            flush_list()
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            if all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
                continue
            out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in cells) + "</tr>")
            continue
        if stripped.startswith("#"):
            flush_list()
            level = len(stripped) - len(stripped.lstrip("#"))
            level = min(level, 6)
            out.append(f"<h{level}>{inline(stripped[level:].strip())}</h{level}>")
            continue
        if stripped.startswith("- ") or stripped.startswith("* "):
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{inline(stripped[2:])}</li>")
            continue
        if stripped.startswith(">"):
            flush_list()
            out.append(f"<blockquote>{inline(stripped.lstrip('> ').strip())}</blockquote>")
            continue
        if re.match(r"^\d+\.\s", stripped):
            flush_list()
            out.append(f"<p>{inline(stripped)}</p>")
            continue
        flush_list()
        out.append(f"<p>{inline(line)}</p>")
    flush_list()
    if in_code and code_buf:
        out.append("<pre><code>" + html.escape("\n".join(code_buf)) + "</code></pre>")
    return "\n".join(out)


def inline(text: str) -> str:
    text = html.escape(text, quote=False)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1", text)
    return text


CSS = """
body { font-family: Georgia, serif; max-width: 52em; margin: 2em auto; padding: 0 1.5em;
       color: #1a1a1a; background: #faf9f7; line-height: 1.6; }
h1 { border-bottom: 2px solid #2a4d69; padding-bottom: 0.3em; }
h2 { color: #2a4d69; margin-top: 1.8em; }
code, pre { font-family: 'SF Mono', Menlo, Consolas, monospace; font-size: 0.9em; }
pre { background: #f0ede9; padding: 1em; overflow-x: auto; border-radius: 4px; }
table { border-collapse: collapse; margin: 1em 0; }
td { border: 1px solid #d0cbc4; padding: 0.4em 0.8em; }
nav a { margin-right: 1em; }
.card { display: inline-block; border: 1px solid #d0cbc4; border-radius: 6px;
        padding: 0.6em 1em; margin: 0.3em; background: #fff; }
blockquote { border-left: 3px solid #2a4d69; margin-left: 0; padding-left: 1em; color: #444; }
"""


def page(title: str, body: str, nav: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<style>{CSS}</style>
</head>
<body>
<nav><a href="index.html">WSF Reference</a><a href="tutorials.html">Tutorials</a></nav>
{body}
<hr>
<p><small>World Semantic Foundation : canonical concept reference. Generated from the wsf and wsf-docs repositories.</small></p>
</body>
</html>"""


def build():
    if not os.path.isdir(WSF_DIR):
        print(f"FATAL: sibling repository not found at {WSF_DIR}")
        sys.exit(2)
    os.makedirs(OUT_DIR, exist_ok=True)

    # Concept pages
    concepts = []
    for f in sorted(glob.glob(os.path.join(WSF_DIR, "concepts", "*.md"))):
        name = os.path.basename(f)[:-3]
        md = open(f, encoding="utf-8").read()
        sid = re.search(r"semantic_id:\s*(\S+)", md)
        tier = re.search(r"classification:.*", md)
        concepts.append((name, sid.group(1) if sid else "", tier.group(0) if tier else ""))
        body = md_to_html_body(md)
        with open(os.path.join(OUT_DIR, f"concept-{name}.html"), "w") as fh:
            fh.write(page(name.capitalize(), f"<h1>{name.capitalize()}</h1>\n{body}", ""))

    # Tutorials page (combined)
    tut = []
    for f in sorted(glob.glob(os.path.join(DOCS_DIR, "tutorials", "*.md"))):
        md = open(f, encoding="utf-8").read()
        tut.append(f"<hr>\n{md_to_html_body(md)}")
    with open(os.path.join(OUT_DIR, "tutorials.html"), "w") as fh:
        fh.write(page("WSF Tutorials", "<h1>WSF Tutorials</h1>\n" + "\n".join(tut), ""))

    # Principles page
    pp = os.path.join(DOCS_DIR, "conceptual", "FOUNDATIONAL-PRINCIPLES.md")
    if os.path.exists(pp):
        body = md_to_html_body(open(pp, encoding="utf-8").read())
        with open(os.path.join(OUT_DIR, "principles.html"), "w") as fh:
            fh.write(page("Foundational Principles", body, ""))

    # Index
    cards = "\n".join(
        f'<a class="card" href="concept-{n}.html"><strong>{n.capitalize()}</strong><br>'
        f"<small>{sid}</small><br><small>{cls}</small></a>"
        for n, sid, cls in concepts
    )
    index_body = f"""<h1>WSF Canonical Concept Reference</h1>
<p>The authoritative reference for the {len(concepts)} foundational, supporting, and specialisation concepts of the World Semantic Foundation.</p>
<p><a href="tutorials.html">Tutorials</a> : <a href="principles.html">Foundational Principles</a></p>
<h2>Concepts</h2>
{cards}
"""
    with open(os.path.join(OUT_DIR, "index.html"), "w") as fh:
        fh.write(page("WSF Concept Reference", index_body, ""))

    print(f"Site built at {OUT_DIR}: {len(concepts)} concept pages, tutorials, principles, index")


if __name__ == "__main__":
    build()
