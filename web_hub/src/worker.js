// SPDX-License-Identifier: Apache-2.0
// Copyright 2026 NAN AI2AI-SI2SI contributors
//
/**
 * NAN AI2AI :  CLOUDFLARE EDGE WORKER (v2.2 TRU-001)
 * Target: https://nan-ai2ai.nexusasianetwork.workers.dev
 * Zero-Budget ($0) | Zero Third-Party Trackers | Strict CSP & Security Headers
 *
 * Manifest TRU-001 chi chua nhung gi da kiem chung duoc. Xem
 * PHRU LUC A cua NAN_AI2AI_COMM_v2_2_Ke_Hoach_15_Ngay_Hoan_Chinh.md.
 */

import { I18N_DICT, POLICY_INSTRUMENTS, OPEN_ISSUES, PDF_ASSETS, RELEASE_TAG, REPO_CORE, REPO_RESEARCH, RELEASE_URL }
  from "./i18n-dict.js";

const TRU001_MANIFEST = {
  project: "NAN AI2AI :  Neutral Technical Evidence Infrastructure PoC",
  version: "v2.2.0-canonical",
  verified_at_utc: "2026-10-22T08:00:00Z",
  budget_vnd: 0,
  licenses: {
    code: "Apache-2.0",
    policy_dataset: "CC-BY-4.0"
  },
  architecture_layers: {
    layer_a: "Neutral Technical Evidence Layer (NAN AI2AI PoC :  SHA-256 payload digests, Ed25519 signatures, canonical JSON, UTC timestamps, nan-receipt/v1 receipts, JWK thumbprints, transporter attestations, JSON Schema subset validation, atomic in-flight claim). Never renders a legal judgment.",
    layer_b: "Legal Arbitration & Adjudication Layer (human tribunals such as VIAC / Courts under Law 54/2010/QH12 and the CIArb 2025 Guidelines)"
  },
  verified_metrics: {
    policy_instruments_count: 23,
    automated_unit_tests_pass: 124,
    ci_jobs_status: "11/11 SUCCESS (3 OS x 3 Python matrix + TruffleHog secret scan + 2 licence compliance gates)",
    open_good_first_issues: 8,
    external_contributors_recorded: 1,
    specialized_department_brains: 7,
    central_core_brains: 1,
    canonical_registry_skills_active: 63,
    canonical_registry_skills_note: "63 = 51 ACTIVE_INTERNAL_ADVISORY_SPECIALIST_GUIDANCE + 12 ACTIVE_INSTALLED. 3 DISABLED and 1 SUPERSEDED are excluded.",
    tru001_truth_discipline: "Declared != Evidenced != Verified != Accepted",
    provenance_gate_fields: 7,
    hitl_digest_lock_enforced: true
  },
  immutable_commitments: [
    "No donations, no fundraising, no courses for sale (0 VND budget).",
    "Full transparency on technical limits ,  early PoC, not a finished product (see TECHNICAL_DEBT.md).",
    "Independent personal initiative ,  does not represent Vietnam's AI community (12-month sunset clause)."
  ],
  policy_references_outside_dataset: [
    {
      id: "VN-QD-1033-2026",
      name: "Quyet dinh 1033/QD-TTg (2026) :  Chuong trinh phat trien kinh te so va xa hoi so 2026-2030",
      note: "Policy reference for the 30% GDP digital economy target. Signed 09/06/2026. NOT one of the 23 instruments in the research dataset.",
      source: "https://mst.gov.vn/500000-doanh-nghiep-chuyen-doi-so-kinh-te-so-dong-gop-30-gdp-197260612165818814.htm"
    }
  ],
  repositories: {
    core_poc: REPO_CORE,
    policy_research: REPO_RESEARCH,
    pdf_release_v0_2_0: RELEASE_URL
  },
  pdf_assets_v0_2_0: PDF_ASSETS.map(function (a) {
    return {
      id: a.id,
      title: a.label,
      filename: a.filename,
      pages: a.pages,
      url: REPO_CORE + "/releases/download/" + RELEASE_TAG + "/" + a.filename
    };
  }),
  open_issues: OPEN_ISSUES.map(function (i) {
    return {
      repository: i.repo,
      number: i.num,
      title: i.title,
      url: (i.repo === "ai2ai-core" ? REPO_CORE : REPO_RESEARCH) + "/issues/" + i.num
    };
  })
};

