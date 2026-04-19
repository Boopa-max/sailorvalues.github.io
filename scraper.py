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
            "categories": {"Fruits": [], "Gamepass": [], "Items": [], "Swords": []}
        }

        # Mencari semua elemen yang berisi nama dan harga
        # Catatan: Selektor ini disesuaikan dengan struktur umum web value Roblox
        for card in soup.find_all(['div', 'tr']):
            text = card.get_text(separator="|").strip()
            if "|" in text:
                parts = [p.strip() for p in text.split("|") if p.strip()]
                if len(parts) >= 2:
                    name, val = parts[0], parts[-1]
                    
                    # Logika kategori otomatis
                    cat = "Items"
                    low_name = name.lower()
                    if "fruit" in low_name or any(f in low_name for f in ["light", "magma", "dark"]): cat = "Fruits"
                    elif "pass" in low_name or "2x" in low_name: cat = "Gamepass"
                    elif "sword" in low_name or "blade" in low_name: cat = "Swords"
                    
                    if len(name) < 40 and any(char.isdigit() for char in val):
                        data["categories"][cat].append({"name": name, "value": val})

        with open('data.json', 'w') as f:
            json.dump(data, f, indent=4)
        print("Scrape Success!")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    scrape()
