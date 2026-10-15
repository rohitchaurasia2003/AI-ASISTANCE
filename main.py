import os

from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

app = Flask(__name__)

load_dotenv()
api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    raise RuntimeError("GROQ_API_KEY is not set. Add it to your .env file.")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1",
)


@app.errorhandler(OpenAIError)
def handle_openai_error(error):
    app.logger.exception("AI provider request failed", exc_info=error)
    return jsonify({"error": "The AI service could not process your request. Please try again."}), 502


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    question = request.form.get("question", "").strip()
    if not question:
        return jsonify({"error": "Please enter a question."}), 400

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": "Act like a helpful personal assistant"},
            {"role": "user", "content": question},
        ],
        temperature=0.7,
        max_tokens=512,
    )

    answer = (response.choices[0].message.content or "").strip()
    return jsonify({"response": answer}), 200


@app.route("/summarize", methods=["POST"])
def summarize():
    email_text = request.form.get("email", "").strip()
    if not email_text:
        return jsonify({"error": "Please enter the email text to summarize."}), 400

    prompt = f"summarize the following email in 2-3 sentences: {email_text}"

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": "Act like an expert email assistant"},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=512,
    )

    summary = (response.choices[0].message.content or "").strip()
    return jsonify({"summary": summary}), 200


if __name__ == "__main__":
    app.run()