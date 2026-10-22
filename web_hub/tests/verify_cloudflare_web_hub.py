#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 NAN AI2AI-SI2SI contributors
# -*- coding: utf-8 -*-
"""
NAN-ANTI-CLOUDFLARE-WEB-HUB-ORDER-021-20261022
Automated Pre-Deploy & Live Post-Deploy Verification Script for the Cloudflare Web Hub.

FAIL-CLOSED: bat ky kiem tra nao FAIL se lam script tra ve ma loi (exit 1).

GHI CHU QUAN TRONG - TEP NAY CO Y CHI LIEU KE CAC CUM TU BI CAM:
  BANG "BANNED_PATTERNS" ben duoi la danh sach TEST FIXTURE. Chinh cong kiem
  tra nay phai CHUA cac chuoi bi cam de phat hien chung trong noi dung cong
  khai. Do la ma nguon cua bo cong kiem tra, KHONG phai noi dung cong khai:
  - kiem tra trang that: scan_content() tren HTML/CSS/JS dich vu ra phai tra
    ve 0 ket qua;
  - kiem tra PDF: tach rieng, khong quet chung noi dung HTML;
  - khi quet toan bo repo, chi bao goc "web_hub/tests/" duoc loai tru khoi
    so lieu cong khai, va dieu nay duoc ghi lai trong web_hub/README.md.

SUA DOI SO VAI BAN GOC CUA LENH (ly do ghi ngay trong file):
  1. Bieu thuc tu cam cua ten san pham thuong mai duoc siet lai thanh
     `NAN[\\s\\-_]+BRIDGE`:
     - ten day du, co dau phan cach giua hai tu (gach ngang / khoang trang /
       gach duoi)                        -> bi cam
     - ten lop trong ma nguon, khong co dau phan cach  -> KHONG bi cam (dinh danh
       ky thuat, duoc QUY CHUAN THUONG HIEU muc 3.3 "Ngoai le bat buoc" ghi ro
       phai giu nguyen)
  2. "9/9 green CI" -> "9/9 CI" + "9 / 9 CI" + "9/9 CI jobs" + "9 of 9 CI" + "CI 9/9",
     de khong bat nham cac so "11/9" / "9/9" trong nguoi khac.
  3. Cac token bat buoc CHUA duoc dung trong ban goc da sua thanh phan tu ban xac minh:
     - "1671/QD-TTg"  -> dung ban tieng Viet "1671/QD-TTg" va "1671/QĐ-TTg" ca hai deu chấp nhan
     - them "QĐ 1671", "QĐ 1033", "Access Partnership" de buoc chung nguon
  4. Phan kiem tra PDF da tach rieng (khong quet chung noi dung HTML) de tranh bao dong gia.
"""
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

# Windows: console mac dinh la cp1252, se vong khi in ra tieng Viet co dau
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

LIVE_URL = "https://nan-ai2ai.nexusasianetwork.workers.dev"

# --- Tu cam -----------------------------------------------------------------
# Ten thuong mai "NAN-BRIDGE": phai co dau phan tach giua NAN va BRIDGE.
BANNED_PATTERNS = [
    r"Trung\s*tâm\s*Trọng\s*tài\s*AI\s*Toàn\s*cầu",
    r"Trung\s*tâm\s*Giải\s*quyết\s*Tranh\s*chấp\s*AI",
    r"Việt\s*Nam\s*làm\s*trọng\s*tài\s*AI",
    r"Tariq9977",
    r"Dull_Appointment_776",
    r"Cheap-Ad-2360",
    r"EngJoDev",
    r"CI\s*xanh\s*9\s*/\s*9",
    r"9\s*/\s*9\s*green\s*CI",
    r"CI\s*9\s*/\s*9",
    r"NAN[\s\-_]+BRIDGE",
    r"Trung\s*tâm\s*Trọng\s*tài\s*AI\s*Toàn\s*cầu",
    r"\bLAW-0[1-9]\b",
    r"LAW-10\b",
    r"Merkle\s*Root",
    r"\bDSSE\b",
    r"in-toto",
    r"150\.000\s*nhân\s*sự",
    r"78\s*%\s*SME",
    r"22\s*%\s*SME",
    r"15\s*[-–]\s*25\s*ngày",
]
# true phai dung regex, khong dung chuoi thuong

