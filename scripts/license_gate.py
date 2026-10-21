#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 NAN AI2AI-SI2SI contributors
"""
license_gate.py — CI gate kiểm tra license trước khi merge / release.

Nguyên tắc: ZERO CASH (0 VND) · READ-ONLY với mã nguồn · báo cáo rõ ràng ·
exit 0 = sạch, exit 1 = có vi phạm, exit 2 = lỗi thực thi.

Kiểm tra:
  1. DEPENDENCY — license của các package cài trong môi trường.
     Chặn: GPL / AGPL / SSPL / UNKNOWN (trừ package trong allowlist).
  2. SOURCE — mọi file mã nguồn trong repo phải có SPDX-License-Identifier.

Dùng:
  python scripts/license_gate.py                 # kiểm tra đầy đủ
  python scripts/license_gate.py --json          # xuất JSON cho CI
  python scripts/license_gate.py --skip-sources  # chỉ kiểm tra dependency
  python scripts/license_gate.py --update-notices
"""
import argparse
import csv
import io
import json
import os
import re
import subprocess
import sys

# Windows: stdout mac dinh la cp1252 — chuyen sang UTF-8 de in duoc tieng Viet co dau
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALLOWLIST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "license_gate_allowlist.txt")
NOTICES = os.path.join(REPO, "THIRD_PARTY_NOTICES.md")

BLOCKED_LICENSE_MARKERS = ("GPL", "AGPL", "SSPL")
WARN_LICENSE_MARKERS = ("LGPL",)
PERMISSIVE_MARKERS = (
    "MIT", "BSD", "APACHE", "ISC", "PSF", "PYTHON SOFTWARE FOUNDATION",
    "ZLIB", "0BSD", "MPL", "CC0", "PUBLIC DOMAIN", "ARTISTIC", "UNLICENSE",
    "PSF-2.0", "PYTHON-2.0", "PERMISSIVE", "APACHE SOFTWARE LICENSE",
    "BSD SIMPLIFIED", "BSD-DARWIN", "OTHER-PERMISSIVE", "CC-BY",
)
SOURCE_EXT = (".py", ".js", ".ts", ".go", ".sh")
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build", ".mypy_cache"}


def log(msg):
    sys.stdout.write(msg + "\n")
    sys.stdout.flush()


def read_allowlist():
    out = set()
    if os.path.exists(ALLOWLIST):
        with io.open(ALLOWLIST, encoding="utf-8") as f:
            for line in f:
                line = line.split("#", 1)[0].strip()
                if line:
                    out.add(line.lower().replace("_", "-"))
    return out


def collect_packages():
    """Lấy (name, version, license, url) từ pip-licenses; fallback sang importlib.metadata."""
    pkgs = []
    try:
        r = subprocess.run(
            ["pip-licenses", "--format=csv", "--with-urls"],
            capture_output=True, text=True, timeout=300)
        if r.returncode == 0 and r.stdout.strip():
            for row in csv.DictReader(io.StringIO(r.stdout)):
                pkgs.append({"name": row.get("Name", ""), "version": row.get("Version", ""),
                             "license": row.get("License", "") or "UNKNOWN",
                             "url": row.get("URL", "") or ""})
            if pkgs:
                return pkgs
    except Exception:
        pass
    try:
        import importlib.metadata as md
        for dist in md.distributions():
            name = (dist.metadata or {}).get("Name")
            if not name:
                continue
            lic = ""
            for cl in (dist.metadata or {}).get_all("Classifier") or []:
                if cl.startswith("License ::"):
                    lic = cl.split("::")[-1].strip()
                    break
            lic = lic or ((dist.metadata or {}).get("License") or "") or "UNKNOWN"
            pkgs.append({"name": name, "version": dist.version or "", "license": lic, "url": ""})
    except Exception:
        pass
    return pkgs


