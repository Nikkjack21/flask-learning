from account import app, db
from flask import render_template, request, redirect, url_for, jsonify
from account.Forms import LoginForm, RegisterForm, AdminLoginForm, CategoryForm
from .models import User, Category, Product
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
def index():
    return render_template("index.html", current_user=current_user)


@app.route("/no")
def noo():
    return "<h1> No wayyyy </h1>"


@app.route("/login", methods=["POST", "GET"])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    else:
        form = LoginForm()
        if form.validate_on_submit():
            check_user_exist = User.query.filter_by(username=form.username.data).first()
            if check_user_exist and check_user_exist.check_password(
                attempted_password=form.password.data
            ):
                login_user(check_user_exist)
                return redirect(url_for("index"))
            else:
                return redirect(url_for("signin"))

    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        print("inside-Form")
        user_to_create = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=form.password1.data,
        )
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for("signin"))

    return render_template("register.html", form=form)


@app.route("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect(url_for("signin"))
    return redirect(url_for("index"))


# Admin-Side


@app.route("/admin")
def admin_dashboard():
    if current_user.is_authenticated and current_user.is_admin:
        return render_template("admin/index.html")
    return redirect(url_for("admin_login"))


@app.route("/admin/login", methods=["POST", "GET"])
def admin_login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        print("hhehherer")
        check_user_is_admin = User.query.filter_by(username=form.username.data).first()
        if check_user_is_admin.is_admin and check_user_is_admin.check_password(
            attempted_password=form.password.data
        ):
            login_user(check_user_is_admin)
            return redirect(url_for("admin_dashboard"))
        else:
            print("Not an Admin User")
            return redirect(url_for("admin_login"))
    return render_template("admin/signin.html", form=form)


@app.route("/admin/logout")
def admin_logout():
    if current_user.is_authenticated and current_user.is_admin:
        logout_user()
        return redirect(url_for("admin_login"))


#Adnin-Category

@app.route('/admin/all-category', methods=['GET'])
def all_category():
    category =  Category.query.all()
    return render_template('admin/all-category.html', category=category)

@app.route('/add-category', methods=["POST"])
def add_category():
    form = CategoryForm()
    if form.validate_on_submit():
        new_category = Category(category_name=form.category_name.data)
        db.session.add(new_category)
        db.session.commit()
        return "Category Added"
    return "Add a category"

@app.route('/admin/category/<int:id>')
def show_category(id):
    cat =  Category.query.get(id)
    return f'<h1> Catgegory -> {cat}'


@app.route('/admin/category/<int:id>/edit', methods=["POST", "GET"])
def edit_category(id):
    category =  Category.query.get(id)
    form =  CategoryForm()
    if request.method == "GET":
        form.category_name.data = category.category_name
    else:

        if form.validate_on_submit():
            form.populate_obj(category)
            category.category_name = form.category_name.data
            db.session.commit()
            return redirect(url_for('all_category'))
    return render_template('admin/edit-category.html', form=form)

@app.route('/admin/category/delete/<int:id>')
def delete_Category(id):
    category =  Category.query.get(id)
    if category:
        db.session.delete(category)
        db.session.commit()
        return "<h1> Category Deleted"
    return "<h1> Category not found</h1>"



#Admin-Products
@app.route('/show-products', methods=["GET"])
def products():
    product = Product.query.all()
    return f'products->{product}'


@app.route('/show-cat-prod/<int:id>', methods=["GET"])
def prod_by_cat(id):
    products = Product.query.filter_by(category=id).all()   
    return f'prod_by_cat----> {products}'

@app.route('/del-product/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return "<h1> Product deleted </h1>"


@app.route('/add-product', methods=["POST"])
def add_product():
    category =  Category.query.all()
    product_name =  request.form.get("product_name")
    price = request.form.get("price")
    stock = request.form.get("stock")
    category_id =  request.form.get("category")

    product = Product(product_name=product_name, price=price, stock=stock, category=category_id)
    db.session.add(product)
    db.session.commit()
    return "<h1> Product added </h1>"


@app.route('/edit-product/<int:id>', methods=["PATCH"])
def edit_product(id):
    product = Product.query.get(id)
    if product:
        product_name =  request.form.get("product_name")
        price = request.form.get("price")
        stock = request.form.get("stock")
        product = Product(product_name=product_name, price=price, stock=stock)
        db.session.add(product)
        db.session.commit()
        return "Product added"
    return render_template("base.html", product=product)






