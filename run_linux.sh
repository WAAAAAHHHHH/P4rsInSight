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
if [ ! -d ".venv" ]; then
    echo "📦 Sanal ortam (.venv) oluşturuluyor..."
    python3 -m venv .venv
    if [ $? -ne 0 ]; then
        echo "❌ Hata: Sanal ortam oluşturulamadı. 'python3-venv' paketinin yüklü olduğundan emin olun."
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
