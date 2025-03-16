import requests

url = "https://models.inference.ai.azure.com"
headers = {
    "Authorization": "Bearer SEU_TOKEN_AQUI",  # Ou "Ocp-Apim-Subscription-Key": "SUA_CHAVE_AQUI"
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers, timeout=5)

print("Status:", response.status_code)
print("Resposta:", response.text)
