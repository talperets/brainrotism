from sqlalchemy import Column, Integer, String, DateTime, Date, Float, JSON, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import datetime


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True, nullable=False, unique=True)
    created_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.UTC))
    date_of_birth = Column(Date, nullable=True)

    # Relationships
    player_cities = relationship("PlayerCity", back_populates="player")


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    country = Column(String, nullable=False)
    lat_min = Column(Float, nullable=False)
    lat_max = Column(Float, nullable=False)
    lng_min = Column(Float, nullable=False)
    lng_max = Column(Float, nullable=False)

    # Relationships
    player_cities = relationship("PlayerCity", back_populates="city")
    items = relationship("Item", back_populates="city")


class PlayerCity(Base):
    __tablename__ = "player_cities"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)
    xp_total = Column(Integer, default=0)
    money_total = Column(Integer, default=0)
    last_active = Column(DateTime, default=lambda: datetime.datetime.now(datetime.UTC))

    # Relationships
    player = relationship("Player", back_populates="player_cities")
    city = relationship("City", back_populates="player_cities")
    player_characters = relationship("PlayerCharacter", back_populates="player_city")
    player_items = relationship("PlayerItem", back_populates="player_city")
    transactions = relationship("Transaction", back_populates="player_city")
    xp_records = relationship("XP", back_populates="player_city")


class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    commonality = Column(Integer, nullable=False)
    asset_name = Column(String, nullable=False)
    icon = Column(String, nullable=False)
    description = Column(String, nullable=True)

    # Relationships
    character_items = relationship("CharacterItem", back_populates="character")
    player_characters = relationship("PlayerCharacter", back_populates="character")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    drop_rate = Column(Float, nullable=False)
    price = Column(Integer, nullable=False)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=True)

    # Relationships
    city = relationship("City", back_populates="items")
    character_items = relationship("CharacterItem", back_populates="item")
    player_items = relationship("PlayerItem", back_populates="item")


class CharacterItem(Base):
    __tablename__ = "character_items"

    character_id = Column(Integer, ForeignKey("characters.id"), primary_key=True)
    item_id = Column(Integer, ForeignKey("items.id"), primary_key=True)

    # Relationships
    character = relationship("Character", back_populates="character_items")
    item = relationship("Item", back_populates="character_items")


class PlayerCharacter(Base):
    __tablename__ = "player_characters"

    id = Column(Integer, primary_key=True, index=True)
    player_city_id = Column(Integer, ForeignKey("player_cities.id"), nullable=False)
    character_id = Column(Integer, ForeignKey("characters.id"), nullable=False)
    coordinates = Column(JSON, nullable=True)
    caught_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.UTC))

    # Relationships
    player_city = relationship("PlayerCity", back_populates="player_characters")
    character = relationship("Character", back_populates="player_characters")


class PlayerItem(Base):
    __tablename__ = "player_items"

    player_city_id = Column(Integer, ForeignKey("player_cities.id"), primary_key=True)
    item_id = Column(Integer, ForeignKey("items.id"), primary_key=True)
    quantity = Column(Integer, default=1)

    # Relationships
    player_city = relationship("PlayerCity", back_populates="player_items")
    item = relationship("Item", back_populates="player_items")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    player_city_id = Column(Integer, ForeignKey("player_cities.id"), nullable=False)
    amount = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.datetime.now(datetime.UTC))

    # Relationships
    player_city = relationship("PlayerCity", back_populates="transactions")


class XP(Base):
    __tablename__ = "xp"

    id = Column(Integer, primary_key=True, index=True)
    player_city_id = Column(Integer, ForeignKey("player_cities.id"), nullable=False)
    amount = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.datetime.now(datetime.UTC))

    # Relationships
    player_city = relationship("PlayerCity", back_populates="xp_records")
