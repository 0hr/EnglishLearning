from unicodedata import category

from fastapi import Depends
from fastapi.params import Query
from fastapi.routing import APIRouter

from sqlalchemy.orm import Session

from app.database import get_db
from app.requests.question import GetQuestion
from app.utils import verify_token
from models import Question, Option

question_route = APIRouter(prefix="/questions", tags=["questions"])


@question_route.get(
    path="/get-placement-questions",
    tags=["questions"],
    summary="Get questions", description="Get questions",
)
async def get_questions(db: Session = Depends(get_db)):
    questions = db.query(Question).filter(Question.category == 'placement').all()
    for q in questions:
        q.options = db.query(Option).filter(Option.question_id == q.id).all()
    return {'success': True, 'data': questions}


@question_route.get(
    path="/get",
    tags=["questions"],
    summary="Get questions",
    description="Get questions",
)
async def get_questions(category: str = Query(...), db: Session = Depends(get_db), token: str = Depends(verify_token)):
    questions = db.query(Question).filter(Question.category == category).all()
    for q in questions:
        q.options = db.query(Option).filter(Option.question_id == q.id).all()
    return {'success': True, 'data': questions}