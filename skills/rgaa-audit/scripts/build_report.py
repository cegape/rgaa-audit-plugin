"""
Construit les livrables RGAA (déclaration .md/.html + grille .csv)
à partir des findings statiques et dynamiques.

Usage:
    python3 build_report.py \\
        --criteres data/criteres_rgaa_4_1_2.json \\
        --static findings_static.json \\
        --dynamic findings_dynamic.json \\
        --out-dir report/ \\
        --site-name "Mon site" \\
        --site-url "https://example.fr" \\
        --org "Mon organisation" \\
        --date 2026-05-21
"""

from __future__ import annotations
import argparse
import json
import pathlib
import datetime
from string import Template


def verdict_for(criteres, static, dynamic):
    """Établit un verdict provisoire par critère."""
    NC_static = set((static or {}).get("findings_by_critere", {}).keys())
    NC_dynamic = set((dynamic or {}).get("nc_criteres", []))
    NA_defaults = {"4.1","4.2","4.3","4.4","4.5","4.6","4.7","4.8","4.9","4.10","4.11","4.12","4.13"}
    if (dynamic or {}).get("na_criteres"):
        NA_defaults |= set(dynamic["na_criteres"])
    verdicts = {}
    for c in criteres:
        cid = c["id"]
        if cid in NC_static or cid in NC_dynamic:
            verdicts[cid] = "NC"
        elif cid in NA_defaults:
            verdicts[cid] = "NA"
        else:
            verdicts[cid] = "NT"  # défaut prudent
    return verdicts


def stats(criteres, verdicts):
    from collections import Counter
    counts = Counter(verdicts[c["id"]] for c in criteres)
    applicable = counts["C"] + counts["NC"]
    tx = (100.0 * counts["C"] / applicable) if applicable else None
    by_theme = {}
    for c in criteres:
        t = c["thematique"]
        by_theme.setdefault(t, Counter())[verdicts[c["id"]]] += 1
    return counts, tx, by_theme


THEMES = {
    1: "Images", 2: "Cadres", 3: "Couleurs", 4: "Multimédia",
    5: "Tableaux", 6: "Liens", 7: "Scripts", 8: "Éléments obligatoires",
    9: "Structuration", 10: "Présentation", 11: "Formulaires",
    12: "Navigation", 13: "Consultation",
}


def render_md(template_path, ctx):
    tpl = pathlib.Path(template_path).read_text(encoding="utf-8")
    return Template(tpl).safe_substitute(ctx)


def build_theme_table_md(by_theme):
    lines = ["| # | Thématique | C | NC | NT | NA |", "|---|---|---:|---:|---:|---:|"]
    tot = {"C": 0, "NC": 0, "NT": 0, "NA": 0}
    for t in sorted(THEMES):
        cv = by_theme.get(t, {})
        c = cv.get("C", 0); nc = cv.get("NC", 0); nt = cv.get("NT", 0); na = cv.get("NA", 0)
        for k, v in (("C", c), ("NC", nc), ("NT", nt), ("NA", na)):
            tot[k] += v
        lines.append(f"| {t} | {THEMES[t]} | {c} | {nc} | {nt} | {na} |")
    lines.append(f"| | **Total** | **{tot['C']}** | **{tot['NC']}** | **{tot['NT']}** | **{tot['NA']}** |")
    return "\n".join(lines)


def build_theme_table_html(by_theme):
    rows = []
    tot = {"C": 0, "NC": 0, "NT": 0, "NA": 0}
    for t in sorted(THEMES):
        cv = by_theme.get(t, {})
        c = cv.get("C", 0); nc = cv.get("NC", 0); nt = cv.get("NT", 0); na = cv.get("NA", 0)
        for k, v in (("C", c), ("NC", nc), ("NT", nt), ("NA", na)):
            tot[k] += v
        rows.append(
            f'<tr><td>{t}</td><td>{THEMES[t]}</td>'
            f'<td class="num c">{c}</td><td class="num nc">{nc}</td>'
            f'<td class="num nt">{nt}</td><td class="num na">{na}</td></tr>'
        )
    rows.append(
        f'<tr><td colspan="2" class="tot">Total</td>'
        f'<td class="num tot">{tot["C"]}</td><td class="num tot">{tot["NC"]}</td>'
        f'<td class="num tot">{tot["NT"]}</td><td class="num tot">{tot["NA"]}</td></tr>'
    )
    return "\n".join(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--criteres", required=True)
    ap.add_argument("--static", default=None)
    ap.add_argument("--dynamic", default=None)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--site-name", required=True)
    ap.add_argument("--site-url", required=True)
    ap.add_argument("--org", required=True)
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    ap.add_argument("--templates-dir", default=str(pathlib.Path(__file__).resolve().parent.parent / "templates"))
    args = ap.parse_args()

    criteres = json.loads(pathlib.Path(args.criteres).read_text(encoding="utf-8"))["criteres"]
    static = json.loads(pathlib.Path(args.static).read_text(encoding="utf-8")) if args.static else None
    dynamic = json.loads(pathlib.Path(args.dynamic).read_text(encoding="utf-8")) if args.dynamic else None

    verdicts = verdict_for(criteres, static, dynamic)
    counts, tx, by_theme = stats(criteres, verdicts)

    out = pathlib.Path(args.out_dir); out.mkdir(parents=True, exist_ok=True)

    common_ctx = {
        "site_name": args.site_name,
        "site_url": args.site_url,
        "organisation": args.org,
        "date": args.date,
        "verdict": "Non conforme" if counts["NC"] else "Partiellement conforme" if tx and tx < 50 else "Conforme",
        "taux": f"{tx:.1f}" if tx is not None else "—",
        "c": counts["C"], "nc": counts["NC"], "nt": counts["NT"], "na": counts["NA"],
    }

    md_tpl = pathlib.Path(args.templates_dir) / "declaration-accessibilite.md.tpl"
    html_tpl = pathlib.Path(args.templates_dir) / "declaration-accessibilite.html.tpl"

    md_ctx = dict(common_ctx, theme_table=build_theme_table_md(by_theme))
    html_ctx = dict(common_ctx, theme_rows=build_theme_table_html(by_theme))

    (out / "declaration-accessibilite.md").write_text(render_md(md_tpl, md_ctx), encoding="utf-8")
    (out / "declaration-accessibilite.html").write_text(render_md(html_tpl, html_ctx), encoding="utf-8")

    # Grille CSV
    import csv
    with (out / "grille-conformite.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["Critère", "Thématique", "Titre", "Verdict", "Commentaire"])
        for c in sorted(criteres, key=lambda c: (c["thematique"], c["numero"])):
            cid = c["id"]; v = verdicts[cid]
            comment = ""
            if static and v == "NC" and cid in static.get("findings_by_critere", {}):
                comment = f"{static['findings_by_critere'][cid]} occurrences détectées en analyse statique"
            w.writerow([cid, THEMES[c["thematique"]], c["titre"], v, comment])

    print(f"✓ Livrables écrits dans {out}")
    print(f"  Verdicts: C={counts['C']} NC={counts['NC']} NT={counts['NT']} NA={counts['NA']}")
    if tx is not None:
        print(f"  Taux de conformité : {tx:.1f}%")


if __name__ == "__main__":
    main()
