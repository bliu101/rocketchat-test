import requests

response_main = requests.get("https://jolly-selia-tuftsuni-5e8bcc9c.koyeb.app/")
print('Web Application Response:\n', response_main.text, '\n\n')


data = {"text":"Edit this resume to fit a product management role."}
response_llmproxy = requests.post("https://jolly-selia-tuftsuni-5e8bcc9c.koyeb.app/query", json=data)
print('LLMProxy Response:\n', response_llmproxy.text)