import os
import re
from flask import Blueprint, render_template, redirect, url_for, request, current_app
from db_config import get_db
from werkzeug.security import generate_password_hash, check_password_hash

reister_bp = Blueprint("register", __name__)
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
MAX_FILE_SIZE_MB = 1


def alowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


@reister_bp.route("/register", methods=["GET", "POST"])
def register():
    errors = {}
    ketqua = ""
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "").strip()
    name = request.form.get("name", "").strip()
    files = request.files.get("avatar")
    if request.method == "POST":
        if not email:
            errors["email"] = "Vui long nhap email"
        elif not is_valid_email(email):
            errors["email"] = "Email khong dung dinh dang"
        if not password:
            errors["password"] = "Vui long nhap password"
        if not name:
            errors["name"] = "Vui long nhap name"
        upload_result = handle_file_upload(files)
        if not upload_result["success"]:
            errors["files"] = upload_result["error"]
        if not errors:
            ketqua = f"DANG KY THANH CONG"
            hashed_password = generate_password_hash(password)
            db = get_db()
            db.execute(
                "INSERT INTO users (email, password, name, avatar) values (?, ?, ?, ?)",
                (email, hashed_password, name, files.filename),
            )
            db.commit()
            UPLOAD_FOLDER = os.path.join(current_app.root_path, "uploads")
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)
            file_path = os.path.join(UPLOAD_FOLDER, files.filename)
            files.save(file_path)
            return redirect(url_for("login.login"))
    return render_template(
        "layout/register.html",
        email=email,
        password=password,
        errors=errors,
        files=files,
        ketqua=ketqua,
    )


def handle_file_upload(files):
    result = {"success": False, "error": None}
    if not files or files.filename == "":
        result["error"] = "Vui long chon file"
        return result
    if not alowed_file(files.filename):
        result["error"] = f"File '{files.filename}' khong hop le."
        return result
    files.seek(0, os.SEEK_END)
    file_size = files.tell()
    files.seek(0)
    if file_size > MAX_FILE_SIZE_MB * 1024 * 1024:
        result["error"] = (
            f"File '{files.filename}' qua lon! chi cho phep toi da {MAX_FILE_SIZE_MB}MB."
        )
        return result
    result["success"] = True
    return result
