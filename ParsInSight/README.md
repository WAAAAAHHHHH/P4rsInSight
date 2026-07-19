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

| Sayfa | Açıklama |
|-------|----------|
| 🏠 Kontrol Paneli | Sistem durumu, güncellemeler, tek tıkla düzeltme |
| 📦 Yazılım Merkezi | 27+ uygulama, kategoriler, APT + Flatpak desteği |
| 🪟 Windows Alternatifleri | 11+ Windows uygulaması → Linux alternatifleri |
| 👤 Kurulum Profilleri | 6 profil (Öğrenci, Oyuncu, Geliştirici...) |
| 🔌 Sürücü Asistanı | Donanım tespiti + sürücü önerileri |
| 🛠️ Sistem Bakımı | 8 bakım aracı, tek tıkla |
| 📚 Öğrenme Merkezi | 8+ Linux eğitimi, başlangıç seviyesi |
| 🆘 Sorun Giderme | 7+ yaygın sorun kılavuzu |
| ⚙️ Ayarlar | Dil, tema, yazı boyutu, animasyonlar |

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
└── i18n/                # Çeviri dosyaları
```

---

## 📜 Lisans / License

GPL-3.0 — TÜBİTAK Pardus için geliştirilmiştir.
