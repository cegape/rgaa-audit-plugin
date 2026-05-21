# Plugin `rgaa-audit`

Plugin Claude (Code / Cowork) pour réaliser un **audit RGAA 4.1.2** complet d'un site ou d'une application web — de l'analyse statique du code source à la génération d'une déclaration d'accessibilité prête à publier.

> RGAA = Référentiel Général d'Amélioration de l'Accessibilité, version 4.1.2, en vigueur en France. Concerne les services publics, leurs délégataires, et les entreprises dont le chiffre d'affaires en France dépasse 250 M€ (article 47 de la loi n° 2005-102 ; arrêté du 20/09/2019).

## Public visé

- **CTO** et leads techniques qui veulent intégrer un audit accessibilité dans leur cycle de développement.
- **RSSI** et délégués à la conformité qui doivent attester l'état d'accessibilité d'un patrimoine applicatif.
- **Responsables accessibilité** et chefs de projet qui pilotent une mise en conformité.
- **Développeurs** qui veulent un retour automatique sur leurs PR avant de les fusionner.

## Ce que fait le plugin

1. **Analyse statique** de l'arborescence — HTML, JSP/JSPF, JSX/TSX (React), Vue, Svelte, PHP/Twig/Blade, ERB, Handlebars + CSS/SCSS/Sass/Less. Détecte les patterns problématiques pour environ 18 critères "outillables" (alt manquants, lang absent, hiérarchie de titres, labels de formulaire, contrastes, tableaux de mise en forme, liens factices, etc.).
2. **Audit dynamique** via Claude in Chrome : injection d'une sonde JS qui mesure `lang`, `title`, hiérarchie de titres, landmarks ARIA, labels, contrastes WCAG calculés, liens factices, tableaux, iframes, focus visible.
3. **Verdict par critère** sur les 106 critères du RGAA 4.1.2 (C / NC / NA / NT).
4. **Génération des livrables** :
   - Déclaration d'accessibilité (Markdown + HTML, prête à publier)
   - Grille de conformité (CSV, traçable critère par critère)
   - Rapport détaillé avec findings (Markdown)
5. **Plan d'action** trié par effort/impact (quick wins → refonte structurelle).

## Périmètre supporté

Le plugin est agnostique du framework. Il fonctionne sur :

- Sites **HTML statiques**
- Applications **Java / JSP / Struts / Spring**
- Projets **React / Next.js / Remix** (JSX / TSX)
- Projets **Vue / Nuxt** (.vue)
- Projets **Svelte / SvelteKit**
- Sites **PHP / Symfony (Twig) / Laravel (Blade) / WordPress**
- Apps **Ruby on Rails** (ERB)
- Templates **Handlebars**, **EJS**, etc.

## Installation

### Comme plugin Claude Code

```bash
# Ajouter ce dépôt comme marketplace
/plugin marketplace add https://github.com/cegape/rgaa-audit-plugin

# Installer le plugin
/plugin install rgaa-audit
```

### Comme skill autonome (Cowork / Claude Code)

```bash
# macOS / Linux — symlink pour suivre les évolutions
git clone https://github.com/cegape/rgaa-audit-plugin.git ~/projects/rgaa-audit-plugin
ln -s ~/projects/rgaa-audit-plugin/skills/rgaa-audit ~/.claude/skills/rgaa-audit
```

Au prochain démarrage, le skill `rgaa-audit` sera proposé automatiquement dès qu'un utilisateur demande un audit RGAA / accessibilité.

## Utilisation

Dans Claude, il suffit de demander en langage naturel :

> « Fais-moi l'audit RGAA du site `https://exemple.fr`, le code est dans `~/repo/monsite/src/` »

Claude va :

1. Poser les questions de cadrage (périmètre, identifiants de test si nécessaire, livrables attendus).
2. Lancer `scripts/audit_static.py` sur le code source.
3. Naviguer sur le site déployé via Claude in Chrome et injecter `scripts/dynamic_probe.js`.
4. Croiser les résultats et générer la déclaration d'accessibilité dans `report/`.

## Utilisation en CLI / CI

```bash
# Analyse statique
python3 skills/rgaa-audit/scripts/audit_static.py ./src ./report/findings_static.json

# Génération de la déclaration
python3 skills/rgaa-audit/scripts/build_report.py \
    --criteres skills/rgaa-audit/data/criteres_rgaa_4_1_2.json \
    --static ./report/findings_static.json \
    --out-dir ./report \
    --site-name "Mon site" \
    --site-url "https://exemple.fr" \
    --org "Mon organisation"
```

À intégrer dans une pipeline CI (GitLab CI / GitHub Actions / Jenkins) pour suivre la régression accessibilité à chaque merge request.

## Limites

- L'analyse statique sur-détecte volontairement (faux positifs préférés aux faux négatifs). La revue manuelle reste indispensable.
- Le plugin sert de pré-audit automatisé et de tableau de bord interne. Pour la crédibilité d'une publication officielle, beaucoup d'organisations font ensuite contre-valider l'audit par un cabinet spécialisé en accessibilité numérique (Access42, Tanaguru, Ideance, Empreinte digitale, Atalan, Koena…) ou un auditeur certifié IAAP (CPACC / WAS) — ce n'est cependant pas une obligation réglementaire.
- Les critères « subjectifs » (pertinence d'un alt, sens d'une liste de choix) sont marqués `NT` et doivent être tranchés manuellement.

## Distribution

Ce plugin peut être :
- Diffusé en interne via un dépôt Git d'entreprise (`/plugin marketplace add <url-interne>`).
- Publié en open source via un dépôt GitHub/GitLab public et référencé dans un marketplace communautaire.
- Installé comme skill autonome par simple copie de `skills/rgaa-audit/`.

## Contribution

Les contributions sont bienvenues : nouvelles règles d'analyse statique, support de nouveaux frameworks, traductions, intégrations CI. Voir `CONTRIBUTING.md` pour les modalités (à venir).

## Licence

MIT — voir `LICENSE`.

## Mainteneur

- Auteur : **Karim Cassam Chenaï** (CEGAPE)
- Contact : karim.cassam@cegape.fr
- Source : https://github.com/cegape/rgaa-audit-plugin
- Issues : https://github.com/cegape/rgaa-audit-plugin/issues

## Référentiel RGAA

Le plugin embarque uniquement la version structurée `data/criteres_rgaa_4_1_2.json` (les 106 critères et leurs tests). Les documents officiels (PDF, ODT, glossaire) ne sont pas embarqués pour éviter la dérive avec la source autoritative.

**Sources officielles** (DINUM) :
- Méthodologie et critères en ligne : https://accessibilite.numerique.gouv.fr/methode/criteres-et-tests/
- Dépôt Git autoritatif : https://github.com/DISIC/RGAA (`criteres.json`, `glossaire.json`)
- PDF officiel : https://accessibilite.numerique.gouv.fr/methode/RGAA-v4.1.2.pdf

**Mise à jour du référentiel** lors d'une nouvelle version (4.1.3, 4.2…) :

```bash
python3 skills/rgaa-audit/scripts/update_referentiel.py --version 4.1.2 --ref main
# ou pour une version future :
python3 skills/rgaa-audit/scripts/update_referentiel.py --version 4.2 --ref 4.2
```

Le script télécharge `criteres.json` depuis le dépôt DINUM, le normalise au format consommé par le skill, et écrit `data/criteres_rgaa_<version>.json`.
