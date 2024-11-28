from sqlalchemy import create_engine, Column, Integer, String, Text, DECIMAL, DateTime, Date, Enum, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime

# Database URL
DATABASE_URL = "mysql+mysqlconnector://root:jov123@localhost/ormtravelbooking_db"
engine = create_engine(DATABASE_URL)

# Base class for all models
Base = declarative_base()

# Define the User model
class User(Base):
    __tablename__ = 'User'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(100), nullable=False)
    phone_number = Column(String(20))
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    user_role = Column(Enum('ADMIN', 'USERS', name='user_role_enum'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime)

# Define the Tour model
class Tour(Base):
    __tablename__ = 'Tours'

    tour_id = Column(Integer, primary_key=True, autoincrement=True)
    tour_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    seats_available = Column(Integer, nullable=False)
    image_url = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime)

# Define the Booking model
class Booking(Base):
    __tablename__ = 'Bookings'

    booking_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('User.user_id'), nullable=False)
    tour_id = Column(Integer, ForeignKey('Tours.tour_id'), nullable=False)
    booking_date = Column(DateTime, default=datetime.utcnow)
    travel_date = Column(Date, nullable=False)
    seats_booked = Column(Integer, nullable=False)
    total_amount = Column(DECIMAL(10, 2), nullable=False)
    payment_status = Column(Enum('SUCCESS', 'FAILED', name='payment_status_enum'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship('User', back_populates='bookings')
    tour = relationship('Tour', back_populates='bookings')

# Define the Payment model
class Payment(Base):
    __tablename__ = 'Payment'

    payment_id = Column(Integer, primary_key=True, autoincrement=True)
    booking_id = Column(Integer, ForeignKey('Bookings.booking_id'), nullable=False)
    payment_date = Column(DateTime, default=datetime.utcnow)
    amount = Column(DECIMAL(10, 2), nullable=False)
    payment_method = Column(Enum('GCASH', name='payment_method_enum'), nullable=False)
    payment_status = Column(Enum('SUCCESS', 'FAILED', name='payment_status_enum'), nullable=False)
    transaction_id = Column(String(100), nullable=False)

    booking = relationship('Booking', back_populates='payments')

# Define the Review model
class Review(Base):
    __tablename__ = 'Reviews'

    review_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('User.user_id'), nullable=False)
    tour_id = Column(Integer, ForeignKey('Tours.tour_id'), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship('User', back_populates='reviews')
    tour = relationship('Tour', back_populates='reviews')

# Define the AdminLogs model
class AdminLog(Base):
    __tablename__ = 'AdminLogs'

    log_id = Column(Integer, primary_key=True, autoincrement=True)
    admin_id = Column(Integer, ForeignKey('User.user_id'), nullable=False)
    action_type = Column(Enum('ADD', 'DELETE', 'UPDATE', name='action_type_enum'), nullable=False)
    description = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    admin = relationship('User', back_populates='admin_logs')


# Add relationships for back_populates
User.bookings = relationship('Booking', back_populates='user')
User.reviews = relationship('Review', back_populates='user')
User.admin_logs = relationship('AdminLog', back_populates='admin')

Tour.bookings = relationship('Booking', back_populates='tour')
Tour.reviews = relationship('Review', back_populates='tour')

Booking.payments = relationship('Payment', back_populates='booking')


# Create tables
Base.metadata.create_all(engine)

# Session creation
Session = sessionmaker(bind=engine)
session = Session()

# Add 5 Users
users = [
    User(username='john_doe', password_hash='hashed_pw_1', email='john@example.com', phone_number='1234567890', first_name='John', last_name='Doe', user_role='ADMIN'),
    User(username='jane_doe', password_hash='hashed_pw_2', email='jane@example.com', phone_number='0987654321', first_name='Jane', last_name='Doe', user_role='USERS'),
    User(username='sam_smith', password_hash='hashed_pw_3', email='sam@example.com', phone_number='1122334455', first_name='Sam', last_name='Smith', user_role='USERS'),
    User(username='emily_brown', password_hash='hashed_pw_4', email='emily@example.com', phone_number='5566778899', first_name='Emily', last_name='Brown', user_role='USERS'),
    User(username='david_lee', password_hash='hashed_pw_5', email='david@example.com', phone_number='6677889900', first_name='David', last_name='Lee', user_role='ADMIN')
]
session.add_all(users)
session.commit()

# Add 5 Tours
tours = [
    Tour(tour_name='Paris Adventure', description='Tour of Paris including major landmarks', price=1000.00, start_date=datetime(2024, 5, 1).date(), end_date=datetime(2024, 5, 7).date(), seats_available=20),
    Tour(tour_name='Rome Exploration', description='Explore the historical sites of Rome', price=800.00, start_date=datetime(2024, 6, 15).date(), end_date=datetime(2024, 6, 20).date(), seats_available=15),
    Tour(tour_name='Tokyo Experience', description='Experience the best of Tokyo and Japan', price=1200.00, start_date=datetime(2024, 7, 1).date(), end_date=datetime(2024, 7, 10).date(), seats_available=25),
    Tour(tour_name='New York City Tour', description='Discover the Big Apple on this guided tour', price=900.00, start_date=datetime(2024, 8, 1).date(), end_date=datetime(2024, 8, 5).date(), seats_available=30),
    Tour(tour_name='London City Break', description='A short trip around London\'s top attractions', price=850.00, start_date=datetime(2024, 9, 10).date(), end_date=datetime(2024, 9, 15).date(), seats_available=10)
]
session.add_all(tours)
session.commit()

# Add 5 Bookings
bookings = [
    Booking(user_id=2, tour_id=1, travel_date=datetime(2024, 5, 2).date(), seats_booked=2, total_amount=2000.00, payment_status='SUCCESS'),
    Booking(user_id=3, tour_id=2, travel_date=datetime(2024, 6, 16).date(), seats_booked=1, total_amount=800.00, payment_status='FAILED'),
    Booking(user_id=4, tour_id=3, travel_date=datetime(2024, 7, 2).date(), seats_booked=3, total_amount=3600.00, payment_status='SUCCESS'),
    Booking(user_id=5, tour_id=4, travel_date=datetime(2024, 8, 2).date(), seats_booked=2, total_amount=1800.00, payment_status='SUCCESS'),
    Booking(user_id=1, tour_id=5, travel_date=datetime(2024, 9, 11).date(), seats_booked=1, total_amount=850.00, payment_status='FAILED')
]
session.add_all(bookings)
session.commit()

# Add 5 Payments
payments = [
    Payment(booking_id=1, amount=2000.00, payment_method='GCASH', payment_status='SUCCESS', transaction_id='TXN001'),
    Payment(booking_id=2, amount=800.00, payment_method='GCASH', payment_status='FAILED', transaction_id='TXN002'),
    Payment(booking_id=3, amount=3600.00, payment_method='GCASH', payment_status='SUCCESS', transaction_id='TXN003'),
    Payment(booking_id=4, amount=1800.00, payment_method='GCASH', payment_status='SUCCESS', transaction_id='TXN004'),
    Payment(booking_id=5, amount=850.00, payment_method='GCASH', payment_status='FAILED', transaction_id='TXN005')
]
session.add_all(payments)
session.commit()

from datetime import datetime, timezone

# Add 5 Reviews
reviews = [
    Review(user_id=2, tour_id=1, rating=5, comment='Amazing tour, highly recommend!', created_at=datetime.now(timezone.utc)),
    Review(user_id=3, tour_id=2, rating=4, comment='Great experience but not enough time to explore.', created_at=datetime.now(timezone.utc)),
    Review(user_id=4, tour_id=3, rating=5, comment='The best tour I\'ve ever had!', created_at=datetime.now(timezone.utc)),
    Review(user_id=5, tour_id=4, rating=3, comment='Good, but the schedule was too tight.', created_at=datetime.now(timezone.utc)),
    Review(user_id=1, tour_id=5, rating=4, comment='Great tour, but the weather wasn\'t great.', created_at=datetime.now(timezone.utc))
]
session.add_all(reviews)
session.commit()

# Add 5 Admin Logs
admin_logs = [
    AdminLog(admin_id=1, action_type='ADD', description='Added new user: jane_doe.', timestamp=datetime.now(timezone.utc)),
    AdminLog(admin_id=1, action_type='UPDATE', description='Updated user details for john_doe.', timestamp=datetime.now(timezone.utc)),
    AdminLog(admin_id=2, action_type='DELETE', description='Deleted tour: Paris Adventure.', timestamp=datetime.now(timezone.utc)),
    AdminLog(admin_id=2, action_type='ADD', description='Added new tour: Rome Exploration.', timestamp=datetime.now(timezone.utc)),
    AdminLog(admin_id=1, action_type='UPDATE', description='Updated payment status for booking ID 1.', timestamp=datetime.now(timezone.utc))
]
session.add_all(admin_logs)
session.commit()

print("Dummy data inserted successfully.")
