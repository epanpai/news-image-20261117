# BUILD LOG — news-image-20261117

- Kompetisi: news-image-20261117 "Sum up 17 November's world news in one image"
- Buka: 2026-11-17T23:43:00Z. Deadline: 2026-11-19T00:00:00Z (= 19 Nov 07:00 WIB).
- Pot $250, escrow terdanai, entry gratis, harness program/v1, 0 submisi saat screening.
- Sesi builder dimulai 18 Nov 2026 ~06:49 WIB (setelah kompetisi buka — thinking_in_window OK).

## Riset berita 17 Nov 2026 (browser.search, 18 Nov 06:50 WIB)
Sumber: Algenom daily edition 17 Nov, Level Headlines daily brief, NPR News Now 5am ET 17 Nov, FeedCast, The Daily Edition.
1. UKRAINA: serangan Ukraina ke Jembatan Kerch/Krim — bentang jalan runtuh, serangan kedua dalam <24 jam (Zelenskyy; Aksyonov konfirmasi).
2. HORMUZ: dua tanker kena ranjau laut & terbakar di selatan Selat Hormuz (IRGC navy); kapal induk AS ketiga tiba.
3. DIPLOMASI: Trump tiba di Manila untuk KTT ASEAN; pertemuan trilateral Xi–Trump–Putin dikonfirmasi Kamis 19 Nov di Shenzhen (APEC).
4. RUANG ANGKASA: roket ULA Vulcan gagal ~10 menit setelah lepas landas, 40 satelit internet Amazon Leo hancur.
5. JUGA: JPMorgan salahkan bug software untuk gangguan perbankan Senin; Nvidia laporkan earnings pertama sejak mundurnya Jensen Huang; Estonia tutup perlintasan perbatasan Rusia 1 Des atas dugaan plot sabotase.

## Rencana gambar (1024x1024, koran front page)
- Masthead "THE WORLD IN ONE DAY" + "TUESDAY, 17 NOVEMBER 2026".
- Lead: Jembatan Kerch (visual jembatan runtuh + asap).
- 3 panel: Tanker Hormuz / Trump Manila + KTT trilateral / Vulcan gagal.
- Ticker bawah: JPMorgan, Nvidia, Estonia.
- main.py (stdlib only) menyalin assets/entry.png -> /output/entry.png (deterministik).
- gen_image.py (PIL, hanya untuk build lokal) menggambar entry.png.

## Langkah
