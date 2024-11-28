from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, Enum, DECIMAL, Date, Boolean
from sqlalchemy.orm import declarative_base, relationship, sessionmaker  # Corrected import
from sqlalchemy.dialects.mysql import BLOB
from datetime import datetime, timezone
import random  # Add missing import

# Database URL
DATABASE_URL = "mysql+mysqlconnector://root:jovs123@localhost/ormjobboard_db"
engine = create_engine(DATABASE_URL)

# Base class for all models
Base = declarative_base()

# Define the Authentication model
class Authentication(Base):
    __tablename__ = 'Authentication'

    authentication_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum('user', 'admin', name='role_enum'), nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))  # UPDATED LINE
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))  # UPDATED LINE
    deleted_at = Column(DateTime, nullable=True)

# Define the User model
class User(Base):
    __tablename__ = 'User'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    authentication_id = Column(Integer, ForeignKey('Authentication.authentication_id'), nullable=False)
    name = Column(String(255), nullable=False)
    birth_date = Column(Date, nullable=True)
    skills = Column(Text, nullable=True)
    work_experience = Column(Text, nullable=True)
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))  # UPDATED LINE

    authentication = relationship('Authentication', backref='users')

# Define the Job Posting model
class JobPosting(Base):
    __tablename__ = 'Job_Posting'

    job_id = Column(Integer, primary_key=True, autoincrement=True)
    employer_id = Column(Integer, ForeignKey('User.user_id'), nullable=False)
    job_title = Column(String(255), nullable=False)
    job_description = Column(Text, nullable=True)
    location = Column(String(255), nullable=True)
    category = Column(String(255), nullable=True)
    industry = Column(String(255), nullable=True)
    min_salary = Column(DECIMAL(10, 2), nullable=True)
    max_salary = Column(DECIMAL(10, 2), nullable=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))  # UPDATED LINE
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))  # UPDATED LINE
    deleted_at = Column(DateTime, nullable=True)

    employer = relationship('User', backref='job_postings')

# Define the Job Performance model
class JobPerformance(Base):
    __tablename__ = 'Job_Performance'

    performance_id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(Integer, ForeignKey('Job_Posting.job_id'), nullable=False)
    applicants_count = Column(Integer, nullable=True)
    views_count = Column(Integer, nullable=True)
    open_date = Column(DateTime, nullable=True)
    close_date = Column(DateTime, nullable=True)
    time_to_fill = Column(Integer, nullable=True)
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))  # UPDATED LINE

    job = relationship('JobPosting', backref='performances')

# Define the Job Interaction model
class JobInteraction(Base):
    __tablename__ = 'Job_Interaction'

    interaction_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('User.user_id'), nullable=False)
    job_id = Column(Integer, ForeignKey('Job_Posting.job_id'), nullable=False)
    interaction_type = Column(Enum('view', 'apply', 'save', name='interaction_type_enum'), nullable=False)
    interaction_date = Column(DateTime, default=datetime.now(timezone.utc))  # UPDATED LINE
    is_applied = Column(Boolean, default=False)

    user = relationship('User', backref='job_interactions')
    job = relationship('JobPosting', backref='job_interactions')

# Define the Application model
class Application(Base):
    __tablename__ = 'Application'

    application_id = Column(Integer, primary_key=True, autoincrement=True)
    job_seeker_id = Column(Integer, ForeignKey('User.user_id'), nullable=False)
    job_id = Column(Integer, ForeignKey('Job_Posting.job_id'), nullable=False)
    resume = Column(BLOB, nullable=True)
    status = Column(Enum('pending', 'interview', 'rejected', 'accepted', name='application_status_enum'), nullable=False)
    skills = Column(Text, nullable=True)
    work_experience = Column(Text, nullable=True)
    applied_at = Column(DateTime, default=datetime.now(timezone.utc))  # UPDATED LINE
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))  # UPDATED LINE
    deleted_at = Column(DateTime, nullable=True)

    job_seeker = relationship('User', backref='applications')
    job = relationship('JobPosting', backref='applications')

