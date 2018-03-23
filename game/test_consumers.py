import pytest
from channels.testing import HttpCommunicator
from myproject.myapp.consumers import MyConsumer

@pytest.mark.asyncio
async def test_my_consumer():
    communicator = HttpCommunicator(MyConsumer, "GET", "/game/")
    response = await communicator.get_response()
    assert response["status"] == 200
    assert response["body"] == b"test response"