# NAN AI2AI-SI2SI — Makefile
#
# Quy tac: ZERO CASH (0 VND) — moi lenh deu chay bang cong cu san co cua he thong.

PYTHON ?= python
PIP    ?= pip

.PHONY: help license-check license-report license-notices test demo scan-license clean

help: ## Hien thi danh sach muc tieu
	@echo "NAN AI2AI-SI2SI — Muc tieu Makefile:"
	@echo "  make license-check    Kiem tra license (dependency + SPDX header) — exit 1 neu co vi pham"
	@echo "  make license-report   Sinh lai THIRD_PARTY_NOTICES.md tu pip-licenses"
	@echo "  make license-notices  Sinh lai THIRD_PARTY_NOTICES.md qua license_gate.py"
	@echo "  make scan-license     Quet ma nguon bang ScanCode"
	@echo "  make test             Chay bo kiem thu don vi"
	@echo "  make demo             Chay demo hello_bridge.py"

license-check: ## Cong kiem tra license
	$(PYTHON) scripts/license_gate.py

license-report: ## Sinh lai THIRD_PARTY_NOTICES.md
	$(PIP) install --quiet pip-licenses
	pip-licenses --format=markdown --with-urls > THIRD_PARTY_NOTICES.md

license-notices: ## Sinh lai THIRD_PARTY_NOTICES.md qua license_gate.py
	$(PYTHON) scripts/license_gate.py --update-notices

scan-license: ## Quet ma nguon bang ScanCode
	$(PIP) install --quiet scancode-toolkit
	scancode -clpi --json-pp license_scan.json --quiet .

test: ## Chay bo kiem thu don vi
	$(PYTHON) -m unittest discover -s tests -v

demo: ## Chay demo
	$(PYTHON) examples/01-hello-agent/hello_bridge.py

clean: ## Xoa file sinh ra
	rm -f license_scan.json license_gate_report.json
