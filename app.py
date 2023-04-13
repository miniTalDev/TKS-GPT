# Standard library
import os
import logging

# Third-party libraries
from dotenv import load_dotenv
from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
import openai

logging.basicConfig(filename='flask_app.log', level=logging.WARNING)

# Load variables from the .env file
load_dotenv()

# Load your API key from an environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initializes the Flask app with the specified static folder for serving the React build
app = Flask(__name__, static_folder='chatbot-ui/build', static_url_path='')

# Enables Cross-Origin Resource Sharing for your Flask app, allowing your React app to make requests to the Flask server
CORS(app)


# Sets up the root route to serve the index.html file from the React build folder.
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

# Sets up the /chat route to handle chat requests from the React app.
@app.route("/chat", methods=["POST"])
def chat():
    message = request.json["message"]

    try:
        response = openai.Completion.create(
            model="text-davinci-003",  # <-- Update the engine here
            prompt=f"User: {message}\nAssistant:",
            temperature=0.7,
            max_tokens=700,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=["\n"],
        )
        ai_message = response.choices[0].text.strip()

    except openai.error.APIError as e:
        print(f"OpenAI API returned an API Error: {e}")
        ai_message = "Error: API Error"

    except openai.error.APIConnectionError as e:
        print(f"Failed to connect to OpenAI API: {e}")
        ai_message = "Error: Connection Error"

    except openai.error.RateLimitError as e:
        print(f"OpenAI API request exceeded rate limit: {e}")
        ai_message = "Error: Rate Limit Exceeded"

    return jsonify({"message": ai_message})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
