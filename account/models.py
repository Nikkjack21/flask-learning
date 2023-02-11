import datetime
from account import db, login_manager, bcrypt
from flask_login import UserMixin
from random import randint
import uuid
import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def generate_order_number():
    order_number = (
        "ORD-"
        + str(int(datetime.datetime.now().strftime("%f%m%H%M%S")))
        + str(uuid.uuid4().int)
    )
    return order_number[:22]


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=20), unique=True, nullable=False)
    email = db.Column(db.String(length=50), unique=True, nullable=False)
    password = db.Column(db.String(length=60), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    cart = db.relationship(
        "Cart", cascade="all, delete, delete-orphan", backref="user_cart", lazy=True
    )
    address = db.relationship(
        "Address",
        cascade="all, delete, delete-orphan",
        backref="user_address",
        lazy=True,
    )
    payments = db.relationship("Payments", backref="user_payment", lazy=True)

    orders = db.relationship(
        "Orders", cascade="all, delete, delete-orphan", backref="user_orders", lazy=True
    )

    @property
    def password_hash(self):
        return self.password_hash

    @password_hash.setter
    def password_hash(self, plain_text_password):
        self.password = bcrypt.generate_password_hash(plain_text_password).decode(
            "utf-8"
        )

    def check_password(self, attempted_password):
        return bcrypt.check_password_hash(self.password, attempted_password)

    def __repr__(self):
        return self.username


class Address(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user = db.Column(db.Integer(), db.ForeignKey("user.id"), nullable=False)
    name = db.Column(db.String(length=20), nullable=False)
    address = db.Column(db.String(length=250), nullable=False)
    pincode = db.Column(db.Integer())
    city = db.Column(db.String(length=20), nullable=False)
    state = db.Column(db.String(length=20), nullable=False)
    phone = db.Column(db.Integer(), nullable=False)
    orders = db.relationship("Orders", backref="order_address", lazy=True)

    def __repr__(self):
        return self.user.username


class Category(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    category_name = db.Column(db.String(length=25), nullable=False, unique=True)
    products = db.relationship(
        "Product",
        cascade="all, delete, delete-orphan",
        backref="product_category",
        lazy=True,
    )

    def __repr__(self):
        return self.category_name


class Product(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    product_name = db.Column(db.String(length=25), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    stock = db.Column(db.Integer(), nullable=False)
    category = db.Column(db.Integer(), db.ForeignKey("category.id"), nullable=False)
    cart = db.relationship(
        "Cart", cascade="all, delete, delete-orphan", backref="cart_products", lazy=True
    )

    def __repr__(self):
        return self.product_name


class Cart(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user = db.Column(db.Integer(), db.ForeignKey("user.id"), nullable=False)
    products = db.Column(db.Integer(), db.ForeignKey("product.id"), nullable=False)
    quantity = db.Column(db.Integer())

    def __repr__(self):
        return self.user.username


class Payments(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user = db.Column(db.Integer(), db.ForeignKey("user.id"), nullable=False)
    amount_paid = db.Column(db.Integer())
    status = db.Column(db.Boolean())
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    payment = db.relationship("Orders", backref="order_payments")

    def __repr__(self):
        return self.user.username


class Orders(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user = db.Column(
        db.Integer(),
        db.ForeignKey("user.id"),
        nullable=False,
    )
    Payments = db.Column(db.Integer(), db.ForeignKey("payments.id"), nullable=False)
    shipping_address = db.Column(
        db.Integer(), db.ForeignKey("address.id"), nullable=False
    )
    order_number = db.Column(db.String(), default=generate_order_number)
    order_total = db.Column(db.Float())
    status = db.Column(db.String(), default="pending")
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    is_ordered = db.Column(db.Boolean(), default=False)

    order_products = db.relationship(
        "OrderProducts", cascade="all, delete, delete-orphan", lazy=True
    )

    def __repr__(self):
        return self.user.username


class OrderProducts(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    orders = db.Column(db.Integer(), db.ForeignKey("orders.id"), nullable=False)
    products = db.Column(db.Integer(), db.ForeignKey("product.id"), nullable=False)
    quantity = db.Column(db.Integer())
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    is_ordered = db.Column(db.Boolean(), default=False)

    def __repr__(self):
        return self.products.product_name
