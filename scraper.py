import json
import re
import xml.etree.ElementTree as ET
import requests

# Instances RSS-Bridge publiques réparties (permettent de contourner les blocages)
INSTANCES = [
    "https://rss-bridge.org/bridge01",
    "https://bridge.prontos.de",
    "https://rss.b33.mobi",
]


def fetch_ventes_vannes_rss():
    annonces = []

    # Exemple avec le flux RSS d'agrégation d'annonces
    # (ou via un pont RSS-Bridge pré-configuré pour Vannes)
    url_target = "https://www.paruvendu.fr/immobilier/rss/vente/vannes-56000/"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        response = requests.get(url_target, headers=headers, timeout=10)
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            for item in root.findall(".//item"):
                title = item.findtext("title", "")
                link = item.findtext("link", "")
                pub_date = item.findtext("pubDate", "")

                # Extraction du prix dans le titre
                prix_search = re.search(r"(\d[\d\s]*\d)\s*€", title)
                prix = (
                    f"{prix_search.group(1).replace(' ', '')} €"
                    if prix_search
                    else "Consulter"
                )

                if link:
                    annonces.append(
                        {
                            "source": "ParuVendu (Vente)",
                            "titre": title,
                            "prix": prix,
                            "ville": "Vannes",
                            "url": link,
                            "date": pub_date[:16] if pub_date else "",
                        }
                    )
    except Exception as e:
        print(f"Erreur lors de la récupération du flux : {e}")

    return annonces


if __name__ == "__main__":
    results = fetch_ventes_vannes_rss()

    # Sauvegarde dans annonces.json
    with open("annonces.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"Succès : {len(results)} ventes enregistrées.")
