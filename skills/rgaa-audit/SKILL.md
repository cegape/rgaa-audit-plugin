---
name: rgaa-audit
description: >-
  Audit RGAA 4.1.2 (Référentiel Général d'Amélioration de l'Accessibilité — France) d'un site ou d'une application web. Outille les 106 critères du RGAA, automatise la collecte de non-conformités via analyse statique (HTML/JSP/PHP/Vue/React/CSS/JS) et audit dynamique (navigateur), puis produit les trois livrables réglementaires : déclaration d'accessibilité (.md/.html), schéma pluriannuel sur 3 ans, et plan d'action annuel. Déclencher dès qu'un utilisateur demande un "audit accessibilité", "audit RGAA", "déclaration d'accessibilité", "schéma pluriannuel", "plan d'action accessibilité", "audit WCAG", "conformité accessibilité numérique", "test accessibilité", ou mentionne le RGAA 4.x. Fonctionne sur n'importe quel projet web : applications Java/JSP, sites statiques HTML, projets React/Vue/Angular/Svelte, sites PHP/WordPress.
---

# RGAA — Audit d'accessibilité numérique

Ce skill outille l'audit RGAA 4.1.2 d'un site ou d'une application web et produit les livrables réglementaires.

## Vue d'ensemble

Le RGAA (Référentiel Général d'Amélioration de l'Accessibilité) est le référentiel français de conformité accessibilité, dérivé de WCAG 2.1 AA. La version courante est **4.1.2** (106 critères répartis en 13 thématiques).

L'obligation s'applique aux personnes morales de droit public et aux entreprises dépassant 250 M€ de CA, sous peine d'amende administrative (arrêté du 20/09/2019).

Le cadre réglementaire (article 47 de la loi n° 2005-102, décret n° 2019-768 du 24/07/2019, arrêté du 20/09/2019) impose **trois livrables**, distincts mais complémentaires :

1. **Déclaration d'accessibilité** — par service en ligne, mentionnant le taux de conformité et les non-conformités constatées. À publier sur la page d'accueil.
2. **Schéma pluriannuel d'accessibilité** — couvrant une période de **3 ans**, présentant la politique, l'organisation et les ressources de l'organisation en matière d'accessibilité numérique.
3. **Plan d'action annuel** — déclinaison opérationnelle du schéma pour l'année en cours (bilan, actions, jalons, indicateurs).

## Quand utiliser ce skill

- "Audit RGAA" / "audit accessibilité" / "audit WCAG" sur un site web ou une application.
- "Déclaration d'accessibilité" à produire ou à mettre à jour.
- Pré-audit interne avant éventuelle contre-validation par un cabinet spécialisé.
- Suivi de mise en conformité (régression automatique en CI).

## Méthodologie (ordre à suivre)

1. **Cadrage** — Demander à l'utilisateur :
   - URL d'une instance accessible (recette ou production) + éventuels identifiants de test.
   - Chemin du code source si analyse statique souhaitée.
   - Pages prioritaires (parcours utilisateur principaux).
   - Format de livrable (déclaration .md/.html, grille .xlsx, rapport .docx).
2. **Référentiel** — Charger `data/criteres_rgaa_4_1_2.json` (106 critères + tests). En cas de nouvelle version du RGAA, lancer `scripts/update_referentiel.py` pour récupérer le criteres.json autoritatif depuis le dépôt DINUM.
3. **Audit statique** — Lancer `scripts/audit_static.py` sur l'arborescence (HTML, JSP, JSX, Vue, PHP, CSS).
4. **Audit dynamique** — Naviguer sur l'application via le MCP Claude in Chrome :
   - Pour chaque page d'échantillon, injecter `scripts/dynamic_probe.js` pour collecter : `lang`, `title`, hiérarchie de titres, landmarks, labels, contrastes WCAG, liens factices, tableaux, iframes.
   - Tester la navigation au clavier (Tab, Shift+Tab, focus visible).
   - Si demandé, tester avec un lecteur d'écran (VoiceOver/NVDA).
5. **Verdict par critère** — Pour chaque critère RGAA : C (Conforme), NC (Non Conforme), NA (Non Applicable) ou NT (Non Testé). Calculer le taux = C / (C + NC).
6. **Livrables réglementaires** — À partir des templates :
   - `templates/declaration-accessibilite.md.tpl` / `.html.tpl` (par service)
   - `templates/schema-pluriannuel.md.tpl` / `.html.tpl` (3 ans, par organisation)
   - `templates/plan-action.md.tpl` / `.html.tpl` (annuel, par organisation)
   - Grille de conformité CSV (traçabilité critère par critère)
7. **Priorisation** — Les actions de remédiation du plan d'action sont triées par effort/impact (quick wins → refonte structurelle) à partir des occurrences de non-conformités détectées.

## Structure du skill

