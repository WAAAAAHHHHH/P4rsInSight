#!/bin/bash
# P4rsInSight - Linux Launch Script
# Automatically sets up python virtual environment, installs dependencies, and runs the application.

# Navigate to the script's directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "🐧 P4rsInSight Linux Başlatıcı..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Hata: Python 3 yüklü değil. Lütfen sisteminize Python 3 kurun."
    read -p "Çıkmak için Enter'a basın..."
    exit 1
fi

# Setup virtual environment if not present
# First check if python3-venv is installed, if not, try to install it
if ! python3 -c "import venv" &> /dev/null; then
    echo "📦 'python3-venv' paketi eksik. Otomatik yükleniyor (sudo yetkisi gerekebilir)..."
    sudo apt update && sudo apt install -y python3-venv
    if [ $? -ne 0 ]; then
        echo "❌ Hata: 'python3-venv' paketi yüklenemedi. Lütfen terminalden elle yüklemeyi deneyin."
        read -p "Çıkmak için Enter'a basın..."
        exit 1
    fi
fi

# Clean up any broken or incomplete .venv folder
if [ -d ".venv" ] && [ ! -f ".venv/bin/activate" ]; then
    echo "🧹 Bozuk sanal ortam (.venv) temizleniyor..."
    rm -rf .venv
fi

if [ ! -d ".venv" ]; then
    echo "📦 Sanal ortam (.venv) oluşturuluyor..."
    python3 -m venv .venv
    if [ $? -ne 0 ]; then
        echo "❌ Hata: Sanal ortam oluşturulamadı."
        read -p "Çıkmak için Enter'a basın..."
        exit 1
    fi
fi

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
echo "📥 Bağımlılıklar kontrol ediliyor..."
pip install -r ParsInSight/requirements.txt

# Run the app
echo "🚀 P4rsInSight başlatılıyor..."
python3 ParsInSight/main.py "$@"
