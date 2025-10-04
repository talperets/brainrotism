from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import datetime
from database import get_db
import models
import schemas
from utils import get_player_city_by_player_id

router = APIRouter(prefix="/economy", tags=["Economy"])


@router.post("/transactions/create", response_model=schemas.TransactionRead)
def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    """Record a money transaction (gain/spend)"""
    # Verify player_city exists
    player_city = db.query(models.PlayerCity).filter(
        models.PlayerCity.id == transaction.player_city_id
    ).first()
    if not player_city:
        raise HTTPException(status_code=404, detail="Player city not found")
    
    db_transaction = models.Transaction(**transaction.dict())
    db.add(db_transaction)
    
    # Update player's money total
    player_city.money_total += transaction.amount
    player_city.last_active = datetime.datetime.now(datetime.UTC)
    
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


@router.get("/transactions/{player_id}", response_model=List[schemas.TransactionRead])
def get_player_transactions(player_id: int, db: Session = Depends(get_db)):
    """Get all transactions for a player"""
    player_city = get_player_city_by_player_id(db, player_id)
    if not player_city:
        raise HTTPException(status_code=404, detail="Player not found in city")
    
    transactions = db.query(models.Transaction).filter(
        models.Transaction.player_city_id == player_city.id
    ).all()
    return transactions


@router.post("/xp/add", response_model=schemas.XPRead)
def add_xp(xp_data: schemas.XPCreate, db: Session = Depends(get_db)):
    """Add an XP entry for a player"""
    # Verify player_city exists
    player_city = db.query(models.PlayerCity).filter(
        models.PlayerCity.id == xp_data.player_city_id
    ).first()
    if not player_city:
        raise HTTPException(status_code=404, detail="Player city not found")
    
    db_xp = models.XP(**xp_data.dict())
    db.add(db_xp)
    
    # Update player's XP total
    player_city.xp_total += xp_data.amount
    player_city.last_active = datetime.datetime.now(datetime.UTC)
    
    db.commit()
    db.refresh(db_xp)
    return db_xp


@router.get("/xp/{player_id}", response_model=List[schemas.XPRead])
def get_player_xp(player_id: int, db: Session = Depends(get_db)):
    """Get XP history for a player"""
    player_city = get_player_city_by_player_id(db, player_id)
    if not player_city:
        raise HTTPException(status_code=404, detail="Player not found in city")
    
    xp_records = db.query(models.XP).filter(
        models.XP.player_city_id == player_city.id
    ).all()
    return xp_records


@router.get("/leaderboard", response_model=List[schemas.LeaderboardEntry])
def get_leaderboard(db: Session = Depends(get_db)):
    """Get leaderboard of players ranked by total XP in the city"""
    # Assuming city_id = 1 for the current city
    leaderboard = db.query(
        models.Player.id,
        models.Player.username,
        models.PlayerCity.xp_total,
        models.PlayerCity.money_total
    ).join(
        models.PlayerCity, models.Player.id == models.PlayerCity.player_id
    ).filter(
        models.PlayerCity.city_id == 1
    ).order_by(
        models.PlayerCity.xp_total.desc()
    ).all()
    
    return [schemas.LeaderboardEntry(
        player_id=entry.id,
        username=entry.username,
        xp_total=entry.xp_total,
        money_total=entry.money_total
    ) for entry in leaderboard]
