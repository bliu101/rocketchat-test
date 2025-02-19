# from llmproxy import generate
# from llmproxy import pdf_upload
# import json

# if __name__ == '__main__':
#     # response_pdf = pdf_upload(
#     #     path = 'lesson_plan.pdf'
#     #     session_id = 'GenericSession'
#     #     strategy = 'smart'
#     # )
#     # print(response_pdf)
#     num_q = input('Number of questions: ')
#     unit_num = input('Which unit? ')
#     # lesson_input = input('Give the daily lesson plan topics to create a checkpoint quiz: ')
#     #example_input = input ('Are there any example questions to base this off of? (optional)')
    
#     query = 'Give me a multiple choice question quiz based on the given unit that is ' + \
#             'delimited by triple astriks ***' + unit_num + '***' + \
#             'to test the students on their knowledge after learning.' + \
#             ' The number of questions is delimited by triple quotes """' + \
#             num_q + '""" '
    
#     system_constant = 'Evaluate if the number of questions is a valid number.' + \
#     'If not, reprompt the number of questions. ' + \
#     'Evaluate if the unit number is a valid number.' + \
#     'If not, reprompt the unit number. ' + \
#     'Answer in a format of question, 4 answer choices. And after all questions, ' + \
#     ' give the key. In the key explain each answer like a helpful tutor, ' + \
#     'assuming no previous knowledge.'

#     print('QUERY::: ' + query + '\n')
    
#     response1 = generate(model = '4o-mini',
#         system = system_constant,
#         query = query,
#         temperature=0.0,
#         lastk=0,
#         session_id='bridgette-rag-test',
#         rag_usage = True,
#         rag_threshold = '0.2',
#         rag_k = 4)
#     #print('4o-mini: ')
#     #print(response1)
#     print(json.dumps(response1, indent=4, ensure_ascii=False))

from flask import Flask, request, jsonify
from flask_cors import CORS
from llmproxy import generate
import json
import os  # Import os to access environment variables

app = Flask(__name__)
# Allow requests only from your GitHub Pages domain
CORS(app, origins=["https://bliu101.github.io"])

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Quiz Generation API is running!"})

@app.route("/generate_quiz", methods=["POST"])
def generate_quiz():
    """
    API endpoint to generate a quiz based on user input.
    Expects JSON with 'num_q' (number of questions) and 'unit_num' (unit number).
    """
    data = request.json

    # Extract user input from request
    num_q = data.get("num_q")
    unit_num = data.get("unit_num")

    # Validate input
    if not num_q or not unit_num:
        return jsonify({"error": "Missing required parameters"}), 400

    if not num_q.isdigit() or not unit_num.isdigit():
        return jsonify({"error": "Invalid input. Please enter numeric values."}), 400

    # Construct query
    query = f"""Give me a multiple choice question quiz based on the given unit that is 
                delimited by triple asterisks ***{unit_num}*** to test the students' knowledge.
                The number of questions is delimited by triple quotes \"\"\"{num_q}\"\"\"."""

    # System instructions for the AI
    system_constant = """Evaluate if the number of questions is a valid number.
    If not, reprompt the number of questions. Evaluate if the unit number is a valid number.
    If not, reprompt the unit number. Answer in a format of question, 4 answer choices. 
    And after all questions, give the key. In the key, explain each answer like a helpful tutor, 
    assuming no previous knowledge."""

    # Generate response using LLM Proxy
    response1 = generate(model="4o-mini",
                         system=system_constant,
                         query=query,
                         temperature=0.0,
                         lastk=0,
                         session_id="bridgette-rag-test",
                         rag_usage=True,
                         rag_threshold="0.2",
                         rag_k=4)

    return jsonify(response1)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Get PORT from Render, default to 5000
    app.run(host="0.0.0.0", port=port)
