import json
import re
import requests
from bs4 import BeautifulSoup

def fetch_ouest_france_immo():
    """Scrape directement les annonces de colocation à Vannes sur Ouest-France Immo"""
    url = "https://www.ouestfrance-immo.com/immobilier/location/colocation/vannes-56-56000/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    annonces = []
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            cards = soup.select(".annCard, .ann-card, article")
            for card in cards:
                link_tag = card.find("a", href=True)
                title_tag = card.select_one(".annTitre, .ann-title, h2, h3")
                price_tag = card.select_one(".annPrix, .ann-price, .price")
                
                if link_tag:
                    href = link_tag['href']
                    full_url = href if href.startswith("http") else f"https://www.ouestfrance-immo.com{href}"
                    title = title_tag.get_text(strip=True) if title_tag else "Colocation Vannes"
                    price = price_tag.get_text(strip=True) if price_tag else "N/C"
                    
                    annonces.append({
                        "source": "Ouest-France Immo",
                        "titre": title,
                        "prix": price,
                        "ville": "Vannes",
                        "url": full_url
                    })
    except Exception as e:
        print(f"Erreur Ouest-France Immo: {e}")
    return annonces

if __name__ == "__main__":
    results = fetch_ouest_france_immo()
    
    # Si aucune annonce en ligne n'est trouvée (ou en cas de blocage ponctuel)
    if not results:
        results = [
            {
                "source": "Recherche Vannes",
                "titre": "Voir toutes les colocations disponibles sur Ouest-France Immo (Vannes)",
                "prix": "Consulter",
                "ville": "Vannes",
                "url": "https://www.ouestfrance-immo.com/immobilier/location/colocation/vannes-56-56000/"
            },
            {
                "source": "Recherche Vannes",
                "titre": "Voir les petites annonces de colocation sur ParuVendu (Vannes)",
                "prix": "Consulter",
                "ville": "Vannes",
                "url": "https://www.paruvendu.fr/immobilier/location/vannes-56000/"
            }
        ]

    with open("annonces.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"Enregistré : {len(results)} éléments dans annonces.json")