# Define the Message model
class Message(Base):
    __tablename__ = 'Message'

    message_id = Column(Integer, primary_key=True, autoincrement=True)
    sender_id = Column(Integer, ForeignKey('User.user_id'), nullable=False)
    recipient_id = Column(Integer, ForeignKey('User.user_id'), nullable=False)
    application_id = Column(Integer, ForeignKey('Application.application_id'), nullable=True)
    message_text = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    message_type = Column(Enum('text', 'image', 'file', name='message_type_enum'), nullable=False)
    sent_at = Column(DateTime, default=datetime.now(timezone.utc))  # UPDATED LINE
    deleted_at = Column(DateTime, nullable=True)

    sender = relationship('User', foreign_keys=[sender_id], backref='sent_messages')
    recipient = relationship('User', foreign_keys=[recipient_id], backref='received_messages')
    application = relationship('Application', backref='messages')


# Create tables
Base.metadata.create_all(engine)

print("Tables created successfully.")

# Session creation
Session = sessionmaker(bind=engine)
session = Session()

# Add 5 Authentication records
authentications = [
    Authentication(username='user1', email='user1@example.com', password_hash='hashed_password1', role='user', created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc)),
    Authentication(username='admin1', email='admin1@example.com', password_hash='hashed_password2', role='admin', created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc)),
    Authentication(username='user2', email='user2@example.com', password_hash='hashed_password3', role='user', created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc)),
    Authentication(username='user3', email='user3@example.com', password_hash='hashed_password4', role='user', created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc)),
    Authentication(username='admin2', email='admin2@example.com', password_hash='hashed_password5', role='admin', created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc))
]
session.add_all(authentications)
session.commit()

# Add 5 User records
users = [
    User(authentication_id=1, name='Roncal', birth_date=datetime(1990, 5, 15), skills='Python, SQL', work_experience='2 years as a developer', updated_at=datetime.now(timezone.utc)),
    User(authentication_id=2, name='Jov', birth_date=datetime(1985, 3, 20), skills='JavaScript, React', work_experience='5 years as a frontend developer', updated_at=datetime.now(timezone.utc)),
    User(authentication_id=3, name='Ramon', birth_date=datetime(1992, 7, 25), skills='Java, Spring', work_experience='3 years as a backend developer', updated_at=datetime.now(timezone.utc)),
    User(authentication_id=4, name='Roel', birth_date=datetime(1988, 8, 30), skills='HTML, CSS, JavaScript', work_experience='4 years as a web developer', updated_at=datetime.now(timezone.utc)),
    User(authentication_id=5, name='Ramon Jov', birth_date=datetime(1995, 12, 5), skills='PHP, Laravel', work_experience='1 year as a full-stack developer', updated_at=datetime.now(timezone.utc))
]
session.add_all(users)
session.commit()

# Add 5 Job Posting records
job_postings = [
    JobPosting(employer_id=1, job_title='Frontend Developer', job_description='Looking for a frontend developer with React experience.', location='New York', category='Engineering', industry='Tech', min_salary=60000, max_salary=80000, created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc)),
    JobPosting(employer_id=2, job_title='Backend Developer', job_description='Looking for a backend developer with Java experience.', location='San Francisco', category='Engineering', industry='Tech', min_salary=70000, max_salary=90000, created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc)),
    JobPosting(employer_id=3, job_title='Full Stack Developer', job_description='Looking for a full-stack developer with experience in Node.js and React.', location='Austin', category='Engineering', industry='Tech', min_salary=75000, max_salary=95000, created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc)),
    JobPosting(employer_id=4, job_title='Web Developer', job_description='Looking for a web developer with HTML, CSS, and JavaScript skills.', location='Chicago', category='Engineering', industry='Tech', min_salary=50000, max_salary=70000, created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc)),
    JobPosting(employer_id=5, job_title='PHP Developer', job_description='Looking for a PHP developer with experience in Laravel.', location='Seattle', category='Engineering', industry='Tech', min_salary=65000, max_salary=85000, created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc))
]
session.add_all(job_postings)
session.commit()

