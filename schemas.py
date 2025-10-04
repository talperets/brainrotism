from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime, date


# Player schemas
class PlayerBase(BaseModel):
    username: str
    date_of_birth: Optional[date] = None


class PlayerCreate(PlayerBase):
    pass


class PlayerRead(PlayerBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# City schemas
class CityBase(BaseModel):
    name: str
    country: str
    lat_min: float
    lat_max: float
    lng_min: float
    lng_max: float


class CityRead(CityBase):
    id: int

    class Config:
        from_attributes = True


# PlayerCity schemas
class PlayerCityBase(BaseModel):
    xp_total: int = 0
    money_total: int = 0


class PlayerCityCreate(BaseModel):
    player_id: int
    city_id: int


class PlayerCityRead(PlayerCityBase):
    id: int
    player_id: int
    city_id: int
    last_active: datetime

    class Config:
        from_attributes = True


class PlayerCityUpdate(BaseModel):
    xp_total: Optional[int] = None
    money_total: Optional[int] = None


# Character schemas
class CharacterBase(BaseModel):
    name: str
    commonality: int
    asset_name: str
    icon: str
    description: Optional[str] = None


class CharacterRead(CharacterBase):
    id: int

    class Config:
        from_attributes = True


# Item schemas
class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    drop_rate: float
    price: int
    city_id: Optional[int] = None


class ItemRead(ItemBase):
    id: int

    class Config:
        from_attributes = True


# PlayerCharacter schemas
class PlayerCharacterCreate(BaseModel):
    player_city_id: int
    character_id: int
    coordinates: Optional[Dict[str, Any]] = None


class PlayerCharacterRead(BaseModel):
    id: int
    player_city_id: int
    character_id: int
    coordinates: Optional[Dict[str, Any]] = None
    caught_at: datetime
    character: CharacterRead

    class Config:
        from_attributes = True


# PlayerItem schemas
class PlayerItemAdd(BaseModel):
    player_city_id: int
    item_id: int
    quantity: int = 1


class PlayerItemRead(BaseModel):
    player_city_id: int
    item_id: int
    quantity: int
    item: ItemRead

    class Config:
        from_attributes = True


class PlayerItemUse(BaseModel):
    quantity: int = 1


# Transaction schemas
class TransactionCreate(BaseModel):
    player_city_id: int
    amount: int


class TransactionRead(BaseModel):
    id: int
    player_city_id: int
    amount: int
    timestamp: datetime

    class Config:
        from_attributes = True


# XP schemas
class XPCreate(BaseModel):
    player_city_id: int
    amount: int


class XPRead(BaseModel):
    id: int
    player_city_id: int
    amount: int
    timestamp: datetime

    class Config:
        from_attributes = True


# Leaderboard schemas
class LeaderboardEntry(BaseModel):
    player_id: int
    username: str
    xp_total: int
    money_total: int

    class Config:
        from_attributes = True


# Admin/Debug schemas
class CharacterSpawn(BaseModel):
    character_id: int
    coordinates: Dict[str, Any]


class ItemDrop(BaseModel):
    player_city_id: int
    item_id: int
    quantity: int = 1
