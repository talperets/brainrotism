from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models
import schemas
from utils import get_player_city_by_player_id

router = APIRouter(prefix="/characters", tags=["Characters"])


@router.get("", response_model=List[schemas.CharacterRead])
def list_characters(db: Session = Depends(get_db)):
    """List all available characters (global)"""
    characters = db.query(models.Character).all()
    return characters


@router.get("/{character_id}", response_model=schemas.CharacterRead)
def get_character(character_id: int, db: Session = Depends(get_db)):
    """Fetch details of a single character"""
    character = db.query(models.Character).filter(models.Character.id == character_id).first()
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    return character


@router.post("/catch", response_model=schemas.PlayerCharacterRead)
def catch_character(player_character: schemas.PlayerCharacterCreate, db: Session = Depends(get_db)):
    """Player captures a character (requires coordinates)"""
    # Verify player_city exists
    player_city = db.query(models.PlayerCity).filter(
        models.PlayerCity.id == player_character.player_city_id
    ).first()
    if not player_city:
        raise HTTPException(status_code=404, detail="Player city not found")
    
    # Verify character exists
    character = db.query(models.Character).filter(
        models.Character.id == player_character.character_id
    ).first()
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    
    db_player_character = models.PlayerCharacter(**player_character.dict())
    db.add(db_player_character)
    db.commit()
    db.refresh(db_player_character)
    return db_player_character


@router.get("/player/{player_id}", response_model=List[schemas.PlayerCharacterRead])
def list_player_characters(player_id: int, db: Session = Depends(get_db)):
    """List all characters caught by a player in the city"""
    player_city = get_player_city_by_player_id(db, player_id)
    if not player_city:
        raise HTTPException(status_code=404, detail="Player not found in city")
    
    player_characters = db.query(models.PlayerCharacter).filter(
        models.PlayerCharacter.player_city_id == player_city.id
    ).all()
    return player_characters
