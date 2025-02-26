import sys
import os

from llmproxy import generate
SESSION_ID = 'bridgette-agent'

def agent_critique(query):
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
        session_id=SESSION_ID,
        rag_usage = False)

    try:
        return response['response']
    except Exception as e:
        print(f"Error occured with parsing output: {response}")
        raise e
    return 

def agent_builder(query):

    system = """
    You are an AI agent designed to make a resume.
    """

    response = generate(model = '4o-mini',
        system = system,
        query = query,
        temperature=0.3,
        lastk=10,
        session_id=SESSION_ID,
        rag_usage = False)

    try:
        return response['response']
    except Exception as e:
        print(f"Error occured with parsing output: {response}")
        raise e

    return

if __name__ == '__main__':
    query = f'Generate a new resume based on the information, work experience, leadership experience, schooling'\
            f'and tailor it based on the following user input delimited in triple astriks. ***product management***'\
            f'If the user input is not related to a career, job industry, or description inform the user in a friendly manner '\
            f'that you can edit the given resume to fit the given job description. '


    agents = [agent_builder, agent_critique]

    max_iterations = 1

    i=0
    while i < max_iterations:

        # flip between agent coder and QA
        active_agent = agents[i%2]


        query = active_agent(query)

        if query == "$$EXIT$$":
            break

        i+=1


