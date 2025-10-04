from sqlalchemy.orm import Session
from sqlalchemy import and_
import models


def get_player_city_by_player_id(db: Session, player_id: int, city_id: int = 1):
    """Get player city record by player_id and city_id (defaults to city 1)"""
    return db.query(models.PlayerCity).filter(
        and_(models.PlayerCity.player_id == player_id, models.PlayerCity.city_id == city_id)
    ).first()
