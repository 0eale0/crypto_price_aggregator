import uvicorn
from fastapi import FastAPI
from auth.auth import sub_app


app = FastAPI()
app.mount(path='/auth', app=sub_app)


@app.get("/")
async def read_info():
    return {'msg': 'Hello world'}


if __name__ == '__main__':
    uvicorn.run("main:app", port=8000, host="127.0.0.1", reload=True)