def classify(lic_raw, _depth=0):
    """Phân loại license expression. Trả về (mức, lý do).

    Biểu thức SPDX có thể lồng nhau (AND/OR trong ngoặc). Dùng đệ quy có
    giới hạn độ sâu + điều kiện "nhánh phải ngắn hơn biểu thức gốc" để
    bảo đảm luôn kết thúc, không bao giờ RecursionError.
    """
    lic = (lic_raw or "").strip()
    if not lic or lic.upper() in ("UNKNOWN", "NONE", "N/A"):
        return "UNKNOWN", "không khai báo license"
    up = lic.upper()
    if _depth >= 4:
        return "UNKNOWN", "biểu thức license quá lồng nhau — cần review thủ công"

    if "OR" in up:
        branches = [b for b in re.split(r"\s+OR\s+", lic, flags=re.I) if b.strip()]
        branches = [b for b in branches if len(b) < len(lic)]
        if branches:
            if any(classify(b, _depth + 1)[0] == "PERMISSIVE" for b in branches):
                return "PERMISSIVE", "biểu thức OR — có ít nhất một nhánh permissive"
            if any(any(m in b.upper() for m in BLOCKED_LICENSE_MARKERS) for b in branches):
                return "BLOCKED", "biểu thức OR — tất cả nhánh đều là copyleft"
    if "AND" in up:
        branches = [b for b in re.split(r"\s+AND\s+", lic, flags=re.I) if b.strip()]
        branches = [b for b in branches if len(b) < len(lic)]
        if branches:
            if any(classify(b, _depth + 1)[0] == "BLOCKED" for b in branches):
                return "BLOCKED", "biểu thức AND — có nhánh copyleft bắt buộc"
            if any(classify(b, _depth + 1)[0] == "UNKNOWN" for b in branches):
                return "UNKNOWN", "biểu thức AND — có nhánh chưa xác định"
    if any(m in up for m in BLOCKED_LICENSE_MARKERS):
        return "BLOCKED", "copyleft (GPL/AGPL/SSPL)"
    if any(m in up for m in WARN_LICENSE_MARKERS):
        return "WARN", "weak copyleft (LGPL) — cần đánh giá cách liên kết"
    if any(m in up for m in PERMISSIVE_MARKERS):
        return "PERMISSIVE", "permissive / weak-permissive"
    return "UNKNOWN", "không phân loại được — cần review thủ công"


def scan_sources():
    """Trả về danh sách file mã nguồn thiếu SPDX-License-Identifier."""
    missing, checked = [], 0
    for dp, dn, fns in os.walk(REPO):
        dn[:] = [d for d in dn if d not in SKIP_DIRS and not d.startswith(".git")]
        for fn in fns:
            if not fn.endswith(SOURCE_EXT):
                continue
            p = os.path.join(dp, fn)
            checked += 1
            try:
                with io.open(p, encoding="utf-8", errors="replace") as f:
                    head = "".join(f.readline() for _ in range(5))
            except Exception:
                continue
            if "SPDX-License-Identifier" not in head:
                missing.append(os.path.relpath(p, REPO))
    return missing, checked