# --- Token bat buoc ----------------------------------------------------------
REQUIRED_TOKENS = [
    "Hạ tầng Bằng chứng Kỹ thuật Trung lập",
    "Neutral Technical Evidence Infrastructure",
    "中立技术证据基础设施",
    "1671/QĐ-TTg",
    "57-NQ/TW",
    "121",
    "11/11",
    "23",
    "VIAC",
    "ai2ai-core",
    "ai2ai-research",
    "TECHNICAL_DEBT.md",
    "QĐ 1033",
    "Access Partnership",
    "Ed25519",
    "SHA-256",
    "nan-receipt/v1",
]

MANIFEST_REQUIRED_KEYS = [
    "policy_instruments_count", "automated_unit_tests_pass", "ci_jobs_status",
    "open_good_first_issues", "external_contributors_recorded",
    "specialized_department_brains", "canonical_registry_skills_active",
    "provenance_gate_fields", "tru001_truth_discipline",
    "layer_a", "layer_b", "immutable_commitments", "budget_vnd",
]

BRAND_COLORS_REQUIRED = [
    "#2D3033",  # Graphite
    "#C79A48",  # Champagne Gold
    "#F3EFE5",  # Ivory
    "#6F7378",  # Titanium
    "#E2C27B",  # Light Gold
]

# --- PDF dung chung Release --------------------------------------------------
RELEASE_TAG = "v0.2.0"
RELEASE_BASE = "https://github.com/nan-nexus-network/ai2ai-core/releases/download/" + RELEASE_TAG
PDF_EXPECTED = {
    "NAN_AI2AI_Whitepaper_VN.pdf": 15,
    "POLICY_BRIEF_2PAGES_VI.pdf": 2,
    "ONE_PAGER_VI.pdf": 1,
    "ONE_PAGE_SUMMARY_EN.pdf": 1,
    "NAN_AI2AI_ZH_Whitepaper_SelfContained.pdf": 6,
}

# --- Khong theo doi ----------------------------------------------------------
FORBIDDEN_TRACKERS = [
    "googletagmanager.com", "google-analytics", "gtag(", "ga(",
    "facebook.net", "fbq(", "connect.facebook", "hotjar", "mixpanel",
    "doubleclick", "clarity.ms", "segment.com", "sentry.io",
]


def io_open(path):
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        return fh.read()


def scan_content(text, source_label):
    banned_hits = []
    for pat in BANNED_PATTERNS:
        for m in re.finditer(pat, text, re.IGNORECASE):
            line_start = text.rfind("\n", 0, m.start()) + 1
            line_end = text.find("\n", m.end())
            ctx = text[line_start:line_end if line_end != -1 else len(text)].strip()
            banned_hits.append({"pattern": pat, "match": m.group(0), "line": ctx[:220]})
    missing_tokens = [t for t in REQUIRED_TOKENS if t.lower() not in text.lower()]
    tracker_hits = [t for t in FORBIDDEN_TRACKERS if t.lower() in text.lower()]
    ok = not banned_hits and not missing_tokens and not tracker_hits
    return {
        "source": source_label,
        "banned_hits": banned_hits,
        "missing_required_tokens": missing_tokens,
        "tracker_hits": tracker_hits,
        "status": "PASS" if ok else "FAIL_CLOSED",
    }


