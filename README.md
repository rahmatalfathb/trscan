# trscan
trscan (v1.0) adalah alat otomatis yang dirancang untuk melakukan pemindaian keamanan pada situs web dengan tujuan mengidentifikasi potensi kerentanannya. Alat ini menggabungkan beberapa teknik dan alat pemindaian yang populer, seperti SQL Injection (SQLi), Remote File Inclusion (RFI), Sensitive File Disclosure, dan melakukan crawling

Here are the quick steps to run trscan:

# Install Python 3 dan pip:

    sudo apt update
    sudo apt install python3 python3-pip python3-venv

Create Virtual Environment (Optional):

    python3 -m venv webscanner_env
    source webscanner_env/bin/activate

Instal Dependencies Python:

    pip install requests beautifulsoup4 tqdm
    pip install setuptools

Install SQLMap dan Dirsearch (menggunakan apt):

    sudo apt install sqlmap dirsearch


Run:

    python3 web_scanner.py [url] --verbose --crawl
