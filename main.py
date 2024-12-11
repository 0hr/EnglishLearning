from dotenv import load_dotenv
load_dotenv()


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from app.routes.speaking import speaking_router



from app.routes.user import user_route
from app.routes.word import word_route
from app.routes.reading import reading_route
from app.routes.question import question_route

app = FastAPI(title="Smart English Api", version="1.0", openapi_url="/openapi.json", docs_url="/docs", redoc_url="/redoc")

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/audio", StaticFiles(directory="temp"), name="audio")
app.include_router(user_route)
app.include_router(word_route)
app.include_router(reading_route)
app.include_router(question_route)
app.include_router(speaking_router)


