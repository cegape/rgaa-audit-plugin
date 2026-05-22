# Plugin `rgaa-audit`

Plugin Claude (Code / Cowork) pour réaliser un **audit RGAA 4.1.2** complet d'un site ou d'une application web — de l'analyse statique du code source à la génération des trois livrables réglementaires : **déclaration d'accessibilité**, **schéma pluriannuel** (3 ans) et **plan d'action annuel**.

> RGAA = Référentiel Général d'Amélioration de l'Accessibilité, version 4.1.2, en vigueur en France. Concerne les services publics, leurs délégataires, et les entreprises dont le chiffre d'affaires en France dépasse 250 M€ (article 47 de la loi n° 2005-102 ; décret n° 2019-768 du 24/07/2019 ; arrêté du 20/09/2019).

## Public visé

- **CTO** et leads techniques qui veulent intégrer un audit accessibilité dans leur cycle de développement.
- **RSSI** et délégués à la conformité qui doivent attester l'état d'accessibilité d'un patrimoine applicatif.
- **Responsables accessibilité** et chefs de projet qui pilotent une mise en conformité.
- **Développeurs** qui veulent un retour automatique sur leurs PR avant de les fusionner.

## Cadre réglementaire

L'accessibilité numérique est encadrée en France par l'**article 47 de la loi n° 2005-102 du 11 février 2005** (modifié par la loi du 7 octobre 2016 dite « pour une République numérique »), précisé par le **décret n° 2019-768 du 24 juillet 2019** et l'**arrêté du 20 septembre 2019** qui approuve la version 4 du RGAA.

### Qui est concerné

- Les personnes morales de droit public (État, collectivités territoriales, établissements publics).
- Les organismes délégataires d'une mission de service public.
- Les organismes privés à but non lucratif fournissant des services essentiels au public ou répondant aux besoins essentiels d'une personne handicapée.
- Les entreprises dont le chiffre d'affaires en France dépasse **250 M€** (moyenne sur les trois derniers exercices).

### Périmètre des services concernés

L'obligation couvre les **sites internet, intranets, extranets, applications mobiles, progiciels et mobilier urbain numérique** édités ou utilisés par les organismes concernés.

### Trois livrables obligatoires

L'arrêté du 20/09/2019 impose la publication de trois documents distincts :

1. **Déclaration d'accessibilité** — un document **par service en ligne**, mentionnant l'état de conformité (conforme / partiellement conforme / non conforme), le taux de conformité au RGAA, les non-conformités constatées et les voies de recours. À publier sur la page d'accueil avec un lien intitulé « Accessibilité ».
2. **Schéma pluriannuel d'accessibilité numérique** — un document **par organisation**, couvrant une période de **3 ans**, présentant la politique, l'organisation, les ressources et les moyens engagés.
3. **Plan d'action annuel** — déclinaison opérationnelle du schéma pour l'année en cours.

### Mentions et pages obligatoires

L'arrêté du 20/09/2019 distingue deux obligations strictes et plusieurs recommandations.

**Obligatoire — sur la page d'accueil**

La page d'accueil affiche obligatoirement l'une des mentions suivantes (telle quelle, sans variante) :

- « **Accessibilité : totalement conforme** » si 100 % des critères RGAA applicables sont respectés ;
- « **Accessibilité : partiellement conforme** » si au moins 50 % des critères RGAA sont respectés ;
- « **Accessibilité : non conforme** » dans les autres cas (ou en l'absence d'audit en cours de validité).

**Obligatoire — page « Accessibilité » accessible depuis toutes les pages**

Le service en ligne dispose d'une page dédiée intitulée « Accessibilité », **accessible directement depuis la page d'accueil et depuis n'importe quelle page du service** (donc en pratique : un lien en pied de page sur toutes les pages). Cette page contient :

- la déclaration d'accessibilité ;
- le schéma pluriannuel de mise en accessibilité (ou un lien vers celui-ci) ;
- le plan d'action de l'année en cours (ou un lien vers celui-ci).

**Recommandé (bonnes pratiques DINUM)**

- Adresse standardisée **`/accessibilite`** pour la page dédiée (`https://www.exemple.fr/accessibilite`).
- Mention de conformité **cliquable**, renvoyant vers la page Accessibilité ou directement vers la déclaration.
- En pratique, l'implémentation standard combine les deux obligations en un seul élément : un lien « **Accessibilité : <niveau>** » placé en pied de page sur toutes les pages, pointant vers `/accessibilite`. Cette combinaison satisfait à la fois l'obligation d'accès depuis toute page et la recommandation de mention cliquable.

### Mise à jour

- La déclaration d'accessibilité doit être réévaluée à toute évolution substantielle du service et, en tout état de cause, au moins **tous les 3 ans**.
- Le schéma pluriannuel est révisé tous les 3 ans.
- Le plan d'action est publié chaque année avec le bilan du plan précédent.

### Sanctions