```
rgaa-audit/
├── SKILL.md                         (ce fichier)
├── data/
│   └── criteres_rgaa_4_1_2.json     (référentiel 106 critères)
├── scripts/
│   ├── audit_static.py              (analyse statique HTML/JSP/JSX/Vue/PHP/CSS)
│   ├── dynamic_probe.js             (à injecter dans une page via Chrome MCP)
│   ├── build_report.py              (agrège static + dynamique → verdicts + livrables)
│   └── update_referentiel.py        (met à jour le criteres.json depuis github.com/DISIC/RGAA)
├── templates/
│   ├── declaration-accessibilite.md.tpl
│   ├── declaration-accessibilite.html.tpl
│   ├── schema-pluriannuel.md.tpl
│   ├── schema-pluriannuel.html.tpl
│   ├── plan-action.md.tpl
│   └── plan-action.html.tpl
└── references/
    └── methodologie.md              (rappel méthodologique RGAA)
```

## Étapes détaillées

### 1) Analyse statique

```bash
python3 scripts/audit_static.py <racine_projet> <output.json>
```

Le script détecte les patterns problématiques pour environ 18 critères "outillables" :
- 1.1, 1.2, 1.3 (images / alt)
- 2.1 (iframe sans title)
- 5.x (tableaux sans th/caption)
- 7.1, 7.3, 7.5 (scripts non interactifs, liens factices)
- 8.1, 8.2, 8.3, 8.5 (DOCTYPE, lang, title)
- 9.1 (hiérarchie / structuration)
- 10.1, 10.4, 10.7 (présentation, unités relatives, focus visible)
- 11.1 (label de formulaire)
- 12.7, 12.10 (lien d'évitement, accesskey)
- 13.2 (target=_blank sans avertissement)

Il scanne `.html`, `.htm`, `.jsp`, `.jspf`, `.jsx`, `.tsx`, `.vue`, `.svelte`, `.php`, `.phtml`, `.twig`, `.hbs`, `.erb`, `.css`, `.scss`, `.sass`, `.less`.

### 2) Audit dynamique

Charger `scripts/dynamic_probe.js` dans le contexte de la page via `mcp__Claude_in_Chrome__javascript_tool`. Le probe retourne un JSON avec :
- `lang`, `title`, `doctype`, `charset`
- compteurs images / formulaires / liens / tableaux / headings / landmarks
- échantillon de contrastes WCAG (texte / fond) avec calcul de ratio
- détection de skipLink, target=_blank sans avertissement, tabindex positifs

Itérer sur l'échantillon de pages : connexion, accueil, formulaire de saisie, liste de données, page d'erreur, mentions légales.

### 3) Agrégation et verdict

```bash
python3 scripts/build_report.py \
  --criteres data/criteres_rgaa_4_1_2.json \
  --static findings_static.json \
  --dynamic findings_dynamic.json \
  --out-dir report/ \
  --site-name "Mon site" \
  --site-url "https://exemple.fr" \
  --org "Mon organisation"
```

Produit `declaration-accessibilite.md`, `declaration-accessibilite.html`, `grille-conformite.csv`.

Pour générer en plus les deux livrables stratégiques (schéma pluriannuel sur 3 ans et plan d'action annuel) :

```bash
python3 scripts/build_report.py \
  --criteres data/criteres_rgaa_4_1_2.json \
  --static findings_static.json \
  --dynamic findings_dynamic.json \
  --out-dir report/ \
  --site-name "Mon site" \
  --site-url "https://exemple.fr" \
  --org "Mon organisation" \
  --with-schema --with-plan \
  --periode 2026-2028 \
  --url-publication "https://exemple.fr/accessibilite"
```

Le plan d'action est pré-rempli avec les non-conformités priorisées par fréquence d'occurrences. Les sections « politique », « ressources humaines / financières », « jalons trimestriels » et « indicateurs cibles » restent à compléter manuellement par le référent accessibilité — ce sont des choix stratégiques propres à chaque organisation.

### 4) Mise à jour des livrables

Avant publication, **toujours** :
- **Déclaration d'accessibilité** : compléter les coordonnées de contact (e-mail, postal). Publier sur la page d'accueil avec un lien "Accessibilité" (article 47). Réévaluer au moins tous les 3 ans, ou à toute évolution substantielle.
- **Schéma pluriannuel** : compléter les coordonnées du référent accessibilité, le périmètre des sites concernés, la politique d'achats publics, le budget. Le schéma porte sur **3 ans** et doit être publié sur le site institutionnel.
- **Plan d'action annuel** : compléter les jalons trimestriels, les indicateurs cibles, le bilan de l'année précédente. À publier chaque année avec le bilan du plan précédent.

## Points d'attention

- L'analyse statique sur-détecte volontairement (faux positifs préférés aux faux négatifs). La revue manuelle reste indispensable.
- Le taux de conformité publié est `C / (C + NC)` sur les critères **applicables**. Les NA ne comptent pas. Les NT empêchent de publier une déclaration valide — il faut statuer.

## Référentiel — accès canonique

Le référentiel officiel (et son `criteres.json` autoritatif) est disponible sur :
- https://accessibilite.numerique.gouv.fr/methode/criteres-et-tests/
- https://github.com/DISIC/RGAA (dépôt officiel DINUM)
