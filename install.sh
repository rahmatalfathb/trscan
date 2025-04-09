#!/bin/bash

# Update sistem dan instalasi Python 3 dan pip
echo "[*] Memperbarui sistem dan menginstal Python3 serta pip..."
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip python3-venv -y

# Membuat virtual environment (opsional)
echo "[*] Membuat virtual environment..."
python3 -m venv webscanner_env
source webscanner_env/bin/activate

# Instal dependencies Python
echo "[*] Menginstal dependencies Python..."
pip install requests beautifulsoup4 tqdm

# Instal SQLMap dan Dirsearch
echo "[*] Menginstal SQLMap dan Dirsearch..."
sudo apt install sqlmap dirsearch -y