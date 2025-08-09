from fastapi import FastAPI
import requests
import os
from flask.config import T
from dotenv import get_key, load_dotenv
import base64
import webserver

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN") 
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
GITHUB_REPO = os.getenv("GITHUB_REPO")

def decode_content(data):
    if not data:
        return ""
    if data.get("encoding") == "base64":
        return base64.b64decode(data["content"]).decode("utf-8")
    return ""

class Github:
    def __init__(self,token, username, repo):
        self.url = f"https://api.github.com/repos/{username}/{repo}/contents/"
        self.token = token
    
    def getData(self, file):
        urls = self.url + file
        headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }
        response = requests.get(urls, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None


app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/orca/{hwid}")
def gethwid_orca(hwid: str):
    git = Github(GITHUB_TOKEN,GITHUB_USERNAME,GITHUB_REPO)
    content = decode_content(git.getData("advancehwid"))
    splitted_line = content.split("\n")
    hwids = []
    for lines in splitted_line:
        try:
            hwids.append(lines.split("=")[0])
        except:
            continue
    found = hwid in hwids
    
    # Corrected logic to encode the result
    result_string = "1" if found else "0"
    encoded_result = base64.b64encode(result_string.encode("utf-8")).decode("utf-8")
    
    return {"result": encoded_result}

@app.get("/normal/{hwid}")
def gethwid_normal(hwid: str):
    git = Github(GITHUB_TOKEN,GITHUB_USERNAME,GITHUB_REPO)
    content = decode_content(git.getData("hwid"))
    splitted_line = content.split("\n")
    hwids = []
    for lines in splitted_line:
        try:
            hwids.append(lines.split("=")[0])
        except:
            continue
    found = hwid in hwids
    
    # Corrected logic to encode the result
    result_string = "1" if found else "0"
    encoded_result = base64.b64encode(result_string.encode("utf-8")).decode("utf-8")
    
    return {"result": encoded_result}