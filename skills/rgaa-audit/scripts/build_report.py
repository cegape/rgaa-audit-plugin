"""
Construit les livrables RGAA réglementaires à partir des findings statiques et dynamiques :
  - Déclaration d'accessibilité (.md + .html)
  - Grille de conformité (.csv)
  - Schéma pluriannuel d'accessibilité, 3 ans (.md + .html, optionnel)
  - Plan d'action annuel (.md + .html, optionnel)

Les trois documents (déclaration / schéma / plan) sont les livrables prévus par
l'article 47 de la loi n° 2005-102, le décret n° 2019-768 et l'arrêté du 20/09/2019.

Usage minimal :
    python3 build_report.py \\
        --criteres data/criteres_rgaa_4_1_2.json \\
        --static findings_static.json \\
        --out-dir report/ \\
        --site-name "Mon site" \\
        --site-url "https://example.fr" \\
        --org "Mon organisation"

Avec schéma pluriannuel et plan d'action :
    python3 build_report.py ... \\
        --with-schema --with-plan \\
        --periode 2026-2028
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


# ────────────────────────────────────────────────────────────────────────────
# Schéma pluriannuel + Plan d'action — pré-remplissage à partir de l'audit
# ────────────────────────────────────────────────────────────────────────────

def parse_periode(periode: str | None, today: datetime.date):
    """Parse une période "2026-2028" ou déduit 3 ans depuis l'année courante."""
    if periode and "-" in periode:
        a, b = periode.split("-", 1)
        return a.strip(), b.strip()
    annee = today.year
    return str(annee), str(annee + 2)


def remediation_actions(criteres, verdicts, static, max_items=10):
    """Construit une liste d'actions de remédiation triées par fréquence d'occurrences."""
    counts_by_cid = (static or {}).get("findings_by_critere", {}) or {}
    titres = {c["id"]: c["titre"] for c in criteres}
    themes = {c["id"]: THEMES[c["thematique"]] for c in criteres}
    nc = [cid for cid, v in verdicts.items() if v == "NC"]
    # Tri : critères avec le plus d'occurrences en analyse statique d'abord
    nc.sort(key=lambda cid: counts_by_cid.get(cid, 0), reverse=True)
    items = []
    for cid in nc[:max_items]:
        nb = counts_by_cid.get(cid, None)
        suffix = f" ({nb} occurrences détectées)" if nb else ""
        items.append(f"- **Critère {cid}** — {themes.get(cid,'?')} — {titres.get(cid,'?')}{suffix}")
    return items


def to_md_list(items):
    return "\n".join(items) if items else "*(à compléter)*"


def to_html_list(items):
    if not items:
        return "<p><em>(à compléter)</em></p>"
    # items déjà en markdown ("- xxx") → convertir
    lis = []
    for it in items:
        line = it.lstrip("- ").strip()
        # gras markdown très simple
        line = line.replace("**", "")
        lis.append(f"<li>{line}</li>")
    return "<ul>\n" + "\n".join(lis) + "\n</ul>"


def build_schema(args, ctx_audit, templates_dir, out, periode_debut, periode_fin):
    annee_courante = str(datetime.date.today().year)
    liste_sites_md = f"- **{args.site_name}** — {args.site_url}"
    liste_sites_html = f"<ul><li><strong>{args.site_name}</strong> — <a href=\"{args.site_url}\">{args.site_url}</a></li></ul>"

    ctx = {
        "organisation": args.org,
        "periode_debut": periode_debut,
        "periode_fin": periode_fin,
        "perimetre": args.perimetre or f"Le présent schéma s'applique à l'ensemble des sites et applications web édités ou maintenus par {args.org}. Service principal couvert au démarrage : {args.site_name} ({args.site_url}).",
        "liste_sites": liste_sites_md,
        "liste_sites_html": liste_sites_html,
        "annee_courante": annee_courante,
        "date": args.date,
        "url_publication": args.url_publication or "*(à compléter)*",
    }

    md_tpl = templates_dir / "schema-pluriannuel.md.tpl"
    html_tpl = templates_dir / "schema-pluriannuel.html.tpl"
    (out / "schema-pluriannuel.md").write_text(render_md(md_tpl, ctx), encoding="utf-8")
    (out / "schema-pluriannuel.html").write_text(render_md(html_tpl, ctx), encoding="utf-8")


