from flask import render_template, Blueprint
from db_config import get_db

index_bp = Blueprint("index", __name__)


@index_bp.route("/")
def index():
    db = get_db()
    products = db.execute("SELECT * FROM product").fetchall()
    return render_template("index.html", products=products)
