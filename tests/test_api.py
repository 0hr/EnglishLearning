import hashlib
import os
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from models import Base, User, Question, Option, ReadingMaterial
from app.database import get_db

# Scenarios
scenarios("features/user.feature")
scenarios("features/question.feature")
scenarios("features/reading.feature")


# Test setup
DATABASE_URL = os.getenv('TEST_DATABASE_URL')
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@given('a clean database')
def clean_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


@given(parsers.parse('a registered user with email "{email}" and password "{password}"'))
def register_user(email, password):
    db = TestingSessionLocal()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    new_user = User(name="Test User", email=email, password=hashed_password, level="user")
    db.add(new_user)
    db.commit()
    db.close()


@when(parsers.parse('I login with email "{email}" and password "{password}"'))
def login_user(email, password):
    response = client.post("/user/login", json={"email": email, "password": password})
    pytest.response = response


@then('I should receive a token if the credentials are valid')
def verify_login_response():
    assert pytest.response.status_code == 200
    assert "access_token" in pytest.response.json()[0]


@when(parsers.parse('I register a new user with email "{email}" and password "{password}"'))
def register_user_endpoint(email, password):
    response = client.post(
        "/user/register",
        json={
            "name": "Test User",
            "email": email,
            "password": password,
            "level": "b1"
        },
    )
    pytest.response = response


@then('I should receive a success message if the registration is valid')
def verify_register_response():
    assert pytest.response.status_code == 200
    assert pytest.response.json()["status"] == "register successfully"


@when(parsers.parse('I request a password reset for email "{email}"'))
def forgot_password(email):
    response = client.post("/user/forgot-password", json={"email": email})
    pytest.response = response


@then('I should receive a password reset token')
def verify_forgot_password_response():
    assert pytest.response.status_code == 200
    assert pytest.response.json()["message"] == "reset token sent successfully"


@when(parsers.parse('I reset my password with token "{token}" and new password "{password}"'))
def reset_password(token, password):
    response = client.post(
        "/user/reset-password", json={"reset_password_token": token, "password": password}
    )
    pytest.response = response


@then('I should receive a success message for the password reset')
def verify_reset_password_response():
    assert pytest.response.status_code == 200
    assert pytest.response.json()["message"] == "Reset password successfully"

@given(parsers.parse('a question with category "{category}"'))
def add_question(category):
    db = TestingSessionLocal()
    new_question = Question(category=category, question="She _____ to the market now.", correct_option=1)
    db.add(new_question)
    db.commit()
    option1 = Option(question_id=new_question.id, option="goes")
    option2 = Option(question_id=new_question.id, option="going")
    option3 = Option(question_id=new_question.id, option="go")
    option4 = Option(question_id=new_question.id, option="went")
    db.add(option1)
    db.add(option2)
    db.add(option3)
    db.add(option4)
    db.commit()
    db.close()


@when('I request placement questions')
def request_placement_questions():
    response = client.get("/questions/get-placement-questions")
    pytest.response = response


@then('I should receive the placement questions')
def verify_placement_questions():
    assert pytest.response.status_code == 200
    assert pytest.response.json()["success"] is True
    assert len(pytest.response.json()["data"]) > 0


@when(parsers.parse('I request questions with category "{category}"'))
def request_questions(category):
    access_token = pytest.response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/questions/get", headers=headers, params={"category": category})
    pytest.response = response


@then(parsers.parse('I should receive the questions with category "{category}"'))
def verify_questions(category):
    assert pytest.response.status_code == 200
    assert pytest.response.json()["success"] is True
    for question in pytest.response.json()["data"]:
        assert question["category"] == category

@given('a reading material exists')
def reading_material_exists():
    db = TestingSessionLocal()
    reading_material = ReadingMaterial(id=1, title="Sample Reading", content="This is a sample reading material.", category="sample")
    db.add(reading_material)
    db.commit()

@when('I request reading texts')
def request_reading_texts():
    access_token = pytest.response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get('/readings/get', headers=headers)
    pytest.response = response

@then('I should receive the reading texts')
def should_receive_reading_texts():
    assert pytest.response.status_code == 200
    assert pytest.response.json()['success'] is True
    assert len(pytest.response.json()['data']) > 0
