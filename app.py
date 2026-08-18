import os
import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify

app = Flask(__name__)

SCRAPER_API_KEY = "e8e19b22c8e960d28f5acaf41a191e11"


@app.route("/annonces")
def get_annonces():
    target_url = (
        "https://www.ouestfrance-immo.com/acheteur/vente/vannes-56-56000/"
    )
    # render=true force ScraperAPI a exécuter le JavaScript de la page
    api_url = f"http://api.scraperapi.com?api_key={SCRAPER_API_KEY}&url={target_url}&render=true"

    annonces = []

    try:
        response = requests.get(api_url, timeout=60)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            # Recherche de tous les liens pointant vers une fiche produit/annonce
            for a_tag in soup.find_all("a", href=True):
                href = a_tag["href"]
                if "/immobilier/vente/" in href or "/annonce-" in href:
                    full_url = (
                        href
                        if href.startswith("http")
                        else f"https://www.ouestfrance-immo.com{href}"
                    )
                    title = a_tag.get_text(strip=True)

                    if len(title) > 10 and not any(
                        x["url"] == full_url for x in annonces
                    ):
                        annonces.append(
                            {
                                "source": "Ouest-France Immo",
                                "titre": title,
                                "prix": "Voir annonce",
                                "ville": "Vannes",
                                "url": full_url,
                            }
                        )
    except Exception as e:
        print(f"Erreur API ScraperAPI : {e}")

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
