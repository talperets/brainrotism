from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from database import get_db
import models
import schemas

router = APIRouter(prefix="/admin", tags=["Admin & Debug"])


@router.post("/characters/spawn")
def spawn_character(spawn_data: schemas.CharacterSpawn, db: Session = Depends(get_db)):
    """Spawn a character instance at coordinates (testing)"""
    # Verify character exists
    character = db.query(models.Character).filter(
        models.Character.id == spawn_data.character_id
    ).first()
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    
    # This would typically spawn a character in the game world
    # For now, just return success
    return {"message": f"Character {spawn_data.character_id} spawned at coordinates {spawn_data.coordinates}"}


@router.post("/items/drop")
def drop_item(drop_data: schemas.ItemDrop, db: Session = Depends(get_db)):
    """Force-drop an item for a player (testing)"""
    # Verify player_city exists
    player_city = db.query(models.PlayerCity).filter(
        models.PlayerCity.id == drop_data.player_city_id
    ).first()
    if not player_city:
        raise HTTPException(status_code=404, detail="Player city not found")
    
    # Verify item exists
    item = db.query(models.Item).filter(models.Item.id == drop_data.item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Add item to player inventory
    existing_player_item = db.query(models.PlayerItem).filter(
        and_(models.PlayerItem.player_city_id == drop_data.player_city_id,
             models.PlayerItem.item_id == drop_data.item_id)
    ).first()
    
    if existing_player_item:
        existing_player_item.quantity += drop_data.quantity
        db.commit()
    else:
        db_player_item = models.PlayerItem(
            player_city_id=drop_data.player_city_id,
            item_id=drop_data.item_id,
            quantity=drop_data.quantity
        )
        db.add(db_player_item)
        db.commit()
    
    return {"message": f"Dropped {drop_data.quantity} of item {drop_data.item_id} for player"}
