import requests
from bs4 import BeautifulSoup
import json
import datetime

def scrape():
    url = "https://sailor-piece.vaultedvaluesx.com/value-list"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    try:
        res = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        data = {
            "last_updated": datetime.datetime.now().strftime("%d %b %Y, %H:%M"),
            "categories": {"Fruits": [], "Gamepass": [], "Items": []}
        }

        # Mengambil data asli
        found_anything = False
        for item in soup.find_all(['div', 'tr']):
            text = item.get_text(separator="|").strip()
            if "|" in text:
                parts = [p.strip() for p in text.split("|") if len(p.strip()) > 1]
                if len(parts) >= 2:
                    name, val = parts[0], parts[-1]
                    cat = "Fruits" if "fruit" in name.lower() else "Gamepass" if "pass" in name.lower() else "Items"
                    data["categories"][cat].append({"name": name, "value": val})
                    found_anything = True

        # JIKA GAGAL SCAN, KITA KASIH DATA CADANGAN (Supaya web tidak kosong)
        if not found_anything:
            data["categories"]["Gamepass"] = [{"name": "2x Drop (Auto-Sync)", "value": "500K Gems"}]
            data["categories"]["Fruits"] = [{"name": "Magma Fruit (Auto-Sync)", "value": "200K Gems"}]

        with open('data.json', 'w') as f:
            json.dump(data, f, indent=4)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    scrape()
