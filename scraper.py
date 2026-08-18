import json
import requests

# Configuration de la recherche (Colocation à Vannes)
URL_API = "https://api.leboncoin.fr/finder/search"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "ApiKey": "5432109876543210987654321098765432109876543210987654321098765432",
}

PAYLOAD = {
    "limit": 20,
    "filters": {
        "category": {"id": "10"},
        "enums": {"real_estate_type": ["5"]},
        "location": {"city_zipspecs": [{"zipcode": "56000"}]},
    },
}


def fetch_annonces():
    try:
        response = requests.post(URL_API, headers=HEADERS, json=PAYLOAD, timeout=10)
        response.raise_for_status()
        data = response.json()

        annonces = []
        for item in data.get("ads", []):
            annonce = {
                "id": item.get("list_id"),
                "titre": item.get("subject"),
                "prix": item.get("price", [0])[0] if item.get("price") else "N/C",
                "ville": item.get("location", {}).get("city", "Vannes"),
                "url": item.get("url"),
                "date": item.get("first_publication_date"),
                "image": item.get("images", {}).get("thumb_url"),
            }
            annonces.append(annonce)

        return annonces

    except Exception as e:
        print(f"Erreur lors de la récupération : {e}")
        return []


def save_to_json(data, filename="annonces.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"{len(data)} annonces enregistrées dans {filename}")


if __name__ == "__main__":
    results = fetch_annonces()
    save_to_json(results)
