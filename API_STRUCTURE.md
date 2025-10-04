# Brainrotism API Structure

## Overview
The API has been reorganized into a clean, modular structure with separate router files for different functionality categories.

## File Structure

```
brainrotism/
├── app.py                    # Main FastAPI application
├── utils.py                  # Helper functions and utilities
├── models.py                 # SQLAlchemy models
├── schemas.py                # Pydantic schemas
├── database.py               # Database configuration
└── routers/                  # Route modules
    ├── __init__.py
    ├── auth.py              # Authentication & Player routes
    ├── cities.py            # City & Progress routes
    ├── characters.py        # Character routes
    ├── items.py             # Item management routes
    ├── economy.py           # Economy, transactions, XP, leaderboard
    └── admin.py             # Admin & Debug routes
```

## Route Categories

### 🔐 Authentication & Players (`/routers/auth.py`)
- `POST /players/register` - Create new player account
- `POST /players/login` - Authenticate player
- `GET /players/{player_id}` - Get player profile

### 🏙️ Cities & Progress (`/routers/cities.py`)
- `GET /city` - Get current city info
- `POST /city/join` - Join a city
- `GET /city/{player_id}` - Get player progress
- `PATCH /city/{player_id}/update` - Update player progress

### 👥 Characters (`/routers/characters.py`)
- `GET /characters` - List all characters
- `GET /characters/{character_id}` - Get character details
- `POST /characters/catch` - Catch a character
- `GET /characters/player/{player_id}` - List player's characters

### 🎒 Items (`/routers/items.py`)
- `GET /items` - List all items
- `GET /items/{item_id}` - Get item details
- `POST /items/add` - Add item to inventory
- `GET /items/player/{player_id}` - List player's items
- `PATCH /items/player/{player_id}/{item_id}/use` - Use an item

### 💰 Economy (`/routers/economy.py`)
- `POST /economy/transactions/create` - Create transaction
- `GET /economy/transactions/{player_id}` - Get player transactions
- `POST /economy/xp/add` - Add XP
- `GET /economy/xp/{player_id}` - Get XP history
- `GET /economy/leaderboard` - Get leaderboard

### 🛠️ Admin & Debug (`/routers/admin.py`)
- `POST /admin/characters/spawn` - Spawn character (testing)
- `POST /admin/items/drop` - Force drop item (testing)

## Benefits of This Structure

1. **Separation of Concerns**: Each router handles a specific domain
2. **Maintainability**: Easy to find and modify specific functionality
3. **Scalability**: Simple to add new features or modify existing ones
4. **Organization**: Clear categorization with descriptive tags
5. **Reusability**: Helper functions in `utils.py` can be shared across routers

## Usage

The main `app.py` file now simply imports and includes all routers:

```python
from fastapi import FastAPI
import models
from database import engine
from routers import auth, cities, characters, items, economy, admin

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Brainrotism API")

# Include all routers
app.include_router(auth.router)
app.include_router(cities.router)
app.include_router(characters.router)
app.include_router(items.router)
app.include_router(economy.router)
app.include_router(admin.router)
```

All routes maintain their original functionality while being properly organized and tagged for better API documentation.
