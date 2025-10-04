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
