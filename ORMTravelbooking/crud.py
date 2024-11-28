from sqlalchemy import create_engine, Column, Integer, String, Enum, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import IntegrityError
from ormtravelbooking import User

# Database URL
DATABASE_URL = "mysql+mysqlconnector://root:jov123@localhost/ormtravelbooking_db"
engine = create_engine(DATABASE_URL, echo=True)

# Base class for all models
Base = declarative_base()





# Session creation
Session = sessionmaker(bind=engine)


def get_session():
    return Session()


# CRUD operations

# Create a new user
def create_user(username, password_hash, email, phone_number, first_name, last_name, user_role):
    session = get_session()
    try:
        print(f"Attempting to create user: {username}")
        new_user = User(
            username=username,
            password_hash=password_hash,
            email=email,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            user_role=user_role
        )
        session.add(new_user)
        session.commit()
        print(f"User {username} created successfully.")
    except IntegrityError:
        session.rollback()
        print(f"Error: User {username} already exists or other integrity issue.")
    finally:
        session.close()


# Get user by ID
def get_user_by_id(user_id):
    session = get_session()
    print(f"Retrieving user with ID {user_id}")
    user = session.query(User).filter(User.user_id == user_id).first()
    session.close()
    if user:
        print(f"User found: {user.first_name} {user.last_name}, Role: {user.user_role}")
    else:
        print(f"User with ID {user_id} not found.")
    return user


# Update user information
def update_user(user_id, username=None, password_hash=None, email=None, phone_number=None, first_name=None,
                last_name=None, user_role=None):
    session = get_session()
    print(f"Attempting to update user with ID {user_id}")
    user = session.query(User).filter(User.user_id == user_id).first()

    if user:
        if username:
            user.username = username
        if password_hash:
            user.password_hash = password_hash
        if email:
            user.email = email
        if phone_number:
            user.phone_number = phone_number
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if user_role:
            user.user_role = user_role
        session.commit()
        print(f"User {user_id} updated successfully.")
    else:
        print(f"User {user_id} not found.")

    session.close()


# Delete a user
def delete_user(user_id):
    session = get_session()
    print(f"Attempting to delete user with ID {user_id}")
    user = session.query(User).filter(User.user_id == user_id).first()

    if user:
        session.delete(user)
        session.commit()
        print(f"User {user_id} deleted successfully.")
    else:
        print(f"User {user_id} not found.")

    session.close()


# Get all users
def get_all_users():
    session = get_session()
    print("Retrieving all users.")
    users = session.query(User).all()
    session.close()
    if users:
        print("All Users:")
        for user in users:
            print(f"ID: {user.user_id}, Name: {user.first_name} {user.last_name}, Role: {user.user_role}")
    else:
        print("No users found.")
    return users


# Demonstration of CRUD operations

def main():
    print("Starting CRUD operations...\n")

    # Create users (only if they don't already exist)
    print("\n--- Creating Users ---")
    create_user('jov_roncal', 'hashed_pw_6', 'jov@example.com', '1234123412', 'Jov', 'Roncal', 'USERS')
    create_user('ramon_roncal', 'hashed_pw_7', 'ramon@example.com', '9876987698', 'Ramon', 'Roncal', 'USERS')

    # Get all users
    print("\n--- Retrieving All Users ---")
    users = get_all_users()

    # Get user by ID
    print("\n--- Retrieving User by ID ---")
    user = get_user_by_id(1)  # Assuming user with ID 1 exists
    if user:
        print(f"User with ID 1: {user.first_name} {user.last_name}, {user.user_role}")

    # Update a user's information
    print("\n--- Updating User ---")
    update_user(1, first_name="John", last_name="Lenon Updated")

    # Get updated user by ID
    user = get_user_by_id(1)
    if user:
        print(f"Updated user: {user.first_name} {user.last_name}, {user.user_role}")

    # Delete a user
    print("\n--- Deleting User ---")
    delete_user(6)  # Deleting user with ID 2

    # Get all users after deletion
    print("\n--- Retrieving All Users After Deletion ---")
    users = get_all_users()


if __name__ == '__main__':
    main()
