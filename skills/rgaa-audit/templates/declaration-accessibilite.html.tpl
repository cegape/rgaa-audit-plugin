<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>Déclaration d'accessibilité — ${site_name}</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  :root{--fg:#1a1a1a;--bg:#fff;--accent:#3a5fcd;--muted:#555;--ko:#b00020;--ok:#1a7f37;--nt:#666;--card:#f6f7fb;}
  body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;color:var(--fg);max-width:880px;margin:2rem auto;padding:0 1.2rem;line-height:1.55}
  header.hero{border-left:6px solid var(--accent);padding:.6rem 1rem;background:var(--card);margin-bottom:1.5rem}
  h1{font-size:1.7rem;border-bottom:2px solid var(--accent);padding-bottom:.3rem}
  h2{font-size:1.3rem;color:var(--accent);margin-top:2.2rem}
  table{border-collapse:collapse;width:100%;margin:1rem 0}
  caption{caption-side:top;text-align:left;font-weight:600;padding:.3rem 0;color:var(--muted)}
  th,td{border:1px solid #ddd;padding:.45rem .6rem;text-align:left}
  th{background:#eef1f7}
  td.num{text-align:right;font-variant-numeric:tabular-nums}
  td.tot{font-weight:600;background:#f4f6fa}
  .c{color:var(--ok);font-weight:600}
  .nc{color:var(--ko);font-weight:600}
  .nt{color:var(--nt)}
  .na{color:var(--muted)}
  .verdict{display:inline-block;padding:.2rem .6rem;border-radius:3px;font-size:.85rem;font-weight:600;background:#fbe6e8;color:var(--ko)}
  .taux{display:inline-block;padding:.2rem .6rem;border-radius:3px;font-size:.85rem;font-weight:600;background:#eef1f7;color:var(--accent)}
  blockquote{border-left:4px solid var(--accent);background:#f6f7fb;padding:.6rem 1rem;color:var(--muted)}
</style>
</head>
<body>
<header class="hero">
  <h1>Déclaration d'accessibilité — ${site_name}</h1>
</header>

<p>${organisation} s'engage à rendre son service de communication au public en ligne ${site_name} accessible conformément à l'article 47 de la loi n° 2005-102 du 11 février 2005.</p>
<p>Cette déclaration d'accessibilité s'applique à : <a href="${site_url}">${site_url}</a>.</p>

<h2>État de conformité</h2>
<p><span class="verdict">${verdict}</span> avec le RGAA 4.1.2.</p>

<h2>Résultats des tests</h2>
<p>L'audit du ${date} révèle un taux de conformité de <span class="taux">${taux} %</span> (${c} conformes / ${nc} non conformes / ${nt} non testés / ${na} non applicables).</p>

<table>
  <caption>Verdicts par thématique</caption>
  <thead>
    <tr><th scope="col">#</th><th scope="col">Thématique</th><th scope="col" class="num">C</th><th scope="col" class="num">NC</th><th scope="col" class="num">NT</th><th scope="col" class="num">NA</th></tr>
  </thead>
  <tbody>
    ${theme_rows}
  </tbody>
</table>

<h2>Établissement de cette déclaration</h2>
<p>Cette déclaration a été établie le <strong>${date}</strong>.</p>
<h3>Technologies utilisées</h3>
<p><em>(à compléter)</em></p>
<h3>Environnement de test</h3>
<p><em>(à compléter — OS, navigateurs, technologies d'assistance utilisées)</em></p>
<h3>Outils utilisés</h3>
<ul>
  <li>Analyse statique du code source (skill <code>rgaa-audit</code>)</li>
  <li>Inspection DOM via Chrome DevTools</li>
</ul>
<h3>Pages auditées</h3>
<p><em>(à compléter)</em></p>

<h2>Retour d'information et contact</h2>
<ul>
  <li>Adresse e-mail : <em>(à compléter)</em></li>
  <li>Adresse postale : <em>(à compléter)</em></li>
</ul>

<h2>Voies de recours</h2>
<ul>
  <li><a href="https://formulaire.defenseurdesdroits.fr/">Écrire un message au Défenseur des droits</a></li>
  <li><a href="https://www.defenseurdesdroits.fr/saisir/delegues">Contacter un délégué dans votre région</a></li>
  <li>Défenseur des droits — Libre réponse 71120 — 75342 Paris CEDEX 07</li>
</ul>
</body>
</html>
