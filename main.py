from fastapi import FastAPI
import requests
import os
from flask.config import T
from dotenv import get_key, load_dotenv
import base64
import webserver

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # environment variable name
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
def gethwid(hwid: str):
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
    a = "1" if found else "0"
    return  {"result": a}


@app.get("/normal/{hwid}")
def gethwid(hwid: str):
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
    a = "1" if found else "0"
        
    return  {"result": a}

