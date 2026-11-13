from types import SimpleNamespace

from fastapi import FastAPI
from fastapi.testclient import TestClient

from routers import chat


def test_chat_init_accepts_request_without_body() -> None:
    test_app = FastAPI()
    test_app.include_router(chat.router)
    test_app.state.chat_manager = SimpleNamespace(load_chat_list=lambda: [])

    response = TestClient(test_app).get("/chat/init")

    assert response.status_code == 200
    assert response.json() == []
