// SPDX-License-Identifier: Apache-2.0
// Copyright 2026 NAN AI2AI-SI2SI contributors
//
// NAN AI2AI - WEB HUB v2.2 | app.js (ES module, zero dependencies, zero trackers)
// Nguon su that cua moi chuoi van ban la /i18n-dict.js do Worker phuc vu.
// Phe bam SHA-256 chay bang Web Crypto API cua trinh duyet: du lieu khong roi ra mayy.
import {
  I18N_DICT, POLICY_INSTRUMENTS, OPEN_ISSUES, PDF_ASSETS,
  RELEASE_TAG, REPO_CORE, REPO_RESEARCH, RELEASE_URL
} from "/i18n-dict.js";

const LANGS = ["vi", "en", "zh"];
const LANG_KEYS = { vi: "vi", en: "en", zh: "zh" };

function currentLang() {
  const q = new URLSearchParams(location.search).get("lang");
  if (q && LANGS.indexOf(q) !== -1) return q;
  const saved = localStorage.getItem("nan-lang");
  if (saved && LANGS.indexOf(saved) !== -1) return saved;
  return "vi";
}

function setLang(lang, pushUrl) {
  if (LANGS.indexOf(lang) === -1) return;
  document.documentElement.setAttribute("data-lang", lang);
  document.documentElement.setAttribute("lang", lang === "zh" ? "zh-Hans" : lang);
  localStorage.setItem("nan-lang", lang);
  document.querySelectorAll("[data-lang-btn]").forEach(function (b) {
    b.setAttribute("aria-pressed", String(b.dataset.langBtn === lang));
  });
  // Tieu de + mo ta.
  // Trang co <title data-title-vi/en/zh> (vi du: privacy.html, terms.html) giu
  // tieu de rieng cua trang; trang chinh dung meta_title cua tu dien.
  const titleEl = document.querySelector("title[data-title-vi]");
  if (titleEl) {
    const tv = titleEl.getAttribute("data-title-" + lang);
    if (tv) document.title = tv;
    const dv = titleEl.getAttribute("data-desc-" + lang);
    if (dv) {
      const mdd = document.querySelector('meta[name="description"]');
      if (mdd) mdd.setAttribute("content", dv);
      const ogd2 = document.querySelector('meta[property="og:description"]');
      if (ogd2) ogd2.setAttribute("content", dv);
    }
    const og2 = document.querySelector('meta[property="og:title"]');
    if (og2 && tv) og2.setAttribute("content", tv);
  } else {
    document.title = I18N_DICT[lang].meta_title;
    const md = document.querySelector('meta[name="description"]');
    if (md) md.setAttribute("content", I18N_DICT[lang].meta_desc);
    const og = document.querySelector('meta[property="og:title"]');
    if (og) og.setAttribute("content", I18N_DICT[lang].meta_title);
    const ogd = document.querySelector('meta[property="og:description"]');
    if (ogd) ogd.setAttribute("content", I18N_DICT[lang].meta_desc);
  }
  // noi dung sinh dong
  renderPolicyTable(lang);
  renderIssueTable(lang);
  renderPdfCards(lang);
  if (pushUrl) {
    const u = new URL(location.href);
    u.searchParams.set("lang", lang);
    history.replaceState({}, "", u.toString());
  }
}

function t(lang, path) {
  return path.split(".").reduce(function (o, k) { return o && o[k] !== undefined ? o[k] : undefined; }, I18N_DICT[lang]);
}

/* ---------------- 23 van ban ---------------- */
let activeFilter = "all";

function renderPolicyTable(lang) {
  const body = document.querySelector("#policy-table tbody");
  if (!body) return;
  const rows = POLICY_INSTRUMENTS.filter(function (r) {
    return activeFilter === "all" || r.group === activeFilter;
  });
  body.innerHTML = rows.map(function (r) {
    const esc = function (s) {
      return String(s === undefined || s === null ? "" : s)
        .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    };
    return "<tr>" +
      '<td class="id">' + esc(r.id) + "</td>" +
      "<td>" + esc(r.name[lang] || r.name.en) + "</td>" +
      "<td>" + esc(r.issuer) + "</td>" +
      '<td class="num">' + esc(r.year || "-") + "</td>" +
      "</tr>";
  }).join("");
}

