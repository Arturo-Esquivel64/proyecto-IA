# proyecto-IA
uso de api con groq

* IA a utizar: llama4 
````python
from groq import Groq

client = Groq()
completion = client.chat.completions.create(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    messages=[
      {
        "role": "user",
        "content": ""
      }
    ],
    temperature=1,
    max_completion_tokens=1024,
    top_p=1,
    stream=True,
    stop=None,
)

for chunk in completion:
    print(chunk.choices[0].delta.content or "", end="")
````
identificar un estado de animo y recomendar que hacer para mejorar estado de animo
