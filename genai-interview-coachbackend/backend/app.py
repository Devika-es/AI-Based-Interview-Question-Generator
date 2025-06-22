from flask import Flask, request, render_template, jsonify
from transformers import pipeline

app = Flask(__name__)

# Load an instruction-tuned model
qa_pipeline = pipeline("text2text-generation", model="MBZUAI/LaMini-Flan-T5-783M")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({'error': 'Prompt missing'}), 400

    # Strong prompt to get quality questions
    final_prompt = f"Generate 5 technical interview questions for the role of a {prompt}. Respond as a numbered list."

    result = qa_pipeline(final_prompt, max_new_tokens=300, temperature=0.7)[0]['generated_text']

    # Parse clean questions
    questions = []
    for line in result.split('\n'):
        line = line.strip()
        if line and any(char.isalpha() for char in line):
            questions.append(line.strip("-•1234567890. ").capitalize())

    return jsonify({'response': questions})

if __name__ == "__main__":
    app.run(debug=True)
