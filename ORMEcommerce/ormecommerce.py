from sqlalchemy import create_engine, Column, Integer, String, Text, DECIMAL, DateTime, Enum, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime

# Database URL
DATABASE_URL = "mysql+mysqlconnector://root:jovs123@localhost/ormecommerce_db"
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

# Define the Product model
class Product(Base):
    __tablename__ = 'PRODUCTS'

    product_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    brand = Column(String(255))
    description = Column(Text)
    price = Column(DECIMAL(10, 2))
    stock = Column(Integer)
    category = Column(String(255))
    SKU = Column(String(255), unique=True)
    image_url = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

# Define the Order model
class Order(Base):
    __tablename__ = 'ORDERS'

    order_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('USER.user_id'))
    total_amount = Column(DECIMAL(10, 2))
    status = Column(Enum('pending', 'shipped', 'delivered', 'cancelled', name='order_status_enum'), default='pending')
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship('User', back_populates='orders')

# Define the OrderItem model
class OrderItem(Base):
    __tablename__ = 'ORDER_ITEMS'

    order_item_id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('ORDERS.order_id'))
    product_id = Column(Integer, ForeignKey('PRODUCTS.product_id'))
    quantity = Column(Integer, nullable=False)
    price = Column(DECIMAL(10, 2))

    order = relationship('Order', back_populates='order_items')
    product = relationship('Product', back_populates='order_items')

# Define the Review model
class Review(Base):
    __tablename__ = 'REVIEWS'

    review_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('USER.user_id'))
    product_id = Column(Integer, ForeignKey('PRODUCTS.product_id'))
    rating = Column(Integer, nullable=False)
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship('User', back_populates='reviews')
    product = relationship('Product', back_populates='reviews')

# Set up the relationships in the models
User.orders = relationship('Order', back_populates='user')
Order.order_items = relationship('OrderItem', back_populates='order')
Product.order_items = relationship('OrderItem', back_populates='product')
Product.reviews = relationship('Review', back_populates='product')
User.reviews = relationship('Review', back_populates='user')

# Create tables
Base.metadata.create_all(engine)

# Session creation
Session = sessionmaker(bind=engine)
session = Session()

# Sample data to insert into tables (5 values for each table)
def add_sample_data():
    # Add Users
    user1 = User(email='customer1@example.com', password='password123', name='Ramon Jov', role='customer')
    user2 = User(email='customer2@example.com', password='password123', name='Ramon', role='customer')
    user3 = User(email='admin1@example.com', password='admin123', name='Admin User', role='admin')
    user4 = User(email='customer3@example.com', password='password123', name='Jov Roncal', role='customer')
    user5 = User(email='customer4@example.com', password='password123', name='Roncal ', role='customer')
    session.add_all([user1, user2, user3, user4, user5])

    # Add Products (Cellphones)
    product1 = Product(name='iPhone 14', brand='Apple', description='Latest iPhone model with 5G support', price=999.99, stock=50, category='Cellphone', SKU='IPH14-001', image_url='iphone14.jpg')
    product2 = Product(name='Samsung Galaxy S22', brand='Samsung', description='Premium Android smartphone with excellent camera', price=799.99, stock=40, category='Cellphone', SKU='SGS22-002', image_url='galaxys22.jpg')
    product3 = Product(name='Google Pixel 6', brand='Google', description='Android phone with Google\'s exclusive features', price=599.99, stock=60, category='Cellphone', SKU='PIX6-003', image_url='pixel6.jpg')
    product4 = Product(name='OnePlus 9 Pro', brand='OnePlus', description='High-performance Android phone with fast charging', price=899.99, stock=30, category='Cellphone', SKU='OP9P-004', image_url='oneplus9pro.jpg')
    product5 = Product(name='Xiaomi Mi 11', brand='Xiaomi', description='Affordable flagship phone with great value', price=699.99, stock=70, category='Cellphone', SKU='XM11-005', image_url='xiaomi11.jpg')
    session.add_all([product1, product2, product3, product4, product5])

    # Add Orders
    order1 = Order(user_id=1, total_amount=1799.98, status='pending')
    order2 = Order(user_id=2, total_amount=1399.98, status='shipped')
    order3 = Order(user_id=4, total_amount=1499.98, status='delivered')
    order4 = Order(user_id=5, total_amount=1299.98, status='pending')
    order5 = Order(user_id=3, total_amount=899.99, status='cancelled')
    session.add_all([order1, order2, order3, order4, order5])

    # Add Order Items
    order_item1 = OrderItem(order_id=1, product_id=1, quantity=1, price=999.99)
    order_item2 = OrderItem(order_id=1, product_id=2, quantity=1, price=799.99)
    order_item3 = OrderItem(order_id=2, product_id=3, quantity=1, price=599.99)
    order_item4 = OrderItem(order_id=2, product_id=4, quantity=1, price=899.99)
    order_item5 = OrderItem(order_id=3, product_id=2, quantity=2, price=799.99)
    session.add_all([order_item1, order_item2, order_item3, order_item4, order_item5])

    # Add Reviews
    review1 = Review(user_id=1, product_id=1, rating=5, comment='Excellent phone, worth the price!')
    review2 = Review(user_id=2, product_id=2, rating=4, comment='Good phone but the battery could be better.')
    review3 = Review(user_id=4, product_id=3, rating=5, comment='Great camera and performance!')
    review4 = Review(user_id=5, product_id=4, rating=4, comment='Solid performance but a bit bulky.')
    review5 = Review(user_id=3, product_id=5, rating=3, comment='Affordable but lacks some premium features.')
    session.add_all([review1, review2, review3, review4, review5])

    session.commit()

# Insert sample data
add_sample_data()

print("Sample data inserted successfully.")

# Closing the session
session.close()
