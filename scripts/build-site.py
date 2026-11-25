#!/usr/bin/env python3
"""
WSF Reference Site Builder
==========================

Generates the World Semantic Foundation public reference site for
humans, AI agents, ontologists, and engineers.

Inputs (sibling repositories):
    ../wsf/                     canonical semantic assets (concepts, relationship registry)
    ../wsf-spec/                normative specs (vocabulary, JSON-LD context)

Output: ./_site

Pages:
    index.html              landing: what is WSF, audience paths, concept search
    concepts.html           searchable / filterable concept browser (client-side JS)
    concept-<name>.html    full concept page (Overview / Ontology / Machine tabs)
    relationships.html      relationship registry explorer
    ontology.html           interactive tier hierarchy tree
    agents.html             AI-agent guide (llms.txt, data endpoints, JSON-LD usage)
    getting-started.html    engineer onboarding (engine, specs, CI)
    tutorials.html          the three tutorials
    principles.html         the 12 foundational principles

Machine-readable artifacts:
    data/concepts.json      complete concept index
    data/relationships.json relationship registry
    data/context.jsonld     the WSF JSON-LD context (copied from wsf-spec)
    llms.txt / llms-full.txt  LLM agent entry points
    sitemap.xml / robots.txt
"""

import glob
import html
import json
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.normpath(os.path.join(HERE, ".."))
WSF_DIR = os.path.normpath(os.path.join(DOCS_DIR, "..", "wsf"))
SPEC_DIR = os.path.normpath(os.path.join(DOCS_DIR, "..", "wsf-spec"))
OUT_DIR = os.path.join(DOCS_DIR, "_site")

SITE = "https://world-semantic-foundation.github.io"

NAV = [
    ("index.html", "Home"),
    ("concepts.html", "Concepts"),
    ("relationships.html", "Relationships"),
    ("ontology.html", "Ontology"),
    ("getting-started.html", "Get Started"),
    ("agents.html", "For AI Agents"),
    ("tutorials.html", "Tutorials"),
    ("principles.html", "Principles"),
]


# ============================================================ data loading

def load_concepts():
    """Extract structured concept data from wsf/concepts/*.md."""
    try:
        import yaml
    except ImportError:
        yaml = None

    concepts = []
    for f in sorted(glob.glob(os.path.join(WSF_DIR, "concepts", "*.md"))):
        slug = os.path.basename(f)[:-3]
        text = open(f, encoding="utf-8").read()

        fields = {}
        yblock = re.search(r"```yaml\n(.*?)```", text, re.S)
        if yblock:
            if yaml:
                try:
                    fields = yaml.safe_load(yblock.group(1)) or {}
                    if not isinstance(fields, dict):
                        fields = {}
                except yaml.YAMLError:
                    fields = {}
            else:  # line parser fallback
                for line in yblock.group(1).splitlines():
                    m = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
                    if m:
                        fields[m.group(1)] = m.group(2).strip()
        aliases = fields.get("aliases") or []
        if isinstance(aliases, str):
            aliases = [a.strip() for a in aliases.strip("[]").split(",") if a.strip()]

        definition = None
        dm = re.search(r"## Definition\n\n(.+?)(?:\n\n|\n##)", text, re.S)
        if dm:
            definition = re.sub(r"[*`]", "", dm.group(1)).strip()
            definition = re.sub(r"\s+", " ", definition)
            if len(definition) > 240:
                definition = definition[:237].rstrip() + "..."

        classification = str(fields.get("classification", ""))
        tier = ("Tier 1" if "Tier 1" in classification or "Foundational" in classification
                else "Tier 2" if "Tier 2" in classification or "Supporting" in classification
                else ("Tier 3" if "Tier 3" in classification or "Derived" in classification
                      else "Tier 3"))

        concepts.append({
            "slug": slug,
            "semantic_id": fields.get("semantic_id", "wsf:" + slug.capitalize()),
            "preferred_name": fields.get("preferred_name") or slug.capitalize(),
            "aliases": [str(a) for a in aliases],
            "status": str(fields.get("status", "Baseline")),
            "version": str(fields.get("version", "0.1.0")),
            "classification": classification or tier,
            "tier": tier,
            "tier_key": tier.replace(" ", "").lower(),
            "domain": str(fields.get("domain", "")),
            "parent": str(fields.get("parent", "")),
            "defined_by": str(fields.get("defined_by", "")),
            "authority": str(fields.get("authority", "WSF")),
            "definition": definition or "",
            "url": f"concept-{slug}.html",
            "source": f"https://github.com/World-Semantic-Foundation/wsf/blob/main/concepts/{slug}.md",
        })
    return concepts


def load_relationships():
    """Load the relationship registry from wsf/relationships/."""
    path = os.path.join(WSF_DIR, "relationships", "foundational-relationships.yaml")
    if not os.path.exists(path):
        return {"relationships": []}
    try:
        import yaml
        with open(path) as fh:
            reg = yaml.safe_load(fh)
    except Exception:
        return {"relationships": []}
    rels = []
    for r in reg.get("relationships", []):
        rels.append({
            "semantic_id": r["semantic_id"],
            "preferred_name": r.get("preferred_name", r["semantic_id"].split(":")[-1]),
            "form": r.get("form", "").split(":")[-1],
            "family": r.get("family", "").split(":")[-1],
            "definition": r.get("definition", ""),
            "domain": r.get("domain", ""),
            "range": r.get("range", ""),
            "specialization_of": r.get("specialization_of", ""),
            "inverse": r.get("inverse", ""),
            "cardinality": r.get("cardinality", ""),
            "status": r.get("status", "Normative"),
        })
    return {"relationships": rels}


