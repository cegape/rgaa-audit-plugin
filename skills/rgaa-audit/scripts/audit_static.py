"""
Analyse statique RGAA pour fichiers HTML/JSP/CSS.

Pour chaque critère "outillable" (testable statiquement de manière fiable),
on retourne :
  - verdict potentiel : C / NC / NT (Non Testé statiquement)
  - liste de findings : fichier, ligne, extrait, message

Les critères non testables statiquement (multimédia, contenus dynamiques,
vidéo, JS au runtime, etc.) sont marqués NT et reportés à l'audit dynamique.

Usage:
    python3 audit_static.py <racine_webapp> <output_json>
"""

from __future__ import annotations
import sys
import re
import json
import pathlib
import collections
import html

EXT_HTMLISH = {".html", ".htm", ".jsp", ".jspf", ".gsp", ".jsx", ".tsx",
               ".vue", ".svelte", ".php", ".phtml", ".twig", ".hbs", ".erb"}
EXT_CSS = {".css", ".scss", ".sass", ".less"}

# Backwards compatibility alias
EXT_JSP = EXT_HTMLISH


def iter_files(root: pathlib.Path, exts: set[str]):
    for p in root.rglob("*"):
        if p.is_file() and p.suffix.lower() in exts:
            yield p


def read(p: pathlib.Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""


def line_of(text: str, idx: int) -> int:
    return text.count("\n", 0, idx) + 1


def excerpt(text: str, idx: int, width: int = 120) -> str:
    start = max(0, idx - 30)
    end = min(len(text), idx + width)
    s = text[start:end].replace("\n", " ⏎ ").strip()
    return s[:200]


# -----------------------------------------------------------------------------
# Détecteurs par critère
# -----------------------------------------------------------------------------

class Finding(dict):
    def __init__(self, critere, file, line, snippet, message, severity="major"):
        super().__init__(
            critere=critere,
            file=str(file),
            line=line,
            snippet=snippet,
            message=message,
            severity=severity,
        )


def check_jsp_file(rel: str, text: str) -> list[dict]:
    findings: list[dict] = []
    lower = text.lower()

    # --- 1.1 / 1.3 alt manquant ou non pertinent ---
    for m in re.finditer(r"<img\b([^>]*)>", text, flags=re.IGNORECASE):
        attrs = m.group(1)
        attrs_lower = attrs.lower()
        has_alt = re.search(r"\balt\s*=", attrs_lower) is not None
        if not has_alt:
            findings.append(Finding("1.1", rel, line_of(text, m.start()), excerpt(text, m.start()),
                                    "Image sans attribut alt", "blocker"))
        else:
            alt_match = re.search(r'\balt\s*=\s*"([^"]*)"', attrs, flags=re.IGNORECASE) or \
                        re.search(r"\balt\s*=\s*'([^']*)'", attrs, flags=re.IGNORECASE)
            if alt_match:
                alt_val = alt_match.group(1).strip()
                src_match = re.search(r'\bsrc\s*=\s*"([^"]*)"', attrs, flags=re.IGNORECASE)
                src_val = src_match.group(1) if src_match else ""
                # 1.3 alt non pertinent : valeurs suspectes
                suspect_alt = {
                    "image", "img", "logo", "icone", "icone1", "icone2", "ico",
                    "icodossier", "icoaide", "icopaiement", "icoimport", "icoadmin",
                    "icostat", "puce", "tab", "fleche", "fleches", "loading",
                    "loader", "ajax-loader", "loader.gif",
                }
                if alt_val.lower() in suspect_alt:
                    findings.append(Finding("1.3", rel, line_of(text, m.start()), excerpt(text, m.start()),
                                            f"Alt non pertinent (\"{alt_val}\")", "major"))
                # 1.2 décoratif: si src évoque une icône/déco mais alt non vide
                if alt_val and any(k in src_val.lower() for k in ("loader", "spinner", "puce", "fleche", "bckg", "icone", "decoration")):
                    findings.append(Finding("1.2", rel, line_of(text, m.start()), excerpt(text, m.start()),
                                            f"Image potentiellement décorative avec alt non vide (\"{alt_val}\")", "minor"))

    # --- 1.6 longdesc / aria-describedby manquant pour images complexes (heuristique faible : skip) ---

    # --- 2.1 iframe sans title ---
    for m in re.finditer(r"<(iframe|frame)\b([^>]*)>", text, flags=re.IGNORECASE):
        attrs = m.group(2)
        if not re.search(r"\btitle\s*=", attrs, flags=re.IGNORECASE):
            findings.append(Finding("2.1", rel, line_of(text, m.start()), excerpt(text, m.start()),
                                    "<iframe>/<frame> sans attribut title", "blocker"))

    # --- 8.1 DOCTYPE & 8.2 valididté ---
    if re.search(r"<html\b", lower):
        if not re.search(r"<!doctype\s+html", lower):
            findings.append(Finding("8.1", rel, 1, "(début de fichier)", "DOCTYPE HTML5 attendu (<!DOCTYPE html>)", "major"))
        elif re.search(r"<!doctype\s+html\s+public", lower):
            findings.append(Finding("8.1", rel, 1, "(début de fichier)", "DOCTYPE legacy (XHTML/HTML4) - migrer vers HTML5", "major"))

    # --- 8.3 lang sur <html> ---
    for m in re.finditer(r"<html\b([^>]*)>", text, flags=re.IGNORECASE):
        attrs = m.group(1)
        if not re.search(r"\blang\s*=", attrs, flags=re.IGNORECASE):
            findings.append(Finding("8.3", rel, line_of(text, m.start()), excerpt(text, m.start()),
                                    "<html> sans attribut lang (fr attendu)", "blocker"))

    # --- 8.5 <title> ---
    if re.search(r"<html\b", lower) and not re.search(r"<title\b[^>]*>[^<]+</title>", text, flags=re.IGNORECASE | re.DOTALL):
        findings.append(Finding("8.5", rel, 1, "(début de fichier)", "Page HTML sans <title> non vide", "major"))

    # --- 9.1 hiérarchie titres (manquante = signal faible) ---
    if re.search(r"<html\b", lower):
        if not re.search(r"<h[1-6]\b", lower):
            findings.append(Finding("9.1", rel, 1, "(début de fichier)", "Page sans aucun titre h1-h6", "major"))

    # --- 9.1 / 5.3 / 5.8 tables de mise en forme ---
    for m in re.finditer(r"<table\b([^>]*)>", text, flags=re.IGNORECASE):
        attrs = m.group(1)
        # rôle présentation ?
        if re.search(r'role\s*=\s*["\']presentation', attrs, flags=re.IGNORECASE):
            findings.append(Finding("5.3", rel, line_of(text, m.start()), excerpt(text, m.start()),
                                    "Tableau de mise en forme déclaré (role=presentation) - vérifier la linéarisation", "info"))
        else:
            # cherchons th/caption/scope/headers à proximité
            close = re.search(r"</table>", text[m.end():], flags=re.IGNORECASE)
            block = text[m.end(): m.end() + (close.start() if close else 2000)]
            has_th = re.search(r"<th\b", block, flags=re.IGNORECASE) is not None
            has_caption = re.search(r"<caption\b", block, flags=re.IGNORECASE) is not None
            if not has_th and not has_caption:
                findings.append(Finding("9.1", rel, line_of(text, m.start()), excerpt(text, m.start()),
                                        "Tableau sans <th>/<caption> : potentielle table de mise en forme à signaler role=presentation", "major"))

    # --- 10.1 styles inline et attributs de présentation ---
    pres_attrs = ("align", "valign", "bgcolor", "border", "cellpadding", "cellspacing",
                  "color", "face", "height", "width", "size", "background")
    for m in re.finditer(r'<\w+[^>]*\s(' + "|".join(pres_attrs) + r')\s*=', text, flags=re.IGNORECASE):
        attr = m.group(1).lower()
        # Tolérer width/height sur <img>/<iframe>/<canvas>/<svg>
        tag_match = re.match(r"<(\w+)", text[m.start():m.start() + 80])
        tag = tag_match.group(1).lower() if tag_match else ""
        if attr in ("width", "height") and tag in ("img", "iframe", "canvas", "svg", "video", "audio", "object", "embed"):
            continue
        if attr == "border" and tag == "table" and "border=\"0\"" in text[m.start():m.start() + 80].lower().replace(" ", ""):
            # cas typique table de mise en forme
            findings.append(Finding("10.1", rel, line_of(text, m.start()), excerpt(text, m.start()),
                                    f"Attribut de présentation HTML déprécié : {attr} sur <{tag}>", "major"))
            continue
        findings.append(Finding("10.1", rel, line_of(text, m.start()), excerpt(text, m.start()),
                                f"Attribut de présentation HTML : {attr} sur <{tag}>", "minor"))

    # style="..." inline
    for m in re.finditer(r'\sstyle\s*=\s*"[^"]+"', text, flags=re.IGNORECASE):
        # filtrer les inclusions Struts dynamiques ?
        findings.append(Finding("10.1", rel, line_of(text, m.start()), excerpt(text, m.start()),
                                "Style en attribut inline (style=...) - préférer une feuille CSS", "info"))

    # éléments présentation dépréciés
    for tag in ("center", "font", "marquee", "blink", "big", "strike", "tt"):
        for m in re.finditer(rf"<{tag}\b", text, flags=re.IGNORECASE):
            findings.append(Finding("10.1", rel, line_of(text, m.start()), excerpt(text, m.start()),
                                    f"Élément HTML déprécié <{tag}>", "blocker"))

    # --- 10.6 liens identifiables (souligne ou non) — non testable statiquement de façon fiable ---

    # --- 11.1 label sur champ ---
    for m in re.finditer(r"<input\b([^>]*)>", text, flags=re.IGNORECASE):
        attrs = m.group(1)
        type_match = re.search(r'\btype\s*=\s*["\']([^"\']+)', attrs, flags=re.IGNORECASE)
        itype = (type_match.group(1) if type_match else "text").lower()
        if itype in ("hidden", "submit", "button", "reset", "image"):
            continue
        # absence d'id ou title ?
        has_id = re.search(r"\bid\s*=", attrs, flags=re.IGNORECASE) is not None
        has_title = re.search(r"\btitle\s*=", attrs, flags=re.IGNORECASE) is not None
        has_aria_label = re.search(r"\baria-label", attrs, flags=re.IGNORECASE) is not None
        has_aria_lb = re.search(r"\baria-labelledby", attrs, flags=re.IGNORECASE) is not None
        if not (has_id or has_title or has_aria_label or has_aria_lb):
            findings.append(Finding("11.1", rel, line_of(text, m.start()), excerpt(text, m.start()),
                                    f"Champ <input type=\"{itype}\"> sans id/title/aria-label : étiquette potentiellement absente", "major"))
    # textarea / select sans label/id
    for tag in ("textarea", "select"):
        for m in re.finditer(rf"<{tag}\b([^>]*)>", text, flags=re.IGNORECASE):
            attrs = m.group(1)
            has_id = re.search(r"\bid\s*=", attrs, flags=re.IGNORECASE) is not None
            has_title = re.search(r"\btitle\s*=", attrs, flags=re.IGNORECASE) is not None
            has_aria = re.search(r"\baria-label", attrs, flags=re.IGNORECASE) is not None
            if not (has_id or has_title or has_aria):
                findings.append(Finding("11.1", rel, line_of(text, m.start()), excerpt(text, m.start()),
                                        f"<{tag}> sans id/title/aria-label", "major"))

    # --- 11.10 / 11.11 contrôle de saisie : difficile statiquement ---

    # --- 12.7 lien d'évitement ---
    # Détection à la racine du layout : on signale seulement dans baseLayout / index
    if re.search(r"<html\b", lower) and "skip" not in lower and "evitement" not in lower and "lien d'évitement" not in text.lower():
        findings.append(Finding("12.7", rel, 1, "(début de fichier)",
                                "Aucun lien d'évitement détecté (texte 'skip' / 'évitement' absent)", "major"))

    # --- 12.10 raccourcis clavier accesskey ---
    for m in re.finditer(r"\baccesskey\s*=", text, flags=re.IGNORECASE):
        findings.append(Finding("12.10", rel, line_of(text, m.start()), excerpt(text, m.start()),
                                "Attribut accesskey : risque de conflit avec raccourcis du navigateur/AT", "info"))

    # --- 13.2 ouverture nouvelle fenêtre sans avertissement ---
    for m in re.finditer(r'target\s*=\s*["\']_blank["\']', text, flags=re.IGNORECASE):
        # Vérifie présence d'un titre/info dans les ~250 char qui précèdent
        snippet = text[max(0, m.start() - 250):m.end() + 50].lower()
        has_warn = ("nouvelle fenêtre" in snippet or "new window" in snippet
                    or "nouvel onglet" in snippet or "rel=\"noopener" in snippet)
        if "title=" not in snippet and not has_warn:
            findings.append(Finding("13.2", rel, line_of(text, m.start()), excerpt(text, m.start()),
                                    "target=\"_blank\" sans signalement (title ou texte) de nouvelle fenêtre", "major"))

    # --- 7.1 onclick sur élément non interactif ---
    for m in re.finditer(r'<(div|span|td|tr|p|li|img)\b[^>]*\bonclick\s*=', text, flags=re.IGNORECASE):
        findings.append(Finding("7.1", rel, line_of(text, m.start()), excerpt(text, m.start()),
                                f"Gestionnaire onclick sur <{m.group(1)}> non interactif (utiliser <button> ou ajouter role/tabindex/keyboard)", "major"))

    # --- 7.3 href="#" + onclick = lien factice ---
    for m in re.finditer(r'<a\b[^>]*href\s*=\s*["\']#["\'][^>]*onclick\s*=', text, flags=re.IGNORECASE):
        findings.append(Finding("7.3", rel, line_of(text, m.start()), excerpt(text, m.start()),
                                "Lien factice href=\"#\" avec onclick (préférer <button>)", "major"))

    # --- 7.5 / 13.10 javascript:void(0) ---
    for m in re.finditer(r"javascript\s*:", text, flags=re.IGNORECASE):
        findings.append(Finding("7.5", rel, line_of(text, m.start()), excerpt(text, m.start()),
                                "URL javascript: dans un lien — non accessible si JS désactivé", "minor"))

    # --- HTML invalide flagrant (8.2) : attribut sans valeur ni quote suspect ---
    if re.search(r'<td\b[^>]*\bcoucou\b', text, flags=re.IGNORECASE):
        for m in re.finditer(r'<td\b[^>]*\bcoucou\b[^>]*>', text, flags=re.IGNORECASE):
            findings.append(Finding("8.2", rel, line_of(text, m.start()), excerpt(text, m.start()),
                                    "Attribut HTML inconnu \"coucou\" : HTML invalide", "blocker"))

    return findings


def check_css_file(rel: str, text: str) -> list[dict]:
    findings: list[dict] = []
    # 10.4 unités relatives — détection des tailles en px sur font-size
    for m in re.finditer(r"font-size\s*:\s*\d+\s*px", text, flags=re.IGNORECASE):
        findings.append(Finding("10.4", rel, line_of(text, m.start()), excerpt(text, m.start()),
                                "font-size en px : préférer rem/em pour permettre l'agrandissement", "info"))
    # 10.5 : !important sur outline (focus visible)
    for m in re.finditer(r"outline\s*:\s*none|outline\s*:\s*0", text, flags=re.IGNORECASE):
        findings.append(Finding("10.7", rel, line_of(text, m.start()), excerpt(text, m.start()),
                                "outline:none — risque de supprimer la prise de focus visible (10.7)", "blocker"))
    return findings


def main():
    if len(sys.argv) < 3:
        print("Usage: audit_static.py <root> <out.json>", file=sys.stderr)
        sys.exit(1)
    root = pathlib.Path(sys.argv[1]).resolve()
    out_path = pathlib.Path(sys.argv[2])

    all_findings: list[dict] = []
    n_jsp = 0
    n_css = 0
    for p in iter_files(root, EXT_JSP):
        n_jsp += 1
        all_findings.extend(check_jsp_file(str(p.relative_to(root)), read(p)))
    for p in iter_files(root, EXT_CSS):
        n_css += 1
        all_findings.extend(check_css_file(str(p.relative_to(root)), read(p)))

    # Synthèse
    by_critere = collections.Counter(f["critere"] for f in all_findings)
    out = {
        "root": str(root),
        "files_analyzed": {"jsp_html": n_jsp, "css": n_css},
        "findings": all_findings,
        "findings_by_critere": dict(sorted(by_critere.items())),
        "total_findings": len(all_findings),
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Analyzed {n_jsp} JSP/HTML + {n_css} CSS files")
    print(f"Total findings: {len(all_findings)}")
    print("By critère:")
    for k, v in sorted(by_critere.items(), key=lambda kv: tuple(int(p) for p in kv[0].split("."))):
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
