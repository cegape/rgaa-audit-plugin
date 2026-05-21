"""
Met à jour data/criteres_rgaa_4_1_2.json (ou suivant) depuis la source autoritative :
le dépôt GitHub officiel de la DINUM (https://github.com/DISIC/RGAA).

Ce script télécharge le fichier criteres.json officiel, le normalise au format
attendu par le skill, et écrit le résultat dans data/.

Usage:
    python3 update_referentiel.py                       # version par défaut (4.1.2)
    python3 update_referentiel.py --version 4.1.2       # version explicite
    python3 update_referentiel.py --ref main            # tag/branch Git
    python3 update_referentiel.py --out data/criteres_rgaa_4_1_3.json
"""

from __future__ import annotations
import argparse
import json
import pathlib
import sys
import urllib.request
import urllib.error

# URL du criteres.json officiel sur le dépôt DINUM
# Le dépôt utilise des branches/tags par version ; on cible par défaut le tag courant.
RAW_URL_TEMPLATE = "https://raw.githubusercontent.com/DISIC/RGAA/{ref}/criteres.json"

# Mapping des thématiques (les 13 du RGAA 4.x)
THEMATIQUES = {
    1: "Images", 2: "Cadres", 3: "Couleurs", 4: "Multimédia",
    5: "Tableaux", 6: "Liens", 7: "Scripts", 8: "Éléments obligatoires",
    9: "Structuration de l'information", 10: "Présentation de l'information",
    11: "Formulaires", 12: "Navigation", 13: "Consultation",
}


def fetch(url: str) -> str:
    print(f"→ GET {url}")
    req = urllib.request.Request(url, headers={"User-Agent": "rgaa-audit-plugin"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        print(f"✗ HTTP {e.code} en récupérant {url}", file=sys.stderr)
        raise


def normalize(raw: dict, version: str) -> dict:
    """Normalise le criteres.json officiel DINUM au format du skill."""
    criteres = []
    # Le criteres.json officiel a une structure {"topics": [...]} avec criteria imbriqués.
    topics = raw.get("topics") or raw.get("thematiques") or []
    for t in topics:
        thm_num = int(t.get("number") or t.get("numero"))
        for c in t.get("criteria", t.get("criteres", [])):
            num = int(c.get("number") or c.get("numero"))
            titre = (c.get("title") or c.get("titre") or "").strip()
            tests = []
            for tst in c.get("tests", []):
                tid = str(tst.get("id") or tst.get("number") or "")
                ttitle = (tst.get("title") or tst.get("titre") or "").strip()
                tests.append({"id": tid, "title": ttitle})
            criteres.append({
                "id": f"{thm_num}.{num}",
                "thematique": thm_num,
                "numero": num,
                "titre": f"Critère {thm_num}.{num} {titre}",
                "tests": tests,
            })
    criteres.sort(key=lambda c: (c["thematique"], c["numero"]))
    return {
        "version": f"RGAA {version}",
        "thematiques": THEMATIQUES,
        "criteres": criteres,
        "total_criteres": len(criteres),
        "source": "https://github.com/DISIC/RGAA",
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--version", default="4.1.2",
                    help="Version du RGAA (sert au nom de fichier et au champ 'version')")
    ap.add_argument("--ref", default="main",
                    help="Branche ou tag Git du dépôt DINUM à utiliser (défaut: main)")
    ap.add_argument("--out", default=None,
                    help="Chemin de sortie du JSON (défaut: data/criteres_rgaa_<version>.json)")
    args = ap.parse_args()

    plugin_root = pathlib.Path(__file__).resolve().parent.parent
    out = pathlib.Path(args.out) if args.out else \
        plugin_root / "data" / f"criteres_rgaa_{args.version.replace('.', '_')}.json"
    out.parent.mkdir(parents=True, exist_ok=True)

    url = RAW_URL_TEMPLATE.format(ref=args.ref)
    raw_text = fetch(url)
    try:
        raw = json.loads(raw_text)
    except json.JSONDecodeError as e:
        print(f"✗ JSON invalide depuis {url}: {e}", file=sys.stderr)
        sys.exit(1)

    normalized = normalize(raw, args.version)
    out.write_text(json.dumps(normalized, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✓ {normalized['total_criteres']} critères écrits dans {out}")
    if normalized["total_criteres"] != 106:
        print(f"⚠ Attendu 106 critères pour RGAA 4.1.2, obtenu {normalized['total_criteres']}.",
              "Vérifiez la branche/le tag.", file=sys.stderr)


if __name__ == "__main__":
    main()
