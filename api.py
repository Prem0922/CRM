from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from database import SessionLocal, engine
from models import Customer, Card, Trip, Case, TapHistory, FareDispute
from pydantic import BaseModel, ConfigDict
from fastapi import Body
from sqlalchemy import func

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic models for request/response
class CustomerBase(BaseModel):
    name: str
    email: str
    phone: str
    address: str
    notifications: str

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(CustomerBase):
    pass

class CustomerResponse(CustomerBase):
    id: str
    join_date: datetime
    
    model_config = ConfigDict(from_attributes=True)

class CardBase(BaseModel):
    id: str
    type: str
    status: str
    balance: float
    customer_id: str

class CardCreate(CardBase):
    pass

class CardUpdate(CardBase):
    pass

class CardResponse(CardBase):
    id: str
    issue_date: datetime
    
    model_config = ConfigDict(from_attributes=True)

class TripBase(BaseModel):
    start_time: datetime
    end_time: datetime
    entry_location: str
    exit_location: str
    fare: float
    route: str
    operator: str
    transit_mode: str  # SubWay, Bus, Rail
    adjustable: str  # Yes, No
    card_id: str

class TripCreate(TripBase):
    pass

class TripUpdate(TripBase):
    pass

class TripResponse(TripBase):
    id: str
    model_config = ConfigDict(from_attributes=True)

class CaseBase(BaseModel):
    customer_id: str
    card_id: str
    case_status: str
    priority: str
    category: str
    assigned_agent: str
    notes: str

class CaseCreate(CaseBase):
    pass

class CaseUpdate(CaseBase):
    pass

class CaseResponse(CaseBase):
    id: str
    created_date: datetime
    last_updated: datetime
    model_config = ConfigDict(from_attributes=True)

class TapHistoryBase(BaseModel):
    tap_time: datetime
    location: str
    device_id: str
    transit_mode: str
    direction: str
    customer_id: str
    result: str

class TapHistoryCreate(TapHistoryBase):
    pass

class TapHistoryUpdate(TapHistoryBase):
    pass

class TapHistoryResponse(TapHistoryBase):
    id: str
    model_config = ConfigDict(from_attributes=True)

class FareDisputeBase(BaseModel):
    dispute_date: datetime
    card_id: str
    amount: float
    description: str = ""
    trip_id: str
    dispute_type: str

class FareDisputeCreate(FareDisputeBase):
    pass

