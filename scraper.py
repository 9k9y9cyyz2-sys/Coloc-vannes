import json
import requests

# URL de ton micro-serveur sur Render
RENDER_URL = "https://coloc-vannes.onrender.com/annonces"


def fetch_from_render():
    try:
        response = requests.get(RENDER_URL, timeout=30)
        if response.status_code == 200:
            return response.json()
        print(f"Erreur HTTP : {response.status_code}")
    except Exception as e:
        print(f"Erreur de connexion à Render : {e}")

    # Fallback si le serveur Render dort ou ne répond pas immédiatement
    return [
        {
            "source": "Ouest-France Immo",
            "titre": "Consulter les ventes à Vannes",
            "prix": "Consulter",
            "ville": "Vannes",
            "url": "https://www.ouestfrance-immo.com/acheteur/vente/vannes-56-56000/",
        }
    ]


if __name__ == "__main__":
    data = fetch_from_render()
    with open("annonces.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Enregistré : {len(data)} annonces depuis Render.")
