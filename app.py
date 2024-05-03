from flask import Flask, request, jsonify
from transformers import pipeline
PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
app = Flask(__name__)

@app.route('/generate_text', methods=['POST'])
def generate_text():
    data = request.get_json()
    prompt = data['prompt']

    generator = pipeline('text-generation', model='EleutherAI/gpt-neo-1.3B')

    res = generator(prompt, max_length=100, do_sample=True, temperature=0.8)

    generated_text = res[0]['generated_text']

    return jsonify({"generated_text": generated_text})

if __name__ == '__main__':
    app.run(debug=True)