# Add 5 Job Performance records
job_performances = [
    JobPerformance(job_id=1, applicants_count=random.randint(5, 50), views_count=random.randint(100, 1000), open_date=datetime.now(timezone.utc), close_date=datetime.now(timezone.utc), time_to_fill=random.randint(10, 30), updated_at=datetime.now(timezone.utc)),
    JobPerformance(job_id=2, applicants_count=random.randint(5, 50), views_count=random.randint(100, 1000), open_date=datetime.now(timezone.utc), close_date=datetime.now(timezone.utc), time_to_fill=random.randint(10, 30), updated_at=datetime.now(timezone.utc)),
    JobPerformance(job_id=3, applicants_count=random.randint(5, 50), views_count=random.randint(100, 1000), open_date=datetime.now(timezone.utc), close_date=datetime.now(timezone.utc), time_to_fill=random.randint(10, 30), updated_at=datetime.now(timezone.utc)),
    JobPerformance(job_id=4, applicants_count=random.randint(5, 50), views_count=random.randint(100, 1000), open_date=datetime.now(timezone.utc), close_date=datetime.now(timezone.utc), time_to_fill=random.randint(10, 30), updated_at=datetime.now(timezone.utc)),
    JobPerformance(job_id=5, applicants_count=random.randint(5, 50), views_count=random.randint(100, 1000), open_date=datetime.now(timezone.utc), close_date=datetime.now(timezone.utc), time_to_fill=random.randint(10, 30), updated_at=datetime.now(timezone.utc))
]
session.add_all(job_performances)
session.commit()

# Add 5 Job Interaction records
job_interactions = [
    JobInteraction(user_id=1, job_id=1, interaction_type='view', interaction_date=datetime.now(timezone.utc), is_applied=False),
    JobInteraction(user_id=2, job_id=2, interaction_type='apply', interaction_date=datetime.now(timezone.utc), is_applied=True),
    JobInteraction(user_id=3, job_id=3, interaction_type='save', interaction_date=datetime.now(timezone.utc), is_applied=False),
    JobInteraction(user_id=4, job_id=4, interaction_type='view', interaction_date=datetime.now(timezone.utc), is_applied=False),
    JobInteraction(user_id=5, job_id=5, interaction_type='apply', interaction_date=datetime.now(timezone.utc), is_applied=True)
]
session.add_all(job_interactions)
session.commit()

# Add 5 Application records
applications = [
    Application(job_seeker_id=1, job_id=1, status='pending', skills='React, JavaScript', work_experience='3 years as a frontend developer', applied_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc)),
    Application(job_seeker_id=2, job_id=2, status='accepted', skills='Java, Spring', work_experience='5 years as a backend developer', applied_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc)),
    Application(job_seeker_id=3, job_id=3, status='interview', skills='Node.js, Express', work_experience='2 years as a full-stack developer', applied_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc)),
    Application(job_seeker_id=4, job_id=4, status='rejected', skills='HTML, CSS', work_experience='4 years as a web developer', applied_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc)),
    Application(job_seeker_id=5, job_id=5, status='pending', skills='PHP, Laravel', work_experience='1 year as a full-stack developer', applied_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc))
]
session.add_all(applications)
session.commit()

# Add 5 Message records
messages = [
    Message(sender_id=1, recipient_id=2, application_id=1, message_text='Looking forward to your response.', message_type='text', sent_at=datetime.now(timezone.utc)),
    Message(sender_id=2, recipient_id=3, application_id=2, message_text='We have shortlisted you for the interview.', message_type='text', sent_at=datetime.now(timezone.utc)),
    Message(sender_id=3, recipient_id=4, application_id=3, message_text='Your application has been rejected.', message_type='text', sent_at=datetime.now(timezone.utc)),
    Message(sender_id=4, recipient_id=5, application_id=4, message_text='We would like to know more about your experience with PHP.', message_type='text', sent_at=datetime.now(timezone.utc)),
    Message(sender_id=5, recipient_id=1, application_id=5, message_text='We would like to schedule an interview with you.', message_type='text', sent_at=datetime.now(timezone.utc))
]
session.add_all(messages)
session.commit()

print("Additional sample data inserted successfully.")


print("Sample data inserted successfully.")
