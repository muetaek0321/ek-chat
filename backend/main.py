import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from modules.response_generator import ChatManager
from modules.schema import ChatMessage

# FastAPIアプリケーションのインスタンスを作成
app = FastAPI()

# ChatManagerのインスタンスを作成
chat = ChatManager()


@app.get("/", response_class=RedirectResponse)
def root() -> RedirectResponse:
    """ルートエンドポイント: SwaggerUIにRedirectする"""

    return RedirectResponse(url="/docs")


@app.post("/chat", response_model=ChatMessage)
def generate_chat_response(payload: ChatMessage) -> ChatMessage:
    """userの入力に対してassistantの応答を返す"""
    chat_message = payload.model_dump()

    # 返答を生成
    response = chat.generate(user_message=chat_message)

    return response


if __name__ == "__main__":
    uvicorn.run(app)
