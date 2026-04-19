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

        # Mencari semua elemen yang kemungkinan berisi item
        items = soup.find_all(['div', 'tr', 'li'])

        for item in items:
            text = item.get_text(separator="|").strip()
            if "|" in text:
                parts = [p.strip() for p in text.split("|") if len(p.strip()) > 1]
                
                # Validasi: Harus ada Nama dan Harga (minimal 2 bagian)
                if len(parts) >= 2:
                    name = parts[0]
                    val = parts[-1]
                    
                    # Filter agar tidak memasukkan teks sampah yang kepanjangan
                    if len(name) < 25 and len(val) < 20 and any(char.isdigit() for char in val):
                        low_name = name.lower()
                        if "fruit" in low_name: cat = "Fruits"
                        elif any(x in low_name for x in ["pass", "2x", "vip"]): cat = "Gamepass"
                        else: cat = "Items"
                        
                        data["categories"][cat].append({"name": name, "value": val})

        with open('data.json', 'w') as f:
            json.dump(data, f, indent=4)
        print("Data berhasil dirapikan!")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    scrape()
