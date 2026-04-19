import requests
from bs4 import BeautifulSoup
import json
import datetime

URL = "https://sailor-piece.vaultedvaluesx.com/value-list"

def scrape_values():
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(URL, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        data_structure = {
            "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "categories": {"Fruits": [], "Gamepass": [], "Items": [], "Swords": []}
        }

        # This looks for any 'row' or 'container' commonly used in value lists
        items_found = soup.find_all(['div', 'tr'], class_=lambda x: x and ('item' in x or 'row' in x))

        for item in items_found:
            # Try to find the name and value inside the item
            name_tag = item.find(['h3', 'b', 'strong', 'td'])
            value_tag = item.find_all(['p', 'span', 'td'])[-1] # Usually the last text is the value
            
            if name_tag and value_tag:
                name = name_tag.text.strip()
                val = value_tag.text.strip()
                
                # Filter into categories based on keywords
                cat = "Items"
                if any(x in name.lower() for x in ["fruit", "light", "magma"]): cat = "Fruits"
                elif any(x in name.lower() for x in ["pass", "2x", "vip"]): cat = "Gamepass"
                
                data_structure["categories"][cat].append({"name": name, "value": val})

        with open('data.json', 'w') as f:
            json.dump(data_structure, f, indent=4)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    scrape_values()
