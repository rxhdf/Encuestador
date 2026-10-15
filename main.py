import requests
from bs4 import BeautifulSoup
import random
import time
import re
import json

def ejecutar_bot_encuestas(url_form, funcion_log, total_encuestas):
    url_response = url_form.replace("viewform", "formResponse")
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    preguntas_mapeadas = []

    funcion_log("Analizando la estructura del formulario...")    
    response = requests.get(url_form, headers=headers)

    if response.status_code != 200:
        funcion_log("Error: No se pudo acceder al formulario.")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    match = re.search(r'FB_PUBLIC_LOAD_DATA_ = (.*?);</script>', response.text)

    if match:
        try:
            data_bruta = json.loads(match.group(1))
            items = data_bruta[1][1]

            for item in items:
                titulo_pregunta = item[1]
                tipo_pregunta = item[3]

                opciones = []
                entry_id = None

                if item[4]:
                    for sub in item[4]:
                        if sub[0]:
                            entry_id = f"entry.{sub[0]}"
                        if sub[1]:
                            opciones.extend([opt[0] for opt in sub[1]])

                if entry_id:
                    preguntas_mapeadas.append({
                        "id": entry_id,
                        "tipo": tipo_pregunta,
                        "opciones": opciones
                    })
            funcion_log(f"✔ Se mapearon {len(preguntas_mapeadas)} preguntas.")
        except Exception as e:
            funcion_log(f"Error procesando los datos internos: {e}")
            return
    else:
        funcion_log("No se pudo extraer el bloque de preguntas.")
        return

    funcion_log(f"Iniciando el envío de {total_encuestas} encuestas...\n")

    for i in range(1, total_encuestas + 1):
        payload = {}

        for pregunta in preguntas_mapeadas:
            entry_id = pregunta["id"]
            opciones = pregunta["opciones"]
            cantidad_opciones = len(opciones)
            
            if cantidad_opciones == 3:
                    pesos = [0.60, 0.30, 0.10]  # 60% la primera, 30% la segunda, 10% la tercera
            elif cantidad_opciones == 2:
                pesos = [0.75, 0.25]        # 75% la primera, 25% la segunda
            elif cantidad_opciones >= 4:
                # Genera una curva decreciente automática para 4 o más opciones
                pesos = [1 / (idx + 1) for idx in range(cantidad_opciones)]
            else:
                pesos = [1.0 / cantidad_opciones] * cantidad_opciones

            # Selección aleatoria basada en los pesos definidos
            respuesta_elegida = random.choices(opciones, weights=pesos, k=1)[0]
            payload[entry_id] = respuesta_elegida


        envio = requests.post(url_response, data=payload, headers=headers)

        if envio.status_code == 200:
            funcion_log(f"Encuesta {i}/{total_encuestas} enviada con éxito")
        else:
            funcion_log(f"Error en la encuesta {i}. Código http: {envio.status_code}")

        time.sleep(0.5)

    funcion_log("¡Proceso finalizado con éxito!")
