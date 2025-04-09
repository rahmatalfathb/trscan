Here are the quick steps to run Web Security Scanner on Kali Linux:

    Install Python 3 dan pip:

sudo apt update
sudo apt install python3 python3-pip python3-venv

Buat Virtual Environment (Opsional):

python3 -m venv webscanner_env
source webscanner_env/bin/activate

Instal Dependencies Python:

pip install requests beautifulsoup4 tqdm

Install SQLMap dan Dirsearch (menggunakan apt):

sudo apt install sqlmap dirsearch

Scan:

python3 web_scanner.py http://bisnis.lrtjakarta.co.id --verbose --crawl