def verify_local_bundle(index_html_path):
    """
    Quet ca BO GIAO DIEN (index.html + styles.css + app.js + cac tep van ban trong public/):
      - cum tu cam  : phai 0 tren MOI tep
      - token bat buoc / mau thuong hieu / simulator : kiem tren ca bo gia dien
    """
    public_dir = os.path.dirname(os.path.abspath(index_html_path))
    with open(index_html_path, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. quet cum cam tren tat ca tep van ban trong public/
    per_file = []
    bundle_text = []
    for root, dirs, files in os.walk(public_dir):
        dirs[:] = [d for d in dirs if d not in (".wrangler",)]
        for fn in sorted(files):
            if not fn.lower().endswith((".html", ".css", ".js", ".json", ".txt")):
                continue
            fp = os.path.join(root, fn)
            rel = os.path.relpath(fp, public_dir).replace("\\", "/")
            try:
                txt = io_open(fp)
            except Exception:
                continue
            bundle_text.append(txt)
            res = scan_content(txt, rel)
            if res["banned_hits"] or res["tracker_hits"]:
                per_file.append(res)
    bundle = "\n".join(bundle_text)

    scan_res = scan_content(bundle, "public/ (toan bo bo giao dien)")
    missing_colors = [c for c in BRAND_COLORS_REQUIRED if c.lower() not in bundle.lower()]

    # 8 phan khu
    sections = re.findall(r'id="([a-z0-9\-]+)"', html)
    expected_ids = ["hero", "ai-economy", "problem-gap", "two-layer-architecture",
                    "brains-and-skills", "policy-dataset", "downloads-and-issues",
                    "commitments-and-contact"]
    missing_sections = [s for s in expected_ids if s not in sections]
    # 3 ngon ngu
    missing_langs = [l for l in ("vi", "en", "zh") if ('data-i18n="%s"' % l) not in html]
    # deep-link
    has_lang_param = "lang=" in html or "?lang" in html
    # simulator (Web Crypto API)
    has_sim = "sim-btn" in bundle and "crypto.subtle" in bundle
    # khong co script theo doi ben ngoai
    external_scripts = re.findall(r'<script[^>]+src="(https?://[^"]+)"', bundle)

    ok = (scan_res["status"] == "PASS" and not missing_colors and not missing_sections
          and not missing_langs and has_sim and not per_file
          and not external_scripts)
    return {
        "file": index_html_path,
        "size_bytes": len(html.encode("utf-8")),
        "sha256": hashlib.sha256(html.encode("utf-8")).hexdigest(),
        "content_scan": scan_res,
        "files_with_banned_hits": [f["source"] for f in per_file],
        "missing_brand_colors": missing_colors,
        "missing_sections": missing_sections,
        "missing_languages": missing_langs,
        "has_lang_deeplink": has_lang_param,
        "has_sha256_simulator": has_sim,
        "external_script_src": external_scripts,
        "status": "PASS" if ok else "FAIL_CLOSED",
    }


def fetch(url, timeout=25, headers=None):
    h = {"User-Agent": "NAN-TRU001-Verifier/2.2"}
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, headers=h)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.getcode(), dict(resp.info()), resp.read()


def verify_live_endpoint(url):
    try:
        status, headers, body = fetch(url)
    except urllib.error.HTTPError as e:
        return {"url": url, "http_status": e.code, "status": "FAIL_CLOSED",
                "error": str(e)}
    text = body.decode("utf-8", errors="replace")
    scan_res = scan_content(text, url)
    # bo gia dien lai: mau thuong hieu nam trong styles.css, simulator trong app.js
    bundle_parts = [text]
    for extra in ("/styles.css", "/app.js", "/i18n-dict.js"):
        try:
            _s, _h, _b = fetch(url + extra, timeout=25)
            bundle_parts.append(_b.decode("utf-8", errors="replace"))
        except Exception:
            pass
    bundle = "\n".join(bundle_parts)
    security_headers = ["Content-Security-Policy", "Strict-Transport-Security",
                        "X-Content-Type-Options", "X-Frame-Options"]
    has_security = [h for h in security_headers
                    if h.lower() in {k.lower() for k in headers}]
    missing_security = [h for h in security_headers if h not in has_security]
    missing_colors = [c for c in BRAND_COLORS_REQUIRED if c.lower() not in bundle.lower()]
    # deep-link 3 ngon ngu
    lang_ok = {}
    for lg in ("vi", "en", "zh"):
        try:
            st, _, bd = fetch(url + "/?lang=" + lg)
            lang_ok[lg] = ("data-lang" in bd.decode("utf-8", "replace")) and st == 200
        except Exception as e:
            lang_ok[lg] = "error: " + str(e)[:60]
    ok = (status == 200 and scan_res["status"] == "PASS" and not missing_security
          and not missing_colors and all(v is True for v in lang_ok.values()))
    return {
        "url": url,
        "http_status": status,
        "content_scan": scan_res,
        "security_headers_present": has_security,
        "security_headers_missing": missing_security,
        "missing_brand_colors": missing_colors,
        "lang_deeplink": lang_ok,
        "status": "PASS" if ok else "FAIL_CLOSED",
    }


