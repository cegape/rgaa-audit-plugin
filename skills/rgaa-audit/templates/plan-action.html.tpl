<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<title>Plan d'action accessibilité ${annee_courante} — ${organisation}</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
  body { font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; max-width: 60rem; margin: 2rem auto; padding: 0 1.5rem; color: #1a1a1a; line-height: 1.55; }
  h1 { border-bottom: 2px solid #000091; padding-bottom: .5rem; }
  h2 { color: #000091; margin-top: 2.5rem; }
  h3 { color: #161616; margin-top: 1.8rem; }
  .meta { background: #f6f6f6; border-left: 4px solid #000091; padding: 1rem 1.25rem; margin: 1.5rem 0; }
  table { border-collapse: collapse; width: 100%; margin: 1rem 0; }
  th, td { border: 1px solid #ddd; padding: .5rem .75rem; text-align: left; }
  th { background: #f0f0f5; font-weight: 600; }
  ul { padding-left: 1.5rem; }
  li { margin: .4rem 0; }
  footer { margin-top: 3rem; padding-top: 1.5rem; border-top: 1px solid #ddd; color: #666; font-size: .9rem; }
  a { color: #000091; }
</style>
</head>
<body>
<h1>Plan d'action accessibilité numérique ${annee_courante} — ${organisation}</h1>

<div class="meta">
Document établi en application de l'article 47 de la loi n° 2005-102 du 11 février 2005, du décret n° 2019-768 du 24 juillet 2019 et de l'arrêté du 20 septembre 2019.
<br><br>
Ce plan d'action décline pour l'année ${annee_courante} le schéma pluriannuel d'accessibilité numérique ${periode_debut} – ${periode_fin}.
</div>

<h2>1. Bilan de l'année ${annee_precedente}</h2>

<h3>Actions réalisées</h3>
${bilan_actions_html}

<h3>Taux de conformité par service audité</h3>
${bilan_taux_html}

<h3>Écarts par rapport au plan ${annee_precedente}</h3>
<p><em>(à compléter — actions reportées, abandonnées, ajoutées)</em></p>

<h2>2. Périmètre du plan d'action ${annee_courante}</h2>
<p>${perimetre}</p>

<h2>3. Actions prévues en ${annee_courante}</h2>

<h3>3.1 Organisation et gouvernance</h3>
${actions_gouvernance_html}

<h3>3.2 Formation et sensibilisation</h3>
${actions_formation_html}

<h3>3.3 Audits et contrôles</h3>
${actions_audits_html}

<h3>3.4 Mises en conformité (remédiation des non-conformités)</h3>
${actions_remediation_html}

<h3>3.5 Achats publics et marchés</h3>
${actions_marches_html}

<h3>3.6 Communication et publication</h3>
${actions_communication_html}

<h2>4. Indicateurs de suivi</h2>
<table>
  <thead>
    <tr><th>Indicateur</th><th>Cible ${annee_courante}</th><th>Mesure</th></tr>
  </thead>
  <tbody>
    <tr><td>Nombre de sites audités</td><td><em>(à compléter)</em></td><td><em>(à compléter)</em></td></tr>
    <tr><td>Nombre de déclarations d'accessibilité publiées</td><td><em>(à compléter)</em></td><td><em>(à compléter)</em></td></tr>
    <tr><td>Taux de conformité moyen RGAA</td><td><em>(à compléter)</em></td><td><em>(à compléter)</em></td></tr>
    <tr><td>Nombre de personnes formées</td><td><em>(à compléter)</em></td><td><em>(à compléter)</em></td></tr>
    <tr><td>Nombre de signalements traités</td><td><em>(à compléter)</em></td><td><em>(à compléter)</em></td></tr>
    <tr><td>Délai moyen de traitement d'un signalement</td><td><em>(à compléter)</em></td><td><em>(à compléter)</em></td></tr>
  </tbody>
</table>

<h2>5. Jalons</h2>
<table>
  <thead>
    <tr><th>Trimestre</th><th>Jalon</th><th>Service / périmètre concerné</th></tr>
  </thead>
  <tbody>
    <tr><td>T1 ${annee_courante}</td><td><em>(à compléter)</em></td><td><em>(à compléter)</em></td></tr>
    <tr><td>T2 ${annee_courante}</td><td><em>(à compléter)</em></td><td><em>(à compléter)</em></td></tr>
    <tr><td>T3 ${annee_courante}</td><td><em>(à compléter)</em></td><td><em>(à compléter)</em></td></tr>
    <tr><td>T4 ${annee_courante}</td><td><em>(à compléter)</em></td><td><em>(à compléter)</em></td></tr>
  </tbody>
</table>

<h2>6. Ressources mobilisées</h2>
<ul>
  <li><strong>Référent accessibilité numérique</strong> : <em>(à compléter — temps consacré)</em>.</li>
  <li><strong>Équipes internes</strong> : <em>(à compléter — directions concernées)</em>.</li>
  <li><strong>Prestataires externes</strong> : <em>(à compléter — audits, formations, contre-validations)</em>.</li>
  <li><strong>Budget prévisionnel</strong> : <em>(à compléter, optionnel)</em>.</li>
</ul>

<h2>7. Modalités de suivi</h2>
<ul>
  <li>Comité de suivi : réunion <em>(fréquence — au moins semestrielle recommandée)</em>.</li>
  <li>Bilan intermédiaire à mi-année.</li>
  <li>Bilan annuel publié avec le plan d'action ${annee_suivante}.</li>
</ul>

<h2>8. Voies de recours</h2>
<p>Toute personne constatant un défaut d'accessibilité peut contacter le référent accessibilité numérique de ${organisation} ou saisir le Défenseur des droits : <a href="https://formulaire.defenseurdesdroits.fr/">https://formulaire.defenseurdesdroits.fr/</a></p>

<footer>
Plan d'action établi le ${date}. Publié sur ${url_publication}.
</footer>
</body>
</html>
