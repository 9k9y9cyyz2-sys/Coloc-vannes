import os
import requests
from flask import Flask, jsonify

app = Flask(__name__)

SCRAPER_API_KEY = "e8e19b22c8e960d28f5acaf41a191e11"

@app.route("/annonces")
def get_annonces():
    # URL de l'API publique de Bien'Ici pour les ventes à Vannes
    target_url = "https://www.bienici.com/realEstateAds.json?filters=%7B%22size%22%3A20%2C%22from%22%3A0%2C%22filterType%22%3A%22buy%22%2C%22propertyType%22%3A%5B%22house%22%2C%22flat%22%5D%2C%22zoneIdsByTypes%22%3A%7B%22zoneIds%22%3A%5B%22zone%3Acity%3A56260%22%5D%7D%7D"
    
    # Appel via ScraperAPI (sans JS pour rester ultra rapide)
    api_url = f"http://api.scraperapi.com?api_key={SCRAPER_API_KEY}&url={target_url}"
    
    annonces = []
    
    try:
        response = requests.get(api_url, timeout=25)
        if response.status_code == 200:
            data = response.json()
            for ad in data.get("realEstateAds", []):
                price = ad.get("price", "N/C")
                price_str = f"{price:,} €".replace(",", " ") if isinstance(price, (int, float)) else "N/C"
                
                title = ad.get("title") or f"{ad.get('propertyType', 'Bien').capitalize()} {ad.get('surfaceArea', '')} m²"
                id_ad = ad.get("id", "")
                
                annonces.append({
                    "source": "Bien'Ici",
                    "titre": title,
                    "prix": price_str,
                    "ville": "Vannes",
                    "url": f"https://www.bienici.com/annonce/{id_ad}"
                })
    except Exception as e:
        print(f"Erreur : {e}")

    # Fallback uniquement si échec complet
    if not annonces:
        annonces = [{
            "source": "Bien'Ici",
            "titre": "Consulter les ventes à Vannes",
            "prix": "Consulter",
            "ville": "Vannes",
            "url": "https://www.bienici.com/recherche/achat/vannes-56000"
        }]

    return jsonify(annonces)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
