import json
import re
import requests
import xml.etree.ElementTree as ET


def fetch_ouest_france():
    """Scrape le flux Ouest-France Immo (Colocations Vannes)"""
    url = "https://www.ouestfrance-immo.com/rss/location/colocation/vannes-56-56000/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    annonces = []
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            root = ET.fromstring(resp.content)
            for item in root.findall(".//item"):
                title = item.findtext("title", "")
                link = item.findtext("link", "")
                pub_date = item.findtext("pubDate", "")

                # Extraction du prix dans le titre si présent
                prix_search = re.search(r"(\d+)\s*€", title)
                prix = int(prix_search.group(1)) if prix_search else "N/C"

                if link:
                    annonces.append(
                        {
                            "source": "Ouest-France Immo",
                            "titre": title,
                            "prix": prix,
                            "ville": "Vannes",
                            "url": link,
                            "date": pub_date[:16] if pub_date else "",
                        }
                    )
    except Exception as e:
        print(f"Erreur Ouest-France: {e}")
    return annonces


def fetch_parvendus():
    """Scrape le flux de recherche de ParVendus pour Vannes"""
    url = "https://www.paruvendu.fr/immobilier/rss/colocation/vannes-56000/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    annonces = []
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            root = ET.fromstring(resp.content)
            for item in root.findall(".//item"):
                title = item.findtext("title", "")
                link = item.findtext("link", "")
                pub_date = item.findtext("pubDate", "")

                prix_search = re.search(r"(\d+)\s*€", title)
                prix = int(prix_search.group(1)) if prix_search else "N/C"

                if link:
                    annonces.append(
                        {
                            "source": "ParuVendu",
                            "titre": title,
                            "prix": prix,
                            "ville": "Vannes",
                            "url": link,
                            "date": pub_date[:16] if pub_date else "",
                        }
                    )
    except Exception as e:
        print(f"Erreur ParuVendu: {e}")
    return annonces


if __name__ == "__main__":
    toutes_les_annonces = []

    # Aggregation des sources sans authentification
    toutes_les_annonces.extend(fetch_ouest_france())
    toutes_les_annonces.extend(fetch_parvendus())

    # Déduplication basée sur l'URL
    annonces_uniques = {a["url"]: a for a in toutes_les_annonces}.values()

    # Enregistrement dans annonces.json
    with open("annonces.json", "w", encoding="utf-8") as f:
        json.dump(list(annonces_uniques), f, ensure_ascii=False, indent=2)

    print(f"Total : {len(annonces_uniques)} annonces réelles récupérées.")
