/**
 * Dynamic RGAA probe — to be injected in a browser tab via
 * Claude in Chrome (mcp__Claude_in_Chrome__javascript_tool).
 *
 * Returns a JSON string with structured findings for the current page.
 * Wrap the call so the LAST expression returns the JSON string, e.g. :
 *
 *   (function(){ <paste this file here>; return rgaaProbe(); })()
 */
function rgaaProbe() {
  function rgb(s) {
    const m = (s || "").match(/rgba?\((\d+),\s*(\d+),\s*(\d+)/);
    return m ? [+m[1], +m[2], +m[3]] : null;
  }
  function relLum(c) {
    const [r, g, b] = c.map(v => {
      v = v / 255;
      return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
    });
    return 0.2126 * r + 0.7152 * g + 0.0722 * b;
  }
  function contrast(c1, c2) {
    const L1 = relLum(c1), L2 = relLum(c2);
    return (Math.max(L1, L2) + 0.05) / (Math.min(L1, L2) + 0.05);
  }
  function effectiveBg(el) {
    let cur = el;
    while (cur && cur !== document.documentElement) {
      const s = getComputedStyle(cur);
      const c = rgb(s.backgroundColor);
      if (c && s.backgroundColor !== "rgba(0, 0, 0, 0)") return c;
      if (s.backgroundImage && s.backgroundImage !== "none") return null; // unknown
      cur = cur.parentElement;
    }
    return [255, 255, 255];
  }

  const r = {};
  r.url = location.href;
  r.title = document.title;
  r.lang = document.documentElement.lang || "";
  r.doctype = document.doctype
    ? (document.doctype.name + " " + (document.doctype.publicId || "")).trim()
    : "";
  r.charset = document.characterSet;

  // Images
  const imgs = Array.from(document.images);
  const altDouteux = /^(image|img|logo|icone|ico|ico_|icon|puce|loader|loading|tab|fleche|fleches|arrow|spinner|placeholder)$/i;
  r.images = {
    total: imgs.length,
    sansAlt: imgs.filter(i => !i.hasAttribute("alt")).length,
    altDouteux: imgs.filter(i => altDouteux.test((i.getAttribute("alt") || "").trim())).length,
    altLong: imgs.filter(i => (i.alt || "").length > 80).length,
    samples: imgs.slice(0, 30).map(i => ({
      src: (i.getAttribute("src") || "").split("/").pop().split("?")[0],
      alt: i.getAttribute("alt"),
    })),
  };

  // Form fields
  const fields = Array.from(document.querySelectorAll("input,select,textarea"))
    .filter(i => i.type !== "hidden");
  r.forms = {
    totalChamps: fields.length,
    sansLabel: fields.filter(i =>
      i.type !== "submit" && i.type !== "button" && i.type !== "image" &&
      (!i.labels || !i.labels.length) &&
      !i.getAttribute("aria-label") &&
      !i.getAttribute("aria-labelledby") &&
      !i.getAttribute("title")
    ).length,
    avecPlaceholderSeulement: fields.filter(i =>
      i.placeholder && (!i.labels || !i.labels.length) && !i.getAttribute("aria-label")
    ).length,
  };

  // Links
  const links = Array.from(document.querySelectorAll("a"));
  const warnRe = /(nouvelle fen|nouvel onglet|new window|new tab|s'ouvre dans)/i;
  r.links = {
    total: links.length,
    factices: links.filter(a => (a.getAttribute("href") === "#") ||
                                (a.getAttribute("href") || "").startsWith("javascript:")).length,
    targetBlankSansWarn: links.filter(a =>
      a.target === "_blank" &&
      !warnRe.test((a.title || "") + " " + (a.getAttribute("aria-label") || "") + " " + a.textContent)
    ).length,
    vides: links.filter(a =>
      !a.textContent.trim() &&
      !a.querySelector("img[alt]:not([alt=''])") &&
      !a.getAttribute("aria-label") &&
      !a.getAttribute("title")
    ).length,
  };

  // Tables
  const tables = Array.from(document.querySelectorAll("table"));
  r.tables = {
    total: tables.length,
    sansCaption: tables.filter(t => !t.caption).length,
    sansTh: tables.filter(t => !t.querySelector("th")).length,
    avecRolePresentation: tables.filter(t => t.getAttribute("role") === "presentation").length,
    avecBorderAttr: tables.filter(t => t.hasAttribute("border")).length,
  };

  // Headings
  const hs = Array.from(document.querySelectorAll("h1,h2,h3,h4,h5,h6"));
  const seq = hs.map(h => parseInt(h.tagName[1]));
  let saut = false;
  for (let i = 1; i < seq.length; i++) {
    if (seq[i] - seq[i - 1] > 1) { saut = true; break; }
  }
  r.headings = {
    total: hs.length,
    h1: document.querySelectorAll("h1").length,
    sequence: seq,
    sautNiveau: saut,
  };

  // Landmarks
  r.landmarks = {
    main: document.querySelectorAll("main, [role=main]").length,
    nav: document.querySelectorAll("nav, [role=navigation]").length,
    header: document.querySelectorAll("header, [role=banner]").length,
    footer: document.querySelectorAll("footer, [role=contentinfo]").length,
    search: document.querySelectorAll("[role=search]").length,
    aside: document.querySelectorAll("aside, [role=complementary]").length,
  };

  // Skip link
  r.skipLink = !!Array.from(document.querySelectorAll("a")).find(a =>
    /aller au contenu|skip|évitement|contenu principal/i.test(a.textContent || "")
  );

  // Frames
  r.iframes = {
    total: document.querySelectorAll("iframe").length,
    sansTitle: Array.from(document.querySelectorAll("iframe")).filter(f => !f.title).length,
  };

  // Inline / deprecated
  r.styleInline = document.querySelectorAll("[style]").length;
  r.deprecated = {
    align: document.querySelectorAll("[align]").length,
    valign: document.querySelectorAll("[valign]").length,
    bgcolor: document.querySelectorAll("[bgcolor]").length,
    border: document.querySelectorAll("table[border]").length,
    center: document.querySelectorAll("center").length,
    font: document.querySelectorAll("font").length,
  };
  r.tabindex = {
    positif: Array.from(document.querySelectorAll("[tabindex]"))
      .filter(e => parseInt(e.getAttribute("tabindex")) > 0).length,
  };

  // Contraste WCAG (échantillon)
  const ctEls = Array.from(document.querySelectorAll("a, button, p, span, td, label, h1, h2, h3, h4"))
    .filter(el => el.textContent.trim().length > 0 &&
                  el.textContent.trim().length < 80 &&
                  el.offsetParent !== null);
  const ctNC = [];
  for (const el of ctEls.slice(0, 200)) {
    const s = getComputedStyle(el);
    const fg = rgb(s.color);
    const bg = effectiveBg(el);
    if (!fg || !bg) continue;
    const ratio = contrast(fg, bg);
    const fs = parseFloat(s.fontSize);
    const bold = parseInt(s.fontWeight) >= 700;
    const large = fs >= 24 || (fs >= 18.66 && bold);
    const seuil = large ? 3.0 : 4.5;
    if (ratio < seuil) {
      ctNC.push({
        tag: el.tagName, text: el.textContent.trim().slice(0, 50),
        fg: "rgb(" + fg.join(",") + ")", bg: "rgb(" + bg.join(",") + ")",
        ratio: ratio.toFixed(2), seuil,
      });
    }
  }
  r.contrast = {
    sampled: Math.min(ctEls.length, 200),
    nonConformes: ctNC.length,
    top: ctNC.slice(0, 20),
  };

  return JSON.stringify(r);
}

// Auto-execute when injected as a single expression
rgaaProbe();
