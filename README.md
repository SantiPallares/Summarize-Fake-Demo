# API de FastAPI en Python

Esta es una API de FastAPI desarrollada en Python que te permite realizar búsquedas de contenido en películas y obtener las escenas más relevantes. Esta API utiliza tecnologías como Streamlit, SpaCy y Google Translator para proporcionar resultados precisos y relevantes.

## Requisitos

Asegúrate de tener Python 3.9.16 o una versión superior instalada en tu sistema. También necesitarás instalar las dependencias listadas en el archivo `requirements.txt`. Puedes hacerlo utilizando pip:

```bash
pip install -r requirements.txt
```

# Cómo usar la API

1. Clona este repositorio en tu máquina local:

```bash
git clone <URL del repositorio>
```
2. Navega a la carpeta del proyecto:
```bash
cd <nombre del proyecto>
```

3. Construye y ejecuta el contenedor de Docker para la API:
```bash
docker-compose up --build
```

4. La API estará disponible en http://localhost:8502. Puedes acceder a la interfaz de usuario a través de tu navegador web.

5. Ingresa una consulta en el campo de texto proporcionado y haz clic en el botón de búsqueda.

6. La API devolverá los resultados de las películas que mejor coinciden con tu consulta, así como las escenas más relevantes dentro de esas películas.

