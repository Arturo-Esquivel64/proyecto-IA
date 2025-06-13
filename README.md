# proyecto-IA
uso de api con groq

# Proyecto de practica 
Dentro de este proyecto buscaremos que nuestro usuario pueda subir una imagen y tener un consejo de la ia sobre su estado de animo

## CODIGO DE GROQ

````
from groq import Groq
import base64

# Configura tu clave de API aquí
API_KEY = "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"

# Carga la imagen local como base64
with open("mi_imagen.jpg", "rb") as img_file:
    base64_img = base64.b64encode(img_file.read()).decode("utf-8")
IMAGE_DATA_URL = f"data:image/jpeg;base64,{base64_img}"

# Crear cliente con tu clave
client = Groq(api_key=API_KEY)

# Crear y enviar la solicitud
completion = client.chat.completions.create(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "dime mi estado de ánimo y dame un consejo"},
                {"type": "image_url", "image_url": {"url": IMAGE_DATA_URL}},
            ]
        }
    ],
    temperature=0.5,
    max_completion_tokens=5750,
    top_p=1,
    stream=True,
)

# Mostrar respuesta por partes
for chunk in completion:
    print(chunk.choices[0].delta.content or "", end="")


````

## CODIGO CURL
````
curl "https://api.groq.com/openai/v1/chat/completions" \
  -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${GROQ_API_KEY}" \
  -d '{
         "messages": [
           {
             "role": "user",
             "content": [
               {
                 "type": "text",
                 "text": "dime mi estado de animo y dime un consejo. \n"
               },
               {
                 "type": "image_url",
                 "image_url": {
                   "url": "'"${IMAGE_DATA_URL}"'"
                 }
               }
             ]
           }
         ],
         "model": "meta-llama/llama-4-scout-17b-16e-instruct",
         "temperature": 0.5,
         "max_completion_tokens": 5750,
         "top_p": 1,
         "stream": true,
         "stop": null
       }'
````

## COdigo de app.py 
````
import web
import base64
import json
import requests
import os

# API KEY Groq (¡NO expongas tu clave en producción!)
GROQ_API_KEY = "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"

urls = ("/", "Index")
app = web.application(urls, globals())

render = web.template.render("templates/")

class Index:
    def GET(self):
        return render.index(result=None, error=None, image_data_url=None)

    def POST(self):
        try:
            user_data = web.input(image_file={})
            image_file = user_data.get("image_file")

            if not hasattr(image_file, 'file') or not getattr(image_file, 'filename', None):
                return render.index(result=None, error="No se subió ningún archivo.", image_data_url=None)

            image_bytes = image_file.file.read()
            import mimetypes
            mime_type, _ = mimetypes.guess_type(image_file.filename)
            if not mime_type:
                mime_type = "application/octet-stream"
            base64_img = base64.b64encode(image_bytes).decode("utf-8")
            image_data_url = f"data:{mime_type};base64,{base64_img}"

            message_payload = {
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "dime mi estado de animo y dime un consejo. \n"
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": image_data_url
                                }
                            }
                        ]
                    }
                ],
                "model": "meta-llama/llama-4-scout-17b-16e-instruct",
                "temperature": 0.5,
                "max_completion_tokens": 5750,
                "top_p": 1,
                "stream": False,
                "stop": None
            }

            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            }

            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                data=json.dumps(message_payload)
            )
            if response.status_code == 200:
                result = response.json()["choices"][0]["message"]["content"]
                return render.index(result=result, error=None, image_data_url=image_data_url)
            else:
                error_msg = f"Error al conectarse a la IA: {response.status_code} - {response.text}"
                print(error_msg)
                return render.index(result=None, error=error_msg, image_data_url=image_data_url)
        except Exception as e:
            error_msg = f"Error en la petición: {str(e)}"
            print(error_msg)
            return render.index(result=None, error=error_msg, image_data_url=None)

if __name__ == "__main__":
    app.run()
import web
import base64
import json
import requests
import os

# API KEY Groq (¡NO expongas tu clave en producción!)
GROQ_API_KEY = "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"

urls = ("/", "Index")
app = web.application(urls, globals())

render = web.template.render("templates/")

class Index:
    def GET(self):
        return render.index(result=None, error=None, image_data_url=None)

    def POST(self):
        try:
            user_data = web.input(image_file={})
            image_file = user_data.get("image_file")

            if not hasattr(image_file, 'file') or not getattr(image_file, 'filename', None):
                return render.index(result=None, error="No se subió ningún archivo.", image_data_url=None)

            image_bytes = image_file.file.read()
            import mimetypes
            mime_type, _ = mimetypes.guess_type(image_file.filename)
            if not mime_type:
                mime_type = "application/octet-stream"
            base64_img = base64.b64encode(image_bytes).decode("utf-8")
            image_data_url = f"data:{mime_type};base64,{base64_img}"

            message_payload = {
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "dime mi estado de animo y dime un consejo. \n"
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": image_data_url
                                }
                            }
                        ]
                    }
                ],
                "model": "meta-llama/llama-4-scout-17b-16e-instruct",
                "temperature": 0.5,
                "max_completion_tokens": 5750,
                "top_p": 1,
                "stream": False,
                "stop": None
            }

            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            }

            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                data=json.dumps(message_payload)
            )
            if response.status_code == 200:
                result = response.json()["choices"][0]["message"]["content"]
                return render.index(result=result, error=None, image_data_url=image_data_url)
            else:
                error_msg = f"Error al conectarse a la IA: {response.status_code} - {response.text}"
                print(error_msg)
                return render.index(result=None, error=error_msg, image_data_url=image_data_url)
        except Exception as e:
            error_msg = f"Error en la petición: {str(e)}"
            print(error_msg)
            return render.index(result=None, error=error_msg, image_data_url=None)

if __name__ == "__main__":
    app.run()
````


## codigo de index.html
````
$def with (result=None, error=None, image_data_url=None)
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Analiza tu estado de ánimo</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f7f7f7; }
        .container { background: #fff; padding: 30px; border-radius: 8px; max-width: 500px; margin: auto; box-shadow: 0 2px 8px #ccc; }
        h1 { color: #333; }
        .resultado { margin-top: 20px; padding: 15px; background: #e3f7e3; border-radius: 5px; }
        .error { margin-top: 20px; padding: 15px; background: #ffe3e3; border-radius: 5px; color: #b00; }
        .imagen { margin-top: 20px; text-align: center; }
        .imagen img { max-width: 100%; border-radius: 8px; box-shadow: 0 1px 4px #aaa; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Sube una imagen para analizar tu estado de ánimo</h1>
        <form method="POST" enctype="multipart/form-data">
            <input type="file" name="image_file" accept="image/*" required>
            <button type="submit">Analizar</button>
        </form>
        <hr>
        $if image_data_url:
            <div class="imagen">
                <strong>Imagen subida:</strong><br>
                <img src="$image_data_url" alt="Imagen subida" />
            </div>
        $if error:
            <div class="error">
                <strong>Error:</strong>
                <p>$error</p>
            </div>
        $elif result:
            <div class="resultado">
                <strong>Respuesta de la IA:</strong>
                <p>$result</p>
            </div>
    </div>
</body>
</html>
````

##codigo de error.html
````
$def with (mensaje)
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Error</title>
</head>
<body>
    <h1>Error</h1>
    <p>$mensaje</p>
    <a href="/">Volver</a>
</body>
</html>
````
