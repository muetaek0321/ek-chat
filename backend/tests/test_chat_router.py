from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

from main import app


def test_chat_init_accepts_request_without_body(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        app.state,
        "chat_manager",
        SimpleNamespace(load_chat_list=lambda: []),
        raising=False,
    )

    response = TestClient(app).get("/chat/init")

    assert response.status_code == 200
    assert response.json() == []
