from flask import Flask, request, jsonify, send_from_directory
import requests

app = Flask(__name__)

MODEL = "qwen2.5:3b"
OLLAMA_URL = "http://localhost:11434/api/generate"

TASKS = {
    "summary": "Create clear, concise study notes with key points.",
    "questions": "Generate 10 important questions and their answers.",
    "flashcards": "Create 8 flashcards in Question and Answer format.",
    "quiz": "Create 5 multiple-choice questions with options and an answer key.",
    "explain": "Explain the topic in simple English with examples."
}


@app.route("/")
def home():
    return send_from_directory(".", "index.html")


@app.route("/<path:filename>")
def files(filename):
    return send_from_directory(".", filename)


@app.route("/api/study", methods=["POST"])
def study():
    data = request.get_json(silent=True) or {}
    notes = data.get("notes", "").strip()
    task = data.get("task", "summary")

    if not notes:
        return jsonify({"error": "Please provide your notes."}), 400

    if task not in TASKS:
        return jsonify({"error": "Invalid study task."}), 400

    prompt = f"""
You are LazyLearn AI, a helpful study assistant.
Use the supplied notes as your main source.
Do not invent facts. If information is missing, say so.
Task: {TASKS[task]}

Study notes:
{notes}

Write the answer clearly in student-friendly English.
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=180
        )
        response.raise_for_status()
        answer = response.json().get("response", "").strip()

        return jsonify({"result": answer})

    except requests.exceptions.ConnectionError:
        return jsonify({
            "error": "Ollama is not running. Please start Ollama."
        }), 503

    except requests.exceptions.RequestException:
        return jsonify({
            "error": "The AI request failed. Please try again."
        }), 502


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)