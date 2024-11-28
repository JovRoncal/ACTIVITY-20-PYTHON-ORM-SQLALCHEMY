from sqlalchemy import create_engine, Column, Integer, String, Text, DECIMAL, DateTime, Enum, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime

# Database URL
DATABASE_URL = "mysql+mysqlconnector://root:jovs123@localhost/ecommerce_db"
engine = create_engine(DATABASE_URL)

# Base class for all models
Base = declarative_base()

# Define the User model
class User(Base):
    __tablename__ = 'USER'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    name = Column(String(255))
    address = Column(String(255))
    phone = Column(String(255))
    role = Column(Enum('customer', 'admin', name='role_enum'), default='customer')
    created_at = Column(DateTime, default=datetime.utcnow)

# Set up session
Session = sessionmaker(bind=engine)
session = Session()

# Ensure the tables exist
Base.metadata.create_all(engine)

# 1. CREATE User: Insert a new user if the email does not already exist
def add_user(email, password, name, address, phone, role='customer'):
    # Check if user already exists by email
    existing_user = session.query(User).filter_by(email=email).first()
    if existing_user:
        print(f"User with email {email} already exists.")
        return existing_user
    else:
        new_user = User(email=email, password=password, name=name, address=address, phone=phone, role=role)
        session.add(new_user)
        session.commit()
        print(f"User '{name}' added with email {email}.")
        return new_user

# 2. READ User: Fetch all users
def get_all_users():
    users = session.query(User).all()
    if users:
        for user in users:
            print(f"User ID: {user.user_id}, Name: {user.name}, Email: {user.email}, Role: {user.role}")
    else:
        print("No users found.")

# 3. UPDATE User: Update user's name or role by user_id
def update_user(user_id, new_name=None, new_role=None):
    user_to_update = session.query(User).filter_by(user_id=user_id).first()
    if user_to_update:
        if new_name:
            user_to_update.name = new_name
        if new_role:
            user_to_update.role = new_role
        session.commit()
        print(f"User ID {user_to_update.user_id} updated to '{user_to_update.name}' with role '{user_to_update.role}'.")
    else:
        print(f"User with ID {user_id} not found.")

# 4. DELETE User: Delete a user by user_id
def delete_user(user_id):
    user_to_delete = session.query(User).filter_by(user_id=user_id).first()
    if user_to_delete:
        session.delete(user_to_delete)
        session.commit()
        print(f"User with ID {user_to_delete.user_id} deleted.")
    else:
        print(f"User with ID {user_id} not found.")

# Example usage of CRUD operations

def perform_crud_operations():
    # Create Users
    add_user('newcustomer@example.com', 'password123', 'New Customer', '123 Street', '555-1234', 'customer')
    add_user('admin@example.com', 'adminpassword', 'Admin User', '456 Admin St', '555-5678', 'admin')

    # Read all Users
    print("\n--- All Users ---")
    get_all_users()

    # Update a User (Change role of user with ID 1)
    print("\n--- Updating User ID 1 ---")
    update_user(1, new_name='Updated Customer', new_role='admin')

    # Read all Users after update
    print("\n--- All Users After Update ---")
    get_all_users()

    # Delete a User (Delete user with ID 2)
    print("\n--- Deleting User ID 2 ---")
    delete_user(2)

    # Read all Users after delete
    print("\n--- All Users After Deletion ---")
    get_all_users()

# Run CRUD operations
perform_crud_operations()

# Close session
session.close()
