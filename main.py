from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import models
import schemas
import crud
from database import engine, get_db
from fastapi.middleware.cors import CORSMiddleware
from ai_service import get_ai_priority
from fastapi.staticfiles import StaticFiles

#Creating all database:
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Support CRM", description="A simple CRM for managing support tickets.", version="1.0.0")

#CORS so that front end can communicate with FAST API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    """
    Health check endpoint to verify the server is running.
    """
    return {"status": "ok", "message": "Datastraw CRM API is up and running!"}

@app.post("/api/tickets")
def create_ticket(ticket: schemas.TicketCreate, db: Session = Depends(get_db)):
    db_ticket = crud.create_ticket(db=db, ticket=ticket)
    
    return {
        "ticket_id": db_ticket.ticket_id, 
        "created_at": db_ticket.created_at
    }

@app.get("/api/tickets")
def list_tickets(
    status: Optional[str] = None, 
    search: Optional[str] = None, 
    sort_by: Optional[str] = "date_desc", 
    db: Session = Depends(get_db)
):
    # 2. Pass sort_by into the CRUD function
    tickets = crud.get_tickets(db, status=status, search=search, sort_by=sort_by)
    
    return [
        {
            "ticket_id": t.ticket_id,
            "customer_name": t.customer_name,
            "subject": t.subject,
            "status": t.status,
            "priority": t.priority,
            "created_at": t.created_at
        } for t in tickets
    ]

@app.get("/api/tickets/{ticket_id}", response_model=schemas.TicketResponse)
def get_ticket(ticket_id: str, db: Session = Depends(get_db)):
    db_ticket = crud.get_ticket_by_ticket_id(db, ticket_id)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return db_ticket

@app.put("/api/tickets/{ticket_id}")
def update_ticket(ticket_id: str, update_data: schemas.TicketUpdate, db: Session = Depends(get_db)):
    db_ticket = crud.update_ticket(db, ticket_id, update_data)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return {
        "success": True, 
        "updated_at": db_ticket.updated_at
    }

@app.post("/api/tickets/{ticket_id}/suggest-priority")
def suggest_ticket_priority(ticket_id: str, db: Session = Depends(get_db)):
    """
    Endpoint to trigger the AI priority suggestion.
    """
    db_ticket = crud.get_ticket_by_ticket_id(db, ticket_id)
    if not db_ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    # Call the helper function from ai_service.py
    suggested_priority = get_ai_priority(db_ticket.description)
    
    # Save the updated priority
    db_ticket.priority = suggested_priority
    db.commit()
    db.refresh(db_ticket)
    
    return {
        "success": True, 
        "ticket_id": db_ticket.ticket_id,
        "suggested_priority": suggested_priority
    }

app.mount("/", StaticFiles(directory="static", html=True), name="static")