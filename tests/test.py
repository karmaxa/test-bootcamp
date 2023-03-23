import requests as rq
from pytest_django import live_server_helper


def test() -> None:
    server = live_server_helper.LiveServer("0.0.0.0:8000")  # noqa: F841

    res = rq.get("http://localhost:8000/")  # noqa: S113
    assert res.ok
