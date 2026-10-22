# Web Hub — trang công khai NAN AI2AI

Day la **nguon su that** cua trang `https://nan-ai2ai.nexusasianetwork.workers.dev`.

## Cau truc

```
web_hub/
├── wrangler.toml    # Cloudflare Workers: assets = ./public, main = src/worker.js
├── public/          # cac file duoc phuc vu tren edge
├── src/             # worker + tu dien 3 ngon ngu (nguon su that duy nhat)
└── tests/           # script kiem toan FAIL-CLOSED
```

## Trien khai

```bash
cd web_hub
npx wrangler deploy
```

Worker: `nan-ai2ai` · `compatibility_date = 2026-10-22` · Cloudflare Workers Free Tier (chi phi 0 VND).

## Kiem toan

```bash
# kiem tra bo giao dien cuc bo (FAIL-CLOSED, exit 1 neu co vi pham)
python tests/verify_cloudflare_web_hub.py local public/index.html

# kiem tra tren URL that + manifest + 5 tep PDF cua Release v0.2.0
python tests/verify_cloudflare_web_hub.py live
```

## Nguyen tac

- **0 cum tu bi cam**: khong dung ten san pham thuong mai, khong dung cum tu da loai bo khoi danh sach tu cam cua lenh dieu hanh.
- **0 em-dash (U+2014)** trong toan bo giao dien cong khai.
- **0 tracker**: khong script theo doi, khong tai nguyen ben ngoai, khong thu vien ngoai.
- **Nguon su that duy nhat**: moi chuoi 3 ngon ngu nam trong `src/i18n-dict.js`; worker phuc vu no tai `/i18n-dict.js` va bien dich tai `/api/tru001-manifest`.
- **Chi phi 0 VND**. Khong goi von, khong ban khoa hoc.

## Rollback

```bash
npx wrangler versions list --name nan-ai2ai   # xem cac version da deploy
npx wrangler rollback --name nan-ai2ai --version-id <VERSION_ID>
```