def build_plan(args, criteres, verdicts, static, tx, templates_dir, out, periode_debut, periode_fin):
    today = datetime.date.today()
    annee_courante = today.year
    annee_precedente = annee_courante - 1
    annee_suivante = annee_courante + 1

    remed = remediation_actions(criteres, verdicts, static)

    # Bilan année écoulée — par défaut "premier exercice" si pas de données fournies
    bilan_actions_md = args.bilan_actions or "- *(premier exercice)* Initialisation de la démarche d'accessibilité numérique."
    bilan_taux_md = (
        f"- **{args.site_name}** : taux de conformité RGAA 4.1.2 = {tx:.1f}%"
        if tx is not None else "- *(à compléter)*"
    )

    actions_gouv_md = [
        "- Désigner et faire connaître le référent accessibilité numérique en interne et en externe.",
        "- Mettre en place le comité de suivi accessibilité (réunion semestrielle au minimum).",
        "- Publier le schéma pluriannuel et le présent plan d'action sur le site institutionnel.",
    ]
    actions_form_md = [
        "- Sensibiliser l'ensemble des équipes projet à l'accessibilité numérique.",
        "- Former les développeurs front-end et intégrateurs au RGAA 4.1.2.",
        "- Former les rédacteurs et contributeurs à l'accessibilité éditoriale.",
    ]
    actions_audits_md = [
        f"- Réaliser ou actualiser l'audit RGAA des services concernés (audit déjà mené sur {args.site_name}).",
        "- Mettre en place un suivi automatisé d'accessibilité en intégration continue.",
        "- Programmer une contre-validation externe avant publication de la déclaration définitive.",
    ]
    actions_marches_md = [
        "- Intégrer une clause RGAA dans les CCTP des marchés relatifs à la conception, refonte ou maintenance de services numériques.",
        "- Ajouter des critères d'évaluation prenant en compte la démarche accessibilité des candidats.",
    ]
    actions_com_md = [
        f"- Publier la déclaration d'accessibilité de {args.site_name} sur la page d'accueil avec un lien \"Accessibilité\".",
        "- Mettre à disposition un formulaire ou une adresse de contact pour les signalements d'usagers.",
        "- Communiquer en interne sur les obligations et la feuille de route.",
    ]

    ctx = {
        "organisation": args.org,
        "annee_courante": str(annee_courante),
        "annee_precedente": str(annee_precedente),
        "annee_suivante": str(annee_suivante),
        "periode_debut": periode_debut,
        "periode_fin": periode_fin,
        "perimetre": args.perimetre or f"Le présent plan d'action s'applique aux sites et applications web édités ou maintenus par {args.org}. Service prioritaire : {args.site_name} ({args.site_url}).",
        "date": args.date,
        "url_publication": args.url_publication or "*(à compléter)*",

        # Markdown
        "bilan_actions": bilan_actions_md,
        "bilan_taux": bilan_taux_md,
        "actions_gouvernance": to_md_list(actions_gouv_md),
        "actions_formation": to_md_list(actions_form_md),
        "actions_audits": to_md_list(actions_audits_md),
        "actions_remediation": to_md_list(remed) if remed else "*(aucune non-conformité prioritaire identifiée à ce stade)*",
        "actions_marches": to_md_list(actions_marches_md),
        "actions_communication": to_md_list(actions_com_md),

        # HTML
        "bilan_actions_html": to_html_list([bilan_actions_md]),
        "bilan_taux_html": to_html_list([bilan_taux_md]),
        "actions_gouvernance_html": to_html_list(actions_gouv_md),
        "actions_formation_html": to_html_list(actions_form_md),
        "actions_audits_html": to_html_list(actions_audits_md),
        "actions_remediation_html": to_html_list(remed),
        "actions_marches_html": to_html_list(actions_marches_md),
        "actions_communication_html": to_html_list(actions_com_md),
    }

    md_tpl = templates_dir / "plan-action.md.tpl"
    html_tpl = templates_dir / "plan-action.html.tpl"
    (out / "plan-action.md").write_text(render_md(md_tpl, ctx), encoding="utf-8")
    (out / "plan-action.html").write_text(render_md(html_tpl, ctx), encoding="utf-8")


