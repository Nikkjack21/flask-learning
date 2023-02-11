from account import db, login_manager, bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class User( db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=20), unique=True, nullable=False)
    email = db.Column(db.String(length=50), unique=True, nullable=False)
    password = db.Column(db.String(length=60), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    cart = db.relationship("Cart", cascade="all, delete, delete-orphan", backref='user_cart', lazy=True)
    address = db.relationship("Address", cascade="all, delete, delete-orphan", backref='user_address', lazy=True)



    @property
    def password_hash(self):
        return self.password_hash

    @password_hash.setter
    def password_hash(self, plain_text_password):
        self.password = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')


    def check_password(self, attempted_password):
        return bcrypt.check_password_hash(self.password, attempted_password)
           


    def __repr__(self) -> str:
        return self.username


class Address(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user = db.Column(db.Integer(), db.ForeignKey("user.id"),  nullable=False)
    name = db.Column(db.String(length=20),  nullable=False)
    address = db.Column(db.String(length=250),  nullable=False)
    pincode = db.Column(db.Integer())
    city = db.Column(db.String(length=20),  nullable=False)
    state = db.Column(db.String(length=20),  nullable=False)
    phone = db.Column(db.Integer(), nullable=False)


    def __repr__(self) -> str:
        return self.user.username



class Category(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    category_name = db.Column(db.String(length = 25), nullable = False, unique = True)
    products = db.relationship('Product',cascade="all, delete, delete-orphan", backref='product_category', lazy=True)


    def __repr__(self) -> str:
        return self.category_name


class Product(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    product_name = db.Column(db.String(length = 25), nullable = False, unique = True)
    price = db.Column(db.Integer(), nullable = False)
    stock =  db.Column(db.Integer(), nullable=False)
    category = db.Column(db.Integer(), db.ForeignKey('category.id'), nullable=False)
    cart = db.relationship("Cart", cascade="all, delete, delete-orphan", backref='cart_products', lazy=True)



    def __repr__(self) -> str:
        return self.product_name



class Cart(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    products = db.Column(db.Integer(), db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer())



    def __repr__(self) -> str:
        return self.user.username


    
