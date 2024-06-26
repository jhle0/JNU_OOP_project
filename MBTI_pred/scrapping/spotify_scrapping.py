from dotenv import load_dotenv
import os
import base64
from requests import post
import json
import requests

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_headers(token):
    return {"Authorization": "Bearer " + token}

token = get_token()

def get_playlists_for_mbti(mbti_type, token):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_headers(token)
    params = {
        "q": mbti_type + " playlist",
        "type": "playlist",
        "limit": 10 
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()

mbti_types = ["INTJ", "INTP", "ENTJ", "ENTP", "INFJ", "INFP", "ENFJ", "ENFP",
            "ISTJ", "ISFJ", "ESTJ", "ESFJ", "ISTP", "ISFP", "ESTP", "ESFP"]

mbti_playlists = {}

for mbti_type in mbti_types:
    playlists = get_playlists_for_mbti(mbti_type, token)
    mbti_playlists[mbti_type] = playlists

json_data = json.dumps(mbti_playlists, indent=4)

def get_playlist_urls_for_mbti(mbti_type):
    if mbti_type in mbti_playlists:
        playlists = mbti_playlists[mbti_type]['playlists']['items']
        urls = [playlist['external_urls']['spotify'] for playlist in playlists]
        return urls
    else:
        return f"MBTI 유형 {mbti_type}에 대한 데이터가 없습니다."

mbti_type = input("당신의 mbti를 입력하세요:")
urls = get_playlist_urls_for_mbti(mbti_type)
for url in urls:
    print(url)