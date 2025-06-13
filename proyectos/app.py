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



