from llmproxy import generate
from llmproxy import pdf_upload

if __name__ == '__main__':
    response_pdf = pdf_upload(
        path = 'unit.pdf',
        session_id = 'bridgette-rag-test',
        strategy = 'smart'
    )
    print(response_pdf)
    
