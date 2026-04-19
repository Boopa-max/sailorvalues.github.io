import requests
from bs4 import BeautifulSoup
import json
import datetime

URL = "https://sailor-piece.vaultedvaluesx.com/value-list"

def scrape_values():
    # We pretend to be a real Chrome browser so the site doesn't block us
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(URL, headers=headers, timeout=20)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # This will hold the items we find
        scraped_data = {
            "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "categories": {
                "Fruits": [],
                "Gamepass": [],
                "Items": []
            }
        }

        # Look for the table rows or cards on the site
        # We search for any 'div' or 'tr' that looks like an item
        for item in soup.find_all(['div', 'tr']):
            text_content = item.get_text(separator='|').strip()
            
            # If the row has a value-like pattern (e.g., '100K' or 'Gems')
            if any(char.isdigit() for char in text_content) and ('|' in text_content):
                parts = text_content.split('|')
                name = parts[0].strip()
                val = parts[-1].strip()

                # Filter into your requested categories
                category = "Items"
                if "fruit" in name.lower(): category = "Fruits"
                elif "pass" in name.lower() or "2x" in name.lower(): category = "Gamepass"
                
                if len(name) > 2 and len(name) < 50: # Ignore random small text
                    scraped_data["categories"][category].append({
                        "name": name, 
                        "value": val
                    })

        with open('data.json', 'w') as f:
            json.dump(scraped_data, f, indent=4)
        print("Done! Data saved to data.json")

    except Exception as e:
        print(f"Error analyzing website: {e}")

if __name__ == "__main__":
    scrape_values()
