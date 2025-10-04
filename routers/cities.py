from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from database import get_db
import models
import schemas
import datetime
from utils import get_player_city_by_player_id

router = APIRouter(prefix="/city", tags=["Cities & Progress"])


@router.get("", response_model=schemas.CityRead)
def get_current_city(db: Session = Depends(get_db)):
    """Return info about the current city (bounds, name, etc.)"""
    # Assuming city with id=1 is the current city
    city = db.query(models.City).filter(models.City.id == 1).first()
    if not city:
        raise HTTPException(status_code=404, detail="Current city not found")
    return city


@router.post("/join", response_model=schemas.PlayerCityRead)
def join_city(player_city: schemas.PlayerCityCreate, db: Session = Depends(get_db)):
    """Attach player to the hardcoded city, initialize xp/money"""
    # Check if player already exists in this city
    existing = db.query(models.PlayerCity).filter(
        and_(models.PlayerCity.player_id == player_city.player_id, 
             models.PlayerCity.city_id == player_city.city_id)
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Player already in this city")
    
    db_player_city = models.PlayerCity(**player_city.dict())
    db.add(db_player_city)
    db.commit()
    db.refresh(db_player_city)
    return db_player_city


@router.get("/{player_id}", response_model=schemas.PlayerCityRead)
def get_player_progress(player_id: int, db: Session = Depends(get_db)):
    """Get player's progress in the city (xp, money, last active)"""
    player_city = get_player_city_by_player_id(db, player_id)
    if not player_city:
        raise HTTPException(status_code=404, detail="Player not found in city")
    return player_city


@router.patch("/{player_id}/update", response_model=schemas.PlayerCityRead)
def update_player_progress(player_id: int, update_data: schemas.PlayerCityUpdate, db: Session = Depends(get_db)):
    """Update xp, money totals (after actions)"""
    player_city = get_player_city_by_player_id(db, player_id)
    if not player_city:
        raise HTTPException(status_code=404, detail="Player not found in city")
    
    if update_data.xp_total is not None:
        player_city.xp_total = update_data.xp_total
    if update_data.money_total is not None:
        player_city.money_total = update_data.money_total
    
    player_city.last_active = datetime.datetime.now(datetime.UTC)
    db.commit()
    db.refresh(player_city)
    return player_city
