# proyecto-IA
uso de api con groq

# Proyecto de practica 
Dentro de este proyecto buscaremos que nuestro usuario pueda subir una imagen y tener un consejo de la ia sobre su estado de animo

## CODIGO DE GROQ

````
from groq import Groq

client = Groq()
completion = client.chat.completions.create(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    messages=[
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "dime mi estado de animo y dime un consejo\n"
          },
          {
            "type": "image_url",
            "image_url": {
              "url": IMAGE_DATA_URL
            }
          }
        ]
      }
    ],
    temperature=0.5,
    max_completion_tokens=5750,
    top_p=1,
    stream=True,
    stop=None,
)

for chunk in completion:
    print(chunk.choices[0].delta.content or "", end="")

````
    