def build_hierarchy(concepts):
    """Map parent (wsf:X) -> children slugs."""
    by_id = {c["semantic_id"]: c for c in concepts}
    children = {}
    roots = []
    for c in concepts:
        parent_id = c["parent"]
        if parent_id and parent_id in by_id:
            children.setdefault(parent_id, []).append(c["semantic_id"])
        else:
            roots.append(c["semantic_id"])
    return by_id, children, roots


# ============================================================ markdown

def md_to_html_body(md_text):
    lines = md_text.split("\n")
    out, in_code, code_buf, in_list, in_table = [], False, [], False, False

    def flush_list():
        nonlocal in_list
        if in_list:
            out.append("</ul>")
            in_list = False

    for line in lines:
        if line.strip().startswith("```"):
            if in_code:
                out.append("<pre><code>" + html.escape("\n".join(code_buf)) + "</code></pre>")
                code_buf, in_code = [], False
            else:
                flush_list()
                in_code = True
            continue
        if in_code:
            code_buf.append(line)
            continue

        stripped = line.strip()
        # tables
        if stripped.startswith("|") and stripped.endswith("|"):
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            if all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
                continue
            if not in_table:
                out.append("<table>")
                in_table = True
                out.append("<tr>" + "".join(f"<th>{inline(c)}</th>" for c in cells) + "</tr>")
                continue
            out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in cells) + "</tr>")
            continue
        elif in_table:
            out.append("</table>")
            in_table = False

        if not stripped:
            flush_list()
            continue
        if stripped.startswith("#"):
            flush_list()
            level = min(len(stripped) - len(stripped.lstrip("#")), 6)
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
    if in_table:
        out.append("</table>")
    flush_list()
    if in_code and code_buf:
        out.append("<pre><code>" + html.escape("\n".join(code_buf)) + "</code></pre>")
    return "\n".join(out)


def inline(text):
    text = html.escape(text, quote=False)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1", text)
    return text


# ============================================================ page shell

def nav_html(active):
    items = "".join(
        f'<a href="{href}"{" aria-current=\"page\"" if href == active else ""} style="{"font-weight:700;text-decoration:underline" if href == active else ""}">{label}</a>'
        for href, label in NAV
    )
    return f'''
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="index.html"><img src="assets/logo.svg" alt="WSF logo"> World Semantic Foundation</a>
    <button id="nav-toggle" aria-label="Toggle navigation">&#9776;</button>
    <nav id="nav-menu">{items}</nav>
  </div>
</header>'''


def footer_html():
    return f'''
<footer class="site-footer">
  <div class="wrap cols">
    <div>
      <h4>WSF</h4>
      <ul>
        <li><a href="index.html">Home</a></li>
        <li><a href="principles.html">Foundational Principles</a></li>
        <li><a href="tutorials.html">Tutorials</a></li>
      </ul>
    </div>
    <div>
      <h4>Reference</h4>
      <ul>
        <li><a href="concepts.html">Concept Browser</a></li>
        <li><a href="relationships.html">Relationship Registry</a></li>
        <li><a href="ontology.html">Tier Hierarchy</a></li>
      </ul>
    </div>
    <div>
      <h4>Build With WSF</h4>
      <ul>
        <li><a href="getting-started.html">Getting Started</a></li>
        <li><a href="agents.html">For AI Agents</a></li>
        <li><a href="data/context.jsonld">JSON-LD Context</a></li>
        <li><a href="llms.txt">llms.txt</a></li>
      </ul>
    </div>
    <div>
      <h4>Source</h4>
      <ul>
        <li><a href="https://github.com/World-Semantic-Foundation/wsf">wsf (canonical)</a></li>
        <li><a href="https://github.com/World-Semantic-Foundation/wsf-spec">wsf-spec (specs)</a></li>
        <li><a href="https://github.com/World-Semantic-Foundation/wsf-software">wsf-software (engine)</a></li>
        <li><a href="https://github.com/World-Semantic-Foundation/wsf-governance">wsf-governance (ADRs)</a></li>
      </ul>
    </div>
  </div>
  <div class="wrap" style="margin-top:1.6rem;font-size:0.8rem">
    &copy; World Semantic Foundation. Generated from the canonical <code>wsf</code> and <code>wsf-spec</code> repositories.
  </div>
</footer>'''


def page(active, title, description, body, extra_head="", jsonld=None, well_known=False):
    structured = ""
    if jsonld:
        structured = (
            '<script type="application/ld+json">'
            + json.dumps(jsonld, ensure_ascii=False).replace("</", "</")
            + "</script>"
        )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
