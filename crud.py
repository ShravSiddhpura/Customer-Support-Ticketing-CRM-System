# All CRUD operations

from sqlalchemy.orm import Session
from sqlalchemy import or_, case
import models
import schemas
from datetime import datetime, timezone
from ai_service import get_ai_priority

def generate_ticket_id(db: Session)->str:
    """ Generating unique ticket ID """
    last_ticket = db.query(models.Ticket).order_by(models.Ticket.id.desc()).first()
    if not last_ticket:
        return "TKT-001"
    
    last_id_num = int(last_ticket.ticket_id.split("-")[1])
    new_id_num = last_id_num + 1
    return f"TKT-{new_id_num:03d}"

def create_ticket(db: Session, ticket: schemas.TicketCreate):
    """ Creating new ticket"""

    new_ticket_id = generate_ticket_id(db)

    assigned_priority = get_ai_priority(ticket.description)
    db_ticket = models.Ticket(
        ticket_id=new_ticket_id,
        customer_name=ticket.customer_name,
        customer_email=ticket.customer_email,
        subject=ticket.subject,
        description=ticket.description,
        priority=assigned_priority
    )
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

def get_tickets(db: Session, status: str = None, search: str = None, sort_by: str = "date_desc"):
    query = db.query(models.Ticket)
    
    if status:
        query = query.filter(models.Ticket.status == status)
    
    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            or_(
                models.Ticket.customer_name.ilike(search_filter),
                models.Ticket.ticket_id.ilike(search_filter),
                models.Ticket.customer_email.ilike(search_filter),
                models.Ticket.description.ilike(search_filter)
            )
        )
    
    # SORTING LOGIC
    if sort_by == "priority":
        # Using a tuple-based case statement is the most reliable method for SQLite
        priority_order = case(
            (models.Ticket.priority == 'High', 1),
            (models.Ticket.priority == 'Medium', 2),
            (models.Ticket.priority == 'Low', 3),
            else_=4
        )
        query = query.order_by(priority_order, models.Ticket.created_at.desc())
        
    elif sort_by == "date_asc":
        query = query.order_by(models.Ticket.created_at.asc())
        
    else: 
        # Default fallback
        query = query.order_by(models.Ticket.created_at.desc())
        
    return query.all()

def get_ticket_by_ticket_id(db: Session, ticket_id: str):
    return db.query(models.Ticket).filter(models.Ticket.ticket_id == ticket_id).first()

def update_ticket(db: Session, ticket_id: str, update_data: schemas.TicketUpdate):
    db_ticket = get_ticket_by_ticket_id(db, ticket_id)
    if not db_ticket:
        return None

    if update_data.status:
        db_ticket.status = update_data.status
    if update_data.priority:
        db_ticket.priority = update_data.priority

    db_ticket.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket 

def create_note(db: Session, ticket_id: str, note: schemas.NoteCreate):
    db_ticket = get_ticket_by_ticket_id(db, ticket_id)
    if not db_ticket:
        return None
    
    new_note = models.Note(
        ticket_id=db_ticket.id,
        note_text=note.note_text
    )
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note
