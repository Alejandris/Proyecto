from serpapi  import GoogleSearch




def buscar_google(palabra_clave, num_paginas=3):
    resultados_totales = []

    for pagina in range(num_paginas):
        params = {
            "q": palabra_clave,  # Término de búsqueda
            "hl": "es",          # Idioma español
            "gl": "co",          # Ubicación (puedes cambiarlo)
            "num": 10,           # Número de resultados por página
            "start": pagina * 10,  # Pagina actual (0, 10, 20, 30, etc.)
            "api_key": "5b53b38ed3ca5793b8c1d4e54448c0c1a7dfcb48e01f98c54339800129fbc4a5"
        }
        search = GoogleSearch(params)
        results = search.get_dict()

        if "organic_results" not in results:
            print(f"⚠ No se encontraron más resultados en la página {pagina + 1}")
            break

        # Extraer títulos, enlaces y fragmentos de texto (snippets)
        resultados_pag = [
            {
                "titulo": resultado.get("title", "Sin título"),
                "enlace": resultado.get("link", "Sin enlace"),
                "texto": resultado.get("snippet", "Sin descripción")
            }
            for resultado in results["organic_results"][:3]
        ]
        
        resultados_totales.extend(resultados_pag)

    return resultados_totales