def main():
    ap = argparse.ArgumentParser(description="License CI gate cho NAN AI2AI-SI2SI")
    ap.add_argument("--json", action="store_true", help="xuất kết quả dạng JSON")
    ap.add_argument("--skip-sources", action="store_true", help="bỏ qua kiểm tra SPDX trong mã nguồn")
    ap.add_argument("--update-notices", action="store_true", help="sinh lại THIRD_PARTY_NOTICES.md")
    args = ap.parse_args()

    if args.update_notices:
        pkgs = collect_packages()
        lines = ["# Third-Party Notices", "",
                 "Dự án **NAN AI2AI-SI2SI** sử dụng các thành phần mã nguồn mở sau.",
                 "Mỗi thành phần giữ nguyên giấy phép gốc của nó.", "",
                 "## Python Dependencies", ""]
        for p in sorted(pkgs, key=lambda x: x["name"].lower()):
            lines.append("- %s %s — `%s` — %s" % (p["name"], p["version"], p["license"], p["url"] or "—"))
        lines += ["", "## Cập nhật", "",
                  "File này được tạo tự động bởi `python scripts/license_gate.py --update-notices`.", ""]
        with io.open(NOTICES, "w", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(lines))
        log("Đã cập nhật %s (%d package)" % (NOTICES, len(pkgs)))
        return 0

    allow = read_allowlist()
    pkgs = collect_packages()

    dep_results = []
    for p in pkgs:
        key = (p["name"] or "").lower().replace("_", "-")
        level, reason = classify(p["license"])
        allowed = key in allow
        effective = "ALLOWED" if allowed else level
        dep_results.append({"name": p["name"], "version": p["version"],
                            "license": p["license"] or "UNKNOWN", "level": effective,
                            "raw_level": level, "reason": reason, "allowlisted": allowed})

    blocked = [d for d in dep_results if d["level"] == "BLOCKED"]
    unknown = [d for d in dep_results if d["level"] == "UNKNOWN"]
    warn = [d for d in dep_results if d["level"] == "WARN"]
    allowed_n = len([d for d in dep_results if d["level"] == "ALLOWED"])

    src_missing, src_checked = ([], 0) if args.skip_sources else scan_sources()

    if not args.json:
        log("=" * 72)
        log("NAN AI2AI-SI2SI — LICENSE GATE")
        log("=" * 72)
        log("Repo            : %s" % REPO)
        log("Allowlist       : %s (%d mục)" % (os.path.basename(ALLOWLIST), len(allow)))
        log("")
        log("[1/2] DEPENDENCY — %d package trong môi trường" % len(dep_results))
        log("      PERMISSIVE/ALLOWED : %d" % allowed_n)
        log("      WARN (LGPL)         : %d" % len(warn))
        log("      BLOCKED (copyleft)  : %d" % len(blocked))
        log("      UNKNOWN             : %d" % len(unknown))
        if blocked:
            log("")
            log("  ❌ BLOCKED — license copyleft, cần thay thế hoặc xin giấy phép thương mại:")
            for d in sorted(blocked, key=lambda x: x["name"].lower()):
                log("     - %s %s  [%s]  (%s)" % (d["name"], d["version"], d["license"], d["reason"]))
        if unknown:
            log("")
            log("  ❌ UNKNOWN — chưa xác minh được license:")
            for d in sorted(unknown, key=lambda x: x["name"].lower()):
                log("     - %s %s  [%s]" % (d["name"], d["version"], d["license"]))
        if warn:
            log("")
            log("  ⚠️  WARN — weak copyleft, cần đánh giá:")
            for d in sorted(warn, key=lambda x: x["name"].lower()):
                log("     - %s %s  [%s]" % (d["name"], d["version"], d["license"]))
        log("")
        log("[2/2] SOURCE — SPDX header trong mã nguồn repo")
        if args.skip_sources:
            log("      BỎ QUA (--skip-sources)")
        else:
            log("      File .py/.js/.ts/.go/.sh đã kiểm tra : %d" % src_checked)
            log("      Thiếu SPDX-License-Identifier          : %d" % len(src_missing))
            for m in src_missing:
                log("     - %s" % m)
        log("")
        log("-" * 72)

    failed = bool(blocked or unknown or src_missing)
    if not args.json:
        if failed:
            log("KẾT QUẢ: ❌ FAIL — cần xử lý trước khi merge/release.")
            log("")
            log("Hành động đề xuất:")
            if blocked:
                log("  1. Thay thế hoặc mua giấy phép thương mại cho các package BLOCKED.")
            if unknown:
                log("  2. Xác minh license của các package UNKNOWN và thêm vào allowlist nếu đã kiểm chứng.")
            if src_missing:
                log("  3. Thêm SPDX-License-Identifier vào %d file mã nguồn thiếu header." % len(src_missing))
        else:
            log("KẾT QUẢ: ✅ PASS — không phát hiện vi phạm license.")
        log("-" * 72)

    if args.json:
        log(json.dumps({"repo": REPO, "packages_total": len(dep_results),
                        "allowed": allowed_n, "warn": len(warn), "blocked": len(blocked),
                        "unknown": len(unknown),
                        "source_files_checked": src_checked,
                        "source_missing_spdx": src_missing,
                        "failed": failed,
                        "details": dep_results}, ensure_ascii=False, indent=1))

    return 1 if failed else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        log("LỖI THỰC THI: %s: %s" % (type(e).__name__, e))
        sys.exit(2)