<link rel="stylesheet" href="assets/style.css">
{structured}
{extra_head}
</head>
<body>
{nav_html(active)}
<main class="wrap">
{body}
</main>
{'' if well_known else footer_html()}
</body>
</html>"""


# ============================================================ pages

def tier_badge(c):
    return f'<span class="tier-badge tier-{c["tier_key"]}">{c["tier"]}</span>'


def index_page(concepts, rels):
    t1 = [c for c in concepts if c["tier_key"] == "tier1"]
    t2 = [c for c in concepts if c["tier_key"] == "tier2"]
    t3 = [c for c in concepts if c["tier_key"] == "tier3"]
    body = f'''
<div class="hero">
  <div class="wrap">
    <p class="kicker">The World Semantic Foundation</p>
    <h1>A governed vocabulary for meaning that machines and humans share.</h1>
    <p class="lead">WSF defines {len(concepts)} foundational concepts, {len(rels)} governed relationships, and the assertion, identity, and provenance models needed to make semantic claims precise, validatable, and portable across systems.</p>
    <div class="hero-search">
      <input id="hero-search" type="search" placeholder="Find a concept: capability, policy, disposition, provenance ..." aria-label="Search concepts">
      <div id="hero-results" hidden></div>
    </div>
    <p style="margin-top:1rem"><a class="btn" href="getting-started.html">Get started</a><a class="btn ghost" href="agents.html">For AI agents</a></p>
    <div class="hero-stats">
      <div class="hero-stat"><b>{len(concepts)}</b><span>governed concepts</span></div>
      <div class="hero-stat"><b>{len(rels)}</b><span>relationship types</span></div>
      <div class="hero-stat"><b>3</b><span>semantic tiers</span></div>
      <div class="hero-stat"><b>7</b><span>namespaces</span></div>
    </div>
  </div>
</div>

<div class="wrap" style="margin-top:2.5rem">
  <h2>Built for every kind of reader</h2>
  <div class="grid cols-4">
    <div class="card"><span class="icon">&#128100;</span><h3>For people</h3><p class="muted">Plain-language concept definitions with canonical examples. Start with the tutorials and browse the concept cards.</p><a href="concepts.html">Browse concepts &rarr;</a></div>
    <div class="card"><span class="icon">&#129302;</span><h3>For AI agents</h3><p class="muted">Structured entry points: llms.txt, JSON data endpoints, and the WSF JSON-LD context for grounding your semantic model.</p><a href="agents.html">Agent guide &rarr;</a></div>
    <div class="card"><span class="icon">&#128300;</span><h3>For ontologists</h3><p class="muted">Governed metadata for every concept: identity, parent, tier, status, provenance, plus the full relationship registry and hierarchy.</p><a href="ontology.html">Explore the ontology &rarr;</a></div>
    <div class="card"><span class="icon">&#128295;</span><h3>For engineers</h3><p class="muted">A deployable Semantic Engine with a REST API, SHACL validation, and pluggable storage. Quickstart in five commands.</p><a href="getting-started.html">Build with the engine &rarr;</a></div>
  </div>
</div>

<div class="wrap">
  <h2>The WSF canon at a glance</h2>
  <div class="grid cols-3">
    <div class="card"><h3>Tier 1: Foundational <span class="muted">({len(t1)})</span></h3><p class="muted">Existence, meaning, assertion, identity, context, time, and space: the concepts everything else inherits from.</p><a href="concepts.html">View Tier 1 &rarr;</a></div>
    <div class="card"><h3>Tier 2: Supporting <span class="muted">({len(t2)})</span></h3><p class="muted">Representation and epistemics: identifier, reference, namespace, term, definition, validity, evidence, provenance, authority.</p><a href="concepts.html">View Tier 2 &rarr;</a></div>
    <div class="card"><h3>Tier 3: Specialisation <span class="muted">({len(t3)})</span></h3><p class="muted">Enterprise-ready constructs: role, process, function, goal, policy, measure, actor, service, organisation, and more.</p><a href="concepts.html">View Tier 3 &rarr;</a></div>
  </div>
  <h2>Governance done in the open</h2>
  <p>Every concept, relationship, and model decision in WSF is governed through Architecture Decision Records and Change Requests, with identity, status, provenance, and version recorded for each artifact. The <a href="https://github.com/World-Semantic-Foundation/wsf-governance">full governance record</a> is public.</p>
</div>'''
    return page("index.html", "World Semantic Foundation",
                "A governed vocabulary of 38 concepts and 29 relationships for precise, validatable, portable semantic claims.",
                body, jsonld={"@context": "https://schema.org", "@type": "WebSite",
                              "name": "World Semantic Foundation", "url": SITE + "/index.html"})


def concepts_page(concepts):
    cards = "\n".join(
        f'<a class="concept-card" href="{c["url"]}">'
        f'<div class="concept-card-head"><span class="concept-name">{html.escape(c["preferred_name"])}</span>{tier_badge(c)}</div>'
        f'<p class="concept-card-def">{html.escape(c["definition"])}</p>'
        f'<code class="concept-card-id">{c["semantic_id"]}</code></a>'
        for c in concepts
    )
    body = f'''
<h1>Concept Browser</h1>
<p class="muted">All {len(concepts)} governed WSF concepts. Search by name, semantic id, alias, or definition; filter by tier.</p>
<div class="filter-bar search-row">
  <input type="search" id="search-box" placeholder="Search concepts ..." aria-label="Search concepts">
  <button class="tier-filter-btn active" data-tier="all">All</button>
  <button class="tier-filter-btn" data-tier="tier1">Tier 1</button>
  <button class="tier-filter-btn" data-tier="tier2">Tier 2</button>
  <button class="tier-filter-btn" data-tier="tier3">Tier 3</button>
</div>
<p class="muted" id="search-count">{len(concepts)} concepts</p>
<div id="concept-list">
{cards}
</div>'''
    return page("concepts.html", "Concept Browser : WSF",
                "Browse and search all WSF foundational, supporting, and specialisation concepts.",
                body, jsonld={"@context": "https://schema.org", "@type": "CollectionPage",
                              "name": "WSF Concept Browser"})


def concept_page(c, concepts, rels, by_id, children):
    parent = by_id.get(c["parent"])
    kids = [by_id[k] for k in children.get(c["semantic_id"], [])]

    relations_html = ""
    if rels:
        rel_rows = "\n".join(
            f"<tr><td><code>{r['semantic_id']}</code></td>"
            f"<td>{html.escape(r['definition'])}</td>"
            f"<td><code>{html.escape(r['domain'])}</code></td>"
            f"<td><code>{html.escape(r['range'])}</code></td></tr>"
            for r in rels
            if r["domain"] == c["semantic_id"] or r["range"] == c["semantic_id"]
        )
        if rel_rows:
            relations_html = f"<h3>Relationships involving this concept</h3><table><tr><th>Relationship</th><th>Definition</th><th>Domain</th><th>Range</th></tr>{rel_rows}</table>"

    source_path = os.path.join(WSF_DIR, "concepts", c["slug"] + ".md")
    md_text = open(source_path, encoding="utf-8").read()

    # split the markdown body into overview-ish and example sections for tabs
    parts = {"overview": [], "example": [], "rest": []}
    current = "overview"
    open_code = False
    for line in md_text.split("\n"):
        if line.strip().startswith("```"):
            open_code = not open_code
        if not open_code:
            if re.match(r"^#+\s*(Canonical Example|Example)\b", line):
                current = "example"
            elif line.startswith("## ") and current == "example":
                current = "rest"
        parts[current].append(line)

    overview_html = md_to_html_body("\n".join(
        l for l in parts["overview"] if not l.startswith("# ") and not l.startswith("> **")))
    example_html = md_to_html_body("\n".join(parts["example"]))
    rest_html = md_to_html_body("\n".join(parts["rest"]))

    meta_rows = "\n".join(f"<tr><th>{k}</th><td>{html.escape(str(v))}</td></tr>"
                         for k, v in [("Semantic ID", c["semantic_id"]),
                                      ("Preferred name", c["preferred_name"]),
                                      ("Aliases", ", ".join(c["aliases"]) or "none"),
                                      ("Tier", c["tier"]),
                                      ("Classification", c["classification"]),
                                      ("Parent", c["parent"] or "none (root)"),
                                      ("Status", c["status"]),
                                      ("Version", c["version"]),
                                      ("Domain", c["domain"]),
                                      ("Defined by", c["defined_by"] or "see source"),
                                      ("Authority", c["authority"])])

    hierarchy_bits = []
    if parent:
        hierarchy_bits.append(f'<p>Parent: <a href="{parent["url"]}">{parent["preferred_name"]}</a> (<code>{parent["semantic_id"]}</code>)</p>')
    else:
        hierarchy_bits.append("<p>Parent: <span class='muted'>none (root concept)</span></p>")
    if kids:
        kid_links = ", ".join(f'<a href="{k["url"]}">{k["preferred_name"]}</a>' for k in kids)
        hierarchy_bits.append(f"<p>Specialised by: {kid_links}</p>")

    concept_json = {k: c[k] for k in ("semantic_id", "preferred_name", "aliases", "tier",
                                      "classification", "parent", "status", "version",
                                      "domain", "definition", "source")}
    example_ld = json.dumps({
        "@context": "https://world-semantic-foundation.org/ns/jsonld",
        "@id": c["semantic_id"],
        "@type": "Concept",
        "preferred_name": c["preferred_name"],
        "tier": c["tier"],
        "status": c["status"],
    }, indent=2)
    ld_escaped = html.escape(example_ld)
    json_escaped = html.escape(json.dumps(concept_json, indent=2))
    machine_html = f"""
