from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
import schemas
import crud
from database import get_db, engine
import datetime
from passlib.context import CryptContext
import uuid
from fastapi import Body


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Brainrotism API")

@app.post("/players/login")
def auth_player(username: str = Body(...), db: Session = Depends(get_db)):
    
    player = db.query(models.Player).filter(models.Player.username == username).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
   
    return player


@app.post("/register")
def register(username: str = Body(...), password: str = Body(...), db: Session = Depends(get_db)):
    # Check if username already exists
    existing_user = db.query(models.Player).filter(models.Player.username == username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Hash the password
    hashed_pw = pwd_context.hash(password)

    # Create user
    user = models.Player(username=username, password=hashed_pw)
    db.add(user)
    db.commit()
    db.refresh(user)

    # Generate a session token
    session_token = str(uuid.uuid4())
    # You would store this in a PlayerSession table if you want persistent login

    return {
        "message": "User registered successfully",
        "player_id": user.id,
        "session_token": session_token
    }

# @app.get("/players/{player_id}")
# def get_player(username: str, DOB:):
#     ###
#     ###
#     ###
#     return {player}

# @app.post("/items/", response_model=schemas.ItemRead)
# def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
#     return crud.create_item(db, item)


# @app.get("/items/{item_id}", response_model=schemas.ItemRead)
# def read_item(item_id: int, db: Session = Depends(get_db)):
#     db_item = crud.get_item(db, item_id)
#     if db_item is None:
#         raise HTTPException(status_code=404, detail="Item not found")
#     return db_item



@app.get("/characters")
def list_characters(db: Session = Depends(get_db)):
    characters = db.query(models.Character).all()
    return characters


@app.get("/characters/{id}")
def get_character(character_id: int, db: Session = Depends(get_db)):
    character = db.query(models.Character).filter(models.Character.id == character_id).first()
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    return character

@app.post("/playercharacters/catch")
def catch_character(db: Session = Depends(get_db)):

    # Create PlayerCharacter
    player_character = models.PlayerCharacter(
        player_city_id=3
        character_id=character_id,
        coordinates=coordinates,
        caught_at=datetime.datetime.now(datetime.timezone.utc)
    )
    db.add(player_character)
    db.commit()
    db.refresh(player_character)
    
    return {"message": "Character caught successfully", "player_character_id": player_character.id}


@app.get("/city")
def get_city(db: Session = Depends(get_db)):
    city = db.query(models.City).filter(models.City.id == 1).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city

@app.get("/items")
def get_items(db: Session = Depends(get_db)):
    items = db.query(models.Item).all()
    return [
        {
            "id": item.id,
            "name": item.name,
            "description": item.description,
            "drop_rate": item.drop_rate,
            "price": item.price,
            "city_id": item.city_id
        }
        for item in items
    ]
