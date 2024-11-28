from sqlalchemy import create_engine, Column, Integer, String, Text, DECIMAL, DateTime, Enum, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from ormjobboard import Authentication

# Database URL (replace with your actual connection details)
DATABASE_URL = "mysql+mysqlconnector://root:jovs123@localhost/ormjobboard_db"

# Base class for the model
Base = declarative_base()

# Define the Authentication model


# Create the engine and session
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# CRUD Operations

# 1. Create Authentication Record
def create_authentication(username, email, password_hash, role):
    new_authentication = Authentication(
        username=username,
        email=email,
        password_hash=password_hash,
        role=role
    )
    session.add(new_authentication)
    session.commit()
    print(f"Authentication record for {username} added successfully.")

# 2. Read Authentication Records
def read_authentication():
    authentications = session.query(Authentication).all()
    if authentications:
        for auth in authentications:
            print(f"ID: {auth.authentication_id}, Username: {auth.username}, Email: {auth.email}, Role: {auth.role}")
    else:
        print("No authentication records found.")

# 3. Update Authentication Record
def update_authentication(authentication_id, new_username=None, new_email=None, new_password_hash=None, new_role=None):
    auth_to_update = session.query(Authentication).filter(Authentication.authentication_id == authentication_id).first()
    if auth_to_update:
        if new_username:
            auth_to_update.username = new_username
        if new_email:
            auth_to_update.email = new_email
        if new_password_hash:
            auth_to_update.password_hash = new_password_hash
        if new_role:
            auth_to_update.role = new_role
        session.commit()
        print(f"Authentication record ID {authentication_id} updated successfully.")
    else:
        print(f"Authentication record ID {authentication_id} not found.")

# 4. Delete Authentication Record
def delete_authentication(authentication_id):
    auth_to_delete = session.query(Authentication).filter(Authentication.authentication_id == authentication_id).first()
    if auth_to_delete:
        session.delete(auth_to_delete)
        session.commit()
        print(f"Authentication record ID {authentication_id} deleted successfully.")
    else:
        print(f"Authentication record ID {authentication_id} not found.")

# Test the CRUD functions
if __name__ == "__main__":
    # Create a new authentication record
    create_authentication('Jovie', 'jovie@example.com', 'hashed_password_123', 'user')

    # Read all authentication records
    print("\n--- Reading Authentication Records ---")
    read_authentication()

    # Update an existing authentication record (example: updating username)
    update_authentication(6, new_username='jovie_updated')

    # Read all authentication records after the update
    print("\n--- Reading Authentication Records After Update ---")
    read_authentication()

    # Delete an authentication record
    delete_authentication(6)

    # Read all authentication records after deletion
    print("\n--- Reading Authentication Records After Deletion ---")
    read_authentication()
