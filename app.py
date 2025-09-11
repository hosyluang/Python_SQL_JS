import os
from flask import Flask, send_from_directory
from db_config import init_db, close_db, get_db
from routes.login import login_bp
from routes.register import reister_bp
from routes.index import index_bp
from routes.product import product_bp

app = Flask(__name__)
app.secret_key = "abc"

app.teardown_appcontext(close_db)

app.register_blueprint(product_bp)
app.register_blueprint(index_bp)
app.register_blueprint(login_bp)
app.register_blueprint(reister_bp)

with app.app_context():
    init_db()

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(os.path.join(app.root_path, 'uploads'), filename)

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
