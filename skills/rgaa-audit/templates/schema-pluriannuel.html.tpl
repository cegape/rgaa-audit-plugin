<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<title>Schéma pluriannuel d'accessibilité numérique — ${organisation}</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
  body { font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; max-width: 60rem; margin: 2rem auto; padding: 0 1.5rem; color: #1a1a1a; line-height: 1.55; }
  h1 { border-bottom: 2px solid #000091; padding-bottom: .5rem; }
  h2 { color: #000091; margin-top: 2.5rem; }
  h3 { color: #161616; margin-top: 1.8rem; }
  .periode { display: inline-block; background: #000091; color: #fff; padding: .5rem 1rem; border-radius: 4px; font-weight: bold; margin: 1rem 0; }
  .meta { background: #f6f6f6; border-left: 4px solid #000091; padding: 1rem 1.25rem; margin: 1.5rem 0; }
  ul { padding-left: 1.5rem; }
  li { margin: .4rem 0; }
  footer { margin-top: 3rem; padding-top: 1.5rem; border-top: 1px solid #ddd; color: #666; font-size: .9rem; }
  a { color: #000091; }
</style>
</head>
<body>
<h1>Schéma pluriannuel d'accessibilité numérique — ${organisation}</h1>

<p class="periode">Période : ${periode_debut} – ${periode_fin} (3 ans)</p>

<div class="meta">
Document établi en application de l'article 47 de la loi n° 2005-102 du 11 février 2005, du décret n° 2019-768 du 24 juillet 2019 et de l'arrêté du 20 septembre 2019 portant référentiel général d'amélioration de l'accessibilité (RGAA 4.1.2).
</div>

<h2>1. Politique d'accessibilité numérique</h2>
<p>${organisation} s'engage à rendre ses services de communication au public en ligne accessibles à toutes les personnes, et notamment aux personnes en situation de handicap, conformément à l'article 47 de la loi n° 2005-102. Cette démarche vise à offrir un service de qualité égale à l'ensemble des usagers et s'inscrit dans une politique plus large de qualité numérique et d'inclusion.</p>

<h3>Engagements</h3>
<ul>
  <li>Mettre en conformité au RGAA 4.1.2 (et versions ultérieures) l'ensemble des sites et applications web édités ou maintenus par l'organisation.</li>
  <li>Publier la déclaration d'accessibilité de chaque service, mise à jour à chaque évolution substantielle et au minimum tous les trois ans.</li>
  <li>Traiter les retours d'usagers signalant un défaut d'accessibilité dans un délai raisonnable.</li>
  <li>Intégrer l'accessibilité dès la conception (« accessibility by design ») de tout nouveau projet.</li>
</ul>

<h2>2. Référent accessibilité numérique</h2>
<ul>
  <li><strong>Nom</strong> : <em>(à compléter)</em></li>
  <li><strong>Fonction</strong> : <em>(à compléter)</em></li>
  <li><strong>Adresse e-mail</strong> : <em>(à compléter)</em></li>
  <li><strong>Téléphone</strong> : <em>(à compléter)</em></li>
</ul>
<p>Le référent est l'interlocuteur unique pour les questions d'accessibilité numérique, en interne comme pour les usagers. Il coordonne la mise en œuvre du présent schéma et l'élaboration des plans d'action annuels.</p>

<h2>3. Organisation et pilotage</h2>

<h3>Gouvernance</h3>
<ul>
  <li>Pilotage opérationnel : le référent accessibilité numérique.</li>
  <li>Pilotage stratégique : <em>(direction concernée — DSI, communication, etc.)</em>.</li>
  <li>Comité de suivi : réunion au minimum <em>(fréquence — semestrielle recommandée)</em> avec les directions métiers concernées.</li>
</ul>

<h3>Périmètre du schéma</h3>
<p>${perimetre}</p>

<h3>Articulation avec les autres démarches</h3>
<p>L'accessibilité numérique s'articule avec les démarches qualité, sécurité (RSSI), protection des données (DPO) et écoresponsabilité numérique de l'organisation.</p>

<h2>4. Ressources humaines et financières</h2>

<h3>Ressources humaines affectées</h3>
<ul>
  <li>Référent accessibilité : <em>(temps consacré — ex. : 0,2 ETP)</em>.</li>
  <li>Équipes mobilisées : équipes projet (chefs de projet, développeurs, designers, rédacteurs), équipes qualité, équipes marchés publics.</li>
  <li>Recours à des prestataires externes pour les audits initiaux, contre-validations et formations spécialisées.</li>
</ul>

<h3>Ressources financières</h3>
<p>Le budget annuel consacré à l'accessibilité numérique couvre :</p>
<ul>
  <li>Les actions de formation et de sensibilisation.</li>
  <li>Les audits externes et contre-validations.</li>
  <li>Les outils d'analyse et de test (lecteurs d'écran, outils automatisés).</li>
  <li>Les coûts de remédiation des non-conformités (interne et prestataires).</li>
</ul>

<h2>5. Prise en compte de l'accessibilité dans les projets</h2>

<h3>Conception</h3>
<ul>
  <li>Intégration des exigences RGAA dans les cahiers des charges et les expressions de besoin.</li>
  <li>Maquettes et prototypes soumis à un contrôle d'accessibilité avant développement.</li>
  <li>Choix des composants et bibliothèques validés sous l'angle accessibilité.</li>
</ul>

<h3>Développement</h3>
<ul>
  <li>Sensibilisation et formation des équipes de développement.</li>
  <li>Revues de code intégrant les bonnes pratiques accessibilité.</li>
  <li>Tests automatisés en intégration continue (analyseurs statiques, audits navigateur).</li>
</ul>

<h3>Recette et tests utilisateurs</h3>
<ul>
  <li>Tests de conformité RGAA sur les parcours utilisateurs critiques.</li>
  <li>Tests avec technologies d'assistance (lecteurs d'écran, navigation clavier, zoom).</li>
  <li>Implication, lorsque possible, d'utilisateurs en situation de handicap.</li>
</ul>

<h3>Maintenance et évolutions</h3>
<ul>
  <li>Surveillance de la régression accessibilité à chaque mise en production.</li>
  <li>Mise à jour des déclarations d'accessibilité à chaque évolution substantielle.</li>
</ul>

<h2>6. Achats publics et prestations externes</h2>
<p>Les marchés publics relatifs à la conception, à la refonte ou à la maintenance de services numériques intègrent :</p>
<ul>
  <li>Une clause de conformité au RGAA dans le CCTP.</li>
  <li>Des critères d'évaluation prenant en compte la démarche accessibilité du prestataire.</li>
  <li>Des pénalités contractuelles en cas de non-conformité avérée à la livraison.</li>
  <li>L'exigence de livraison d'une déclaration d'accessibilité actualisée à la mise en production.</li>
</ul>

<h2>7. Formation et sensibilisation</h2>

<h3>Plan de formation</h3>
<ul>
  <li><strong>Sensibilisation générale</strong> : tous les collaborateurs concernés par la production numérique.</li>
  <li><strong>Formation technique RGAA</strong> : développeurs front-end, intégrateurs, designers, testeurs.</li>
  <li><strong>Formation rédacteurs</strong> : rédacteurs de contenus, contributeurs CMS.</li>
  <li><strong>Formation référents</strong> : approfondissement méthodologique et juridique.</li>
</ul>

<h3>Sensibilisation continue</h3>
<ul>
  <li>Actualité accessibilité diffusée régulièrement en interne.</li>
  <li>Partage de retours d'expérience entre projets.</li>
  <li>Documentation interne de bonnes pratiques à jour.</li>
</ul>

<h2>8. Recours à des prestations externes</h2>
<p>L'organisation a recours à des prestataires externes pour :</p>
<ul>
  <li>Audits de conformité RGAA initiaux et contre-validations.</li>
  <li>Tests utilisateurs avec des personnes en situation de handicap.</li>
  <li>Formations spécialisées (technologies d'assistance, expertise approfondie).</li>
  <li>Accompagnement à la remédiation sur des chantiers complexes.</li>
</ul>

<h2>9. Liste des sites et applications concernés</h2>
${liste_sites_html}

<h2>10. Plan d'action</h2>
<p>Le présent schéma est décliné chaque année en un <strong>plan d'action annuel</strong> détaillant les chantiers prioritaires, les indicateurs de suivi et les jalons. Le plan d'action de l'année ${annee_courante} est annexé au présent schéma.</p>

<h2>11. Modalités d'évaluation et de mise à jour</h2>
<ul>
  <li><strong>Bilan annuel</strong> publié avec le plan d'action de l'année suivante.</li>
  <li><strong>Réévaluation complète</strong> du schéma pluriannuel tous les 3 ans, ou en cas d'évolution substantielle de l'organisation ou du périmètre des services concernés.</li>
  <li><strong>Mise à jour des déclarations</strong> d'accessibilité de chaque service à chaque évolution substantielle.</li>
</ul>

<h2>12. Voies de recours</h2>
<p>Toute personne constatant un défaut d'accessibilité l'empêchant d'accéder à un contenu ou à un service peut :</p>
<ul>
  <li>Contacter le référent accessibilité (coordonnées au §2).</li>
  <li>Saisir le Défenseur des droits : <a href="https://formulaire.defenseurdesdroits.fr/">https://formulaire.defenseurdesdroits.fr/</a></li>
</ul>

<footer>
Schéma pluriannuel établi le ${date}. Publié sur ${url_publication}.
</footer>
</body>
</html>
