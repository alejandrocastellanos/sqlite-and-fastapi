from fastapi import FastAPI

from infraestructure.db.db import engine
from infraestructure.routes.user_router import router as UserRouter

from infraestructure.models.user import Base
app = FastAPI(debug=True)

Base.metadata.create_all(bind=engine)

app.include_router(UserRouter)
