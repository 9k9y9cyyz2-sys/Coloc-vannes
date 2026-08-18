import json
import requests
import xml.etree.ElementTree as ET

# Flux RSS / Source alternative
URL_RSS = "https://www.ouestfrance-immo.com/rss/location/colocation/vannes-56-56000/"

def fetch_annonces():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    annonces = []
    
    try:
        response = requests.get(URL_RSS, headers=headers, timeout=10)
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            for item in root.findall(".//item"):
                annonces.append({
                    "titre": item.findtext("title", "Colocation Vannes"),
                    "prix": "Consulter",
                    "ville": "Vannes",
                    "url": item.findtext("link", "#"),
                    "date": item.findtext("pubDate", "")
                })
    except Exception as e:
        print(f"Erreur RSS : {e}")

    # Données par défaut si aucun flux n'a répondu
    if not annonces:
        annonces = [
            {
                "id": "1",
                "titre": "Chambre en colocation - Proche centre Vannes",
                "prix": 450,
                "ville": "Vannes",
                "url": "https://www.leboncoin.fr",
                "date": "2026-08-18"
            }
        ]

    return annonces

if __name__ == "__main__":
    data = fetch_annonces()
    with open("annonces.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"{len(data)} annonces enregistrées.")
