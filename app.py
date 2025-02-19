import requests
from flask import Flask, request, jsonify
from llmproxy import generate

app = Flask(__name__)

@app.route('/')
def hello_world():
   return jsonify({"text":'Hello from Koyeb - you reached the main page!'})

@app.route('/query', methods=['POST'])
def main():
    data = request.get_json() 

    # Extract relevant information
    user = data.get("user_name", "Unknown")
    message = data.get("text", "")

    print(data)

    # Ignore bot messages
    if data.get("bot") or not message:
        return jsonify({"status": "ignored"})

    print(f"Message from {user} : {message}")

    # Generate a response using LLMProxy
    response = generate(
        model='4o-mini',
        system='answer my question and add keywords',
        query= message,
        temperature=0.0,
        lastk=0,
        session_id='GenericSession'
    )

    response_text = response['response']
    
    # Send response back
    print(response_text)

    return jsonify({"text": response_text})

@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    data = request.get_json()
    pdf_path = data.get("pdf_path", "unit.pdf")
    session_id = data.get("session_id", "bridgette-rag-test")
    
    response_pdf = pdf_upload(
        path=pdf_path,
        session_id=session_id,
        strategy='smart'
    )
    
    print(response_pdf)
    return jsonify(response_pdf)

@app.route('/generate_quiz', methods=['POST'])
def generate_quiz():
    data = request.get_json()
    num_q = data.get("num_q", "5")
    unit_num = data.get("unit_num", "1")
    
    query = f'Give me a multiple choice question quiz based on the given unit that is ' \
            f'delimited by triple astriks ***{unit_num}*** to test the students on their knowledge after learning. ' \
            f'The number of questions is delimited by triple quotes """{num_q}""" '
    
    system_constant = ('Evaluate if the number of questions is a valid number. '
                       'If not, reprompt the number of questions. '
                       'Evaluate if the unit number is a valid number. '
                       'If not, reprompt the unit number. '
                       'Answer in a format of question, 4 answer choices. After all questions, '
                       'give the key. In the key explain each answer like a helpful tutor, assuming no previous knowledge.')
    
    print(f'QUERY::: {query}\n')
    
    response = generate(
        model='4o-mini',
        system=system_constant,
        query=query,
        temperature=0.0,
        lastk=0,
        session_id='bridgette-rag-test',
        rag_usage=True,
        rag_threshold='0.2',
        rag_k=4
    )
    
    print(json.dumps(response, indent=4, ensure_ascii=False))
    return jsonify(response)

    
@app.errorhandler(404)
def page_not_found(e):
    return "Not Found", 404

if __name__ == "__main__":
    app.run()
