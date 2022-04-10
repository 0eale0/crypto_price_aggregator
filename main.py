import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_info(request: Request):
    return templates.TemplateResponse("signup.html", {'request': request})


if __name__ == '__main__':
    uvicorn.run("main:app", port=8090, host="127.0.0.1", reload=True)
