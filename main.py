from fastapi import FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import models, schemas, auth, uuid
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.post("/signup", response_model=schemas.UserResponse)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pwd = auth.get_password_hash(user.password)
    new_user = models.User(email=user.email, hashed_password=hashed_pwd)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not db_user or not auth.verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = auth.create_access_token(data={"sub": db_user.email})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/events", response_model=schemas.EventResponse)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db), current_user: str = Depends(auth.get_current_user)):
    user = db.query(models.User).filter(models.User.email == current_user).first()
    new_event = models.Event(**event.dict(), owner_id=user.id)
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event

@app.get("/my-events")
def get_my_events(db: Session = Depends(get_db), current_user: str = Depends(auth.get_current_user)):
    user = db.query(models.User).filter(models.User.email == current_user).first()
    return db.query(models.Event).filter(models.Event.owner_id == user.id).all()

@app.post("/sub-events", response_model=schemas.SubEventResponse)
def create_sub_event(sub: schemas.SubEventCreate, db: Session = Depends(get_db)):
    new_sub = models.SubEvent(**sub.dict())
    db.add(new_sub)
    db.commit()
    db.refresh(new_sub)
    return new_sub

@app.post("/register-team/{event_id}")
def register_team(event_id: int, user_email: str, team_name: str, team_size: int, db: Session = Depends(get_db)):
    if team_size < 2 or team_size > 5:
        raise HTTPException(status_code=400, detail="Team size must be between 2 and 5")
    user = db.query(models.User).filter(models.User.email == user_email).first()
    ticket_code = f"TEAM-{str(uuid.uuid4())[:8].upper()}"
    new_reg = models.Registration(user_id=user.id, event_id=event_id, ticket_code=ticket_code, team_name=team_name, team_size=team_size)
    db.add(new_reg)
    db.commit()
    return {"status": "Team registered", "ticket_code": ticket_code}

@app.post("/announcements")
async def post_announcement(event_id: int, message: str, db: Session = Depends(get_db)):
    new_announcement = models.Announcement(event_id=event_id, message=message)
    db.add(new_announcement)
    db.commit()
    await manager.broadcast(f"New Announcement: {message}")
    return {"status": "Announcement posted"}

@app.websocket("/ws/announcements")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)