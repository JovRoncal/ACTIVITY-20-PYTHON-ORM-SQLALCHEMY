from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, Date
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# Database URL
DATABASE_URL = "mysql+mysqlconnector://root:jovs123@localhost/ormeventmanagement_db"
engine = create_engine(DATABASE_URL)

# Base class for all models
Base = declarative_base()

# Admin model
class Admin(Base):
    __tablename__ = 'Admin'

    admin_id = Column(Integer, primary_key=True, autoincrement=True)
    admin_username = Column(String(255))
    admin_email = Column(String(255))
    admin_password = Column(String(255))

# User model
class User(Base):
    __tablename__ = 'User'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_gmail = Column(String(255))
    user_password = Column(String(255))
    user_firstname = Column(String(255))
    user_lastname = Column(String(255))

# Events model
class Events(Base):
    __tablename__ = 'Events'

    event_id = Column(Integer, primary_key=True, autoincrement=True)
    event_title = Column(String(255))
    event_description = Column(Text)
    event_additional_description = Column(Text)
    event_address = Column(String(255))
    event_planner = Column(String(255))
    event_image = Column(String(255))
    event_status = Column(String(255))
    event_start = Column(Date)

# Invited model
class Invited(Base):
    __tablename__ = 'Invited'

    invitation_id = Column(Integer, primary_key=True, autoincrement=True)
    invited_name = Column(String(255))
    event_id = Column(Integer, ForeignKey('Events.event_id'), nullable=False)
    attendee_type = Column(String(255))
    seat_number = Column(String(255))

    event = relationship('Events', back_populates='invited')

# Attendees model
class Attendees(Base):
    __tablename__ = 'Attendees'

    attendee_id = Column(Integer, primary_key=True, autoincrement=True)
    invitation_id = Column(Integer, ForeignKey('Invited.invitation_id'), nullable=False)

    invitation = relationship('Invited', back_populates='attendees')

# Agenda model
class Agenda(Base):
    __tablename__ = 'Agenda'

    agenda_id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(Integer, ForeignKey('Events.event_id'), nullable=False)
    agenda_name = Column(String(255))
    agenda_time_start = Column(String(255))
    agenda_time_end = Column(String(255))

    event = relationship('Events', back_populates='agenda')


# Relationships
Events.invited = relationship('Invited', back_populates='event', cascade="all, delete-orphan")
Invited.attendees = relationship('Attendees', back_populates='invitation', cascade="all, delete-orphan")
Events.agenda = relationship('Agenda', back_populates='event', cascade="all, delete-orphan")


# Create tables
Base.metadata.create_all(engine)

# Session creation
Session = sessionmaker(bind=engine)
session = Session()

# Add data to the tables

# 1. Admin
admins = [
    Admin(admin_username='admin1', admin_email='admin1@example.com', admin_password='adminpass1'),
    Admin(admin_username='admin2', admin_email='admin2@example.com', admin_password='adminpass2'),
    Admin(admin_username='admin3', admin_email='admin3@example.com', admin_password='adminpass3'),
    Admin(admin_username='admin4', admin_email='admin4@example.com', admin_password='adminpass4'),
    Admin(admin_username='admin5', admin_email='admin5@example.com', admin_password='adminpass5')
]

# 2. User
users = [
    User(user_gmail='user1@example.com', user_password='userpass1', user_firstname='John', user_lastname='Doe'),
    User(user_gmail='user2@example.com', user_password='userpass2', user_firstname='Jane', user_lastname='Doe'),
    User(user_gmail='user3@example.com', user_password='userpass3', user_firstname='Jim', user_lastname='Beam'),
    User(user_gmail='user4@example.com', user_password='userpass4', user_firstname='Jack', user_lastname='Daniels'),
    User(user_gmail='user5@example.com', user_password='userpass5', user_firstname='Jill', user_lastname='Smith')
]

# 3. Events
events = [
    Events(event_title='Tech Conference 2024', event_description='A conference on technology trends',
           event_additional_description='Networking sessions included', event_address='123 Tech St',
           event_planner='TechCorp', event_image='tech_event.jpg', event_status='Scheduled', event_start='2024-05-10'),
    Events(event_title='Health & Wellness Fair', event_description='A fair promoting healthy living',
           event_additional_description='Free health checkups available', event_address='456 Wellness Ave',
           event_planner='Wellness Inc.', event_image='wellness_fair.jpg', event_status='Scheduled', event_start='2024-06-12'),
    Events(event_title='Business Expo 2024', event_description='An expo for entrepreneurs and startups',
           event_additional_description='Includes pitching sessions', event_address='789 Startup Blvd',
           event_planner='Expo Ltd.', event_image='business_expo.jpg', event_status='Scheduled', event_start='2024-07-15'),
    Events(event_title='Music Festival 2024', event_description='A celebration of music and culture',
           event_additional_description='Multiple stages with various genres', event_address='321 Music Ave',
           event_planner='Festivals Co.', event_image='music_festival.jpg', event_status='Scheduled', event_start='2024-08-20'),
    Events(event_title='Food & Wine Gala', event_description='A fine dining experience with wine pairings',
           event_additional_description='Exclusive tasting menu', event_address='654 Gourmet Rd',
           event_planner='Gala Events', event_image='food_wine_gala.jpg', event_status='Scheduled', event_start='2024-09-25')
]

# 4. Invited
invited = [
    Invited(invited_name='Alice', event_id=1, attendee_type='VIP', seat_number='A1'),
    Invited(invited_name='Bob', event_id=2, attendee_type='General', seat_number='B2'),
    Invited(invited_name='Charlie', event_id=3, attendee_type='VIP', seat_number='C3'),
    Invited(invited_name='David', event_id=4, attendee_type='VIP', seat_number='D4'),
    Invited(invited_name='Eve', event_id=5, attendee_type='General', seat_number='E5')
]

# 5. Attendees
attendees = [
    Attendees(invitation_id=1),
    Attendees(invitation_id=2),
    Attendees(invitation_id=3),
    Attendees(invitation_id=4),
    Attendees(invitation_id=5)
]

# 6. Agenda
agenda = [
    Agenda(event_id=1, agenda_name='Opening Keynote', agenda_time_start='09:00', agenda_time_end='10:00'),
    Agenda(event_id=2, agenda_name='Health Talk', agenda_time_start='10:00', agenda_time_end='11:00'),
    Agenda(event_id=3, agenda_name='Business Panel', agenda_time_start='14:00', agenda_time_end='15:00'),
    Agenda(event_id=4, agenda_name='Concert Performance', agenda_time_start='18:00', agenda_time_end='20:00'),
    Agenda(event_id=5, agenda_name='Wine Tasting', agenda_time_start='17:00', agenda_time_end='18:00')
]

# Insert the data into tables
session.add_all(admins)
session.add_all(users)
session.add_all(events)
session.add_all(invited)
session.add_all(attendees)
session.add_all(agenda)

session.commit()

print("Dummy data inserted successfully.")
