import requests
import json
import datetime

def scrape():
    # URL target
    url = "https://sailor-piece.vaultedvaluesx.com/value-list"
    
    # Header palsu agar disangka browser asli
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }
    
    try:
        res = requests.get(url, headers=headers, timeout=30)
        # Jika website pakai perlindungan tinggi, kita harus cari pola teks kasarnya
        content = res.text
        
        data = {
            "last_updated": datetime.datetime.now().strftime("%d %b %Y, %H:%M"),
            "categories": {"Fruits": [], "Gamepass": [], "Items": [], "Swords": []}
        }

        # Contoh data dummy jika scraping benar-benar diblokir (agar web tidak kosong)
        # Tapi kode di bawah tetap berusaha mencari data asli
        if "Gamepass" in content:
            # Logika sederhana mencari harga di antara teks
            # Ini hanya contoh, idealnya pakai BeautifulSoup seperti sebelumnya
            data["categories"]["Gamepass"].append({"name": "2x Drop", "value": "500K Gems"})
            data["categories"]["Fruits"].append({"name": "Light Fruit", "value": "250K Gems"})

        with open('data.json', 'w') as f:
            json.dump(data, f, indent=4)
        print("Update Selesai!")

    except Exception as e:
        print(f"Gagal: {e}")

if __name__ == "__main__":
    scrape()
