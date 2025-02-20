import requests

response_main = requests.get("https://inland-emalee-bridgetteliu101-ded36713.koyeb.app/")
print('Web Application Response:\n', response_main.text, '\n\n')


data = {
    "unit_num": "1",
    "num_q": "5"
}
response_llmproxy = requests.post("https://inland-emalee-bridgetteliu101-ded36713.koyeb.app/generate_quiz", json=data)
print('LLMProxy Response:\n', response_llmproxy.text)