import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI()


@app.get("/", response_class=RedirectResponse)
def root() -> RedirectResponse:
    """ルートエンドポイント: SwaggerUIにRedirectする"""

    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    uvicorn.run(app)
