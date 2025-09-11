import re
from flask import Blueprint, render_template, request, session, redirect, url_for
from db_config import get_db
from werkzeug.security import check_password_hash

login_bp = Blueprint("login", __name__)

def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


@login_bp.route("/login", methods=["GET", "POST"])
def login():
    errors = {}
    ketqua = ""
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "").strip()
    if request.method == "POST":
        if not email:
            errors["email"] = "Vui long nhap Email"
        elif not is_valid_email(email):
            errors["email"] = "Email khong dung dinh dang"
        if not password:
            errors["password"] = "Vui long nhap Password"
        if not errors:
            db = get_db()
            user = db.execute(
                "SELECT * FROM users WHERE email = ?",(email,)).fetchone()
            if user and check_password_hash(user["password"], password):
                session["user_id"] = user["id"]
                session["email"] = user["email"]
                ketqua = "Đăng nhập thành công"
            else:
                ketqua = "Email hoặc mật khẩu không đúng"
    return render_template(
        "layout/login.html", errors=errors, email=email, password=password, ketqua=ketqua
    )

@login_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login.login'))

@login_bp.route('/account')
def account():
    return render_template('layout/account.html')