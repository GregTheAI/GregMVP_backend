from typing import Coroutine

from fastapi import APIRouter
from fastapi.params import Depends
from starlette.exceptions import WebSocketException
from starlette.websockets import WebSocket

from app.dtos.user_dto import UserResponseDto
from app.entities import Conversation
from app.middlewares.authenticate import get_current_user, get_current_user_websocket
from app.services import UserService
from app.services.conversation_service import ConversationService
from app.services.dependencies import get_conversation_service

router = APIRouter(tags=["conversations"])


@router.websocket("/{session_id}", dependencies=[Depends(get_current_user_websocket)])
async def start_conversation(web_socket: WebSocket, session_id: str, conversation_service: ConversationService=Depends(get_conversation_service)):
    await web_socket.accept()

    try:
        while True:
            data = await web_socket.receive_json()

            response = await conversation_service.handle_conversation(session_id, data)

            full_reply = ""
            async for chunk in response:
                delta = chunk.choices[0].delta
                content = delta.get("content", "")
                full_reply += content

                if content:
                    await web_socket.send_text(content)
            # Here you would handle the incoming message and send a response
            await web_socket.send_text(f"Message received: {data}")

    except WebSocketException as e:
        await web_socket.close(code=1000, reason=str(e))
    except Exception as e:
        await web_socket.close(code=1000, reason=str(e))

@router.get("/", dependencies=[Depends(get_current_user)])
async def get_conversations():

    return {
        "message": "welcome to the conversations API"}