import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from api.routes.api import router as api_router


def get_application() -> FastAPI:
    app = FastAPI()

    origins = [
        "http://127.0.0.1:8000/",
        "https://127.0.0.1:8000/",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(SessionMiddleware, secret_key="!secret")

    app.include_router(api_router)

    return app


app = get_application()


@app.get("/")
async def read_info():
    return {"msg": "Welcome"}


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host="127.0.0.1", reload=True)