class FareDisputeResponse(FareDisputeBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# Customer endpoints
@router.get("/customers/", response_model=List[CustomerResponse])
def get_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    customers = db.query(Customer).offset(skip).limit(limit).all()
    return customers

@router.get("/customers/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: str, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.post("/customers/", response_model=CustomerResponse)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    db_customer = Customer(
        id=f"C{str(len(db.query(Customer).all()) + 1).zfill(3)}",
        **customer.dict(),
        join_date=datetime.now()
    )
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

@router.put("/customers/{customer_id}", response_model=CustomerResponse)
def update_customer(customer_id: str, customer: CustomerUpdate, db: Session = Depends(get_db)):
    db_customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    for key, value in customer.dict().items():
        setattr(db_customer, key, value)
    
    db.commit()
    db.refresh(db_customer)
    return db_customer

@router.delete("/customers/{customer_id}")
def delete_customer(customer_id: str, db: Session = Depends(get_db)):
    db_customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    db.delete(db_customer)
    db.commit()
    return {"message": "Customer deleted successfully"}

# Card endpoints
@router.get("/cards/", response_model=List[CardResponse])
def get_cards(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cards = db.query(Card).offset(skip).limit(limit).all()
    return cards

@router.get("/cards/{card_id}", response_model=CardResponse)
def get_card(card_id: str, db: Session = Depends(get_db)):
    card = db.query(Card).filter(Card.id == card_id).first()
    if card is None:
        raise HTTPException(status_code=404, detail="Card not found")
    return card

@router.post("/cards/", response_model=CardResponse)
def create_card(card: CardCreate, db: Session = Depends(get_db)):
    db_card = Card(
        id=card.id,
        **card.dict(exclude={"id"}),
        product="Standard",
        issue_date=datetime.now()
    )
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card

@router.put("/cards/{card_id}", response_model=CardResponse)
def update_card(card_id: str, card: CardUpdate, db: Session = Depends(get_db)):
    db_card = db.query(Card).filter(Card.id == card_id).first()
    if db_card is None:
        raise HTTPException(status_code=404, detail="Card not found")
    
    for key, value in card.dict().items():
        setattr(db_card, key, value)
    
    db.commit()
    db.refresh(db_card)
    return db_card

@router.delete("/cards/{card_id}")
def delete_card(card_id: str, db: Session = Depends(get_db)):
    db_card = db.query(Card).filter(Card.id == card_id).first()
    if db_card is None:
        raise HTTPException(status_code=404, detail="Card not found")
    
    db.delete(db_card)
    db.commit()
    return {"message": "Card deleted successfully"}

# Trip endpoints
@router.get("/trips/", response_model=List[TripResponse])
def get_trips(skip: int = 0, db: Session = Depends(get_db)):
    trips = db.query(Trip).offset(skip).all()
    return trips

@router.get("/trips/{trip_id}", response_model=TripResponse)
def get_trip(trip_id: str, db: Session = Depends(get_db)):
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip

@router.post("/trips/", response_model=TripResponse)
def create_trip(trip: TripCreate, db: Session = Depends(get_db)):
    db_trip = Trip(
        id=f"T{str(len(db.query(Trip).all()) + 1).zfill(3)}",
        **trip.dict()
    )
    db.add(db_trip)
    db.commit()
    db.refresh(db_trip)
    return db_trip

@router.put("/trips/{trip_id}", response_model=TripResponse)
def update_trip(trip_id: str, trip: TripUpdate, db: Session = Depends(get_db)):
    db_trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if db_trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    for key, value in trip.dict().items():
        setattr(db_trip, key, value)
    
    db.commit()
    db.refresh(db_trip)
    return db_trip

@router.delete("/trips/{trip_id}")
def delete_trip(trip_id: str, db: Session = Depends(get_db)):
    db_trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if db_trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    db.delete(db_trip)
    db.commit()
    return {"message": "Trip deleted successfully"}

# Case endpoints
@router.get("/cases/", response_model=List[CaseResponse])
def get_cases(db: Session = Depends(get_db)):
    cases = db.query(Case).order_by(Case.created_date.desc()).all()
    return cases

@router.get("/cases/{case_id}", response_model=CaseResponse)
def get_case(case_id: str, db: Session = Depends(get_db)):
    case = db.query(Case).filter(Case.id == case_id).first()
    if case is None:
        raise HTTPException(status_code=404, detail="Case not found")
    return case

@router.post("/cases/", response_model=CaseResponse)
def create_case(case: CaseCreate, db: Session = Depends(get_db)):
    db_case = Case(
        id=f"CS{str(len(db.query(Case).all()) + 1).zfill(3)}",
        **case.dict(),
        created_date=datetime.now(),
        last_updated=datetime.now()
    )
    db.add(db_case)
    db.commit()
    db.refresh(db_case)
    return db_case

@router.put("/cases/{case_id}", response_model=CaseResponse)
def update_case(case_id: str, case: CaseUpdate, db: Session = Depends(get_db)):
    db_case = db.query(Case).filter(Case.id == case_id).first()
    if db_case is None:
        raise HTTPException(status_code=404, detail="Case not found")
    
    for key, value in case.dict().items():
        setattr(db_case, key, value)
    
    db.commit()
    db.refresh(db_case)
    return db_case

@router.delete("/cases/{case_id}")
def delete_case(case_id: str, db: Session = Depends(get_db)):
    db_case = db.query(Case).filter(Case.id == case_id).first()
    if db_case is None:
        raise HTTPException(status_code=404, detail="Case not found")
    
    db.delete(db_case)
    db.commit()
    return {"message": "Case deleted successfully"}

# Tap History endpoints
@router.get("/tap-history/", response_model=List[TapHistoryResponse])
def get_tap_history(
    skip: int = 0,
    limit: int = 100,
    customer_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(TapHistory)
    if customer_id:
        query = query.filter(TapHistory.customer_id == customer_id)
    tap_history = query.offset(skip).limit(limit).all()
    return tap_history

@router.get("/tap-history/{tap_id}", response_model=TapHistoryResponse)
def get_tap_entry(tap_id: str, db: Session = Depends(get_db)):
    tap_entry = db.query(TapHistory).filter(TapHistory.id == tap_id).first()
    if tap_entry is None:
        raise HTTPException(status_code=404, detail="Tap history entry not found")
    return tap_entry

@router.post("/tap-history/", response_model=TapHistoryResponse)
def create_tap_entry(tap_entry: TapHistoryCreate, db: Session = Depends(get_db)):
    db_tap_entry = TapHistory(
        id=f"TH{str(len(db.query(TapHistory).all()) + 1).zfill(6)}",
        **tap_entry.dict()
    )
    db.add(db_tap_entry)
    db.commit()
    db.refresh(db_tap_entry)
    return db_tap_entry

@router.put("/tap-history/{tap_id}", response_model=TapHistoryResponse)
def update_tap_entry(tap_id: str, tap_entry: TapHistoryUpdate, db: Session = Depends(get_db)):
    db_tap_entry = db.query(TapHistory).filter(TapHistory.id == tap_id).first()
    if db_tap_entry is None:
        raise HTTPException(status_code=404, detail="Tap history entry not found")
    
    for key, value in tap_entry.dict().items():
        setattr(db_tap_entry, key, value)
    
    db.commit()
    db.refresh(db_tap_entry)
    return db_tap_entry

@router.delete("/tap-history/{tap_id}")
def delete_tap_entry(tap_id: str, db: Session = Depends(get_db)):
    db_tap_entry = db.query(TapHistory).filter(TapHistory.id == tap_id).first()
    if db_tap_entry is None:
        raise HTTPException(status_code=404, detail="Tap history entry not found")
    
    db.delete(db_tap_entry)
    db.commit()
    return {"message": "Tap history entry deleted successfully"}

# Fare Dispute endpoints
@router.get("/fare-disputes/", response_model=List[FareDisputeResponse])
def get_fare_disputes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    disputes = db.query(FareDispute).offset(skip).limit(limit).all()
    return disputes

@router.post("/fare-disputes/", response_model=FareDisputeResponse)
def create_fare_dispute(dispute: FareDisputeCreate, db: Session = Depends(get_db)):
    db_dispute = FareDispute(
        dispute_date=dispute.dispute_date,
        card_id=dispute.card_id,
        amount=dispute.amount,
        description=dispute.description,
        trip_id=dispute.trip_id,
        dispute_type=dispute.dispute_type
    )
    db.add(db_dispute)
    db.commit()
    db.refresh(db_dispute)
    return db_dispute

@router.put("/fare-disputes/{dispute_id}", response_model=FareDisputeResponse)
def update_fare_dispute(dispute_id: int, dispute: FareDisputeCreate, db: Session = Depends(get_db)):
    db_dispute = db.query(FareDispute).filter(FareDispute.id == dispute_id).first()
    if db_dispute is None:
        raise HTTPException(status_code=404, detail="Fare Dispute not found")
    for key, value in dispute.dict().items():
        setattr(db_dispute, key, value)
    db.commit()
    db.refresh(db_dispute)
    return db_dispute

@router.delete("/fare-disputes/{dispute_id}")
def delete_fare_dispute(dispute_id: int, db: Session = Depends(get_db)):
    db_dispute = db.query(FareDispute).filter(FareDispute.id == dispute_id).first()
    if db_dispute is None:
        raise HTTPException(status_code=404, detail="Fare Dispute not found")
    db.delete(db_dispute)
    db.commit()
    return {"message": "Fare Dispute deleted successfully"} 

# --- POS Integration Endpoints ---

@router.post("/cards/issue", response_model=CardResponse)
def issue_card(card: CardCreate, db: Session = Depends(get_db)):
    # Issue a new card (wrapper for create_card, but with a dedicated endpoint)
    db_card = Card(
        id=card.id,
        **card.dict(exclude={"id"}),
        product="Standard",
        issue_date=datetime.now()
    )
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card

class ProductAddRequest(BaseModel):
    product: str
    value: float = 0.0

@router.post("/cards/{card_id}/products")
def add_product(card_id: str, req: ProductAddRequest, db: Session = Depends(get_db)):
    card = db.query(Card).filter(Card.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    card.product = req.product
    if req.value:
        card.balance += req.value
    db.commit()
    db.refresh(card)
    return {"message": f"Product {req.product} added to card {card_id}", "card": card.id}

class ReloadRequest(BaseModel):
    amount: float

@router.post("/cards/{card_id}/reload")
def reload_card(card_id: str, req: ReloadRequest, db: Session = Depends(get_db)):
    card = db.query(Card).filter(Card.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    card.balance += req.amount
    db.commit()
    db.refresh(card)
    return {"message": f"Card {card_id} reloaded with {req.amount}", "balance": card.balance}

@router.get("/cards/{card_id}/balance")
def get_card_balance(card_id: str, db: Session = Depends(get_db)):
    card = db.query(Card).filter(Card.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    return {"card_id": card.id, "balance": card.balance}

class PaymentSimRequest(BaseModel):
    card_id: str
    amount: float
    method: str

@router.post("/payment/simulate")
def simulate_payment(req: PaymentSimRequest, db: Session = Depends(get_db)):
    card = db.query(Card).filter(Card.id == req.card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    if card.balance < req.amount:
        return {"success": False, "message": "Insufficient balance"}
    card.balance -= req.amount
    db.commit()
    db.refresh(card)
    return {"success": True, "message": f"Payment of {req.amount} by {req.method} successful", "balance": card.balance}

@router.get("/cards/{card_id}/transactions")
def get_card_transactions(card_id: str, db: Session = Depends(get_db)):
    trips = db.query(Trip).filter(Trip.card_id == card_id).order_by(Trip.start_time.desc()).all()
    return [{
        "trip_id": t.id,
        "start_time": t.start_time,
        "end_time": t.end_time,
        "entry_location": t.entry_location,
        "exit_location": t.exit_location,
        "fare": t.fare,
        "route": t.route,
        "operator": t.operator,
        "transit_mode": t.transit_mode
    } for t in trips]

@router.get("/reports/summary")
def get_reports_summary(db: Session = Depends(get_db)):
    total_cards = db.query(func.count(Card.id)).scalar()
    total_customers = db.query(func.count(Customer.id)).scalar()
    total_trips = db.query(func.count(Trip.id)).scalar()
    total_balance = db.query(func.sum(Card.balance)).scalar() or 0.0
    return {
        "total_cards": total_cards,
        "total_customers": total_customers,
        "total_trips": total_trips,
        "total_balance": total_balance
    } 