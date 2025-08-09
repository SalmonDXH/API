from fastapi import FastAPI
import requests
import os
from dotenv import get_key, load_dotenv
import base64
from fastapi import FastAPI, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded


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

limiter = Limiter(key_func=get_remote_address, default_limits=["1/minute"])
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.get("/")
@limiter.limit("1/minute")
def read_root(request: Request):  # <- add this
    return {"message": "Hello World"}

@app.get("/orca/{hwid}")
@limiter.limit("10/minute")
def gethwid_orca(hwid: str,request: Request):
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
    
    result_string = "1" if found else "0"
    encoded_result = base64.b64encode(result_string.encode("utf-8")).decode("utf-8")
    
    return {"result": encoded_result}

@app.get("/normal/{hwid}")
@limiter.limit("10/minute")
def gethwid_normal(hwid: str,request: Request):
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
    
    result_string = "1" if found else "0"
    encoded_result = base64.b64encode(result_string.encode("utf-8")).decode("utf-8")
    
    return {"result": encoded_result}