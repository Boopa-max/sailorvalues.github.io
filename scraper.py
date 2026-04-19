import requests
from bs4 import BeautifulSoup
import json
import datetime

# The URL you provided
URL = "https://sailor-piece.vaultedvaluesx.com/value-list"

def scrape_values():
    try:
        response = requests.get(URL, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # This dictionary will hold our categorized data
        data_structure = {
            "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "categories": {
                "Gamepass": [],
                "Fruits": [],
                "Items": [],
                "Swords": []
            }
        }

        # Logic to find items based on the site's structure
        # Note: We look for containers that likely hold the name and value
        for card in soup.find_all(['div', 'tr'], class_=['item', 'value-row']):
            name = card.find(['h3', 'td', 'span'], class_='name').text.strip()
            val = card.find(['p', 'td', 'span'], class_='value').text.strip()
            
            # Simple keyword matching to sort them into categories
            category = "Items"
            if any(x in name.lower() for x in ["gamepass", "2x", "drop"]): category = "Gamepass"
            elif any(x in name.lower() for x in ["fruit", "light", "quake"]): category = "Fruits"
            elif any(x in name.lower() for x in ["sword", "katana", "blade"]): category = "Swords"
            
            data_structure["categories"][category].append({
                "name": name,
                "value": val,
                "rarity": "Legendary" # Default or scraped if available
            })

        with open('data.json', 'w') as f:
            json.dump(data_structure, f, indent=4)
        print("Successfully updated data.json")

    except Exception as e:
        print(f"Error scraping: {e}")

if __name__ == "__main__":
    scrape_values()
