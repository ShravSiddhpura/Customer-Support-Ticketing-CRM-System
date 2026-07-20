#This defines the actual tables in the SQLite database.

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey,text
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime, timezone

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(String, unique=True, index=True) 
    customer_name = Column(String, index=True)
    customer_email = Column(String, index=True)
    subject = Column(String)
    description = Column(String)
    status = Column(String, default="Open") # Open / In Progress / Closed
    priority = Column(String, default="Unassigned") # We'll use this for Groq AI classification
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    #relationship to Notes
    notes = relationship("Note", back_populates="ticket", cascade="all, delete-orphan")

class Note(Base):
    __tablename__ = "notes"

    id= Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"))
    note_text = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationship back to Ticket
    ticket = relationship("Ticket", back_populates="notes")