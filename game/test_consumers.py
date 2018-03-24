# import pytest
# from channels.testing import ApplicationCommunicator, HttpCommunicator
# from game.consumers import GameConsumer

# @pytest.mark.asyncio
# async def test_my_consumer():
#     communicator = HttpCommunicator(GameConsumer, "GET", "/game/")
#     response = await communicator.get_response()
#     assert response["status"] == 200
#     assert response["body"] == b"test response"

# @pytest.mark.asyncio
# async def test_my_application_communicator():
#     communicator = ApplicationCommunicator(
#         GameConsumer,
#         {"type": "game_update"},
#     )

#     await communicator.send_input({
#         "type": "http.request",
#         "body": {"message" : "some message"},
#     })

#     event = await communicator.receive_output(timeout=1)
#     assert event["type"] == "http.response.start"
