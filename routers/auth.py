from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas

router = APIRouter(prefix="/players", tags=["Authentication & Players"])


@router.post("/register", response_model=schemas.PlayerRead)
def register_player(player: schemas.PlayerCreate, db: Session = Depends(get_db)):
    """Create a new player account"""
    # Check if username already exists
    existing_player = db.query(models.Player).filter(models.Player.username == player.username).first()
    if existing_player:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    db_player = models.Player(**player.dict())
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player


@router.post("/login", response_model=schemas.PlayerRead)
def login_player(username: str, db: Session = Depends(get_db)):
    """Authenticate player"""
    player = db.query(models.Player).filter(models.Player.username == username).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player


@router.get("/{player_id}", response_model=schemas.PlayerRead)
def get_player(player_id: int, db: Session = Depends(get_db)):
    """Fetch player profile (username, DOB, created_at)"""
    player = db.query(models.Player).filter(models.Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player
