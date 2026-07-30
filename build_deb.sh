#!/bin/bash
# P4rsInSight - Debian Package Creator
# Compiles the app with PyInstaller and packages it into a .deb file.

echo "📦 Debian paketi oluşturma süreci başlıyor..."

# 1. Install pyinstaller inside virtual environment if not present
if [ ! -d ".venv" ]; then
    echo "❌ Hata: Sanal ortam (.venv) bulunamadı. Lütfen önce ./run_linux.sh çalıştırın."
    exit 1
fi

source .venv/bin/activate
pip install pyinstaller

# 2. Compile using PyInstaller
echo "🚀 PyInstaller ile derleniyor..."
cd ParsInSight
pyinstaller --clean ParsInSight.spec
cd ..

if [ ! -f "ParsInSight/dist/ParsInSight" ]; then
    echo "❌ Hata: Derleme başarısız oldu!"
    exit 1
fi

# 3. Create Debian structure
echo "📂 Debian paket yapısı kuruluyor..."
PKG_DIR="parsinsight_1.0.0_amd64"
rm -rf "$PKG_DIR"
mkdir -p "$PKG_DIR/DEBIAN"
mkdir -p "$PKG_DIR/opt/parsinsight"
mkdir -p "$PKG_DIR/usr/share/applications"
mkdir -p "$PKG_DIR/usr/bin"

# 4. Create DEBIAN/control file
cat <<EOT > "$PKG_DIR/DEBIAN/control"
Package: parsinsight
Version: 1.0.0
Section: utils
Priority: optional
Architecture: amd64
Maintainer: TUBITAK Pardus
Description: Pardus Linux akilli baslangic ve sistem yonetim uygulamasi.
EOT

# 5. Copy files
echo "💾 Dosyalar kopyalanıyor..."
# Copy the compiled single executable binary
cp ParsInSight/dist/ParsInSight "$PKG_DIR/opt/parsinsight/"

# Create launcher script in /usr/bin
cat <<EOT > "$PKG_DIR/usr/bin/parsinsight"
#!/bin/bash
/opt/parsinsight/ParsInSight "\$@"
EOT
chmod +x "$PKG_DIR/usr/bin/parsinsight"

# Create desktop entry
cat <<EOT > "$PKG_DIR/usr/share/applications/parsinsight.desktop"
[Desktop Entry]
Name=P4rsInSight
Comment=Pardus Linux için akıllı başlangıç ve sistem yönetim uygulaması
Exec=/usr/bin/parsinsight
Icon=utilities-system-monitor
Terminal=false
Type=Application
Categories=System;Utility;
StartupNotify=true
EOT

# 6. Build the package
echo "🛠️ dpkg-deb ile paketleniyor..."
dpkg-deb --build "$PKG_DIR"

# Clean up
rm -rf "$PKG_DIR"

echo "✅ Tamamlandı! '${PKG_DIR}.deb' dosyası oluşturuldu."
