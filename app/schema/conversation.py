from pydantic import BaseModel

class ConversationRequest(BaseModel):
    conversation_id: str
    content: str
    suggested: int
    
class ReportRequest(BaseModel):
    conversation_id: str
    content: str
    
class NewConversation(BaseModel):
    conversation_id: str