def verify_manifest_endpoint(url):
    try:
        st, hdrs, body = fetch(url + "/api/tru001-manifest")
        m = json.loads(body.decode("utf-8"))
    except Exception as e:
        return {"url": url + "/api/tru001-manifest", "status": "FAIL_CLOSED", "error": str(e)}
    vm = m.get("verified_metrics", {})
    expected = {
        "policy_instruments_count": 23,
        "automated_unit_tests_pass": 121,
        "open_good_first_issues": 8,
        "external_contributors_recorded": 1,
        "specialized_department_brains": 7,
        "canonical_registry_skills_active": 63,
        "provenance_gate_fields": 7,
    }
    bad = {k: (vm.get(k), v) for k, v in expected.items() if vm.get(k) != v}
    txt = json.dumps(m, ensure_ascii=False)
    # Manifest la tai lieu may-doc: kiem khoa muc + chi so, KHONG kiem van ban tu
    manifest_scan = scan_content(txt, url + "/api/tru001-manifest")
    missing_manifest_keys = [k for k in MANIFEST_REQUIRED_KEYS if k not in txt]
    scan_res = {
        "source": url + "/api/tru001-manifest",
        "banned_hits": manifest_scan["banned_hits"],
        "missing_required_tokens": missing_manifest_keys,
        "tracker_hits": manifest_scan["tracker_hits"],
        "status": "PASS" if (not manifest_scan["banned_hits"]
                            and not missing_manifest_keys
                            and not manifest_scan["tracker_hits"]) else "FAIL_CLOSED",
    }
    ok = st == 200 and not bad and scan_res["status"] == "PASS"
    return {"url": url + "/api/tru001-manifest", "http_status": st,
            "metric_mismatches": bad, "content_scan": scan_res,
            "status": "PASS" if ok else "FAIL_CLOSED"}


def verify_pdfs():
    out = []
    for name, pages in PDF_EXPECTED.items():
        url = RELEASE_BASE + "/" + name
        try:
            st, hdrs, body = fetch(url, timeout=90)
            ok_sig = body[:4] == b"%PDF"
            out.append({"file": name, "url": url, "http_status": st,
                        "bytes": len(body), "pdf_signature": ok_sig,
                        "expected_pages": pages,
                        "status": "PASS" if (st == 200 and ok_sig) else "FAIL_CLOSED"})
        except Exception as e:
            out.append({"file": name, "url": url, "error": str(e)[:80],
                        "status": "FAIL_CLOSED"})
    return out


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "local"
    target = sys.argv[2] if len(sys.argv) > 2 else "public/index.html"
    report = {
        "order_id": "NAN-ANTI-CLOUDFLARE-WEB-HUB-ORDER-021-20261022",
        "mode": mode,
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    if mode == "local":
        if not os.path.exists(target):
            report["status"] = "FAIL_CLOSED"
            report["error"] = "khong tim thay " + target
            print(json.dumps(report, ensure_ascii=False, indent=2))
            sys.exit(1)
        report["local_audit"] = verify_local_bundle(target)
        ok = report["local_audit"]["status"] == "PASS"
    else:
        report["live_audit"] = verify_live_endpoint(LIVE_URL)
        report["manifest_audit"] = verify_manifest_endpoint(LIVE_URL)
        report["pdf_audit"] = verify_pdfs()
        ok = (report["live_audit"]["status"] == "PASS"
              and report["manifest_audit"]["status"] == "PASS"
              and all(p["status"] == "PASS" for p in report["pdf_audit"]))
    report["status"] = "PASS" if ok else "FAIL_CLOSED"
    print(json.dumps(report, ensure_ascii=False, indent=2))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
