import os
import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify

app = Flask(__name__)

# Ta clé ScraperAPI configurée
SCRAPER_API_KEY = "e8e19b22c8e960d28f5acaf41a191e11"


@app.route("/annonces")
def get_annonces():
    target_url = (
        "https://www.ouestfrance-immo.com/acheteur/vente/vannes-56-56000/"
    )
    # Requête passant par le proxy résidentiel de ScraperAPI
    api_url = f"http://api.scraperapi.com?api_key={SCRAPER_API_KEY}&url={target_url}"

    annonces = []

    try:
        response = requests.get(api_url, timeout=30)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            cards = soup.select(".annCard, .ann-card, article")
            for card in cards:
                link_tag = card.find("a", href=True)
                title_tag = card.select_one(".annTitre, .ann-title, h2, h3")
                price_tag = card.select_one(".annPrix, .ann-price, .price")

                if link_tag:
                    href = link_tag["href"]
                    full_url = (
                        href
                        if href.startswith("http")
                        else f"https://www.ouestfrance-immo.com{href}"
                    )
                    title = (
                        title_tag.get_text(strip=True)
                        if title_tag
                        else "Bien à vendre - Vannes"
                    )
                    price = (
                        price_tag.get_text(strip=True) if price_tag else "N/C"
                    )

                    annonces.append(
                        {
                            "source": "Ouest-France Immo",
                            "titre": title,
                            "prix": price,
                            "ville": "Vannes",
                            "url": full_url,
                        }
                    )
    except Exception as e:
        print(f"Erreur API ScraperAPI : {e}")

    # Valeur de secours si la réponse est vide
    if not annonces:
        annonces = [
            {
                "source": "Ouest-France Immo",
                "titre": "Consulter les ventes à Vannes",
                "prix": "Consulter",
                "ville": "Vannes",
                "url": "https://www.ouestfrance-immo.com/acheteur/vente/vannes-56-56000/",
            }
        ]

    return jsonify(annonces)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
