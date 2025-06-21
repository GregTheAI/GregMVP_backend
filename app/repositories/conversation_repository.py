from app.entities import Conversation
from app.repositories.base_repository import BaseRepository


class ConversationRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(Conversation, db)

    def get_conversation(self, conversation_id):
        return self.db.query(self.model).filter(self.model.id == conversation_id).first()

    def get_conversations_by_session_id_paginated(self, session_id, page_size):
        return self.get_all(filters={"session_id": session_id}, page_size=page_size)


    async def create_conversation(self, conversation_data: Conversation) -> Conversation:
        return await self.create(conversation_data.model_dump())

    def update_conversation(self, conversation_id, conversation_data):
        conversation = self.get_conversation(conversation_id)
        for key, value in conversation_data.items():
            setattr(conversation, key, value)
        self.db.commit()
        return conversation

    def delete_conversation(self, conversation_id):
        conversation = self.get_conversation(conversation_id)
        if conversation:
            self.db.delete(conversation)
            self.db.commit()
            return True
        return False