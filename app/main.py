from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from app.models import user_models, engine
from app.users import db_with_dummy_data
from app.users.endpoints import router as user_router
from app.async_queries.endpoints import router as async_router


# Handle CORS with app
middleware = [Middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True,
                         allow_methods=['*'], allow_headers=['*'])]


app = FastAPI(middleware=middleware)
app.include_router(user_router, prefix='/api')
app.include_router(async_router, prefix='/api')


@app.on_event("startup")
async def fill_with_dummy_data():
    # Create db tables if not exists
    user_models.Base.metadata.create_all(bind=engine)
    db_with_dummy_data.fill()
