from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, Enum, Boolean, DateTime, DECIMAL, TIMESTAMP
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

# Database URL
DATABASE_URL = "mysql+mysqlconnector://root:jovs123@localhost/ormquiz_db"
engine = create_engine(DATABASE_URL)

# Base class for all models
Base = declarative_base()

# Define the User model
class User(Base):
    __tablename__ = 'User'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(Enum('teacher', 'student', name='role_enum'), nullable=False, default='student')
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Define the Quiz model
class Quiz(Base):
    __tablename__ = 'Quiz'

    quiz_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    quiz_code = Column(String(255), unique=True)
    teacher_id = Column(Integer, ForeignKey('User.user_id'), nullable=False)
    duration = Column(Integer)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    teacher = relationship('User', back_populates='quizzes')

# Define the Question model
class Question(Base):
    __tablename__ = 'Question'

    question_id = Column(Integer, primary_key=True, autoincrement=True)
    quiz_id = Column(Integer, ForeignKey('Quiz.quiz_id'), nullable=False)
    question_text = Column(Text, nullable=False)
    question_type = Column(Enum('MCQ', 'True/False', 'Short Answer', 'Multimedia', name='question_type_enum'), nullable=False)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    quiz = relationship('Quiz', back_populates='questions')

# Define the OptionTable model
class OptionTable(Base):
    __tablename__ = 'OptionTable'

    option_id = Column(Integer, primary_key=True, autoincrement=True)
    quiz_id = Column(Integer, ForeignKey('Quiz.quiz_id'), nullable=False)
    question_id = Column(Integer, ForeignKey('Question.question_id'), nullable=False)
    option_text = Column(String(255), nullable=False)
    is_correct = Column(Boolean, default=False)

# Define the Answer model
class Answer(Base):
    __tablename__ = 'Answer'

    answer_id = Column(Integer, primary_key=True, autoincrement=True)
    question_id = Column(Integer, ForeignKey('Question.question_id'), nullable=False)
    student_id = Column(Integer, ForeignKey('User.user_id'), nullable=False)
    answer_text = Column(Text)
    submitted_at = Column(DateTime, default=datetime.utcnow)

# Define the Result model
class Result(Base):
    __tablename__ = 'Result'

    result_id = Column(Integer, primary_key=True, autoincrement=True)
    quiz_id = Column(Integer, ForeignKey('Quiz.quiz_id'), nullable=False)
    student_id = Column(Integer, ForeignKey('User.user_id'), nullable=False)
    score = Column(DECIMAL(5,2))
    submitted_at = Column(DateTime, default=datetime.utcnow)

# Relationship setups
User.quizzes = relationship('Quiz', back_populates='teacher')
Quiz.questions = relationship('Question', back_populates='quiz')




# Create tables
Base.metadata.create_all(engine)

# Session creation
Session = sessionmaker(bind=engine)
session = Session()

# Add 5 Users
users = [
    User(name='Jov Roncal 1', email='jovroncal1@example.com', password='password123', role='teacher'),
    User(name='Jov Roncal 2', email='jovroncal2@example.com', password='password123', role='student'),
    User(name='Jov Roncal 3', email='jovroncal3@example.com', password='password123', role='student'),
    User(name='Jov Roncal 4', email='jovroncal4@example.com', password='password123', role='student'),
    User(name='Jov Roncal 5', email='jovroncal5@example.com', password='password123', role='teacher')
]

session.add_all(users)
session.commit()

# Add 5 Quizzes
quizzes = [
    Quiz(title='Math Quiz 2', description='Intermediate Math Quiz', teacher_id=1, quiz_code='MATH456', duration=40),
    Quiz(title='Science Quiz 2', description='Advanced Science Quiz', teacher_id=2, quiz_code='SCI456', duration=50),
    Quiz(title='History Quiz 2', description='Advanced History Quiz', teacher_id=3, quiz_code='HIST456', duration=30),
    Quiz(title='Geography Quiz 2', description='Advanced Geography Quiz', teacher_id=4, quiz_code='GEO456', duration=45),
    Quiz(title='Literature Quiz 2', description='Advanced Literature Quiz', teacher_id=5, quiz_code='LIT456', duration=60)
]
session.add_all(quizzes)
session.commit()

