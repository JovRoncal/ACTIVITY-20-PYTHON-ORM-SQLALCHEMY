from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ormeventmanagement import Admin

# Database URL
DATABASE_URL = "mysql+mysqlconnector://root:jovs123@localhost/ormeventmanagement_db"
engine = create_engine(DATABASE_URL)

# Session creation
Session = sessionmaker(bind=engine)
session = Session()

# Create Admin
def create_admin(username, email, password):
    new_admin = Admin(admin_username=username, admin_email=email, admin_password=password)
    session.add(new_admin)
    session.commit()
    print(f"Admin '{new_admin.admin_username}' created successfully.")

# Read Admins
def read_all_admins():
    admins = session.query(Admin).all()
    if admins:
        for admin in admins:
            print(f"Admin ID: {admin.admin_id}, Username: {admin.admin_username}, Email: {admin.admin_email}")
    else:
        print("No admins found.")

# Update Admin
def update_admin(admin_id, new_username=None, new_email=None, new_password=None):
    admin = session.query(Admin).filter(Admin.admin_id == admin_id).first()
    if admin:
        if new_username:
            admin.admin_username = new_username
        if new_email:
            admin.admin_email = new_email
        if new_password:
            admin.admin_password = new_password
        session.commit()
        print(f"Admin ID {admin_id} updated.")
    else:
        print(f"Admin with ID {admin_id} not found.")

# Delete Admin
def delete_admin(admin_id):
    admin = session.query(Admin).filter(Admin.admin_id == admin_id).first()
    if admin:
        session.delete(admin)
        session.commit()
        print(f"Admin ID {admin_id} deleted.")
    else:
        print(f"Admin with ID {admin_id} not found.")

# Running the CRUD operations
if __name__ == "__main__":
    # Create a new admin
    create_admin('admin6', 'admin6@example.com', 'adminpass6')

    # Read all admins
    print("\nReading all admins:")
    read_all_admins()

    # Update an existing admin (e.g., update admin with ID 1)
    print("\nUpdating admin with ID 1:")
    update_admin(1, new_username='admin1_updated', new_email='admin1_updated@example.com')

    # Read again after update
    print("\nReading all admins after update:")
    read_all_admins()

    # Delete an admin (e.g., delete admin with ID 5)
    print("\nDeleting admin with ID 5:")
    delete_admin(5)

    # Read again after delete
    print("\nReading all admins after delete:")
    read_all_admins()
