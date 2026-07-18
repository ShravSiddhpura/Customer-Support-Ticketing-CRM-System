#schemas.py uses Pydantic to validate the data sent to and from our API endpoints.

from pydantic import BaseModel, EmailStr
from typing import Optional, List 
from datetime import datetime

# Note Schemas:
class NoteBase(BaseModel):
    note_text:str

class NoteCreate(NoteBase):
    pass

class NoteResponse(NoteBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Ticket Schemas:

class TicketBase(BaseModel):
    customer_name: str
    customer_email: EmailStr
    subject: str
    description: str

class TicketCreate(TicketBase):
    pass

class TicketUpdate(BaseModel):
    status: Optional[str] = None
    priority: Optional[str] = None
    note_text: Optional[str] = None

class TicketResponse(TicketBase):
    id: int
    ticket_id: str
    status: str
    priority: str
    created_at: datetime
    updated_at: datetime
    notes: List[NoteResponse] = []

    class Config:
        from_attributes = True