# Add 5 Questions for each quiz (total 5 quizzes)
questions = [
    # Math Quiz 2
    Question(quiz_id=1, question_text='What is 15 * 3?', question_type='MCQ'),
    Question(quiz_id=1, question_text='True or False: Pi is a rational number.', question_type='True/False'),
    # Science Quiz 2
    Question(quiz_id=2, question_text='What is the chemical symbol for Water?', question_type='MCQ'),
    Question(quiz_id=2, question_text='True or False: Light travels faster than sound.', question_type='True/False'),
    # History Quiz 2
    Question(quiz_id=3, question_text='Who wrote the Declaration of Independence?', question_type='Short Answer')
]

session.add_all(questions)
session.commit()

# Add 5 Options for each question
options = [
    # Math Quiz 2 - 1st Question
    OptionTable(quiz_id=1, question_id=1, option_text='40', is_correct=False),
    OptionTable(quiz_id=1, question_id=1, option_text='45', is_correct=True),
    # Science Quiz 2 - 1st Question
    OptionTable(quiz_id=2, question_id=3, option_text='H2O', is_correct=True),
    OptionTable(quiz_id=2, question_id=3, option_text='CO2', is_correct=False),
    # History Quiz 2 - 1st Question
    OptionTable(quiz_id=3, question_id=5, option_text='Thomas Jefferson', is_correct=True)
]

session.add_all(options)
session.commit()

# Add 5 Answers for questions
answers = [
    Answer(question_id=1, student_id=1, answer_text='45'),
    Answer(question_id=2, student_id=2, answer_text='False'),
    Answer(question_id=3, student_id=3, answer_text='H2O'),
    Answer(question_id=4, student_id=4, answer_text='True'),
    Answer(question_id=5, student_id=5, answer_text='Thomas Jefferson')
]

session.add_all(answers)
session.commit()

# Add 5 Results
results = [
    Result(quiz_id=1, student_id=1, score=85.0),
    Result(quiz_id=2, student_id=2, score=95.0),
    Result(quiz_id=3, student_id=3, score=80.0),
    Result(quiz_id=4, student_id=4, score=90.0),
    Result(quiz_id=5, student_id=5, score=98.0)
]

session.add_all(results)
session.commit()

print("Dummy data inserted successfully.")

# Create a new user
def add_user():
    user_data = {
        "name": "ramon jov",
        "email": "hotdog@example.com",
        "password": "password123",
        "role": "student"
    }
    new_user = User(**user_data)
    session.add(new_user)
    session.commit()
    print(f"User titled '{new_user.name}' added.")


# Read all users
def get_all_users():
    users = session.query(User).all()
    if users:
        for user in users:
            print(f"User: {user.name}, Email: {user.email}, Role: {user.role}")
    else:
        print("No users found.")


# Update an existing user
def update_user():
    user_to_update = session.query(User).filter_by(user_id=1).first()
    if user_to_update:
        user_to_update.name = "Jov Roncal"
        user_to_update.role = "teacher"
        session.commit()
        print(f"User ID {user_to_update.user_id} updated to '{user_to_update.name}' with role '{user_to_update.role}'.")
    else:
        print("User not found.")


# Delete a user
def delete_user():
    user_to_delete = session.query(User).filter_by(user_id=6).first()
    if user_to_delete:
        session.delete(user_to_delete)
        session.commit()
        print(f"User titled '{user_to_delete.name}' deleted.")
    else:
        print("User not found.")


# Running the CRUD operations for User
if __name__ == "__main__":
    print("\n--- User CRUD Operations ---")
    print("\n--- Initial Users ---")
    get_all_users()

    print("\nAdding a new user...")
    add_user()

    print("\nReading users after adding...")
    get_all_users()

    print("\nUpdating a user...")
    update_user()

    print("\nReading users after updating...")
    get_all_users()

    print("\nDeleting a user...")
    delete_user()

    print("\nReading users after deleting...")
    get_all_users()

