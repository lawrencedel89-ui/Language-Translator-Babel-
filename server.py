from flask import Flask, request, jsonify
import json
import base64
import os

from worker import (
    speech_to_text,
    text_to_speech,
    watsonx_process_message
)

app = Flask(__name__)

# ---- Health check (important!) ----
@app.route("/", methods=["GET"])
def health():
    return "Server is running", 200


# ---- Speech-to-Text ----
@app.route("/speech-to-text", methods=["POST"])
def speech_to_text_route():
    audio_binary = request.data
    text = speech_to_text(audio_binary)
    return jsonify({"text": text})


# ---- Watsonx + Text-to-Speech ----
@app.route("/process-message", methods=["POST"])
def process_message_route():
    data = request.get_json()

    user_message = data.get("userMessage", "")
    voice = data.get("voice", "default")

    # Watsonx translation
    response_text = watsonx_process_message(user_message)
    response_text = os.linesep.join(
        [s for s in response_text.splitlines() if s]
    )

    # Convert to speech
    audio_binary = text_to_speech(response_text, voice)
    audio_b64 = base64.b64encode(audio_binary).decode("utf-8")

    return jsonify({
        "watsonxResponseText": response_text,
        "watsonxResponseSpeech": audio_b64
    })


# ---- Run server on port 5000 ----
if __name__ == "__main__":
    print("Starting Flask server on http://0.0.0.0:5000")
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
        use_reloader=False
    )
