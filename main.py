from fastapi import FastAPI
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
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


@app.get('/v2/premium')
@limiter.limit('10/minute')
async def v2_premium(request: Request):
    try:
        data = await request.json()
        hwid = data['hwid']
        user_data = (supabase.table("Premium").select("username", "role").eq("hwid", hwid).execute()).data[0]
        return {'result': 'True', 'role': user_data['role'], 'username':user_data['username']}
    except Exception as e:
        raise HTTPException(status_code=400, detail="You are not registed")

@app.get('/v2/check')
@limiter.limit('10/minute')
async def v2_check(request: Request):
    try:
        data = await request.json()
        hwid = data['hwid']
        user_data =  (supabase.rpc('check_key_2', {'p_hwid': hwid}).execute()).dict()['data'][0]
        return user_data
    except Exception as e:
        print(str(e))
        state = 'Tester'
        return {'username': '', 'role': 'Free', 'state': state}


@app.get('/v2/state')
@limiter.limit('5/minute')
async def v2_state(request: Request):
    try:
        res = (supabase.table("State").select("type").eq("id", 1).execute()).data[0]['type']
        return {'result': res}
    except Exception as e:
        raise HTTPException(status_code=404, detail="Item not found")

