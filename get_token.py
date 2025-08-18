import requests

# Kullanıcı bilgileriniz
username = "your_email@example.com"
password = "your_password"

token_url = "http://127.0.0.1:8000/token"

# POST isteği için veri
data = {
    "username": username,
    "password": password
}

# İstek başlıkları
headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}

try:
    response = requests.post(token_url, data=data, headers=headers)
    response.raise_for_status() # HTTP hataları için istisna fırlatır

    token_data = response.json()
    access_token = token_data.get("access_token")
    token_type = token_data.get("token_type")

    if access_token and token_type:
        print(f"Access Token: {access_token}")
        print(f"Token Type: {token_type}")
        # Bu token'ı bir sonraki adımda kullanmak üzere saklayın
    else:
        print("Token alınamadı. Yanıt:", token_data)

except requests.exceptions.RequestException as e:
    print(f"Token alırken hata oluştu: {e}")
    if hasattr(e, 'response') and e.response is not None:
        print(f"Yanıt içeriği: {e.response.text}")
