from fastapi import FastAPI
import os
from dotenv import load_dotenv
import base64
from fastapi import FastAPI, Request, HTTPException, Depends
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from supabase import create_client, Client
from slowapi.errors import RateLimitExceeded


load_dotenv()
supaurl: str = os.environ.get("supaurl")
supakey: str = os.environ.get("supakey")
supabase: Client = create_client(supaurl, supakey)
website : str = os.environ.get('website')


app = FastAPI()

limiter = Limiter(key_func=get_remote_address, default_limits=["1/minute"])
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

async def verify_origin(request: Request):
    origin  = request.headers.get("origin")
    referer = request.headers.get("referer")
    if origin and origin != website:
        raise HTTPException(status_code=403, detail="Forbidden")
    if referer and not referer.startswith(website):
        raise HTTPException(status_code=403, detail="Forbidden")
    if not origin and not referer:
         raise HTTPException(status_code=403, detail="Forbidden")
    return True

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



@app.get('/v2/orca')
@limiter.limit('10/minute')
async def v2_orca(request: Request):
    try:
        data = await request.json()
        hwid = data['hwid']
        (supabase.table("Orca").select("username").eq("hwid", hwid).execute()).data[0]
        return {'result': 'True'}
    except Exception as e:
        return {'result': 'Fail'}

@app.get('/v2/donator')
@limiter.limit('10/minute')
async def v2_donator(request: Request):
    try:
        data = await request.json()
        hwid = data['hwid']
        (supabase.table("Donator").select("username").eq("hwid", hwid).execute()).data[0]
        return {'result': 'True'}
    except Exception as e:
        return {'result': 'Fail'}

@app.get('/v2/tester')
@limiter.limit('10/minute')
async def v2_tester(request: Request):
    try:
        data = await request.json()
        hwid = data['hwid']
        (supabase.table("Tester").select("username").eq("hwid", hwid).execute()).data[0]
        return {'result': 'True'}
    except Exception as e:
        return {'result': 'Fail'}

@app.get('/v2/premium')
@limiter.limit('10/minute')
async def v2_premium(request: Request):
    try:
        data = await request.json()
        hwid = data['hwid']
        user_data = (supabase.table("Premium").select("username", "role").eq("hwid", hwid).execute()).data[0]
        result = supabase.rpc('increment_login', {'user_id': 1}).execute()
        return {'result': 'True', 'role': user_data['role'], 'username':user_data['username']}
    except Exception as e:
        print(str(e))
        return {'result': 'Fail'}

@app.get('/v2/check')
@limiter.limit('10/minute')
async def v2_premium(request: Request):
    try:
        data = await request.json()
        hwid = data['hwid']
        user_data =  (supabase.rpc('check_key', {'p_hwid': hwid}).execute()).dict()['data'][0]
        supabase.rpc('increment_login', {'user_id': 1}).execute()
        return user_data
    except Exception as e:
        print(str(e))
        return {'result': 'Fail'}


@app.get('/v2/state')
@limiter.limit('5/minute')
async def v2_state(request: Request):
    try:
        res = (supabase.table("State").select("type").eq("id", 1).execute()).data[0]['type']
        return {'result': res}
    except Exception as e:
        return {'result': 'Error'}

@app.get('/api/statistic')
async def api_statistic(request: Request, verified:bool = Depends(verify_origin)):
    try:
        result = (supabase.rpc('macro_statistic', {}).execute()).dict()['data'][0]
        return result
    except:
        raise HTTPException(status_code=400, detail="Something went wrong")