/* ---------------- 8 issue ---------------- */
function renderIssueTable(lang) {
  const body = document.querySelector("#issue-table tbody");
  if (!body) return;
  const esc = function (s) {
    return String(s === undefined || s === null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  };
  body.innerHTML = OPEN_ISSUES.map(function (i) {
    const repoUrl = i.repo === "ai2ai-core" ? REPO_CORE : REPO_RESEARCH;
    return "<tr>" +
      "<td>" + esc(i.repo) + "</td>" +
      '<td class="num">#' + esc(i.num) + "</td>" +
      '<td><a href="' + repoUrl + "/issues/" + esc(i.num) + '" rel="noopener">' +
      esc(i.title[lang] || i.title.en) + "</a></td>" +
      "</tr>";
  }).join("");
}

/* ---------------- 5 the PDF ---------------- */
function renderPdfCards(lang) {
  const wrap = document.getElementById("pdf-cards");
  if (!wrap) return;
  const esc = function (s) {
    return String(s === undefined || s === null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  };
  wrap.innerHTML = PDF_ASSETS.map(function (a) {
    const url = REPO_CORE + "/releases/download/" + RELEASE_TAG + "/" + a.filename;
    return '<div class="card">' +
      '<div class="metric">' + esc(a.pages) + " trang" +
      '<small>' + esc(a.label[lang] || a.label.en) + "</small></div>" +
      '<p style="margin-top:10px;"><a href="' + url + '" rel="noopener" style="color:#2D3033;font-weight:600;">' +
      esc(a.filename) + "</a></p>" +
      "</div>";
  }).join("");
}

/* ---------------- Bo mo phong SHA-256 ---------------- */
function canonicalize(text) {
  // Sap xep khoa theo thu tu chuoi, giong cach PoC canonicalize
  let obj;
  try {
    obj = JSON.parse(text);
  } catch (e) {
    return null;
  }
  if (obj === null || typeof obj !== "object" || Array.isArray(obj)) return null;
  return obj;
}

function canonicalJson(value) {
  if (value === null || typeof value !== "object") return JSON.stringify(value);
  if (Array.isArray(value)) {
    return "[" + value.map(canonicalJson).join(",") + "]";
  }
  const keys = Object.keys(value).sort();
  return "{" + keys.map(function (k) {
    return JSON.stringify(k) + ":" + canonicalJson(value[k]);
  }).join(",") + "}";
}

function bytesToHex(buf) {
  return Array.from(new Uint8Array(buf)).map(function (b) {
    return b.toString(16).padStart(2, "0");
  }).join("");
}

async function runSimulator(lang) {
  const input = document.getElementById("sim-input");
  const out = document.getElementById("sim-out");
  const btn = document.getElementById("sim-btn");
  const raw = input.value.trim();
  if (!raw) {
    out.textContent = (lang === "en" ? "Enter a JSON payload first."
      : lang === "zh" ? "请先输入 JSON 内容。" : "Hãy nhập nội dung JSON trước.");
    return;
  }
  const obj = canonicalize(raw);
  if (obj === null) {
    out.textContent = (lang === "en" ? "That is not valid JSON."
      : lang === "zh" ? "这不是有效的 JSON。" : "Nội dung này không phải JSON hợp lệ.");
    return;
  }
  btn.disabled = true;
  try {
    const canonical = canonicalJson(obj);
    const bytes = new TextEncoder().encode(canonical);
    const digest = await crypto.subtle.digest("SHA-256", bytes);
    const hex = bytesToHex(digest);
    const receipt = {
      receipt_type: "nan-receipt/v1",
      payload_sha256: hex,
      canonical_bytes: bytes.length,
      timestamp_utc: new Date().toISOString(),
      note: {
        vi: "Giao diện minh hoa. Khong dung thu vien cua PoC va khong gui du lieu ra ngoai.",
        en: "Illustrative interface. Does not use the PoC library and sends nothing out.",
        zh: "仅作界面演示，未调用 PoC 库，且不向外发送任何数据。"
      }[lang]
    };
    out.textContent = JSON.stringify(receipt, null, 2);
  } catch (e) {
    out.textContent = (lang === "en" ? "Could not compute the digest: " + e.message
      : lang === "zh" ? "无法计算摘要：" + e.message : "Không tính được mã băm: " + e.message);
  } finally {
    btn.disabled = false;
  }
}

/* ---------------- khoi tao ---------------- */
function init() {
  const lang = currentLang();

  document.querySelectorAll("[data-lang-btn]").forEach(function (b) {
    b.addEventListener("click", function () {
      setLang(b.dataset.langBtn, true);
    });
  });

  document.querySelectorAll("#policy-filters button").forEach(function (b) {
    b.addEventListener("click", function () {
      activeFilter = b.dataset.filter;
      document.querySelectorAll("#policy-filters button").forEach(function (x) {
        x.setAttribute("aria-pressed", String(x === b));
      });
      renderPolicyTable(document.documentElement.getAttribute("data-lang"));
    });
  });

  const input = document.getElementById("sim-input");
  const d = I18N_DICT[lang];
  if (input) input.value = d.sim_default;
  const btn = document.getElementById("sim-btn");
  if (btn) btn.addEventListener("click", function () { runSimulator(document.documentElement.getAttribute("data-lang")); });

  setLang(lang, false);
  if (new URLSearchParams(location.search).get("lang")) {
    const u = new URL(location.href);
    u.searchParams.set("lang", lang);
    history.replaceState({}, "", u.toString());
  }
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", init);
} else {
  init();
}
