from flask import Blueprint, Flask, request, jsonify
from models.SearchGoogle import buscar_google  # Importa la función que hace la búsqueda en Google
from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup
import random
from flask_cors import CORS

scrape = Blueprint('scrape', __name__)
CORS(scrape)  # Habilitar CORS para todas las rutas

TAGS_TO_SEARCH = ["p", "div", "span", "article", "section", "h1", "h2", "h3", "h4", "h5", "h6"]
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/92.0",
]

def scrape_site(url, keywords):
    try:
        headers = {"User-Agent": random.choice(USER_AGENTS)}
        response = requests.get(url, timeout=10, headers=headers)
        
        if response.status_code != 200:
            return {"url": url, "error": f"HTTP {response.status_code}"}

        soup = BeautifulSoup(response.text, 'html.parser')
        extracted_texts = []

        for tag in TAGS_TO_SEARCH:
            elements = soup.find_all(tag)
            for element in elements:
                text = element.get_text().strip()
                if any(keyword.lower() in text.lower() for keyword in keywords):
                    extracted_texts.append({
                        "tag": tag,
                        "id": element.get("id", ""),
                        "text": text
                    })
        for element in soup.find_all(True):  # Encuentra cualquier etiqueta HTML
            element_class = element.get("class", "")
            element_id = element.get("id", "")

            if any(keyword.lower() in str(element_class).lower() for keyword in keywords) or \
               any(keyword.lower() in str(element_id).lower() for keyword in keywords):

                extracted_texts.append({
                    "tag": element.name,
                    "class": element_class,
                    "id": element_id,
                    "text": element.get_text().strip()
                })

        return {"url": url, "matches": extracted_texts}

    except Exception as e:
        return {"url": url, "error": str(e)}

@scrape.route('/scrape', methods=['POST'])
def search_and_scrape():
    """
    Endpoint que realiza la búsqueda en Google y el scraping de las URLs encontradas, todo en una sola solicitud POST.
    """
    print('Solicitud recibida en /scrape')
    data = request.get_json()  # Obtén los datos en formato JSON
    print('Datos recibidos:', data)
    keyword = data.get('keyword')  # Extrae la palabra clave
    pages = data.get('pages', 1)  # Obtiene el número de páginas (por defecto 1)

    if not keyword:
        return jsonify({"error": "Se requiere una palabra clave para la búsqueda"}), 400

    try:
        # Paso 1: Realizar la búsqueda en Google con la función buscar_google
        search_results = buscar_google(keyword, num_paginas=pages)
        fetched_links = [result['enlace'] for result in search_results]
    
        if not fetched_links:
            return jsonify({"error": "No se encontraron resultados de búsqueda relevantes"}), 404
        else:
            print(f"Se encontraron {len(fetched_links)} enlaces relevantes.")
        # Paso 2: Realizar scraping en las URLs obtenidas
        results = []
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = {executor.submit(scrape_site, url, [keyword]): url for url in fetched_links}
            for future in futures:
                results.append(future.result())

        return jsonify({"results": results})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


