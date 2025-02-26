# import requests
# from flask import Flask, request, jsonify
# from llmproxy import generate

import requests
import json
from flask import Flask, request, jsonify
from llmproxy import generate, pdf_upload
import uuid

def get_session_id(data):
    user = data.get("user_name", "Unknown")
    return f"bridgette-agent-{user}-{uuid.uuid4().hex[:8]}"  # Example: 'john-3fa85f'


app = Flask(__name__)

SESSION_ID = 'bridgette-agent'

@app.route('/')
def hello_world():
   return jsonify({"text":'Hello from Koyeb - you reached the main page!'})

@app.route('/query', methods=['POST'])
def main():
    data = request.get_json() 

    # Extract relevant information
    
    user = data.get("user_name", "Unknown")
    message = data.get("text", "")

    sess_id = f"bridgette-agent-{user}-{uuid.uuid4().hex[:8]}"
    print('SESS_ID+++++++:')
    print(sess_id)
    print(data)

    # Ignore bot messages
    if data.get("bot") or not message:
        return jsonify({"status": "ignored"})

    print(f"Message from {user} : {message}")

    response_pdf = pdf_upload(
        path = 'resume.pdf',
        session_id = sess_id,
        strategy = 'smart'
    )

    print(response_pdf)

    query = f'Generate a new resume based on uploaded pdf information, work experience, leadership experience, schooling'\
            f'and tailor it based on the following user input delimited in triple astriks. ***{message}***'\
            f'If the user input is not related to a career, job industry, or description inform the user in a friendly manner '\
            f'that you can edit the given resume to fit the given job description. '

    # system_constant = ('If the user message is not related to the AP/IB prematricualtion credits at Tufts, '
    #                    'prompt the user in a friendly manner to list their AP/IB test and their school '
    #                    'Arts and Sciences or Engineering so that you can analyze what pre-matriculation credits '
    #                    'they have earned based on the uploaded file '
    #                    'Answer related questions or lists of courses properly based on the uploaded file by '
    #                    'breaking down each test score and the number of credits recieved for it '
    #                    'Ensure that the college is specified: Arts and Sciences or Engineering before giving an answer'
    #                    'Act as a welcoming and helpful guide for incoming freshmen who may be confused.')

    agents = [agent_builder, agent_critique]

    max_iterations = 1

    i=0
    while i < max_iterations:

        # flip between agent coder and QA
        active_agent = agents[i%2]
        query = active_agent(query, sess_id)

        if query == "$$EXIT$$":
            break

        i+=1
    
    print(query)
    return query
    # response_text = query['resume']
    # print(response_text)

    # return jsonify({"text": response_text})

def agent_critique(query, sess_id):
    system = """
    You are an AI agent designed critque a resume written by a college student or new graduate.
    The goal is to create a resume that will standout and hit relevant industry words and
    sythesize on the experiences listed on the given resume.

    You have two options:
    ### Option 1 ###
    If you see any lacking parts, respond with pointing out any lacking information or unneccessary information,
    suggestions for simplifying, improving, and optimizing the resume..
    
    ### Option 2 ###
    2. If you don't see any issues with the resume, respond with "$$EXIT$$" and nothing else.
    """

    response = generate(model = '4o-mini',
        system = system,
        query = query,
        temperature=0.3,
        lastk=10,
        session_id=sess_id,
        rag_usage = True,
        rag_threshold='0.2',
        rag_k=4)

    try:
        return response['response']
    except Exception as e:
        print(f"Error occured with parsing output: {response}")
        raise e
    return 

def agent_builder(query, sess_id):

    system = """
    You are an AI agent designed to make a resume.
    """

    response = generate(model = '4o-mini',
        system = system,
        query = query,
        temperature=0.3,
        lastk=10,
        session_id=sess_id,
        rag_usage = True, 
        rag_threshold='0.2',
        rag_k=4)

    try:
        return response['response']
    except Exception as e:
        print(f"Error occured with parsing output: {response}")
        raise e

    return

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
