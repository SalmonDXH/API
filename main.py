from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/hwid/{hwid}")
def say_hello(hwid: str):
    return {"test": hwid}