# ────────────────────────────────────────────────────────────────────────────
# Main
# ────────────────────────────────────────────────────────────────────────────

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

    # Schéma pluriannuel + plan d'action
    ap.add_argument("--with-schema", action="store_true", help="Générer le schéma pluriannuel d'accessibilité (3 ans)")
    ap.add_argument("--with-plan", action="store_true", help="Générer le plan d'action annuel pré-rempli à partir des NC priorisées")
    ap.add_argument("--periode", default=None, help="Période du schéma pluriannuel, ex. 2026-2028 (par défaut: année courante + 2)")
    ap.add_argument("--perimetre", default=None, help="Périmètre couvert par le schéma/plan (texte libre)")
    ap.add_argument("--url-publication", default=None, help="URL où sera publié le schéma/plan")
    ap.add_argument("--bilan-actions", default=None, help="Bilan des actions de l'année écoulée (markdown libre)")

    args = ap.parse_args()

    criteres = json.loads(pathlib.Path(args.criteres).read_text(encoding="utf-8"))["criteres"]
    static = json.loads(pathlib.Path(args.static).read_text(encoding="utf-8")) if args.static else None
    dynamic = json.loads(pathlib.Path(args.dynamic).read_text(encoding="utf-8")) if args.dynamic else None

    verdicts = verdict_for(criteres, static, dynamic)
    counts, tx, by_theme = stats(criteres, verdicts)

    out = pathlib.Path(args.out_dir); out.mkdir(parents=True, exist_ok=True)
    templates_dir = pathlib.Path(args.templates_dir)

    common_ctx = {
        "site_name": args.site_name,
        "site_url": args.site_url,
        "organisation": args.org,
        "date": args.date,
        "verdict": "Non conforme" if counts["NC"] else "Partiellement conforme" if tx and tx < 50 else "Conforme",
        "taux": f"{tx:.1f}" if tx is not None else "—",
        "c": counts["C"], "nc": counts["NC"], "nt": counts["NT"], "na": counts["NA"],
    }

    # ── Déclaration d'accessibilité ────────────────────────────────────────
    md_tpl = templates_dir / "declaration-accessibilite.md.tpl"
    html_tpl = templates_dir / "declaration-accessibilite.html.tpl"

    md_ctx = dict(common_ctx, theme_table=build_theme_table_md(by_theme))
    html_ctx = dict(common_ctx, theme_rows=build_theme_table_html(by_theme))

    (out / "declaration-accessibilite.md").write_text(render_md(md_tpl, md_ctx), encoding="utf-8")
    (out / "declaration-accessibilite.html").write_text(render_md(html_tpl, html_ctx), encoding="utf-8")

    # ── Grille CSV ─────────────────────────────────────────────────────────
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

    # ── Schéma pluriannuel + Plan d'action (optionnels) ────────────────────
    periode_debut, periode_fin = parse_periode(args.periode, datetime.date.today())

    if args.with_schema:
        build_schema(args, common_ctx, templates_dir, out, periode_debut, periode_fin)

    if args.with_plan:
        build_plan(args, criteres, verdicts, static, tx, templates_dir, out, periode_debut, periode_fin)

    # ── Récapitulatif ──────────────────────────────────────────────────────
    print(f"✓ Livrables écrits dans {out}")
    print(f"  - declaration-accessibilite.md / .html")
    print(f"  - grille-conformite.csv")
    if args.with_schema:
        print(f"  - schema-pluriannuel.md / .html (période {periode_debut}–{periode_fin})")
    if args.with_plan:
        print(f"  - plan-action.md / .html")
    print(f"  Verdicts: C={counts['C']} NC={counts['NC']} NT={counts['NT']} NA={counts['NA']}")
    if tx is not None:
        print(f"  Taux de conformité : {tx:.1f}%")


if __name__ == "__main__":
    main()
