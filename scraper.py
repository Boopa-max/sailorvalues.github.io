import requests
from bs4 import BeautifulSoup
import json
import datetime

def scrape():
    url = "https://sailor-piece.vaultedvaluesx.com/value-list"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        data = {"last_updated": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"), 
                "categories": {"Fruits": [], "Gamepass": [], "Items": []}}
        
        # Cari semua baris atau div yang ada teks harga
        for row in soup.find_all(['div', 'tr']):
            text = row.get_text(separator="|").strip()
            if "|" in text:
                parts = text.split("|")
                name, price = parts[0].strip(), parts[-1].strip()
                if len(name) < 30 and any(i.isdigit() for i in price):
                    cat = "Fruits" if "fruit" in name.lower() else "Gamepass" if "pass" in name.lower() else "Items"
                    data["categories"][cat].append({"name": name, "value": price})
        
        with open('data.json', 'w') as f:
            json.dump(data, f, indent=4)
    except:
        print("Gagal ambil data")

if __name__ == "__main__":
    scrape()
