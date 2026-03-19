from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

OLLAMA_URL = "http://localhost:11434/api/generate"

def generar_respuesta(prompt):
    response = requests.post(OLLAMA_URL, json={
    "model": "phi3",
    "prompt": prompt,
    "stream": False,
    "options": {
        "temperature": 0.2,
        "num_predict": 100
    }
})

    data = response.json()

    if "response" not in data:
        print("ERROR OLLAMA:", data)
        return "Error generando respuesta. Revisá Ollama."

    return data["response"]

@app.route("/propuesta", methods=["POST"])
def propuesta():
    data = request.json
    user_input = data["input"]

    prompt = f"""
Sos un freelancer real que responde clientes.

NO repitas el pedido.
NO expliques nada.
Escribí una propuesta corta, clara y lista para copiar.
Tu tarea es responder con una propuesta para vender.

Pedido:
{user_input}

IMPORTANTE:
- NO digas "Creo" dí "Diseño".
- NO repitas el pedido.
- NO inventes introducciones.
- NO dejes campos vacíos.
- TODO debe estar completo.
- No usar "ofrecemos".
- No sonar formal.
- Precio en USD obligatorio.
- Tiempo concreto obligatorio.
- Cierre directo (para cerrar venta)

Formato EXACTO y OBLIGATORIO (copiar y completar):

Qué hago: ...
Tiempo: ...
Precio: ... USD
Cierre: ...

EJEMPLO DEL FORMATO:
Qué hago: Diseño un logo moderno y profesional para tu marca.
Tiempo: 3 días
Precio: 150 USD
Cierre: Si querés algo claro y rápido, lo hago.

Reglas:
- Máximo 50 palabras.
- Español simple.
- Todo concreto (números reales)
- Nada de texto extra.
- Sin errores de escritura.
- Sonar natural (como humano)
- NO agregues formas raras de hablar, siempre de forma cotidiana y neutral.
- NO usar COMILLAS.
- UN CIERRE DE VENTA RESUMIDO, SIMPLE Y EFICAZ.

Si no seguís el formato exacto, está mal.
"""

    respuesta = generar_respuesta(prompt)
    return jsonify({"respuesta": respuesta})


@app.route("/respuesta", methods=["POST"])
def respuesta_cliente():
    data = request.json
    user_input = data["input"]

    prompt = f"""
Actúa como un freelancer experto.

Responde este mensaje de cliente de forma profesional y persuasiva:

{user_input}
"""

    respuesta = generar_respuesta(prompt)
    return jsonify({"respuesta": respuesta})


@app.route("/precio", methods=["POST"])
def precio():
    data = request.json
    user_input = data["input"]

    prompt = f"""
Sos experto en precios freelance.

Basado en este pedido:

{user_input}

Decí:
- Precio recomendado en USD
- Rango
- Justificación breve
"""

    respuesta = generar_respuesta(prompt)
    return jsonify({"respuesta": respuesta})


if __name__ == "__main__":
    app.run(debug=True)

