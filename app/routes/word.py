from fastapi import Depends
from fastapi.routing import APIRouter

from sqlalchemy.orm import Session

from app.database import get_db
from models import Word

word_route = APIRouter(prefix="/words", tags=["words"])

@word_route.get(
    path="/get",
    tags=["words"],
    summary="Get words texts", description="Get words texts",
)
async def get_words(db: Session = Depends(get_db)):
    questions = db.query(Word).all()
    return {'success': True, 'data': questions}
