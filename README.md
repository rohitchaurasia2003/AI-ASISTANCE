# AI Personal Assistant

A small Flask web app that uses Groq's API to answer questions and summarize email text. It has a simple browser interface for both tasks.

## Features

- Ask a question and receive an AI-generated answer.
- Paste an email and get a summary in 2–3 sentences.
- Show loading and error messages when requests are being processed or fail.

## Requirements

- Python 3.9 or newer
- A Groq API key

## Getting started

1. Clone the repository and open its directory:

   ```bash
   git clone <your-repository-url>
   cd <repository-directory>
   ```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

   On Windows, activate it with:

   ```powershell
   .venv\Scripts\activate
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project directory and add your Groq API key:

   ```env
   GROQ_API_KEY=your_groq_api_key
   ```

   Keep your API key private. Do not commit your `.env` file or put the key in source code.

5. Start the app:

   ```bash
   python main.py
   ```

6. Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

## API endpoints

The app accepts form-encoded `POST` requests:

| Endpoint | Form field | Success response |
| --- | --- | --- |
| `/ask` | `question` | `{"response": "..."}` |
| `/summarize` | `email` | `{"summary": "..."}` |

Blank input returns a `400` response with an `error` message. If the AI provider request fails, the app returns a `502` response.

## Model

Both features currently use Groq's `openai/gpt-oss-20b` model. The Groq API is accessed through the OpenAI Python client.
