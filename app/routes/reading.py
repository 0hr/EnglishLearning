from fastapi import Depends
from fastapi.routing import APIRouter

from sqlalchemy.orm import Session

from app.database import get_db
from app.utils import verify_token
from models import ReadingMaterial

reading_route = APIRouter(prefix="/readings", tags=["readings"], dependencies=[Depends(verify_token)])

@reading_route.get(
    path="/get",
    tags=["reading"],
    summary="Get reading texts", description="Get reading texts",
)
async def get_questions(db: Session = Depends(get_db)):
    questions = db.query(ReadingMaterial).all()
    return {'success': True, 'data': questions}
