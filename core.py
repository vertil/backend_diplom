from fastapi import FastAPI

from api.routers import router
from fastapi.middleware.cors import CORSMiddleware


tags_metadata = [
    {
        'name': 'auth',
        'description': "Authorization and registration"
    },
    {
        'name': 'core',
        'description': "Work with database data"
    },

]

app = FastAPI(
    title='myCV',
    description='myCV API',
    version='1.0.0',
    openapi_tags=tags_metadata,
)
app.include_router(router)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)