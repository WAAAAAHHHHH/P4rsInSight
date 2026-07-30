# P4rsInSight 🐧

**P4rsInSight** — Pardus Linux için akıllı başlangıç ve sistem yönetim uygulaması.

> *An intelligent onboarding and system management application for Pardus Linux.*

---

## 🚀 Kurulum / Installation

### Gereksinimler / Requirements
- Python 3.10+
- PySide6 6.6+

### Kurulum Adımları / Setup Steps

```bash
# 1. Bağımlılıkları kur / Install dependencies
pip install -r requirements.txt

# 2. Uygulamayı başlat / Run the application
python main.py
```

---

## ✨ Özellikler / Features

| Sayfa / Page | Açıklama / Description |
|---|---|
| 🏠 Kontrol Paneli / Dashboard | Sistem durumu, güncellemeler, tek tıkla düzeltme |
| 📦 Yazılım Merkezi / Software Center | 27+ uygulama, kategoriler, APT + Flatpak desteği |
| 🪟 Windows Alternatifleri / Windows Alternatives | 11+ Windows uygulaması → Linux alternatifleri |
| 👤 Kurulum Profilleri / Profiles | 6 profil (Öğrenci, Oyuncu, Geliştirici...) |
| 🔌 Sürücü Asistanı / Driver Assistant | Donanım tespiti + sürücü önerileri |
| 🛠️ Sistem Bakımı / Maintenance | 8 bakım aracı, tek tıkla |
| 📚 Öğrenme Merkezi / Learning Center | 8+ Linux eğitimi, başlangıç seviyesi |
| 🆘 Sorun Giderme / Troubleshooting | 7+ yaygın sorun kılavuzu |
| ⚙️ Ayarlar / Settings | Dil, tema, yazı boyutu, animasyonlar |

---

## 🌍 Desteklenen Diller / Supported Languages

🇹🇷 Türkçe • 🇬🇧 English • 🇩🇪 Deutsch • 🇫🇷 Français • 🇪🇸 Español • 🇮🇹 Italiano • 🇸🇦 العربية

---

## 🎨 Temalar / Themes

- ☀️ **Açık Tema** — Pardus Mavi (#1565C0) aksan rengiyle temiz ve modern
- 🌙 **Koyu Tema** — Göz yormayan koyu mavi tema

---

## 🔐 Güvenlik / Security

- Her komut çalıştırılmadan önce **gösterilir ve açıklanır**
- Kullanıcı onayı olmadan **hiçbir komut** çalıştırılmaz
- Terminal Öğrenme Modu her komutu öğretici şekilde gösterir

---

## 📸 Ekran Görüntüleri / Screenshots

<details>
<summary>🏠 Kontrol Paneli / Dashboard (Genişlet / Expand)</summary>
<p align="center">
  <img src="assets/screenshots/dashboard.png" alt="Kontrol Paneli" width="800">
</p>
</details>

<details>
<summary>📦 Yazılım Merkezi / Software Center (Genişlet / Expand)</summary>
<p align="center">
  <img src="assets/screenshots/software_center.png" alt="Yazılım Merkezi" width="800">
</p>
</details>

<details>
<summary>🪟 Windows Alternatifleri / Windows Alternatives (Genişlet / Expand)</summary>
<p align="center">
  <img src="assets/screenshots/windows_alternatives.png" alt="Windows Alternatifleri" width="800">
</p>
</details>

<details>
<summary>👤 Kurulum Profilleri / Profiles (Genişlet / Expand)</summary>
<p align="center">
  <img src="assets/screenshots/profiles.png" alt="Kurulum Profilleri" width="800">
</p>
</details>

<details>
<summary>🔌 Sürücü Asistanı / Driver Assistant (Genişlet / Expand)</summary>
<p align="center">
  <img src="assets/screenshots/driver_assistant.png" alt="Sürücü Asistanı" width="800">
</p>
</details>

<details>
<summary>🛠️ Sistem Bakımı / Maintenance (Genişlet / Expand)</summary>
<p align="center">
  <img src="assets/screenshots/maintenance.png" alt="Sistem Bakımı" width="800">
</p>
</details>

<details>
<summary>📚 Öğrenme Merkezi / Learning Center (Genişlet / Expand)</summary>
<p align="center">
  <img src="assets/screenshots/learning_center.png" alt="Öğrenme Merkezi" width="800">
</p>
</details>

<details>
<summary>🆘 Sorun Giderme / Troubleshooting (Genişlet / Expand)</summary>
<p align="center">
  <img src="assets/screenshots/troubleshooting.png" alt="Sorun Giderme" width="800">
</p>
</details>

<details>
<summary>⚙️ Ayarlar / Settings (Genişlet / Expand)</summary>
<p align="center">
  <img src="assets/screenshots/settings.png" alt="Ayarlar" width="800">
</p>
</details>

---

## 🗺️ Yol Haritası / Roadmap

- [x] **v1.0.0 — Temel Sürüm (Mevcut)**
  - PySide6 tabanlı modern arayüz ve koyu tema
  - Yazılım Merkezi (Flatpak + APT) ve Windows Alternatifleri
  - Donanım tespiti ve Sürücü Asistanı
  - Sistem Bakımı, Öğrenme Merkezi ve Sorun Giderme
  - Çoklu dil desteği (7 Dil)
- [ ] **v1.1.0 — Arayüz & Deneyim İyileştirmeleri**
  - [ ] Açık Tema (Light Theme) desteğinin modern bir tasarım diliyle sıfırdan yazılması
  - [ ] Sayfalar arası geçiş animasyonlarının optimize edilmesi
  - [ ] Masaüstü bildirim sistemi entegrasyonu
- [ ] **v1.2.0 — Paket Yönetimi Genişletmesi**
  - [ ] Snap paket desteği ve daha geniş yazılım kataloğu (50+ Uygulama)
  - [ ] Kullanıcı tanımlı özel kurulum profilleri (Custom Profiles) oluşturma yeteneği
- [ ] **v1.3.0 — İzleme & Güvenlik**
  - [ ] Canlı CPU/RAM/Ağ tüketim grafikleri
  - [ ] Pardus UFW (Güvenlik Duvarı) kolay yönetim arayüzü
  - [ ] Sistem yedekleme asistanı entegrasyonu (Timeshift/Rsync)

---

## 🏗️ Mimari / Architecture

```
ParsInSight/
├── main.py              # Giriş noktası
├── core/                # Çekirdek servisler (i18n, settings, system_info, package_manager)
├── ui/
│   ├── components/      # Yeniden kullanılabilir widget'lar
│   ├── pages/           # Sayfa bileşenleri
│   └── styles/          # QSS tema dosyaları
├── data/                # JSON veri dosyaları
├── i18n/                # Çeviri dosyaları
assets/
└── screenshots/         # Uygulama ekran görüntüleri
```

---

## 📜 Lisans / License

GPL-3.0 — TÜBİTAK Pardus için geliştirilmiştir.
