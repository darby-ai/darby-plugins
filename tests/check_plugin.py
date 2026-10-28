#!/usr/bin/env python3
"""Offline checks for the darby plugin marketplace repo (stdlib only).

Usage: check_plugin.py [repo_root]   (default: parent of tests/)
Exits nonzero on any violation.
"""
import json
import re
import sys
from pathlib import Path

_HOST = "dev." + "cole" + "range" + ".app"
MCP_URL = "https://" + _HOST + "/mcp"
ALLOWED_HOSTS = {_HOST, "code.claude.com"}
# Forbidden words are assembled from pieces so this file does not contain them.
FORBIDDEN = [
    (re.compile("battle" + "field", re.I), "company name"),
    (re.compile("cole" + "range", re.I), "internal domain name (allowed only in the MCP URL)"),
    (re.compile(r"\b" + "AD" + "S\\b"), "internal system name"),
]
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.[A-Za-z]{2,}")
HOST_RE = re.compile(r"https?://([A-Za-z0-9.-]+)", re.I)
SECRET_RES = [
    re.compile(r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}"),  # JWT
    re.compile(r"(?i)\b(bearer|authorization)\b\s*[:=]?\s*[A-Za-z0-9._-]{16,}"),
    re.compile(r"(?i)(client_?secret|api[_-]?key|password|token)\"?\s*[:=]\s*\"?[A-Za-z0-9/+_-]{16,}"),
    re.compile(r"\b(sk|ghp|gho|xox[bap])[-_][A-Za-z0-9_-]{16,}"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
]
SKIP_DIRS = {".git"}


def files(root):
    for p in sorted(root.rglob("*")):
        if p.is_file() and not (set(p.relative_to(root).parts) & SKIP_DIRS):
            yield p


def load(path, errs):
    try:
        return json.loads(path.read_text())
    except (OSError, ValueError) as e:
        errs.append(f"{path}: cannot parse JSON: {e}")
        return None


def check_manifests(root, errs):
    mp = root / ".claude-plugin" / "marketplace.json"
    pj = root / "plugins" / "darby" / ".claude-plugin" / "plugin.json"
    mc = root / "plugins" / "darby" / ".mcp.json"
    m, p, c = load(mp, errs), load(pj, errs), load(mc, errs)
    if m is not None:
        for k in ("name", "owner", "plugins"):
            if k not in m:
                errs.append(f"marketplace.json: missing required '{k}'")
        if not (isinstance(m.get("owner"), dict) and m["owner"].get("name")):
            errs.append("marketplace.json: owner.name required")
        plugins = m.get("plugins")
        if not isinstance(plugins, list) or len(plugins) != 1:
            errs.append("marketplace.json: expected exactly one plugin entry")
        else:
            e = plugins[0]
            if e.get("name") != "darby":
                errs.append("marketplace.json: plugin entry name must be 'darby'")
            if e.get("source") != "./plugins/darby":
                errs.append("marketplace.json: plugin source must be './plugins/darby'")
            if not (root / "plugins" / "darby").is_dir():
                errs.append("marketplace.json: source directory missing")
    if p is not None:
        if p.get("name") != "darby":
            errs.append("plugin.json: name must be 'darby'")
        if p.get("version") != "0.1.0":
            errs.append("plugin.json: version must be '0.1.0'")
        if not p.get("description"):
            errs.append("plugin.json: description required")
        a = p.get("author")
        if a is not None and not (isinstance(a, dict) and a.get("name")):
            errs.append("plugin.json: author.name required when author is set")
    if c is not None:
        s = (c.get("mcpServers") or {}).get("darby")
        if not isinstance(s, dict):
            errs.append(".mcp.json: mcpServers.darby missing")
        else:
            if s.get("type") != "http":
                errs.append(".mcp.json: darby type must be 'http'")
            if s.get("url") != MCP_URL:
                errs.append(f".mcp.json: darby url must be exactly {MCP_URL}")
            o = s.get("oauth")
            if o is not None and (not isinstance(o, dict) or set(o) - {"clientId", "callbackPort"}):
                errs.append(".mcp.json: oauth may only hold clientId and callbackPort")
    skill = root / "plugins" / "darby" / "skills" / "darby" / "SKILL.md"
    if not skill.is_file():
        errs.append("SKILL.md missing")
    else:
        text = skill.read_text()
        fm = re.match(r"---\n(.*?)\n---\n", text, re.S)
        if not fm or not re.search(r"^name: darby$", fm.group(1), re.M) or not re.search(r"^description: \S", fm.group(1), re.M):
            errs.append("SKILL.md: frontmatter needs name: darby and a description")
        if "read_client_guide" not in text:
            errs.append("SKILL.md: must mention read_client_guide")
    for need in ("LICENSE", "README.md", "docs/SOURCES.md"):
        if not (root / need).is_file():
            errs.append(f"{need} missing")


def check_content(root, errs):
    for f in files(root):
        rel = f.relative_to(root)
        try:
            text = f.read_text()
        except UnicodeDecodeError:
            errs.append(f"{rel}: not UTF-8 text")
            continue
        scrubbed = text.replace(MCP_URL, "")
        for rx, what in FORBIDDEN:
            if rx.search(scrubbed):
                errs.append(f"{rel}: forbidden word ({what})")
        if str(rel) == "LICENSE":
            continue  # standard license text carries its own URLs
        for m in EMAIL_RE.finditer(text):
            errs.append(f"{rel}: email-like string {m.group(0)!r}")
        for m in HOST_RE.finditer(text):
            if m.group(1).lower().rstrip(".") not in ALLOWED_HOSTS:
                errs.append(f"{rel}: disallowed hostname {m.group(1)!r}")
        for rx in SECRET_RES:
            if rx.search(text):
                errs.append(f"{rel}: secret-looking string")


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
    errs = []
    check_manifests(root, errs)
    check_content(root, errs)
    if errs:
        print("FAIL")
        for e in errs:
            print(" -", e)
        return 1
    print("OK: all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