Le défaut de publication des documents prévus, ou le défaut de la mention d'accessibilité, fait l'objet d'une **sanction administrative** prononcée par l'autorité de contrôle. Le montant maximal est fixé par les textes en vigueur (porté à 50 000 € par service en ligne par la loi REEN n° 2021-1485) et peut être renouvelé chaque année tant que le manquement persiste.

### Pour aller plus loin

- Méthode RGAA et critères : https://accessibilite.numerique.gouv.fr/
- Obligations légales (DINUM) : https://accessibilite.numerique.gouv.fr/obligations/
- Article 47 modifié : [Légifrance](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000033219922/)
- Décret n° 2019-768 : [Légifrance](https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000038811937)
- Arrêté du 20/09/2019 : [Légifrance](https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000039125722)

## Ce que fait le plugin

1. **Analyse statique** de l'arborescence — HTML, JSP/JSPF, JSX/TSX (React), Vue, Svelte, PHP/Twig/Blade, ERB, Handlebars + CSS/SCSS/Sass/Less. Détecte les patterns problématiques pour environ 18 critères "outillables" (alt manquants, lang absent, hiérarchie de titres, labels de formulaire, contrastes, tableaux de mise en forme, liens factices, etc.).
2. **Audit dynamique** via Claude in Chrome : injection d'une sonde JS qui mesure `lang`, `title`, hiérarchie de titres, landmarks ARIA, labels, contrastes WCAG calculés, liens factices, tableaux, iframes, focus visible.
3. **Verdict par critère** sur les 106 critères du RGAA 4.1.2 (C / NC / NA / NT).
4. **Génération des trois livrables réglementaires** (article 47 de la loi n° 2005-102, décret n° 2019-768, arrêté du 20/09/2019) :
   - **Déclaration d'accessibilité** par service (Markdown + HTML, prête à publier sur la page d'accueil).
   - **Schéma pluriannuel d'accessibilité** sur 3 ans (politique, organisation, ressources humaines et financières, formation, marchés publics).
   - **Plan d'action annuel** (bilan, actions par thématique, jalons trimestriels, indicateurs), pré-rempli avec les non-conformités priorisées issues de l'audit.
5. **Grille de conformité CSV** (traçable critère par critère) pour pilotage interne et CI.
6. **Priorisation** des actions de remédiation par effort/impact (quick wins → refonte structurelle).

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

### Dans Claude Cowork (interface graphique)

1. Ouvrir **Customize** (menu paramètres).
2. **Ajouter un plugin personnel** → **Créer un plugin** → **Ajouter une marketplace**.
3. Coller l'URL : `https://github.com/cegape/rgaa-audit-plugin`
4. Cliquer sur **Synchro**, puis installer le plugin `rgaa-audit`.

### Dans Claude Code (CLI)

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

Deux façons d'invoquer le plugin dans Claude (Cowork ou Code) :

**En langage naturel** (déclenchement automatique sur le sens de la demande) :

> « Fais-moi l'audit RGAA du site `https://exemple.fr`, le code est dans `~/repo/monsite/src/` »

**De manière explicite** via le picker de commandes :

> Tape `/` puis sélectionne `rgaa-audit` dans la liste.

Dans les deux cas, Claude va :

1. Poser les questions de cadrage (périmètre, identifiants de test si nécessaire, livrables attendus parmi déclaration / schéma / plan).
2. Lancer `scripts/audit_static.py` sur le code source.
3. Naviguer sur le site déployé via Claude in Chrome et injecter `scripts/dynamic_probe.js`.
4. Croiser les résultats et générer les livrables réglementaires dans `report/` : déclaration d'accessibilité, schéma pluriannuel (3 ans) et plan d'action annuel.

## Utilisation en CLI / CI

```bash
# Analyse statique
python3 skills/rgaa-audit/scripts/audit_static.py ./src ./report/findings_static.json

# Génération de la déclaration d'accessibilité seule
python3 skills/rgaa-audit/scripts/build_report.py \
    --criteres skills/rgaa-audit/data/criteres_rgaa_4_1_2.json \
    --static ./report/findings_static.json \
    --out-dir ./report \
    --site-name "Mon site" \
    --site-url "https://exemple.fr" \
    --org "Mon organisation"

# Génération des trois livrables réglementaires
# (déclaration + schéma pluriannuel 3 ans + plan d'action annuel)
python3 skills/rgaa-audit/scripts/build_report.py \
    --criteres skills/rgaa-audit/data/criteres_rgaa_4_1_2.json \
    --static ./report/findings_static.json \
    --out-dir ./report \
    --site-name "Mon site" \
    --site-url "https://exemple.fr" \
    --org "Mon organisation" \
    --with-schema --with-plan \
    --periode 2026-2028 \
    --url-publication "https://exemple.fr/accessibilite"
```

Le plan d'action est pré-rempli avec les non-conformités priorisées par fréquence. Les sections stratégiques (politique, jalons, indicateurs, ressources humaines et financières) restent à compléter par le référent accessibilité.


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