<h3>Concept record (JSON)</h3>
<pre><code id="c-json">{json_escaped}</code></pre><button class="copy-btn" data-copy-target="#c-json">Copy JSON</button>
<h3>Fetch from the Semantic Engine</h3>
<pre><code id="c-curl">curl http://localhost:8080/v1/concepts/{c['semantic_id']}</code></pre><button class="copy-btn" data-copy-target="#c-curl">Copy command</button>
<h3>JSON-LD example</h3>
<pre><code id="c-ld">{ld_escaped}</code></pre><button class="copy-btn" data-copy-target="#c-ld">Copy JSON-LD</button>
<p class="muted">Source of truth: <a href="{c['source']}">{c['slug']}.md</a> in the canonical wsf repository.</p>
"""

    body = f'''
<div class="concept-hero">
  <h1>{html.escape(c["preferred_name"])}</h1>
  {tier_badge(c)}
  <span class="chip">{c["status"]}</span>
  <span class="chip">v{c["version"]}</span>
</div>
<p><code>{c["semantic_id"]}</code></p>

<div class="tab-group">
  <div class="tabs" role="tablist">
    <button class="tab-btn active" id="tab-overview" data-tab-target="panel-overview" role="tab" aria-selected="true">Overview</button>
    <button class="tab-btn" id="tab-ontologist" data-tab-target="panel-ontologist" role="tab" aria-selected="false">Ontology</button>
    <button class="tab-btn" id="tab-machine" data-tab-target="panel-machine" role="tab" aria-selected="false">Machine-readable</button>
    <button class="tab-btn" id="tab-example" data-tab-target="panel-example" role="tab" aria-selected="false">Canonical example</button>
  </div>
  <div class="tab-panel" id="panel-overview">
    {overview_html}
    {rest_html if not example_html else ""}
  </div>
  <div class="tab-panel" id="panel-ontologist" hidden>
    <h3>Metadata</h3>
    <table class="meta-table">{meta_rows}</table>
    <h3>Hierarchy</h3>
    {"".join(hierarchy_bits)}
    {relations_html}
    <p><a href="ontology.html">View the full hierarchy &rarr;</a></p>
  </div>
  <div class="tab-panel" id="panel-machine" hidden>
    {machine_html}
  </div>
  <div class="tab-panel" id="panel-example" hidden>
    {example_html or "<p class='muted'>No canonical example in the source file.</p>"}
  </div>
</div>'''
    return page(c["url"], f"{c['preferred_name']} : WSF Concept",
                c["definition"][:150] if c["definition"] else f"WSF concept {c['semantic_id']}",
                body,
                jsonld={"@context": SITE + "/data/context.jsonld",
                        "@id": c["semantic_id"], "@type": "Concept",
                        "preferred_name": c["preferred_name"], "tier": c["tier"],
                        "status": c["status"], "version": c["version"],
                        "definition": c["definition"]})


def relationships_page(rels):
    rows = "\n".join(
        f"<tr><td><code>{r['semantic_id']}</code></td>"
        f"<td>{html.escape(r['preferred_name'])}</td>"
        f"<td><span class='chip'>{r['form']}</span></td>"
        f"<td><span class='chip'>{r['family']}</span></td>"
        f"<td>{html.escape(r['definition'])}</td>"
        f"<td><code>{html.escape(r['domain'])}</code></td>"
        f"<td><code>{html.escape(r['range'])}</code></td></tr>"
        for r in rels
    )
    body = f'''
<h1>Relationship Registry</h1>
<p class="muted">The {len(rels)} governed relationship types of WSF, per ADR-WSF-19. Every relationship has a stable identity, a specified domain and range, explicit mathematical properties, and a defined family and form. Registry data is available as JSON at <a href="data/relationships.json">data/relationships.json</a>.</p>
<table>
<tr><th>Semantic ID</th><th>Name</th><th>Form</th><th>Family</th><th>Definition</th><th>Domain</th><th>Range</th></tr>
{rows}
</table>
<h2>The Four Forms of Relation</h2>
<div class="grid cols-4">
  <div class="card"><h3>Structural</h3><p class="muted">Composition, containment, classification, specialization.</p></div>
  <div class="card"><h3>Temporal</h3><p class="muted">Order and duration in time. Precedence is not causality.</p></div>
  <div class="card"><h3>Causal</h3><p class="muted">Cause, trigger, contribution. Carries causal commitment.</p></div>
  <div class="card"><h3>Dispositional</h3><p class="muted">Possession, participation, realization, enablement: potentials.</p></div>
</div>'''
    return page("relationships.html", "Relationship Registry : WSF",
                "Governed semantic relationships: forms, families, domains, and ranges.",
                body, jsonld={"@context": "https://schema.org", "@type": "CollectionPage",
                              "name": "WSF Relationship Registry"})


def ontology_page(concepts, by_id, children, roots):
    def node(cid, depth=0):
        c = by_id[cid]
        kids = children.get(cid, [])
        if not kids:
            return (f'<li><div class="node"><a href="{c["url"]}">{c["preferred_name"]}</a>'
                    f'{tier_badge(c)}</div></li>')
        tid = "tree-" + cid.replace(":", "-")
        return (f'<li><div class="node"><button class="tree-toggle" data-tree-target="{tid}" '
                f'aria-label="Expand">{c["preferred_name"].__len__() and "+"}</button>'
                f'<a href="{c["url"]}">{c["preferred_name"]}</a>{tier_badge(c)}</div>'
                f'<ul class="tree-children" id="{tid}">'
                + "".join(node(k, depth + 1) for k in kids) + "</ul></li>")

    tree_html = "<ul class='tree'>" + "".join(node(r) for r in sorted(roots)) + "</ul>"
    body = f'''
<h1>Tier Hierarchy</h1>
<p class="muted">The WSF concept inheritance tree. Concepts specialise their parent and inherit its semantics (per semantic inheritance). Click a node name to open its page; toggle to expand. Tier 1 concepts are the roots of meaning.</p>
{tree_html}
<h2>Tier definitions</h2>
<table>
<tr><th>Tier</th><th>Role</th><th>Examples</th></tr>
<tr><td><b>Tier 1 : Foundational</b></td><td>Roots of meaning: what exists, what is claimed, how identity works</td><td>Entity, Concept, Assertion, Identity, Context, Time, Space</td></tr>
<tr><td><b>Tier 2 : Supporting</b></td><td>Representation and epistemic machinery</td><td>Identifier, Reference, Namespace, Definition, Evidence, Authority</td></tr>
<tr><td><b>Tier 3 : Specialisation</b></td><td>Domain-ready constructs grounded in Tier 1 and 2</td><td>Capability, Process, Goal, Policy, Measure, Organisation, Actor</td></tr>
</table>'''
    return page("ontology.html", "Tier Hierarchy : WSF",
                "Interactive hierarchy of all WSF concepts across the three semantic tiers.",
                body, jsonld={"@context": "https://schema.org", "@type": "ItemList",
                              "name": "WSF Tier Hierarchy"})


def agents_page(concepts, rels):
    concept_names = ", ".join(c["semantic_id"] for c in concepts)
    pattern_snippet = html.escape(json.dumps({
        "@context": "https://world-semantic-foundation.org/ns/jsonld",
        "@type": "Concept",
        "@id": "wsf:Capability",
        "preferred_name": "Capability",
        "tier": "Tier 3",
        "status": "Baseline",
        "definition": "A stable, reusable potential of an entity to produce an outcome",
    }, indent=2))
    assertion_snippet = html.escape(json.dumps({
        "semantic_id": "wsf-assertion:example-001",
        "subject": "wsf-ex:OTCHERE-Inc",
        "relationship": "wsf-rel:possesses",
        "object": "wsf-ex:OrderManagementCapability",
        "context": "wsf-ctx:enterprise-architecture",
        "provenance": {"asserted_by": "wsf-ex:Kwesi", "asserted_at": "2026-08-29"},
        "status": "Active",
    }, indent=2))
    body = f'''
<h1>WSF for AI Agents</h1>
<p class="muted">This site is designed to be usable by autonomous agents: every artifact has a stable URL, structured metadata, and a machine-readable twin. Use the entry points below to ground your semantic reasoning in the WSF canon.</p>

<h2>Primary entry points</h2>
<div class="grid cols-3">
  <div class="card"><h3><a href="llms.txt">llms.txt</a></h3><p class="muted">Curated index of the site for LLM agents, following the llms.txt convention. Start here.</p></div>
  <div class="card"><h3><a href="llms-full.txt">llms-full.txt</a></h3><p class="muted">The complete corpus in one markdown document for ingestion.</p></div>
  <div class="card"><h3><a href="data/concepts.json">data/concepts.json</a></h3><p class="muted">Structured index of all {len(concepts)} concepts: ids, definitions, tiers, parents, statuses.</p></div>
</div>
<div class="grid cols-3" style="margin-top:1.2rem">
  <div class="card"><h3><a href="data/relationships.json">data/relationships.json</a></h3><p class="muted">The governed relationship registry with domains, ranges, and properties.</p></div>
  <div class="card"><h3><a href="data/context.jsonld">data/context.jsonld</a></h3><p class="muted">The WSF JSON-LD context: canonical IRI mappings for all namespaces, concepts, and relationships.</p></div>
  <div class="card"><h3><a href="sitemap.xml">sitemap.xml</a></h3><p class="muted">Machine-readable site map.</p></div>
</div>

<h2>How to represent a WSF concept</h2>
<p>Every concept page carries JSON-LD structured data with <code>@context</code> pointing at the WSF context document. The minimal pattern:</p>
<pre><code id="a-pattern">{pattern_snippet}</code></pre><button class="copy-btn" data-copy-target="#a-pattern">Copy</button>

<h2>Semantic assertions in WSF form</h2>
<p>To make claims validatable, use the assertion pattern (Subject, Relationship, Object + Context, Time, Evidence, Provenance). The governed relationship vocabulary is limited to the registry; do not invent relationship types:</p>
<pre><code id="a-assertion">{assertion_snippet}</code></pre><button class="copy-btn" data-copy-target="#a-assertion">Copy</button>

<h2>The governed vocabulary</h2>
<p class="muted">Valid concept identities:</p>
<p><code>{html.escape(concept_names)}</code></p>

<h2>Rules agents should respect</h2>
<ul>
<li><b>Identity is not name.</b> Reference concepts by their semantic id (<code>wsf:Capability</code>), never by label alone; labels and aliases vary.</li>
<li><b>Relationships are governed.</b> Only use relationship types from <a href="data/relationships.json">the registry</a>, with matching domain and range.</li>
<li><b>Assertions are not truth.</b> A WSF assertion is a claim with provenance; always carry the provenance and status fields.</li>
<li><b>Status matters.</b> Concepts move through Candidate, Investigating, Proposed, Normative, Deprecated, Retired. Check <code>status</code> before relying on a concept.</li>
<li><b>Specialization preserves semantics.</b> A specialised concept inherits its parent's meaning contract.</li>
</ul>

<h2>Engine API</h2>
<p>The Semantic Engine exposes a REST surface; see <a href="https://github.com/World-Semantic-Foundation/wsf-spec/blob/main/openapi/wsf-semantic-engine.openapi.yaml">the OpenAPI 3.1 specification</a> for the normative contract (concepts, assertions, relationships, validation, namespaces, resolution, inference, audit).</p>
'''
    return page("agents.html", "WSF for AI Agents",
                "Machine-readable entry points for agents using the WSF canon: llms.txt, JSON endpoints, JSON-LD context.",
                body, jsonld={"@context": "https://schema.org", "@type": "WebPage",
                              "name": "WSF for AI Agents",
                              "audience": {"@type": "Audience", "audienceType": "AI agents"}})


def getting_started_page(concepts):
    body = '''
<h1>Get Started</h1>
<p class="muted">Five ways in, depending on who you are and what you are building.</p>

<div class="tab-group">
  <div class="tabs" role="tablist">
    <button class="tab-btn active" id="tab-quickstart" data-tab-target="panel-quickstart" role="tab" aria-selected="true">Run the engine</button>
    <button class="tab-btn" id="tab-derive" data-tab-target="panel-derive" role="tab" aria-selected="false">Use the specs</button>
    <button class="tab-btn" id="tab-learn" data-tab-target="panel-learn" role="tab" aria-selected="false">Learn the model</button>
  </div>

  <div class="tab-panel" id="panel-quickstart">
    <h3>WSF Semantic Engine quickstart</h3>
    <p>The <a href="https://github.com/World-Semantic-Foundation/wsf-software">Semantic Engine</a> operationalises the full vocabulary with pluggable storage (in-memory, PostgreSQL, Neo4j, MongoDB, SQLite) and SHACL validation.</p>
    <pre><code id="g-quick">git clone https://github.com/World-Semantic-Foundation/wsf-software
cd wsf-software
npm install
npm test        # 112 tests
npm run build && node dist/server/main.js</code></pre><button class="copy-btn" data-copy-target="#g-quick">Copy</button>
    <p>Then talk to it:</p>
    <pre><code id="g-curl">curl http://localhost:8080/v1/health
curl -X POST http://localhost:8080/v1/concepts -H 'Content-Type: application/json' \\
  -d '{"semantic_id": "wsf:Capability", "preferred_name": "Capability", "tier": "Tier 3"}'</code></pre><button class="copy-btn" data-copy-target="#g-curl">Copy</button>
  </div>

  <div class="tab-panel" id="panel-derive" hidden>
    <h3>Build against the normative specs</h3>
    <p>The single source of truth for any WSF-compatible implementation is <a href="https://github.com/World-Semantic-Foundation/wsf-spec">wsf-spec</a>:</p>
    <table>
      <tr><th>Artifact</th><th>Use</th></tr>
      <tr><td><code>turtle/wsf-vocabulary.ttl</code></td><td>The canonical vocabulary (RDF/Turtle)</td></tr>
      <tr><td><code>shacl/wsf-shapes.ttl</code></td><td>SHACL shapes for conformance validation</td></tr>
      <tr><td><code>jsonld/wsf-context.jsonld</code></td><td>JSON-LD context for JSON APIs</td></tr>
      <tr><td><code>openapi/wsf-semantic-engine.openapi.yaml</code></td><td>REST API contract</td></tr>
      <tr><td><code>protobuf/wsf-semantic-engine.proto</code></td><td>gRPC service definitions</td></tr>
    </table>
    <p>Contract changes flow only through <a href="https://github.com/World-Semantic-Foundation/wsf-governance">ADRs and CRs</a>; if your implementation conforms, file issues early.</p>
  </div>

  <div class="tab-panel" id="panel-learn" hidden>
    <h3>Learn the model</h3>
    <ol>
      <li>Read the <a href="principles.html">12 Foundational Principles</a>.</li>
      <li>Take the three <a href="tutorials.html">tutorials</a> (Tier 1, Tier 2, Tier 3).</li>
      <li>Browse the <a href="concepts.html">concept browser</a> and the <a href="ontology.html">hierarchy</a>.</li>
      <li>Study the <a href="relationships.html">relationship registry</a>: what connects to what, and how.</li>
      <li>Read the <a href="agents.html">machine-readable guide</a> if you are integrating an automated consumer.</li>
    </ol>
  </div>
</div>

<h2>Ecosystem map</h2>
<table>
<tr><th>Repository</th><th>Role</th></tr>
<tr><td><a href="https://github.com/World-Semantic-Foundation/wsf">wsf</a></td><td>Canonical semantic assets: concepts, relationships, identity, assertions, context, temporal, spatial, provenance modules</td></tr>
<tr><td><a href="https://github.com/World-Semantic-Foundation/wsf-spec">wsf-spec</a></td><td>Normative machine-readable specifications: Turtle, SHACL, OpenAPI, Protobuf, JSON-LD</td></tr>
<tr><td><a href="https://github.com/World-Semantic-Foundation/wsf-software">wsf-software</a></td><td>The deployable Semantic Engine</td></tr>
<tr><td><a href="https://github.com/World-Semantic-Foundation/wsf-connectors">wsf-connectors</a></td><td>Federation adapters: OpenDEA, Schema.org, SKOS, TM Forum</td></tr>
<tr><td><a href="https://github.com/World-Semantic-Foundation/wsf-governance">wsf-governance</a></td><td>ADRs, CRs, lifecycle, and the investigation record</td></tr>
<tr><td><a href="https://github.com/World-Semantic-Foundation/wsf-examples">wsf-examples</a></td><td>Worked examples per concept (Enterprise: OTCHERE Inc)</td></tr>
<tr><td><a href="https://github.com/World-Semantic-Foundation/wsf-ecosystem">wsf-ecosystem</a></td><td>Concept map, research notes, proposals</td></tr>
<tr><td><a href="https://github.com/World-Semantic-Foundation/wsf-test-probe">wsf-test-probe</a></td><td>Cross-repo conformance probe (runs daily)</td></tr>
</table>
'''
    return page("getting-started.html", "Get Started : WSF",
                "Run the Semantic Engine, build against the normative specs, or learn the WSF model.",
                body, jsonld={"@context": "https://schema.org", "@type": "HowTo", "name": "Getting started with WSF"})


def tutorials_page():
    parts = []
    titles = []
    for f in sorted(glob.glob(os.path.join(DOCS_DIR, "tutorials", "*.md"))):
        md = open(f, encoding="utf-8").read()
        m = re.match(r"#\s*(.+)", md)
        titles.append(m.group(1).strip() if m else os.path.basename(f))
        parts.append(f"<hr>\n{md_to_html_body(md)}")
    body = "<h1>WSF Tutorials</h1><p class='muted'>" + ". ".join(t[:30] for t in titles) + "</p>\n" + "\n".join(parts)
    return page("tutorials.html", "Tutorials : WSF", "Learn WSF tier by tier: foundations, supporting constructs, specialisations.",
                body, jsonld={"@context": "https://schema.org", "@type": "CollectionPage", "name": "WSF Tutorials"})


def principles_page():
    pp = os.path.join(DOCS_DIR, "conceptual", "FOUNDATIONAL-PRINCIPLES.md")
    body = ""
    if os.path.exists(pp):
        body = md_to_html_body(open(pp, encoding="utf-8").read())
    return page("principles.html", "Foundational Principles : WSF",
                "The 12 foundational principles of the World Semantic Foundation.", body,
                jsonld={"@context": "https://schema.org", "@type": "WebPage", "name": "WSF Foundational Principles"})


# ============================================================ machine artifacts

def build_llms(concepts, rels):
    lines = [
        "# World Semantic Foundation",
        "",
        "> A governed vocabulary and semantic foundation for precise, validatable, portable semantic claims. "
        f"{len(concepts)} concepts across 3 tiers, {len(rels)} governed relationship types, ADR-based governance.",
        "",
        "## Docs",
        "- [Concept Browser](concepts.html): all governed concepts, searchable",
        "- [Relationship Registry](relationships.html): the governed relationship vocabulary",
        "- [Tier Hierarchy](ontology.html): the concept inheritance tree",
        "- [Getting Started](getting-started.html): engine quickstart, specs, learning path",
        "- [For AI Agents](agents.html): machine-readable entry points and usage rules",
        "- [Tutorials](tutorials.html): tier-by-tier walkthroughs",
        "- [Foundational Principles](principles.html): the 12 principles",
        "",
        "## Data",
        "- [concepts.json](data/concepts.json): complete structured concept index",
        "- [relationships.json](data/relationships.json): relationship registry",
        "- [context.jsonld](data/context.jsonld): WSF JSON-LD context (canonical IRI mappings)",
        "",
        "## Concepts",
    ]
    for c in concepts:
        lines.append(f"- [{c['preferred_name']}]({c['url']}): {c['definition']}")
    lines += ["", "## Relationships", ""]
    for r in rels:
        lines.append(f"- {r['semantic_id']}: {r['definition']} ({r['domain']} -> {r['range']})")

    llms = "\n".join(lines) + "\n"

    # full corpus: append entire source markdown files
    full = [llms, "\n---\n"]
    for f in sorted(glob.glob(os.path.join(WSF_DIR, "concepts", "*.md"))):
        full.append(f"\n<!-- {os.path.basename(f)} (source: wsf) -->\n\n")
        full.append(open(f, encoding="utf-8").read())
    for f in sorted(glob.glob(os.path.join(DOCS_DIR, "tutorials", "*.md"))):
        full.append(f"\n<!-- {os.path.basename(f)} (source: wsf-docs) -->\n\n")
        full.append(f'\n1. ' and open(f, encoding="utf-8").read())
    if os.path.exists(os.path.join(DOCS_DIR, "conceptual", "FOUNDATIONAL-PRINCIPLES.md")):
        full.append(open(os.path.join(DOCS_DIR, "conceptual", "FOUNDATIONAL-PRINCIPLES.md"), encoding="utf-8").read())
    return llms, "\n".join(full)


def build_sitemap(pages):
    urls = "\n".join(f"  <url><loc>{SITE}/{p}</loc></url>" for p in sorted(pages))
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n'


# ============================================================ main

def main():
    if not os.path.isdir(WSF_DIR):
        print(f"FATAL: sibling repository not found at {WSF_DIR}")
        sys.exit(2)
    if os.path.isdir(OUT_DIR):
        shutil.rmtree(OUT_DIR)
    os.makedirs(OUT_DIR)

    concepts = load_concepts()
    rels = load_relationships()["relationships"]
    by_id, children, roots = build_hierarchy(concepts)

    pages = {}

    pages["index.html"] = index_page(concepts, rels)
    pages["concepts.html"] = concepts_page(concepts)
    pages["relationships.html"] = relationships_page(rels)
    pages["ontology.html"] = ontology_page(concepts, by_id, children, roots)
    pages["agents.html"] = agents_page(concepts, rels)
    pages["getting-started.html"] = getting_started_page(concepts)
    pages["tutorials.html"] = tutorials_page()
    pages["principles.html"] = principles_page()
    for c in concepts:
        pages[c["url"]] = concept_page(c, concepts, rels, by_id, children)

    for name, content in pages.items():
        with open(os.path.join(OUT_DIR, name), "w") as fh:
            fh.write(content)

    # data artifacts
    os.makedirs(os.path.join(OUT_DIR, "data"))
    with open(os.path.join(OUT_DIR, "data", "concepts.json"), "w") as fh:
        json.dump({"concepts": concepts}, fh, indent=2)
    with open(os.path.join(OUT_DIR, "data", "relationships.json"), "w") as fh:
        json.dump({"relationships": rels}, fh, indent=2)
    context_src = os.path.join(SPEC_DIR, "jsonld", "wsf-context.jsonld")
    if os.path.exists(context_src):
        shutil.copy(context_src, os.path.join(OUT_DIR, "data", "context.jsonld"))

    # llms.txt
    llms, llms_full = build_llms(concepts, rels)
    open(os.path.join(OUT_DIR, "llms.txt"), "w").write(llms)
    open(os.path.join(OUT_DIR, "llms-full.txt"), "w").write(llms_full)

    # robots + sitemap
    open(os.path.join(OUT_DIR, "robots.txt"), "w").write(
        "User-agent: *\nAllow: /\nSitemap: " + SITE + "/sitemap.xml\n")
    open(os.path.join(OUT_DIR, "sitemap.xml"), "w").write(build_sitemap(pages.keys()))

    # assets
    assets_src = os.path.join(HERE, "site-assets")
    assets_dst = os.path.join(OUT_DIR, "assets")
    shutil.copytree(assets_src, assets_dst)

    n_concept_pages = len(concepts)
    print(f"Site built at {OUT_DIR}")
    print(f"  pages: {len(pages)} ({n_concept_pages} concept pages + {len(pages) - n_concept_pages} section pages)")
    print(f"  data: concepts.json, relationships.json, context.jsonld, llms.txt, llms-full.txt, sitemap.xml, robots.txt")


if __name__ == "__main__":
    main()
