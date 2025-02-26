# import requests
# from flask import Flask, request, jsonify
# from llmproxy import generate

import requests
import json
from flask import Flask, request, jsonify
from llmproxy import generate, pdf_upload

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

    response_pdf = pdf_upload(
        path = 'prematriculation_credits.pdf',
        session_id = 'bridgette-rag-test',
        strategy = 'smart'
    )

    query = f'Given this message delimited in triple astriks, reply by giving the number of credits for each listed class, '\
            f'based on the uploaded file. '\
            # f'Answer the given question or command delimited in triple astriks. First, give a straightforward answer based on the file,' \
            # f'and then synthesize to give possible solutions and idea brainstorming.'\
            f'***{message}***'

    system_constant = ('If the user message is not related to the AP/IB prematricualtion credits at Tufts, '
                        'prompt the user in a friendly manner to list their AP/IB test and their school '
                       'Arts and Sciences or Engineering so that you can analyze what pre-matriculation credits '
                       'they have earned based on the uploaded file '
                       'Answer related questions or lists of courses properly based on the uploaded file by '
                       'breaking down each test score and the number of credits recieved for it '
                       'Ensure that the college is specified: Arts and Sciences or Engineering before giving an answer'
                       'Act as a welcoming and helpful guide for incoming freshmen who may be confused.')



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
    
    response_text = response['response']
    print(response_text)
    # print(json.dumps(response, indent=4, ensure_ascii=False))

    # session["unit_num"] = None
    # session["num_q"] = None
    return jsonify({"text": response_text})

# @app.route('/upload_pdf', methods=['POST'])
# def upload_pdf():
#     data = request.get_json()
#     pdf_path = data.get("pdf_path", "unit.pdf")
#     session_id = data.get("session_id", "bridgette-rag-test")
    
#     response_pdf = pdf_upload(
#         path=pdf_path,
#         session_id=session_id,
#         strategy='smart'
#     )
    
#     print(response_pdf)
#     return jsonify(response_pdf)

@app.route('/generate_quiz', methods=['POST'])
def generate_quiz():
    data = request.get_json()

    # user_input = data.get("message", "").strip().lower()
    user = data.get("user_name", "Unknown")
    message = data.get("text", "")

    # Ignore bot messages
    if data.get("bot") or not message:
        return jsonify({"status": "ignored"})

    print(f"Message from {user} : {message}")

    # Initialize session variables if not set
    # if "unit_num" not in session:
    #     session["unit_num"] = None
    # if "num_q" not in session:
    #     session["num_q"] = None

    # # Step 1: Ask for unit number if not provided
    # if session["unit_num"] is None:
    #     session["unit_num"] = user_input
    #     return jsonify({"response": "How many questions?"})

    # # Step 2: Ask for number of questions if not provided
    # if session["num_q"] is None:
    #     if not user_input.isdigit():  # Validate input
    #         return jsonify({"response": "Please enter a valid number for questions."})
    #     session["num_q"] = user_input


    # pdf_path = data.get("pdf_path", "unit.pdf")
    # session_id = data.get("session_id", "bridgette-rag-test")
    
    # response_pdf = pdf_upload(
    #     path=pdf_path,
    #     session_id=session_id,
    #     strategy='smart'
    # )
    response_pdf = pdf_upload(
        path = 'unit.pdf',
        session_id = 'bridgette-rag-test',
        strategy = 'smart'
    )
    
    # print(response_pdf)

    # num_q = data.get("num_q", "5")
    # unit_num = data.get("unit_num", "1")
    
    # query = f'Give me a multiple choice question quiz based on the given unit that is ' \
    #         f'delimited by triple astriks ***{unit_num}*** to test the students on their knowledge after learning. ' \
    #         f'The number of questions is delimited by triple quotes """{num_q}""" '
    
    # system_constant = ('Evaluate if the number of questions is a valid number. '
    #                    'If not, reprompt the number of questions. '
    #                    'Evaluate if the unit number is a valid number. '
    #                    'If not, reprompt the unit number. '
    #                    'Answer in a format of question, 4 answer choices. After all questions, '
    #                    'give the key. In the key explain each answer like a helpful tutor, assuming no previous knowledge.')
    query = f'If the message delimited in triple astriks is not a question or command, '\
            f'ask the chatter to ask a question regarding the Grade 6 Math Scope and Sequence Outline. '\
            f'Answer the given question or command delimited in triple astriks. First, give a straightforward answer based on the file,' \
            f'and then synthesize to give possible solutions and idea brainstorming.'\
            f'This is the message: ***{message}***'

    system_constant = ('Prompt the user in a friendly manner to ask a question or command'
                       'regarding the Grade 6 Math Scope and Sequence Outline and specify '
                       'each unit and te topics in each unit '
                       'Do not outwardly specify whether the given message is a question or command.'
                       'Act as a helpful teaching assistant that will give detailed '
                       'information on the question based on the uploaded file.')



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
    
    response_text = response['response']
    print(response_text)
    # print(json.dumps(response, indent=4, ensure_ascii=False))

    # session["unit_num"] = None
    # session["num_q"] = None
    return jsonify({"text": response_text})

    
@app.errorhandler(404)
def page_not_found(e):
    return "Not Found", 404

if __name__ == "__main__":
    app.run()
