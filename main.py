from fastapi import FastAPI
import os
from dotenv import load_dotenv
import base64
from fastapi import FastAPI, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from supabase import create_client, Client
from slowapi.errors import RateLimitExceeded


load_dotenv()
supaurl: str = os.environ.get("supaurl")
supakey: str = os.environ.get("supakey")
supabase: Client = create_client(supaurl, supakey)


app = FastAPI()

limiter = Limiter(key_func=get_remote_address, default_limits=["1/minute"])
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)



@app.get("/")
@limiter.limit("1/minute")
def read_root(request: Request):  
    return {"message": "Hello World"}

@app.get("/orca/{hwid}")
@limiter.limit("10/minute")
def gethwid_orca(hwid: str,request: Request):
    result_string = "0"
    try:
        user_data = (supabase.table("Orca").select("username").eq("hwid", hwid).execute()).data[0]
        result_string = "1"
    except:
        result_string = "0"
    encoded_result = base64.b64encode(result_string.encode("utf-8")).decode("utf-8")
    
    return {"result": encoded_result}

@app.get("/normal/{hwid}")
@limiter.limit("10/minute")
def gethwid_normal(hwid: str,request: Request):
    result_string = "0"
    try:
        user_data = (supabase.table("Donator").select("username").eq("hwid", hwid).execute()).data[0]
        result_string = "1"
    except:
        result_string = "0"
    encoded_result = base64.b64encode(result_string.encode("utf-8")).decode("utf-8")
    
    return {"result": encoded_result}

@app.get("/tester/{hwid}")
@limiter.limit("10/minute")
def gethwid_tester(hwid: str,request: Request):
    result_string = "0"
    try:
        user_data = (supabase.table("Tester").select("username").eq("hwid", hwid).execute()).data[0]
        result_string = "1"
    except:
        result_string = "0"
    encoded_result = base64.b64encode(result_string.encode("utf-8")).decode("utf-8")
    
    return {"result": encoded_result}