const SECURITY_HEADERS = {
  "Content-Security-Policy": "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; font-src 'self'; media-src 'self'; object-src 'none'; frame-ancestors 'none'; base-uri 'self'; form-action 'self';",
  "Strict-Transport-Security": "max-age=31536000; includeSubDomains; preload",
  "X-Content-Type-Options": "nosniff",
  "X-Frame-Options": "DENY",
  "Referrer-Policy": "strict-origin-when-cross-origin",
  "Permissions-Policy": "camera=(), microphone=(), geolocation=(), payment=(), interest-cohort=()",
  "Cross-Origin-Opener-Policy": "same-origin",
  "X-NAN-Governance": "TRU-001-VERIFIED; ZERO-CASH; LAYER-A-TECHNICAL-EVIDENCE-ONLY"
};

function withSecurityHeaders(response, extraHeaders = {}) {
  const newHeaders = new Headers(response.headers);
  for (const [k, v] of Object.entries(SECURITY_HEADERS)) {
    newHeaders.set(k, v);
  }
  for (const [k, v] of Object.entries(extraHeaders)) {
    newHeaders.set(k, v);
  }
  return new Response(response.body, {
    status: response.status,
    statusText: response.statusText,
    headers: newHeaders
  });
}

function json(body, cacheSeconds) {
  return new Response(JSON.stringify(body, null, 2), {
    status: 200,
    headers: {
      "Content-Type": "application/json; charset=utf-8",
      "Cache-Control": "public, max-age=" + (cacheSeconds || 300)
    }
  });
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // 1. Machine-readable TRU-001 Evidence Manifest
    if (url.pathname === "/api/tru001-manifest" || url.pathname === "/api/status") {
      return withSecurityHeaders(json(TRU001_MANIFEST, 300));
    }

    // 2. Single source of truth for the 3 languages, served as an ES module
    if (url.pathname === "/i18n-dict.js") {
      const src = "export const I18N_DICT = " + JSON.stringify(I18N_DICT) + ";\n" +
        "export const POLICY_INSTRUMENTS = " + JSON.stringify(POLICY_INSTRUMENTS) + ";\n" +
        "export const OPEN_ISSUES = " + JSON.stringify(OPEN_ISSUES) + ";\n" +
        "export const PDF_ASSETS = " + JSON.stringify(PDF_ASSETS) + ";\n" +
        "export const RELEASE_TAG = " + JSON.stringify(RELEASE_TAG) + ";\n" +
        "export const REPO_CORE = " + JSON.stringify(REPO_CORE) + ";\n" +
        "export const REPO_RESEARCH = " + JSON.stringify(REPO_RESEARCH) + ";\n" +
        "export const RELEASE_URL = " + JSON.stringify(RELEASE_URL) + ";\n";
      return withSecurityHeaders(new Response(src, {
        status: 200,
        headers: { "Content-Type": "application/javascript; charset=utf-8" }
      }), { "Cache-Control": "public, max-age=300" });
    }

    // 3. robots.txt fallback (Cloudflare managed file is served otherwise)
    if (url.pathname === "/robots.txt") {
      const robots = "User-agent: *\nAllow: /\n";
      return withSecurityHeaders(new Response(robots, {
        status: 200,
        headers: { "Content-Type": "text/plain; charset=utf-8" }
      }));
    }

    // 4. Static assets from ./public (index.html reads ?lang=vi|en|zh)
    if (env.ASSETS) {
      const assetResponse = await env.ASSETS.fetch(request);
      return withSecurityHeaders(assetResponse);
    }

    return withSecurityHeaders(
      new Response("NAN AI2AI Edge Worker Active", { status: 200 })
    );
  }
};
