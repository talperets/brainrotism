from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List
from database import get_db
import models
import schemas
from utils import get_player_city_by_player_id

router = APIRouter(prefix="/items", tags=["Items"])


@router.get("", response_model=List[schemas.ItemRead])
def list_items(db: Session = Depends(get_db)):
    """List all items (both global and city-specific)"""
    items = db.query(models.Item).all()
    return items


@router.get("/{item_id}", response_model=schemas.ItemRead)
def get_item(item_id: int, db: Session = Depends(get_db)):
    """Fetch details about one item"""
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.post("/add", response_model=schemas.PlayerItemRead)
def add_player_item(player_item: schemas.PlayerItemAdd, db: Session = Depends(get_db)):
    """Add an item to player inventory (loot drop, purchase, etc.)"""
    # Verify player_city exists
    player_city = db.query(models.PlayerCity).filter(
        models.PlayerCity.id == player_item.player_city_id
    ).first()
    if not player_city:
        raise HTTPException(status_code=404, detail="Player city not found")
    
    # Verify item exists
    item = db.query(models.Item).filter(models.Item.id == player_item.item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Check if player already has this item
    existing_player_item = db.query(models.PlayerItem).filter(
        and_(models.PlayerItem.player_city_id == player_item.player_city_id,
             models.PlayerItem.item_id == player_item.item_id)
    ).first()
    
    if existing_player_item:
        existing_player_item.quantity += player_item.quantity
        db.commit()
        db.refresh(existing_player_item)
        return existing_player_item
    else:
        db_player_item = models.PlayerItem(**player_item.dict())
        db.add(db_player_item)
        db.commit()
        db.refresh(db_player_item)
        return db_player_item


@router.get("/player/{player_id}", response_model=List[schemas.PlayerItemRead])
def list_player_items(player_id: int, db: Session = Depends(get_db)):
    """List all items a player owns in the city"""
    player_city = get_player_city_by_player_id(db, player_id)
    if not player_city:
        raise HTTPException(status_code=404, detail="Player not found in city")
    
    player_items = db.query(models.PlayerItem).filter(
        models.PlayerItem.player_city_id == player_city.id
    ).all()
    return player_items


@router.patch("/player/{player_id}/{item_id}/use")
def use_player_item(player_id: int, item_id: int, use_data: schemas.PlayerItemUse, db: Session = Depends(get_db)):
    """Use or consume an item"""
    player_city = get_player_city_by_player_id(db, player_id)
    if not player_city:
        raise HTTPException(status_code=404, detail="Player not found in city")
    
    player_item = db.query(models.PlayerItem).filter(
        and_(models.PlayerItem.player_city_id == player_city.id,
             models.PlayerItem.item_id == item_id)
    ).first()
    
    if not player_item:
        raise HTTPException(status_code=404, detail="Player does not have this item")
    
    if player_item.quantity < use_data.quantity:
        raise HTTPException(status_code=400, detail="Not enough quantity")
    
    player_item.quantity -= use_data.quantity
    
    if player_item.quantity <= 0:
        db.delete(player_item)
    else:
        db.commit()
        db.refresh(player_item)
    
    db.commit()
    return {"message": f"Used {use_data.quantity} of item {item_id}"}
